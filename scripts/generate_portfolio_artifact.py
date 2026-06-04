import csv
import json
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "analysis" / "outputs"
SRC_DIR = ROOT / "src"
SEED = 42


PRODUCT_BLUEPRINTS = [
    ("PF001", "Solenoid Valve Platform", "Fluid control", "valves"),
    ("PF002", "Pneumatic Cylinder Range", "Motion control", "pneumatics"),
    ("PF003", "Valve Island Controls", "Motion control", "controls"),
    ("PF004", "Precision Regulator Family", "Pressure control", "regulators"),
    ("PF005", "Hazardous Location Switches", "Position sensing", "sensors"),
    ("PF006", "Actuator Accessory Kit", "Valve automation", "actuators"),
    ("PF007", "Miniature Analytical Valve", "Analytical devices", "valves"),
    ("PF008", "Smart Air Preparation Unit", "Factory automation", "pneumatics"),
    ("PF009", "High Pressure Gas Regulator", "Pressure control", "regulators"),
    ("PF010", "Discrete Valve Monitor", "Position sensing", "sensors"),
    ("PF011", "Legacy Manifold Series", "Fluid control", "valves"),
    ("PF012", "Electric Motion Module", "Motion control", "actuators"),
]

LIFECYCLE_FACTORS = {
    "growth": {"margin": 0.42, "inflation": 0.04, "service": 0.16, "dependency": 0.46},
    "core": {"margin": 0.37, "inflation": 0.06, "service": 0.24, "dependency": 0.66},
    "mature": {"margin": 0.31, "inflation": 0.09, "service": 0.38, "dependency": 0.78},
    "harvest": {"margin": 0.25, "inflation": 0.12, "service": 0.54, "dependency": 0.71},
    "transition": {"margin": 0.22, "inflation": 0.14, "service": 0.68, "dependency": 0.58},
}

STAGES = ["growth", "core", "mature", "harvest", "transition"]
REGIONS = ["North America", "EMEA", "APAC", "Latin America"]
OWNERS = ["Product", "Sales", "Operations", "Supply chain", "Engineering"]


def clamp(value, low, high):
    return max(low, min(high, value))


def score_product(row):
    margin_gap = clamp((35 - row["gross_margin_pct"]) / 20, 0, 1)
    inflation = clamp(row["cost_inflation_pct"] / 18, 0, 1)
    lead_time = clamp((row["lead_time_days"] - 35) / 95, 0, 1)
    service_drag = clamp(row["service_burden"] / 100, 0, 1)
    competitive = clamp(row["competitive_pressure"] / 100, 0, 1)
    need = clamp(row["customer_need_score"] / 100, 0, 1)
    dependency = clamp(row["installed_base_dependency"] / 100, 0, 1)
    substitution = clamp(row["substitution_fit"] / 100, 0, 1)
    transition = 100 * (
        0.22 * margin_gap
        + 0.15 * inflation
        + 0.13 * lead_time
        + 0.14 * service_drag
        + 0.10 * competitive
        + 0.13 * dependency
        + 0.13 * substitution
    )
    npd = 100 * (
        0.24 * need
        + 0.20 * clamp(row["npd_fit"] / 100, 0, 1)
        + 0.18 * clamp(row["launch_readiness"] / 100, 0, 1)
        + 0.15 * (1 - margin_gap)
        + 0.13 * (1 - lead_time)
        + 0.10 * (1 - service_drag)
    )
    pricing = 100 * (
        0.32 * margin_gap
        + 0.20 * inflation
        + 0.18 * competitive
        + 0.18 * need
        + 0.12 * clamp(row["data_confidence"] / 100, 0, 1)
    )
    return {
        "transition_urgency": round(transition, 1),
        "npd_gate_score": round(npd, 1),
        "pricing_confidence": round(pricing, 1),
        "portfolio_action_score": round(0.44 * transition + 0.32 * pricing + 0.24 * npd, 1),
    }


