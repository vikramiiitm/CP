#!/usr/bin/env python3
"""
Score Jev results against the labelled population.

Reads results.json (written by run_jev_tests.py) + population.json (the labels),
joins them by id, and reports how well Jev's numbers match the expected labels:

  - coreSkillDepth: Spearman rank correlation (Jev mean vs expected band midpoint)
                    + "within expected band" hit-rate
  - seniorityFit:   accuracy + confusion matrix (under/matched/over)
  - hasShipped:     accuracy + confusion (threshold prob >= 0.5)
  - stability:      per-candidate stdev of coreSkillDepth across runs
  - confidence:     range + whether it varies (it should)

Stdlib only. Usage:
    python3 run_jev_tests.py --candidates population.json --tier 9   # produce results.json
    python3 score_population.py                                      # score it

Demo without any API (fabricates plausible results FROM the labels, so you can see
the scorecard format and confirm the pipeline runs):
    python3 score_population.py --simulate

>>> --simulate numbers are FAKE (derived from the labels + noise). They tell you
    NOTHING about Jev. They exist only to exercise this script end to end.
"""
import argparse
import json
import math
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent


def band_mid(band: str) -> float:
    lo, hi = band.split("-")
    return (float(lo) + float(hi)) / 2.0


def band_contains(band: str, x: float) -> bool:
    lo, hi = band.split("-")
    return float(lo) <= x <= float(hi)


def spearman(xs, ys):
    """Spearman rho, stdlib only (Pearson on average-ranks). Returns None if degenerate."""
    n = len(xs)
    if n < 3:
        return None

    def ranks(v):
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0  # average rank (1-based)
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    rx, ry = ranks(xs), ranks(ys)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return None if den == 0 else num / den


def load_population(path):
    spec = json.loads(Path(path).read_text())
    return {c["id"]: c for c in spec["test_cases"]}


def simulate_results(pop):
    """Fabricate plausible per-candidate results from the labels. FAKE — for demo only."""
    cases = []
    for i, (cid, c) in enumerate(pop.items()):
        exp = c["_expected"]
        mid = band_mid(exp["coreSkillDepth_band"])
        rows = []
        for r in range(1, 4):
            # deterministic tiny noise so stability is visible but small
            noise = ((i * 7 + r * 13) % 5 - 2) * 0.05
            rows.append({
                "run": r,
                "coreSkillDepth": {"value": round(min(4, max(0, mid + noise)), 2),
                                   "confidence": round(0.7 + ((i + r) % 6) * 0.04, 2)},
                "seniorityFit": {"value": exp["seniorityFit"],
                                 "confidence": round(0.75 + ((i * 3 + r) % 5) * 0.03, 2)},
                "hasShippedProduction": {"value": 0.9 if exp["hasShippedProduction"] else 0.15,
                                         "confidence": None},
                "_elapsed_s": 0.12,
            })
        cases.append({"id": cid, "label": c["label"], "tier": 9, "expected": exp, "rows": rows})
    return {"model": "SIMULATED", "endpoint": "n/a", "runs": 3, "cases": cases}


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def score(results, pop):
    paired = []  # (id, jev_csd_mean, csd_std, exp_mid, band, snr_pred, snr_exp, ship_pred, ship_exp, conf_mean)
    skipped = 0
    for case in results["cases"]:
        cid = case["id"]
        exp = case.get("expected") or (pop.get(cid) or {}).get("_expected")
        if not exp:
            continue
        csd_vals, confs, snr_votes, ship_probs = [], [], [], []
        for row in case["rows"]:
            if row.get("dry_run") or "error" in row:
                continue
            cv = num(row.get("coreSkillDepth", {}).get("value"))
            if cv is not None:
                csd_vals.append(cv)
            cf = num(row.get("coreSkillDepth", {}).get("confidence"))
            if cf is not None:
                confs.append(cf)
            sv = row.get("seniorityFit", {}).get("value")
            if sv:
                snr_votes.append(sv)
            sp = num(row.get("hasShippedProduction", {}).get("value"))
            if sp is not None:
                ship_probs.append(sp)
        if not csd_vals:
            skipped += 1
            continue
        csd_mean = statistics.mean(csd_vals)
        csd_std = statistics.pstdev(csd_vals) if len(csd_vals) > 1 else 0.0
        snr_pred = max(set(snr_votes), key=snr_votes.count) if snr_votes else None
        ship_pred = (statistics.mean(ship_probs) >= 0.5) if ship_probs else None
        paired.append((cid, csd_mean, csd_std, band_mid(exp["coreSkillDepth_band"]),
                       exp["coreSkillDepth_band"], snr_pred, exp["seniorityFit"],
                       ship_pred, exp["hasShippedProduction"],
                       statistics.mean(confs) if confs else None))
    return paired, skipped


