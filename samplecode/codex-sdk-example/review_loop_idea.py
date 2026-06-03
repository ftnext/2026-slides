# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "openai-codex>=0.1.0b2",
# ]
# ///
import json
import subprocess
import tempfile
from pathlib import Path
from shutil import which

from openai_codex import ApprovalMode, Codex, CodexConfig, Sandbox

MODEL = "gpt-5.5"
MAX_REVIEW_CYCLES = 5

REVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "has_findings": {"type": "boolean"},
        "summary": {"type": "string"},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {"type": "string"},
                    "file": {"type": "string"},
                    "line": {"type": "integer"},
                    "message": {"type": "string"},
                },
                "required": ["severity", "file", "line", "message"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["has_findings", "summary", "findings"],
    "additionalProperties": False,
}


def _create_sample_project(root: Path) -> None:
    (root / "calculator.py").write_text(
        "\n".join(
            [
                "def add(left: int, right: int) -> int:",
                "    return left + right",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (root / "test_calculator.py").write_text(
        "\n".join(
            [
                "import unittest",
                "",
                "from calculator import add",
                "",
                "",
                "class CalculatorTest(unittest.TestCase):",
                "    def test_add(self) -> None:",
                "        self.assertEqual(add(2, 3), 5)",
                "",
                "",
                "if __name__ == '__main__':",
                "    unittest.main()",
                "",
            ]
        ),
        encoding="utf-8",
    )
    _run_git(root, "init")
    _run_git(root, "add", ".")
    _run_git(
        root,
        "-c",
        "user.name=Codex SDK Example",
        "-c",
        "user.email=codex-sdk-example@example.com",
        "commit",
        "-m",
        "Create sample project",
    )


def _run_git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _parse_review(text: str | None) -> dict:
    if not text:
        raise RuntimeError("Review turn did not return JSON text.")
    return json.loads(text)


def _print_review(review: dict) -> None:
    print("Review summary:", review["summary"])
    if not review["findings"]:
        print("Review findings: none")
        return

    print("Review findings:")
    for finding in review["findings"]:
        location = f"{finding['file']}:{finding['line']}"
        print(f"- [{finding['severity']}] {location} {finding['message']}")


def _git_diff(root: Path) -> str:
    return subprocess.run(
        ["git", "diff", "--", "calculator.py", "test_calculator.py"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def _run_implementation_review_loop(
    codex: Codex,
    project_root: Path,
    task: str,
    approval_mode: ApprovalMode,
    workspace_write: Sandbox,
    read_only: Sandbox,
) -> None:
    implementer = codex.thread_start(
        cwd=str(project_root),
        model=MODEL,
        config={"model_reasoning_effort": "high"},
        approval_mode=approval_mode,
        sandbox=workspace_write,
    )

    implementation_result = implementer.run(
        (
            "Implement this request in the sample Python project:\n"
            f"{task}\n\n"
            "Keep the change small. Update or add unittest coverage when behavior changes, "
            "run the relevant tests, and summarize the files changed and test result."
        ),
        approval_mode=approval_mode,
        cwd=str(project_root),
        sandbox=workspace_write,
    )

    print("\nImplementation:")
    print(implementation_result.final_response or "[no final response]")

    reviewer = codex.thread_start(
        cwd=str(project_root),
        model=MODEL,
        config={"model_reasoning_effort": "high"},
        approval_mode=approval_mode,
        sandbox=read_only,
    )

    for cycle in range(1, MAX_REVIEW_CYCLES + 1):
        review_result = reviewer.run(
            (
                "Review the current uncommitted changes in this repository. "
                "Focus on correctness bugs, regressions, missing tests, and unsafe behavior. "
                "Return JSON matching the requested schema. If there are no actionable issues, "
                "set has_findings to false and use an empty findings array."
            ),
            approval_mode=approval_mode,
            cwd=str(project_root),
            output_schema=REVIEW_SCHEMA,
            sandbox=read_only,
        )
        review = _parse_review(review_result.final_response)

        print(f"\nReview cycle {cycle}:")
        _print_review(review)

        if not review["has_findings"]:
            break

        if cycle == MAX_REVIEW_CYCLES:
            print(
                "\nReached review loop limit; leaving remaining findings for the caller."
            )
            break

        fix_result = implementer.run(
            (
                "Fix these review findings, keep the patch minimal, and rerun the relevant tests:\n"
                f"{json.dumps(review['findings'], indent=2)}"
            ),
            approval_mode=approval_mode,
            cwd=str(project_root),
            sandbox=workspace_write,
        )

        print(f"\nFix cycle {cycle}:")
        print(fix_result.final_response or "[no final response]")

    print("\nCurrent diff:")
    print(_git_diff(project_root).rstrip() or "[no diff]")


with tempfile.TemporaryDirectory(
    prefix="codex-sdk-implementation-review-"
) as temp_root:
    project_root = Path(temp_root).resolve()
    _create_sample_project(project_root)

    approval_mode = ApprovalMode.deny_all
    workspace_write = Sandbox.workspace_write
    read_only = Sandbox.read_only

    print("Sample project:", project_root)
    print("Implementation/review CLI. Type /diff to show the current diff.")
    print("Type /exit or /quit to stop.")

    with Codex(config=CodexConfig(codex_bin=which("codex"))) as codex:
        while True:
            try:
                task = input("\ntask> ").strip()
            except EOFError:
                break

            if not task:
                continue
            if task in {"/exit", "/quit"}:
                break
            if task == "/diff":
                print(_git_diff(project_root).rstrip() or "[no diff]")
                continue

            _run_implementation_review_loop(
                codex,
                project_root,
                task,
                approval_mode,
                workspace_write,
                read_only,
            )