def make_products():
    random.seed(SEED)
    rows = []
    for index, (family_id, family_name, platform, category) in enumerate(PRODUCT_BLUEPRINTS):
        stage = STAGES[index % len(STAGES)]
        factors = LIFECYCLE_FACTORS[stage]
        for region_index, region in enumerate(REGIONS):
            revenue_k = random.randint(740, 4600) + index * 190 + region_index * 85
            margin = clamp(random.gauss(factors["margin"], 0.045), 0.16, 0.49)
            cost_inflation = clamp(random.gauss(factors["inflation"], 0.018), 0.015, 0.19)
            lead_days = int(clamp(random.gauss(38 + index * 3 + factors["inflation"] * 280, 13), 18, 135))
            warranty = clamp(random.gauss(1.4 + factors["service"] * 5, 0.7), 0.4, 8.8)
            dependency = clamp(random.gauss(factors["dependency"] * 100, 10), 20, 96)
            need = clamp(random.gauss(72 if stage in ("growth", "core") else 58, 13), 24, 96)
            pressure = clamp(random.gauss(46 + factors["inflation"] * 220, 14), 18, 92)
            service = clamp(random.gauss(factors["service"] * 100, 12), 8, 94)
            training_gap = clamp(random.gauss(30 + factors["service"] * 45, 12), 8, 88)
            substitution = clamp(random.gauss(64 if stage in ("harvest", "transition") else 44, 13), 12, 92)
            npd_fit = clamp(random.gauss(70 if stage in ("growth", "core", "mature") else 53, 12), 18, 94)
            launch_readiness = clamp(random.gauss(62 if stage in ("growth", "core") else 48, 14), 15, 91)
            confidence = clamp(random.gauss(83 - factors["service"] * 24, 8), 42, 96)
            row = {
                "family_id": family_id,
                "family_name": family_name,
                "platform": platform,
                "category": category,
                "lifecycle_stage": stage,
                "region_scope": region,
                "annual_revenue_k": int(revenue_k),
                "gross_margin_pct": round(margin * 100, 1),
                "unit_volume": int(revenue_k * random.uniform(4.5, 14.5)),
                "list_price_index": round(random.uniform(92, 118), 1),
                "cost_inflation_pct": round(cost_inflation * 100, 1),
                "lead_time_days": lead_days,
                "warranty_claim_rate_pct": round(warranty, 1),
                "installed_base_dependency": round(dependency, 1),
                "customer_need_score": round(need, 1),
                "competitive_pressure": round(pressure, 1),
                "service_burden": round(service, 1),
                "training_gap": round(training_gap, 1),
                "substitution_fit": round(substitution, 1),
                "npd_fit": round(npd_fit, 1),
                "launch_readiness": round(launch_readiness, 1),
                "data_confidence": round(confidence, 1),
            }
            row.update(score_product(row))
            rows.append(row)
    return rows


def make_business_cases(products):
    cases = []
    top = sorted(products, key=lambda row: row["portfolio_action_score"], reverse=True)[:14]
    for index, row in enumerate(top, start=1):
        if row["transition_urgency"] > 68 and row["substitution_fit"] > 58:
            action = "Migration and retirement"
            next_gate = "Substitution map and last-time-buy plan"
            lift = row["annual_revenue_k"] * 0.085 + row["service_burden"] * 4.5
            risk = row["annual_revenue_k"] * (0.07 + row["installed_base_dependency"] / 1000)
        elif row["pricing_confidence"] > 60:
            action = "Targeted price reset"
            next_gate = "Distributor impact review"
            lift = row["annual_revenue_k"] * 0.052 + row["cost_inflation_pct"] * 18
            risk = row["annual_revenue_k"] * 0.045
        elif row["npd_gate_score"] > 63:
            action = "NPD discovery gate"
            next_gate = "Concept charter and alpha customer evidence"
            lift = row["annual_revenue_k"] * 0.11
            risk = row["annual_revenue_k"] * 0.035
        else:
            action = "Sales enablement refresh"
            next_gate = "Positioning update and training package"
            lift = row["annual_revenue_k"] * 0.036 + row["training_gap"] * 5
            risk = row["annual_revenue_k"] * 0.025
        confidence = "High" if row["data_confidence"] >= 78 else "Medium" if row["data_confidence"] >= 62 else "Needs validation"
        cases.append({
            "action_id": f"CASE{index:03d}",
            "family_id": row["family_id"],
            "family_name": row["family_name"],
            "region_scope": row["region_scope"],
            "action_type": action,
            "rationale": f"{row['lifecycle_stage']} lifecycle, {row['gross_margin_pct']}% margin, {row['lead_time_days']} day lead time",
            "annual_margin_lift_k": round(lift, 1),
            "revenue_at_risk_k": round(risk, 1),
            "confidence": confidence,
            "cross_functional_owner": OWNERS[index % len(OWNERS)],
            "next_gate": next_gate,
            "time_to_value_months": 2 + index % 5,
        })
    return cases


def make_npd(products):
    concepts = []
    candidates = sorted(products, key=lambda row: row["npd_gate_score"], reverse=True)[:10]
    for index, row in enumerate(candidates, start=1):
        investment = round(row["annual_revenue_k"] * random.uniform(0.10, 0.24), 1)
        value = round(row["annual_revenue_k"] * random.uniform(0.18, 0.42), 1)
        concepts.append({
            "concept_id": f"NPD{index:03d}",
            "platform": row["platform"],
            "concept_name": f"{row['family_name']} next generation option",
            "customer_problem": "Reduce integration time, warranty friction, and field substitution risk",
            "estimated_annual_value_k": value,
            "investment_required_k": investment,
            "gate_score": row["npd_gate_score"],
            "payback_months": max(6, int(math.ceil(12 * investment / max(value, 1)))),
            "evidence_status": "Gate ready" if row["npd_gate_score"] >= 70 else "Needs customer proof",
            "sales_enablement_need": "Competitive positioning, launch training, and distributor objection handling",
            "launch_dependency": "Supplier qualification" if row["lead_time_days"] > 75 else "Pilot account feedback",
        })
    return concepts


