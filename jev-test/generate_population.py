#!/usr/bin/env python3
"""
Generate a diverse, LABELLED synthetic candidate population -> population.json.

Why labelled: the brief's real trial is "20-30 portfolios where we already know
who we'd rank highly". Volume alone proves nothing; you need ground truth to
check whether Jev's ranking matches a human's. So every generated candidate
carries an `_expected` block (expected coreSkillDepth band, seniorityFit,
hasShippedProduction) derived transparently from the spec below.

>>> The `_expected` labels are HEURISTIC, produced by the mapping in this file,
    NOT authoritative human judgement. Before using them as a benchmark, have a
    real recruiter review/adjust them. They are a first pass, clearly flagged.

Reproducible: deterministic, no randomness. Re-run to regenerate; edit SPECS to
extend. Run against the harness with:
    python3 run_jev_tests.py --candidates population.json --tier 9
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

DEFAULT_ROLE = {
    "title": "Senior Backend Engineer",
    "seniority": "5+ years",
    "must_have": ["Python", "Django", "PostgreSQL"],
    "nice_to_have": ["AWS", "data pipelines"],
    "domain": "healthcare SaaS",
}

# ---- how well each specialism fits the DEFAULT role (0..1) ------------------ #
SPECIALISM_FIT = {
    "backend_django": 1.00, "fullstack_django": 0.85, "backend_other": 0.60,
    "data_eng": 0.40, "qa": 0.35, "devops": 0.30, "ml": 0.30,
    "mobile": 0.15, "frontend": 0.15,
}
SPECIALISM_SKILLS = {
    "backend_django": ["Python", "Django", "PostgreSQL", "Celery", "AWS"],
    "fullstack_django": ["Python", "Django", "React", "PostgreSQL", "JavaScript"],
    "backend_other": ["Python", "FastAPI", "PostgreSQL", "Go", "Redis"],
    "data_eng": ["Python", "SQL", "Airflow", "Spark", "dbt"],
    "qa": ["Python", "pytest", "Selenium", "SQL"],
    "devops": ["Terraform", "Kubernetes", "AWS", "Python", "Bash"],
    "ml": ["Python", "PyTorch", "pandas", "scikit-learn"],
    "mobile": ["Kotlin", "Swift", "React Native", "REST"],
    "frontend": ["React", "TypeScript", "CSS", "Next.js"],
}
# demonstration strength -> weight, and whether it implies shipped-to-prod
DEMO = {"none": 0.0, "claimed": 0.15, "one": 0.5, "several": 0.8, "led": 1.0}
DEMO_SHIPPED = {"none": False, "claimed": False, "one": True, "several": True, "led": True}

SENIORITY = {  # -> (years, seniorityFit vs "5+ years", title prefix)
    "intern":    (0, "under", "Intern"),
    "junior":    (2, "under", "Junior "),
    "mid":       (4, "under", ""),
    "senior":    (7, "matched", "Senior "),
    "staff":     (11, "over", "Staff "),
    "principal": (16, "over", "Principal "),
}

_FIRST = [
    "Rahul", "Priya", "Imran", "Anthony", "Sneha", "Arjun", "Fatima", "Joseph",
    "Ananya", "Vikas", "Meera", "Daniyal", "Grace", "Rohit", "Lakshmi", "Sahil",
    "Aisha", "Thomas", "Divya", "Karan", "Zoya", "Nikhil", "Ritu", "Sunil",
    "Nadia", "Aditya", "Kavya", "Farhan", "Neha", "Manish", "Pooja", "Yusuf",
    "Rebecca", "Harsh", "Ishita", "Deepak", "Sara", "Amit", "Tara", "Omar",
]
_LAST = [
    "Sharma", "Nair", "Qureshi", "Fernandes", "Patel", "Reddy", "Sheikh", "Mathew",
    "Ghosh", "Yadav", "Iyer", "Khan", "DSouza", "Verma", "Menon", "Kapoor",
    "Begum", "Varghese", "Rao", "Mehta", "Ansari", "Joshi", "Agarwal", "Pillai",
]
# Deterministic unique-ish names for up to len(_FIRST)*len(_LAST) candidates.
NAMES = [f"{_FIRST[i % len(_FIRST)]} {_LAST[(i // len(_FIRST)) % len(_LAST)]}"
         for i in range(len(_FIRST) * len(_LAST))]
CITIES = ["Bengaluru", "Pune", "Hyderabad", "Chennai", "Gurugram", "Mumbai", "Kochi",
          "Indore (tier-2)", "Bhagalpur (small town)", "Remote"]
COMPANIES = {
    "product": ["Nimbus Health", "MedCore", "ClinicStack", "PayBridge", "Finlytics",
                "CareLoop", "VitalsIO", "LedgerWorks"],
    "bigtech": ["Meridian (big-tech)", "Orbital Systems", "Northstar"],
    "startup": ["LeafRoute (seed)", "Kettle & Byte", "Trailhead (early-stage)", "Qubit Labs"],
    "services": ["GlobalTech Services", "Cognisys Consulting", "Delta IT Solutions"],
    "agency":   ["Pixel & Poll", "Craftbyte Studio"],
}
ROUTES = {
    "degree":      "B.Tech Computer Science, {}",
    "top_degree":  "B.Tech Computer Science, National Institute of Technology, {}",
    "phd":         "PhD Computer Science, {}",
    "bootcamp":    "Full-stack coding bootcamp, {} (no university degree)",
    "selftaught":  "Self-taught, no formal CS degree",
    "careerchange": "B.A prior field; transitioned to software via online courses, {}",
    "mca":         "MCA, {}",
}

# ---- Weighted archetypes -> a realistically-skewed applicant population -------- #
# A real applicant pool for a Senior Backend Django role is mostly NOT strong
# matches: lots of adjacent/off-target/junior/claims-heavy applicants, a few great
# ones. Each row: (count, specialism, seniority, demo, routes, styles, signal_sets).
# A field given as a list is cycled across that archetype's `count` candidates.
# style: neutral|terse|verbose ; signals: gap/jobhop/oss/pub/longtenure/freelance/services
ARCHETYPES = [
    # strong, in-role matches (the minority)
    (12, "backend_django", "senior", ["led", "several"], ["top_degree", "degree", "selftaught"], ["neutral", "terse", "verbose"], [[], ["oss"], ["longtenure"]]),
    (5,  "backend_django", "staff", "led", ["top_degree", "degree"], ["terse", "neutral"], [["oss", "longtenure"], ["longtenure"]]),
    (3,  "backend_django", "principal", "led", ["top_degree", "degree"], ["terse", "neutral"], [["oss", "longtenure"]]),  # overqualified
    (12, "backend_django", "mid", ["several", "one"], ["degree", "mca", "bootcamp"], ["neutral", "verbose"], [[], ["gap"]]),
    (8,  "backend_django", "junior", ["one", "several"], ["bootcamp", "degree", "selftaught"], ["neutral", "verbose"], [[], ["oss"]]),
    # partial fit: full-stack with Django
    (14, "fullstack_django", ["senior", "mid", "junior"], ["several", "one"], ["degree", "bootcamp", "mca"], ["neutral", "verbose", "terse"], [[], ["startup"], ["jobhop"]]),
    # adjacent: backend, not Django
    (12, "backend_other", ["senior", "mid"], ["led", "several"], ["top_degree", "degree"], ["neutral", "terse"], [[], ["jobhop"]]),
    # weak fit: data engineering
    (8,  "data_eng", ["senior", "mid"], ["led", "several"], ["degree", "mca"], ["neutral", "verbose"], [[]]),
    # poor fit: ML/research
    (6,  "ml", ["senior", "mid"], ["led", "several"], ["phd", "degree"], ["verbose", "neutral"], [["pub"], []]),
    # poor fit: frontend/mobile/devops/qa (discrimination test)
    (12, ["frontend", "mobile", "devops", "qa"], ["senior", "mid"], ["led", "several"], ["degree", "bootcamp"], ["neutral", "terse"], [[], ["oss"]]),
    # junior/intern/tutorial-level (weak)
    (10, ["backend_django", "fullstack_django"], ["junior", "intern"], ["one", "none", "claimed"], ["bootcamp", "selftaught", "degree"], ["verbose", "neutral"], [[]]),
    # claims-heavy / keyword-y, thin substance (weak)
    (8,  ["backend_django", "backend_other"], "mid", "claimed", ["degree", "bootcamp"], ["verbose"], [[]]),
    # services-company (ambiguous ownership)
    (8,  ["backend_django", "fullstack_django"], ["senior", "mid"], "several", ["mca", "degree"], ["verbose", "neutral"], [["services"], ["services", "jobhop"]]),
    # freelancers (ambiguous outcomes)
    (8,  ["backend_django", "fullstack_django"], ["senior", "mid"], "several", ["selftaught", "bootcamp"], ["neutral", "verbose"], [["freelance"]]),
    # career changers (+ gaps)
    (6,  ["backend_django", "data_eng"], "mid", ["several", "one"], ["careerchange"], ["verbose", "neutral"], [["gap"]]),
    # returners with gaps
    (6,  "backend_django", "senior", "several", ["degree", "top_degree"], ["neutral", "terse"], [["gap", "longtenure"], ["gap"]]),
]


def _cycle(v, j):
    return v[j % len(v)] if isinstance(v, (list, tuple)) else v


def build_specs():
    specs, i = [], 0
    for count, spec_o, sen_o, demo_o, routes, styles, sig_sets in ARCHETYPES:
        for j in range(count):
            specs.append((
                i, i % len(CITIES),
                _cycle(spec_o, j), _cycle(sen_o, j), _cycle(demo_o, j),
                routes[j % len(routes)], styles[j % len(styles)],
                list(sig_sets[j % len(sig_sets)]),
            ))
            i += 1
    return specs


SPECS = build_specs()

YEAR_BASE = 2025


def pick_company(specialism, signals):
    if "services" in signals:
        return COMPANIES["services"][0]
    if "startup" in signals or "freelance" in signals:
        return COMPANIES["startup"][0]
    if specialism in ("ml",):
        return COMPANIES["bigtech"][0]
    return COMPANIES["product"][0]


def bullets_for(specialism, seniority, demo, style, name):
    verb = {"led": "Led", "several": "Built", "one": "Contributed to", "claimed": "Worked on", "none": "Studied"}[demo]
    core = {
        "backend_django": f"{verb} the {'patient-records ' if seniority in ('senior','staff','principal') else ''}backend on Django and PostgreSQL",
        "fullstack_django": f"{verb} full-stack features (Django backend, React frontend) on PostgreSQL",
        "backend_other": f"{verb} backend services in Python (FastAPI) on PostgreSQL",
        "data_eng": f"{verb} data pipelines in Python (Airflow, Spark) over SQL warehouses",
        "qa": f"{verb} automated test suites (pytest, Selenium)",
        "devops": f"{verb} infrastructure (Terraform, Kubernetes, AWS)",
        "ml": f"{verb} ML models (PyTorch) and training pipelines",
        "mobile": f"{verb} mobile apps (Kotlin/Swift)",
        "frontend": f"{verb} frontend applications (React, TypeScript)",
    }[specialism]
    scale = {"senior": " serving ~500k users", "staff": " at company scale (millions of requests)",
             "principal": " as chief architect across multiple teams", "mid": " used by real customers",
             "junior": " under senior review", "intern": " as a learning project"}[seniority]
    out = [core + (scale if demo in ("several", "led") else "")]
    if demo in ("several", "led"):
        out.append("Owned the work in production and handled on-call/incidents.")
    if seniority in ("senior", "staff", "principal") and demo == "led":
        out.append("Mentored engineers and set code-review standards.")
    if style == "verbose":
        out = ["I " + b[0].lower() + b[1:] + ", thoughtfully and with great care for craft." for b in out]
    if style == "terse":
        out = [b.split(" serving")[0].split(" used by")[0] for b in out]
    return out


def build(spec):
    ni, ci, specialism, sen, demo, route, style, signals = spec
    name = NAMES[ni]
    city = CITIES[ci]
    years, snr_fit, title_prefix = SENIORITY[sen]
    company = pick_company(specialism, signals)
    grad_year = YEAR_BASE - years - 1
    skills = [{"name": s, "claimed_years": max(1, years - i), "demonstrated_in": (["e1"] if demo != "none" else [])}
              for i, s in enumerate(SPECIALISM_SKILLS[specialism][:4])]

    exp = []
    if demo != "none" or sen != "intern":
        exp.append({
            "id": "e1", "company": company,
            "title": f"{title_prefix}{'Software' if specialism in ('ml','mobile','frontend','devops') else 'Backend'} Engineer".strip(),
            "start": str(YEAR_BASE - years), "end": "present", "location": city,
            "production": DEMO_SHIPPED[demo], "users_claimed": "real users" if DEMO_SHIPPED[demo] else "n/a",
            "bullets": bullets_for(specialism, sen, demo, style, name),
        })
    if "jobhop" in signals:
        exp.append({"id": "e2", "company": COMPANIES["startup"][1], "title": "Engineer",
                    "start": str(YEAR_BASE - years - 1), "end": str(YEAR_BASE - years),
                    "location": city, "production": True, "users_claimed": "some",
                    "bullets": ["Short 10-month stint; left before shipping major work."]})
    if "longtenure" in signals and exp:
        exp[0]["start"] = str(YEAR_BASE - years)

    projects = [{"id": "e1", "title": f"{specialism.replace('_',' ')} work at {company}",
                 "role": {"led": "lead", "several": "core contributor", "one": "contributor",
                          "claimed": "listed", "none": "student"}[demo],
                 "production": DEMO_SHIPPED[demo],
                 "has_problem_process_outcome": demo in ("several", "led"),
                 "summary": " ".join(bullets_for(specialism, sen, demo, style, name))}]

    cand = {
        "name": name,
        "headline": f"{title_prefix}{'Backend' if 'backend' in specialism else specialism.split('_')[0].capitalize()} Engineer".strip(),
        "summary": f"{years} years experience, {specialism.replace('_',' ')}. Based in {city}.",
        "total_years_claimed": years,
        "location": city,
        "skills": skills,
        "experience": exp,
        "education": ROUTES[route].format(grad_year) if "{}" in ROUTES[route] else ROUTES[route],
        "projects": projects,
    }
    if "oss" in signals:
        cand["open_source"] = [{"name": "django-utils-fork (maintainer)", "stars_claimed": "1.8k",
                                "summary": "Maintains a Django utility library used by third parties."}]
    if "pub" in signals:
        cand["publications"] = ["2 first-author papers at ML venues (claimed)"]
    if "gap" in signals:
        cand["career_gap"] = f"{grad_year+2}-{grad_year+4}, caregiving (stated)"
    if "freelance" in signals:
        cand["headline"] = "Freelance " + cand["headline"]

    # ---- heuristic expected label (FLAGGED: needs human review) ----
    fit = SPECIALISM_FIT[specialism] * DEMO[demo]
    score = round(fit * 4, 2)
    lo, hi = max(0.0, score - 0.4), min(4.0, score + 0.4)
    expected = {
        "coreSkillDepth_band": f"{lo:.1f}-{hi:.1f}",
        "seniorityFit": snr_fit,
        "hasShippedProduction": DEMO_SHIPPED[demo],
        "_basis": f"specialism_fit({SPECIALISM_FIT[specialism]}) x demo({DEMO[demo]}) x 4; seniority={sen}",
        "_label_status": "HEURISTIC - review with a recruiter before using as ground truth",
    }
    return {
        "id": f"pop_{spec[0]:02d}_{specialism}_{sen}",
        "tier": 9,
        "label": f"{name} | {specialism} | {sen} | demo={demo} | {route}",
        "candidate": cand,
        "_expected": expected,
    }


def main():
    cases = [build(s) for s in SPECS]
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids)), "duplicate ids"
    spec = {
        "_comment": "Generated by generate_population.py. tier 9 = labelled population. "
                    "_expected labels are HEURISTIC (see _label_status) - review before use.",
        "default_role": DEFAULT_ROLE,
        "roles": {"backend_senior": DEFAULT_ROLE},
        "test_cases": cases,
    }
    out = HERE / "population.json"
    out.write_text(json.dumps(spec, indent=2) + "\n")
    # quick distribution report
    from collections import Counter
    spec_by = Counter(s[2] for s in SPECS)
    sen_by = Counter(s[3] for s in SPECS)
    print(f"Wrote {out} with {len(cases)} candidates.")
    print("By specialism:", dict(spec_by))
    print("By seniority:", dict(sen_by))


if __name__ == "__main__":
    main()
