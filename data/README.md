# Data Overview

All data in this folder is synthetic and reproducible from `scripts/generate_portfolio_artifact.py`.

The synthetic data is modeled on common industrial automation portfolio structures: valves, pneumatic products, regulators, actuators, sensors, controls, product lifecycle stages, ERP item master fields, CRM opportunity feedback, supplier lead-time files, quality claims, sales training trackers, and roadmap intake logs.

## Files

- `product_portfolio.csv`: Product-family and region records used to score portfolio action priority.
- `pricing_obsolescence_cases.csv`: Recommended price, migration, retirement, NPD, and sales enablement cases.
- `npd_gate_candidates.csv`: Early product concepts with value, investment, payback, evidence status, and launch dependency.
- `source_quality_controls.csv`: Data-quality controls for the source signals used in the artifact.

## Assumptions

- Annual revenue is generated in thousands of dollars and varies by product family, region, and lifecycle stage.
- Gross margin is lower for harvest and transition-stage products, and higher for growth and core-stage products.
- Cost inflation, lead time, service burden, and training gaps increase as product families move toward harvest or transition.
- NPD gate readiness is strongest when customer need, product fit, launch readiness, and data confidence are high.
- Transition urgency is strongest when margin gap, cost inflation, lead time, service burden, installed-base dependency, and substitution fit are high.

No row should be interpreted as real company, customer, supplier, SKU, or margin data.
