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

NAMES = [
    "Rahul Sharma", "Priya Nair", "Imran Qureshi", "Anthony Fernandes", "Sneha Patel",
    "Arjun Reddy", "Fatima Sheikh", "Joseph Mathew", "Ananya Ghosh", "Vikas Yadav",
    "Meera Iyer", "Daniyal Khan", "Grace DSouza", "Rohit Verma", "Lakshmi Menon",
    "Sahil Kapoor", "Aisha Begum", "Thomas Varghese", "Divya Rao", "Karan Mehta",
    "Zoya Ansari", "Nikhil Joshi", "Ritu Agarwal", "Sunil Pillai", "Nadia Hussain",
    "Aditya Bose", "Kavya Krishnan", "Farhan Ali", "Neha Gupta", "Manish Tiwari",
    "Pooja Shetty", "Yusuf Ahmed", "Rebecca Thomas", "Harsh Vardhan", "Ishita Sen",
    "Deepak Choudhary", "Sara Kurian", "Amit Ranjan", "Tara Malhotra", "Omar Farooq",
]
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

# ---- SPECS: (name_i, city_i, specialism, seniority, demo, route, style, signals) #
# style: neutral|terse|verbose ; signals: subset of gap/jobhop/oss/pub/longtenure/freelance/services
SPECS = [
    # --- strong backend-django matches, various seniorities/styles ---
    (0, 0, "backend_django", "senior", "led", "top_degree", "neutral", []),
    (1, 1, "backend_django", "senior", "several", "degree", "verbose", ["longtenure"]),
    (2, 2, "backend_django", "mid", "several", "degree", "neutral", []),
    (3, 3, "backend_django", "junior", "one", "bootcamp", "neutral", []),
    (4, 4, "backend_django", "staff", "led", "top_degree", "terse", ["oss"]),
    (5, 5, "backend_django", "principal", "led", "degree", "verbose", ["longtenure"]),
    (6, 6, "backend_django", "senior", "several", "selftaught", "neutral", ["oss"]),
    (7, 7, "backend_django", "mid", "one", "careerchange", "neutral", ["gap"]),
    (8, 8, "backend_django", "senior", "several", "degree", "terse", ["gap"]),
    (9, 9, "fullstack_django", "senior", "several", "degree", "neutral", ["startup"]),
    (10, 0, "fullstack_django", "mid", "several", "bootcamp", "verbose", []),
    (11, 1, "fullstack_django", "junior", "one", "degree", "neutral", []),
    # --- adjacent (partial fit): backend but not django ---
    (12, 2, "backend_other", "senior", "led", "top_degree", "neutral", []),
    (13, 3, "backend_other", "mid", "several", "degree", "neutral", ["jobhop"]),
    (14, 4, "backend_other", "senior", "several", "degree", "terse", []),
    # --- data engineering (weak-ish fit for this role) ---
    (15, 5, "data_eng", "senior", "led", "degree", "neutral", []),
    (16, 6, "data_eng", "mid", "several", "mca", "verbose", []),
    # --- ML / research (poor fit) ---
    (17, 7, "ml", "senior", "led", "phd", "verbose", ["pub"]),
    (18, 8, "ml", "mid", "several", "degree", "neutral", []),
    # --- frontend / mobile / devops / qa (poor fit, tests discrimination) ---
    (19, 9, "frontend", "senior", "led", "degree", "neutral", []),
    (20, 0, "mobile", "senior", "several", "degree", "neutral", []),
    (21, 1, "devops", "senior", "led", "degree", "terse", ["oss"]),
    (22, 2, "qa", "mid", "several", "degree", "neutral", []),
    # --- services-company (unclear ownership) ---
    (23, 3, "backend_django", "senior", "several", "mca", "verbose", ["services"]),
    (24, 4, "fullstack_django", "mid", "several", "degree", "neutral", ["services", "jobhop"]),
    # --- freelancers ---
    (25, 5, "backend_django", "mid", "several", "selftaught", "neutral", ["freelance"]),
    (26, 6, "fullstack_django", "senior", "several", "bootcamp", "verbose", ["freelance"]),
    # --- juniors / interns / tutorial-level (weak) ---
    (27, 7, "backend_django", "intern", "one", "degree", "neutral", []),
    (28, 8, "fullstack_django", "junior", "claimed", "bootcamp", "verbose", []),
    (29, 9, "backend_django", "junior", "none", "selftaught", "verbose", []),
    # --- claims-heavy / weak substance ---
    (30, 0, "backend_django", "mid", "claimed", "degree", "verbose", []),
    (31, 1, "backend_other", "junior", "claimed", "bootcamp", "verbose", []),
    # --- overqualified ---
    (32, 2, "backend_django", "principal", "led", "top_degree", "terse", ["oss", "longtenure"]),
    (33, 3, "backend_django", "staff", "led", "degree", "neutral", ["longtenure"]),
    # --- career changers ---
    (34, 4, "backend_django", "mid", "several", "careerchange", "verbose", ["gap"]),
    (35, 5, "data_eng", "mid", "several", "careerchange", "neutral", ["gap"]),
    # --- returners / gaps ---
    (36, 6, "backend_django", "senior", "several", "degree", "neutral", ["gap", "longtenure"]),
    (37, 7, "fullstack_django", "senior", "several", "degree", "terse", ["gap"]),
    # --- strong OSS but thin employment ---
    (38, 8, "backend_django", "junior", "several", "selftaught", "neutral", ["oss"]),
    # --- solid mid, unremarkable ---
    (39, 9, "backend_django", "mid", "several", "degree", "neutral", []),
]

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
