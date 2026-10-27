"""Validate an externally supplied assessment, score it and render a report.

Usage:
    python scripts/run_evaluation.py --job JD.md --cv CV.md --assessment A.json \
        [--standard STANDARD.md] [--output REPORT.md]

All inputs are explicit paths; nothing is discovered automatically. The tool
never calls a language model and never assigns statuses itself.

Exit codes: 0 success, 1 invalid input (parse, validation or scoring error),
2 command-line usage error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make the `src` package importable when run as a script. This locates the
# framework's code only; every data file still comes from a CLI argument.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.evaluator import check_standard_consistency, evaluate  # noqa: E402
from src.models import FrameworkError  # noqa: E402
from src.parser import load_assessment, parse_cv, parse_job_description  # noqa: E402
from src.report import render_report  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--job", required=True, type=Path, help="job description Markdown file")
    parser.add_argument("--cv", required=True, type=Path, help="candidate CV Markdown file")
    parser.add_argument("--assessment", required=True, type=Path, help="structured assessment JSON file")
    parser.add_argument(
        "--standard",
        type=Path,
        help="evaluation standard Markdown file; if given, its scoring tables must match the evaluator",
    )
    parser.add_argument("--output", type=Path, help="write the report here instead of printing it")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.standard:
            check_standard_consistency(args.standard)
        job = parse_job_description(args.job)
        cv = parse_cv(args.cv)
        submission = load_assessment(args.assessment)
        result = evaluate(job, cv, submission)
    except FrameworkError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    report = render_report(result)
    if args.output:
        args.output.write_text(report, encoding="utf-8")
        print(f"Wrote {args.output} (total {result.score.total:.1f}, {result.score.band.value})")
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
