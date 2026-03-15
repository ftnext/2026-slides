# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "numpy>=2.4.3",
#     "openai>=2.28.0",
#     "pynput>=1.8.1",
#     "sounddevice>=0.5.5",
# ]
# ///

from __future__ import annotations

import io
import os
import queue
import sys
import tempfile
import threading
import wave
from dataclasses import dataclass

import numpy as np
import sounddevice as sd
from openai import OpenAI
from pynput import keyboard

SAMPLE_RATE = 16_000
CHANNELS = 1
MIN_DURATION_SECONDS = 1.0
LIVE_POLL_SECONDS = 0.8
MODEL = "gpt-4o-transcribe"


def normalize_peak_int16(samples: np.ndarray, headroom: float = 0.9) -> np.ndarray:
    """Apply simple peak normalization, similar to the Rust implementation."""
    if samples.size == 0:
        return samples
    peak = int(np.max(np.abs(samples)))
    if peak <= 0:
        return samples
    target = int(np.iinfo(np.int16).max * headroom)
    gain = target / peak
    scaled = np.clip(np.round(samples.astype(np.float32) * gain), -32768, 32767)
    return scaled.astype(np.int16)


def wav_bytes_from_int16(samples: np.ndarray, sample_rate: int = SAMPLE_RATE) -> bytes:
    """Encode mono int16 PCM samples into an in-memory WAV file."""
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(samples.tobytes())
    return buf.getvalue()


@dataclass
class RecorderState:
    recording: bool = False
    live_prompt: str = ""


class SpacebarLiveTranscriber:
    def __init__(self) -> None:
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set")

        self.client = OpenAI()
        self.state = RecorderState()
        self._chunks: list[np.ndarray] = []
        self._chunk_queue: queue.Queue[np.ndarray] = queue.Queue()
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._live_thread: threading.Thread | None = None
        self._stream: sd.InputStream | None = None
        self._last_live_len = 0

    def _audio_callback(self, indata: np.ndarray, frames: int, t, status) -> None:
        del frames, t
        if status:
            print(f"[audio] {status}", file=sys.stderr, flush=True)
        pcm = np.copy(indata[:, 0]).astype(np.int16)
        self._chunk_queue.put(pcm)

    def _drain_queue(self) -> None:
        while True:
            try:
                chunk = self._chunk_queue.get_nowait()
            except queue.Empty:
                return
            self._chunks.append(chunk)

    def _current_samples(self) -> np.ndarray:
        self._drain_queue()
        if not self._chunks:
            return np.array([], dtype=np.int16)
        return np.concatenate(self._chunks)

    def _transcribe_bytes(self, wav_data: bytes, prompt: str | None = None) -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
            tmp.write(wav_data)
            tmp.flush()
            with open(tmp.name, "rb") as f:
                result = self.client.audio.transcriptions.create(
                    model=MODEL,
                    file=f,
                    prompt=prompt,
                )
        text = (result.text or "").strip()
        return text

    def _live_loop(self) -> None:
        while not self._stop_event.wait(LIVE_POLL_SECONDS):
            with self._lock:
                if not self.state.recording:
                    return
                samples = self._current_samples()
                duration = samples.size / SAMPLE_RATE if SAMPLE_RATE else 0.0
                if duration < MIN_DURATION_SECONDS:
                    continue
                normalized = normalize_peak_int16(samples)
                wav_data = wav_bytes_from_int16(normalized)

            try:
                text = self._transcribe_bytes(wav_data, prompt=self.state.live_prompt)
            except Exception as e:  # noqa: BLE001
                print(f"\n[live transcription error] {e}", file=sys.stderr, flush=True)
                continue

            if len(text) <= self._last_live_len:
                continue

            print(f"\rLive: {text}", end="", flush=True)
            self._last_live_len = len(text)
            with self._lock:
                self.state.live_prompt = text

    def start_recording(self) -> None:
        with self._lock:
            if self.state.recording:
                return
            self.state.recording = True
            self.state.live_prompt = ""
            self._last_live_len = 0
            self._chunks.clear()
            self._stop_event.clear()

            self._stream = sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype="int16",
                callback=self._audio_callback,
            )
            self._stream.start()

            self._live_thread = threading.Thread(target=self._live_loop, daemon=True)
            self._live_thread.start()

        print("\n🎙️ Recording... (space を離すと停止)", flush=True)

    def stop_recording(self) -> None:
        with self._lock:
            if not self.state.recording:
                return
            self.state.recording = False
            self._stop_event.set()

            if self._stream is not None:
                self._stream.stop()
                self._stream.close()
                self._stream = None

            samples = self._current_samples()

        if self._live_thread is not None:
            self._live_thread.join(timeout=2.0)
            self._live_thread = None

        duration = samples.size / SAMPLE_RATE if SAMPLE_RATE else 0.0
        if duration < MIN_DURATION_SECONDS:
            print(
                f"\n⏹️ 録音が短すぎます ({duration:.2f}s < {MIN_DURATION_SECONDS:.2f}s)。",
                flush=True,
            )
            return

        print("\n🧠 最終文字起こし中...", flush=True)
        try:
            normalized = normalize_peak_int16(samples)
            wav_data = wav_bytes_from_int16(normalized)
            text = self._transcribe_bytes(wav_data)
        except Exception as e:  # noqa: BLE001
            print(f"❌ transcription failed: {e}", file=sys.stderr, flush=True)
            return

        print(f"✅ Final: {text}\n", flush=True)


def main() -> int:
    print("Space長押しで録音、離して停止。Ctrl+C で終了します。", flush=True)
    transcriber = SpacebarLiveTranscriber()

    def on_press(key) -> None:
        if key == keyboard.Key.space:
            transcriber.start_recording()

    def on_release(key):
        if key == keyboard.Key.space:
            transcriber.stop_recording()
        if key == keyboard.Key.esc:
            return False
        return None

    listener_kwargs = {
        "on_press": on_press,
        "on_release": on_release,
        # Prevent the focused terminal from echoing the pressed space when supported.
        "suppress": True,
    }

    try:
        listener = keyboard.Listener(**listener_kwargs)
    except TypeError:
        listener_kwargs.pop("suppress", None)
        print(
            "⚠️ keyboard suppress が使えないため、スペース入力が端末に見える場合があります。",
            file=sys.stderr,
            flush=True,
        )
        listener = keyboard.Listener(**listener_kwargs)

    with listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
