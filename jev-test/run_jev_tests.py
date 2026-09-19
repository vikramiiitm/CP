#!/usr/bin/env python3
"""
Jev evaluation harness (Portfolios.tech candidate matching).

Runs the Tier 1 + Phase 2 candidates from candidates.json against the Jev
question schema, N times each, and writes a results table.

HONESTY NOTE
------------
The exact TypeSafe HTTP request/response field names could NOT be verified when
this was written (the docs domains were network-blocked). Everything the model
was *sure* of comes from the test brief you supplied: the question-schema shape,
the state shape, and that score/choice report a confidence while noul does not.

The parts that are a BEST-EFFORT GUESS and that you must confirm against the real
SDK/docs on first run are marked  # >>> VERIFY:
  - the endpoint path (JEV_ENDPOINT_PATH)
  - the request body wrapping (how `state`, `questions`, `model` are keyed)
  - the response field names (parsed defensively in parse_answer())

Run `--dry-run` first: it prints the exact request body without calling the API,
so you can diff it against the console/playground before spending anything.

USAGE
-----
  export TYPESAFE_API_KEY=...          # a FRESH key (never one pasted into chat)
  python3 run_jev_tests.py --dry-run                 # show payloads, no API call
  python3 run_jev_tests.py                           # run everything, 3x each
  python3 run_jev_tests.py --runs 3 --tier 1         # only Tier 1
  python3 run_jev_tests.py --case t2_weak_but_loud   # a single case
  python3 run_jev_tests.py --raw-only                # dump raw responses, skip table

Config via env:
  TYPESAFE_API_KEY     (required unless --dry-run)
  TYPESAFE_BASE_URL    default https://api.typesafe.ai       # >>> VERIFY
  JEV_ENDPOINT_PATH    default /v1/systemone                 # >>> VERIFY
  TYPESAFE_MODEL       default jev-latest
  JEV_RUNS             default 3
"""

import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent

BASE_URL = os.environ.get("TYPESAFE_BASE_URL", "https://api.typesafe.ai").rstrip("/")
ENDPOINT_PATH = os.environ.get("JEV_ENDPOINT_PATH", "/v1/systemone")  # >>> VERIFY
MODEL = os.environ.get("TYPESAFE_MODEL", "jev-latest")
DEFAULT_RUNS = int(os.environ.get("JEV_RUNS", "3"))


# --------------------------------------------------------------------------- #
# Data loading
# --------------------------------------------------------------------------- #
def load_json(path: Path):
    with path.open() as f:
        return json.load(f)


def load_schema(schema_ref: str | None):
    name = schema_ref or "questions_schema.json"
    schema = load_json(HERE / name)
    # Strip metadata keys (anything starting with "_") so only real questions go out.
    return {k: v for k, v in schema.items() if not k.startswith("_")}


def resolve_role(case: dict, spec: dict) -> dict:
    ref = case.get("role_ref")
    if ref:
        return spec["roles"][ref]
    return spec["default_role"]


# --------------------------------------------------------------------------- #
# The one function that talks to Jev. Everything guessed is marked VERIFY.
# --------------------------------------------------------------------------- #
def build_request_body(state: dict, questions: dict) -> dict:
    # >>> VERIFY: how the API wants state/questions/model wrapped. The brief only
    # documents the *contents* of the State and Questions panels, not the JSON
    # envelope the HTTP API expects. This is the most likely shape; adjust to match.
    return {
        "model": MODEL,
        "state": state,
        "questions": questions,
    }


def call_jev(state: dict, questions: dict, timeout: int = 60) -> dict:
    api_key = os.environ.get("TYPESAFE_API_KEY")
    if not api_key:
        raise RuntimeError("TYPESAFE_API_KEY is not set. Use --dry-run to test without it.")

    url = BASE_URL + ENDPOINT_PATH
    body = json.dumps(build_request_body(state, questions)).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {api_key}")  # >>> VERIFY auth header scheme

    ctx = ssl.create_default_context()
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {e.code} from {url}: {detail}") from e
    elapsed = time.time() - started

    parsed = json.loads(raw)
    return {"_elapsed_s": round(elapsed, 3), "_raw": parsed}


# --------------------------------------------------------------------------- #
# Defensive response parsing. We don't know exact field names, so search for the
# most likely ones and fall back to recording the raw structure.
# --------------------------------------------------------------------------- #
def _first(d: dict, keys):
    for k in keys:
        if isinstance(d, dict) and k in d and d[k] is not None:
            return d[k]
    return None


def parse_answer(qtype: str, ans) -> dict:
    """Return {'value':..., 'confidence':...} best-effort. qtype in score|choice|noul."""
    if not isinstance(ans, dict):
        return {"value": ans, "confidence": None}

    conf = _first(ans, ["confidence", "conf"])
    if qtype == "score":
        val = _first(ans, ["value", "score", "result", "answer"])
    elif qtype == "choice":
        val = _first(ans, ["value", "choice", "selected", "answer", "option"])
        if conf is None:
            conf = _first(ans, ["confidence"])
    elif qtype == "noul":
        # noul = probability of true; no confidence field per the brief.
        val = _first(ans, ["probability", "value", "true_probability", "p_true", "answer"])
        conf = None
    else:
        val = _first(ans, ["value", "answer"])
    return {"value": val, "confidence": conf}