def make_quality_controls():
    controls = [
        ("ERP item master", "Lifecycle status mapped to SKU family", 1248, 18, "watch"),
        ("ERP margin extract", "Unit cost and list price joined by active SKU", 1248, 11, "pass"),
        ("CRM opportunity export", "Win loss reason captured for priced quotes", 836, 74, "watch"),
        ("Supplier lead time file", "Lead time present for constrained components", 392, 37, "watch"),
        ("Quality claims log", "Warranty claims linked to product family", 618, 16, "pass"),
        ("Sales training tracker", "Launch and transition training completion", 455, 91, "fail"),
        ("Roadmap intake", "NPD idea has problem statement and value hypothesis", 68, 7, "watch"),
        ("Distributor feedback notes", "Competitive pressure coded by category", 291, 29, "watch"),
    ]
    rows = []
    for index, (source, check, records, failures, status) in enumerate(controls, start=1):
        rows.append({
            "control_id": f"DQ{index:03d}",
            "source_system": source,
            "control": check,
            "records_checked": records,
            "failed_records": failures,
            "failure_rate_pct": round(100 * failures / records, 1),
            "status": status,
            "owner": OWNERS[index % len(OWNERS)],
        })
    return rows


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_payload(products, cases, concepts, controls):
    total_revenue = sum(row["annual_revenue_k"] for row in products)
    weighted_margin = sum(row["annual_revenue_k"] * row["gross_margin_pct"] for row in products) / total_revenue
    margin_at_risk = sum(case["revenue_at_risk_k"] for case in cases if case["action_type"] != "NPD discovery gate")
    lift = sum(case["annual_margin_lift_k"] for case in cases)
    stage_counts = {stage: sum(1 for row in products if row["lifecycle_stage"] == stage) for stage in STAGES}
    platform_rows = []
    for platform in sorted({row["platform"] for row in products}):
        subset = [row for row in products if row["platform"] == platform]
        revenue = sum(row["annual_revenue_k"] for row in subset)
        margin = sum(row["annual_revenue_k"] * row["gross_margin_pct"] for row in subset) / revenue
        platform_rows.append({
            "platform": platform,
            "revenue_k": round(revenue, 1),
            "gross_margin_pct": round(margin, 1),
            "avg_transition_urgency": round(sum(row["transition_urgency"] for row in subset) / len(subset), 1),
            "avg_pricing_confidence": round(sum(row["pricing_confidence"] for row in subset) / len(subset), 1),
            "avg_npd_gate_score": round(sum(row["npd_gate_score"] for row in subset) / len(subset), 1),
        })
    return {
        "generatedFrom": "scripts/generate_portfolio_artifact.py",
        "cards": [
            {"label": "Portfolio revenue", "value": f"${total_revenue / 1000:.1f}M", "note": "synthetic annualized"},
            {"label": "Weighted margin", "value": f"{weighted_margin:.1f}%", "note": "portfolio mix"},
            {"label": "Margin lift queue", "value": f"${lift / 1000:.1f}M", "note": "ranked actions"},
            {"label": "Revenue at risk", "value": f"${margin_at_risk / 1000:.1f}M", "note": "transition and price"},
        ],
        "stageCounts": stage_counts,
        "platforms": sorted(platform_rows, key=lambda row: row["avg_transition_urgency"], reverse=True),
        "topProducts": sorted(products, key=lambda row: row["portfolio_action_score"], reverse=True)[:12],
        "businessCases": cases,
        "npdConcepts": concepts,
        "qualityControls": controls,
        "roleFit": [
            "Product lifecycle and portfolio tradeoff logic",
            "Pricing and gross-margin business case framing",
            "Early NPD gate evidence and sales enablement handoff",
            "ERP, CRM, supplier, quality, and training data confidence",
        ],
    }


def main():
    DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    products = make_products()
    cases = make_business_cases(products)
    concepts = make_npd(products)
    controls = make_quality_controls()
    payload = build_payload(products, cases, concepts, controls)

    write_csv(DATA_DIR / "product_portfolio.csv", products)
    write_csv(DATA_DIR / "pricing_obsolescence_cases.csv", cases)
    write_csv(DATA_DIR / "npd_gate_candidates.csv", concepts)
    write_csv(DATA_DIR / "source_quality_controls.csv", controls)
    with (OUTPUT_DIR / "app_payload.json").open("w") as file:
        json.dump(payload, file, indent=2)
    with (SRC_DIR / "data.js").open("w") as file:
        file.write("window.portfolioArtifact = ")
        json.dump(payload, file, indent=2)
        file.write(";\n")

    print("Generated portfolio artifact data")
    print(f"Product family rows: {len(products)}")
    print(f"Business cases: {len(cases)}")
    print(f"NPD concepts: {len(concepts)}")
    print(f"Quality controls: {len(controls)}")


if __name__ == "__main__":
    main()