def report(paired, skipped, results):
    n = len(paired)
    lines = []
    P = lines.append
    banner = "  *** SIMULATED DATA — NOT REAL JEV OUTPUT ***" if results.get("model") == "SIMULATED" else ""
    P(f"# Jev population scorecard{banner}\n")
    P(f"Model: {results.get('model')}   scored candidates: {n}   skipped (no numeric data): {skipped}\n")
    if n == 0:
        P("No scorable candidates. Run: python3 run_jev_tests.py --candidates population.json --tier 9")
        return "\n".join(lines)

    # coreSkillDepth ranking
    rho = spearman([p[1] for p in paired], [p[3] for p in paired])
    in_band = sum(1 for p in paired if band_contains(p[4], p[1]))
    P("## coreSkillDepth (ranking quality)")
    P(f"- Spearman rank corr (Jev mean vs expected band midpoint): "
      f"{'%.3f' % rho if rho is not None else 'n/a'}  "
      f"({'strong' if rho and rho >= 0.8 else 'moderate' if rho and rho >= 0.5 else 'weak/none'})")
    P(f"- Within expected band: {in_band}/{n} ({100*in_band/n:.0f}%)")
    # biggest misses
    misses = sorted(paired, key=lambda p: -abs(p[1] - p[3]))[:5]
    P("- Largest gaps (Jev mean vs expected mid):")
    for p in misses:
        P(f"    {p[0]}: jev {p[1]:.2f} vs exp {p[3]:.2f} (band {p[4]})")

    # seniorityFit
    labels = ["under", "matched", "over"]
    conf = {a: {b: 0 for b in labels} for a in labels}
    snr_ok = snr_tot = 0
    for p in paired:
        pred, exp = p[5], p[6]
        if pred in labels and exp in labels:
            conf[exp][pred] += 1
            snr_tot += 1
            snr_ok += (pred == exp)
    P("\n## seniorityFit (accuracy)")
    P(f"- Accuracy: {snr_ok}/{snr_tot} ({(100*snr_ok/snr_tot) if snr_tot else 0:.0f}%)")
    P("- Confusion (rows=expected, cols=predicted):")
    P("    | exp\\pred | under | matched | over |")
    P("    |---|---|---|---|")
    for a in labels:
        P(f"    | {a} | {conf[a]['under']} | {conf[a]['matched']} | {conf[a]['over']} |")

    # hasShipped
    tp = tn = fp = fn = 0
    for p in paired:
        pred, exp = p[7], p[8]
        if pred is None:
            continue
        if exp and pred:
            tp += 1
        elif exp and not pred:
            fn += 1
        elif not exp and pred:
            fp += 1
        else:
            tn += 1
    shp_tot = tp + tn + fp + fn
    P("\n## hasShippedProduction (accuracy, threshold p>=0.5)")
    P(f"- Accuracy: {tp+tn}/{shp_tot} ({(100*(tp+tn)/shp_tot) if shp_tot else 0:.0f}%)  "
      f"| TP={tp} TN={tn} FP={fp} FN={fn}")

    # stability
    stds = [p[2] for p in paired]
    P("\n## Stability (stdev of coreSkillDepth across runs)")
    P(f"- median {statistics.median(stds):.3f}  max {max(stds):.3f}  "
      f"(>0.3 on identical input would be concerning)")

    # confidence
    confs = [p[9] for p in paired if p[9] is not None]
    if confs:
        P("\n## Confidence")
        P(f"- range {min(confs):.2f}–{max(confs):.2f}, spread(stdev) {statistics.pstdev(confs):.3f} "
          f"({'varies (good)' if statistics.pstdev(confs) > 0.03 else 'nearly constant — human-review routing at risk'})")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default=str(HERE / "results.json"))
    ap.add_argument("--population", default=str(HERE / "population.json"))
    ap.add_argument("--simulate", action="store_true", help="fabricate results from labels (FAKE, demo only)")
    ap.add_argument("--out", default=str(HERE / "scorecard.md"))
    args = ap.parse_args()

    pop = load_population(args.population)
    if args.simulate:
        results = simulate_results(pop)
        args.out = str(HERE / "scorecard.sim.md")
    else:
        rp = Path(args.results)
        if not rp.exists():
            print(f"{rp} not found. Run the harness first, or try --simulate for a demo.")
            return
        results = json.loads(rp.read_text())

    paired, skipped = score(results, pop)
    text = report(paired, skipped, results)
    Path(args.out).write_text(text + "\n")
    print(text)
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