def extract_answers(raw: dict, questions: dict) -> dict:
    """Locate the per-question answers inside the raw response."""
    # >>> VERIFY: where answers live. Try a few likely containers.
    container = None
    for key in ("answers", "results", "questions", "output", "data"):
        if isinstance(raw.get(key), dict):
            container = raw[key]
            break
    if container is None:
        # Maybe the answers are top-level keyed by question name.
        if all(qn in raw for qn in questions):
            container = raw
        else:
            container = {}

    out = {}
    for qname, qdef in questions.items():
        ans = container.get(qname) if isinstance(container, dict) else None
        out[qname] = parse_answer(qdef["type"], ans) if ans is not None else {"value": None, "confidence": None}
    return out


# --------------------------------------------------------------------------- #
# Run loop
# --------------------------------------------------------------------------- #
def run_case(case: dict, spec: dict, runs: int, dry_run: bool):
    role = resolve_role(case, spec)
    questions = load_schema(case.get("schema_ref"))
    state = {"role": role, "candidate": case["candidate"]}

    (HERE / "raw_responses").mkdir(exist_ok=True)
    rows = []
    for r in range(1, runs + 1):
        if dry_run:
            print(f"\n--- DRY RUN {case['id']} run {r} ---")
            print("POST", BASE_URL + ENDPOINT_PATH)
            print(json.dumps(build_request_body(state, questions), indent=2))
            rows.append({"run": r, "dry_run": True})
            continue
        try:
            resp = call_jev(state, questions)
        except Exception as e:  # noqa: BLE001 - we want to record every failure
            print(f"[{case['id']} run {r}] ERROR: {e}", file=sys.stderr)
            rows.append({"run": r, "error": str(e)})
            continue

        raw = resp["_raw"]
        (HERE / "raw_responses" / f"{case['id']}_run{r}.json").write_text(json.dumps(raw, indent=2))
        answers = extract_answers(raw, questions)
        answers["_elapsed_s"] = resp["_elapsed_s"]
        answers["run"] = r
        rows.append(answers)
        print(f"[{case['id']} run {r}] {resp['_elapsed_s']}s -> "
              + ", ".join(f"{q}={answers[q]['value']}(c={answers[q]['confidence']})"
                          for q in questions))
    return {"case": case, "questions": list(questions), "rows": rows}


def fmt(v):
    return "" if v is None else (v if isinstance(v, str) else str(v))


def render_table(results) -> str:
    lines = [
        "| Candidate | Tier | Run | coreSkillDepth | Conf | seniorityFit | Conf | hasShippedProduction | Elapsed(s) |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for res in results:
        c = res["case"]
        for row in res["rows"]:
            if row.get("dry_run"):
                continue
            if "error" in row:
                lines.append(f"| {c['label']} | {c['tier']} | {row['run']} | ERROR: {row['error'][:40]} | | | | | |")
                continue
            csd = row.get("coreSkillDepth", {})
            snr = row.get("seniorityFit", {})
            shp = row.get("hasShippedProduction", {})
            lines.append(
                f"| {c['label']} | {c['tier']} | {row['run']} "
                f"| {fmt(csd.get('value'))} | {fmt(csd.get('confidence'))} "
                f"| {fmt(snr.get('value'))} | {fmt(snr.get('confidence'))} "
                f"| {fmt(shp.get('value'))} | {fmt(row.get('_elapsed_s'))} |"
            )
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Jev evaluation harness")
    ap.add_argument("--runs", type=int, default=DEFAULT_RUNS)
    ap.add_argument("--tier", type=int, help="only run this tier")
    ap.add_argument("--case", help="only run this case id")
    ap.add_argument("--dry-run", action="store_true", help="print payloads, do not call the API")
    ap.add_argument("--raw-only", action="store_true", help="skip the markdown table")
    ap.add_argument("--out", default=str(HERE / "results_table.md"))
    ap.add_argument("--candidates", default=str(HERE / "candidates.json"),
                    help="candidate spec file (e.g. population.json)")
    args = ap.parse_args()

    spec = load_json(Path(args.candidates))
    cases = spec["test_cases"]
    if args.tier is not None:
        cases = [c for c in cases if c["tier"] == args.tier]
    if args.case:
        cases = [c for c in cases if c["id"] == args.case]
    if not cases:
        print("No matching cases.", file=sys.stderr)
        sys.exit(1)

    if not args.dry_run and not os.environ.get("TYPESAFE_API_KEY"):
        print("TYPESAFE_API_KEY not set. Either export it or pass --dry-run.", file=sys.stderr)
        sys.exit(2)

    print(f"Model={MODEL}  endpoint={BASE_URL + ENDPOINT_PATH}  runs={args.runs}  cases={len(cases)}")
    results = [run_case(c, spec, args.runs, args.dry_run) for c in cases]

    if args.dry_run or args.raw_only:
        return

    # machine-readable results for the scorer
    results_json = {
        "model": MODEL, "endpoint": BASE_URL + ENDPOINT_PATH, "runs": args.runs,
        "cases": [
            {
                "id": r["case"]["id"], "label": r["case"]["label"], "tier": r["case"]["tier"],
                "expected": r["case"].get("_expected"),
                "rows": r["rows"],
            }
            for r in results
        ],
    }
    (HERE / "results.json").write_text(json.dumps(results_json, indent=2) + "\n")

    table = render_table(results)
    header = (f"# Jev results table\n\n"
              f"**Generated:** {date.today().isoformat()}  \n"
              f"**Model:** {MODEL}  \n"
              f"**Endpoint:** {BASE_URL + ENDPOINT_PATH}  \n"
              f"**Runs per candidate:** {args.runs}\n\n")
    Path(args.out).write_text(header + table + "\n")
    print("\n" + table)
    print(f"\nWrote {args.out}")
    print(f"Wrote {HERE / 'results.json'} (feed this to score_population.py)")
    print(f"Raw responses in {HERE / 'raw_responses'}/")


if __name__ == "__main__":
    main()
