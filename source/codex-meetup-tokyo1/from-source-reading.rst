==================================================
Codex CLIで（を）ソースコードリーディング！
==================================================

Codex CLIで（を）ソースコードリーディング！
==================================================

あの機能はどうできている？

:Event: Codex Meetup Tokyo #1
:Presented: 2026/03/19 nikkie

Codexはソースが **公開** されている🤗
==================================================

https://github.com/openai/codex

例えば Codex App
--------------------------------------------------

* :command:`codex app-server`
* JSON-RPCによるプロトコル（`Codex App Server <https://developers.openai.com/codex/app-server>`__）

.. Python SDK準備中みたい

CodexのソースコードをCodex {CLI,App}に解説してもらう日々
------------------------------------------------------------

その中から **小さな機能2つ** と、どう実装されているかを共有します

1️⃣シンタックスハイライト
==================================================

Codex CLIについて（Appも差分のコードに色ついてますね）

https://developers.openai.com/codex/cli/features#syntax-highlighting-and-themes

.. revealjs-break::
    :notitle:

.. image:: ../_static/codex-meetup-tokyo1/codex-cli-syntax-highlight-example.png
    :scale: 70%

(GPT-5.4 medium effort)

.. _v0.105.0: https://github.com/openai/codex/releases/tag/rust-v0.105.0

`v0.105.0`_ にてシンタックスハイライト追加
--------------------------------------------------

    The TUI now syntax-highlights fenced code blocks and diffs, adds a /theme picker with live preview, and uses better theme-aware diff colors for light and dark terminals.

コードブロックや実行するコマンドが **劇的に読みやすく**

では、どう実装されている？
==================================================

.. https://nikkie-ftnext.hatenablog.com/entry/codex-cli-v0.105.0-syntax-highlight-by-syntect-minimum-clone-like-bat

* `feat(tui): syntax highlighting via syntect with theme picker #11447 <https://github.com/openai/codex/pull/11447>`__
* `syntect <https://github.com/trishume/syntect>`__
* ``cat`` cloneの :command:`bat` でも使われている

.. https://github.com/openai/codex/blob/rust-v0.115.0/codex-rs/tui/src/render/highlight.rs#L570

.. _two-face: https://github.com/CosmicHorrorDev/two-face

テーマは `two-face`_
--------------------------------------------------

.. image:: ../_static/codex-meetup-tokyo1/codex-cli-themes.png

.. https://github.com/openai/codex/blob/rust-v0.115.0/codex-rs/tui/src/render/highlight.rs#L136

.. カスタムもできる（例）

2️⃣音声入力
==================================================

Codex CLI（とCodex App）について

半角スペースを長押し（Codex CLI）
--------------------------------------------------

.. image:: ../_static/codex-meetup-tokyo1/codex-cli-transcribe.png

:kbd:`Ctrl+M` （Codex App, macOS）
--------------------------------------------------

.. image:: ../_static/codex-meetup-tokyo1/codex-app-transcribe.png

:command:`codex features list`
--------------------------------------------------

.. code-block:: txt

    voice_transcription              under development  false

.. code-block:: txt

    % codex --version
    codex-cli 0.115.0-alpha.27

Codex CLIの設定を変える
--------------------------------------------------

.. https://developers.openai.com/codex/cli/features#feature-flags

.. code-block:: toml
    :caption: :file:`~/.codex/config.toml`

    [features]
    voice_transcription = true

.. code-block:: shell

    codex features enable voice_transcription

起動時に一時的に
--------------------------------------------------

.. code-block:: shell

    codex --enable voice_transcription
    codex -c features.voice_transcription=true

では、どう実装されている？ (Codex CLI)
==================================================

* APIキーの場合 `gpt-4o-mini-transcribe <https://developers.openai.com/api/docs/models/gpt-4o-mini-transcribe>`__
* ChatGPTアカウントの場合、/backend-api/transcribe へ

.. https://github.com/openai/codex/blob/rust-v0.115.0/codex-rs/tui/src/voice.rs#L789

promptパラメタでひと工夫
--------------------------------------------------

* https://developers.openai.com/api/docs/guides/speech-to-text#prompting
* 前方にあるテキスト（ユーザ入力やそれまでの書き起こし）も合わせてgpt-4o-mini-transcribeへ送る

.. 参考にPython実装
    サポートありがとう

まとめ🌯：あの機能はどうできている？
==================================================

* シンタックスハイライト：syntect（bat同様）、テーマはtwo-face
* 音声入力：gpt-4o-mini-transcribe、promptパラメタの工夫
* Codex CLIやCodex Appで気になるソースコードを読むのは、いいぞ

ご清聴ありがとうございました（最後に、お前、誰よ）
--------------------------------------------------

* nikkie（にっきー）・Python歴8年
* 機械学習エンジニア。 `Speeda AI Agent <https://jp.ub-speeda.com/news/speeda-promotion-gallery/>`__ 開発（`We're hiring! <https://hrmos.co/pages/uzabase/jobs/1829077236709650481>`__）

.. image:: ../_static/uzabase-white-logo.png
