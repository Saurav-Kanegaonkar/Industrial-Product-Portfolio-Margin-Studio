# Data Dictionary

## product_portfolio.csv

| Column | Description |
| --- | --- |
| family_id | Synthetic product family identifier. |
| family_name | Product family label modeled on industrial automation categories. |
| platform | Portfolio platform, such as fluid control, pressure control, or motion control. |
| category | Product category. |
| lifecycle_stage | Growth, core, mature, harvest, or transition. |
| region_scope | Region for the portfolio record. |
| annual_revenue_k | Synthetic annualized revenue in thousands of dollars. |
| gross_margin_pct | Synthetic gross margin percentage. |
| unit_volume | Synthetic annual unit volume. |
| list_price_index | Relative list price index. |
| cost_inflation_pct | Synthetic cost inflation percentage. |
| lead_time_days | Supplier or component lead-time signal. |
| warranty_claim_rate_pct | Warranty claim rate proxy. |
| installed_base_dependency | Index for customer installed-base dependency. |
| customer_need_score | Index for customer pull or problem urgency. |
| competitive_pressure | Index for competitor or substitution pressure. |
| service_burden | Index for support and service friction. |
| training_gap | Index for sales and channel enablement gap. |
| substitution_fit | Index for migration or replacement feasibility. |
| npd_fit | Index for roadmap fit. |
| launch_readiness | Index for launch execution readiness. |
| data_confidence | Index for source quality and reconciliation confidence. |
| transition_urgency | Weighted score for migration, retirement, or transition action. |
| npd_gate_score | Weighted score for early NPD gate readiness. |
| pricing_confidence | Weighted score for price action confidence. |
| portfolio_action_score | Combined portfolio priority score. |

## pricing_obsolescence_cases.csv

| Column | Description |
| --- | --- |
| action_id | Synthetic case identifier. |
| family_id | Product family identifier. |
| family_name | Product family label. |
| region_scope | Region for the case. |
| action_type | Price, migration, retirement, NPD, or enablement move. |
| rationale | Short reason built from lifecycle, margin, and lead-time signals. |
| annual_margin_lift_k | Estimated annual margin lift in thousands of dollars. |
| revenue_at_risk_k | Revenue at risk in thousands of dollars. |
| confidence | Data and business confidence level. |
| cross_functional_owner | Function expected to own the next action. |
| next_gate | Next decision gate or evidence requirement. |
| time_to_value_months | Estimated time to value. |

## npd_gate_candidates.csv

| Column | Description |
| --- | --- |
| concept_id | Synthetic NPD concept identifier. |
| platform | Portfolio platform. |
| concept_name | Concept label. |
| customer_problem | Problem statement. |
| estimated_annual_value_k | Estimated annual value in thousands of dollars. |
| investment_required_k | Estimated investment in thousands of dollars. |
| gate_score | NPD gate readiness score. |
| payback_months | Estimated payback period. |
| evidence_status | Gate-ready or needs customer proof. |
| sales_enablement_need | Sales handoff requirement. |
| launch_dependency | Launch dependency to resolve. |

## source_quality_controls.csv

| Column | Description |
| --- | --- |
| control_id | Synthetic data control identifier. |
| source_system | Source-system label. |
| control | Control performed against the source. |
| records_checked | Synthetic record count checked. |
| failed_records | Synthetic failure count. |
| failure_rate_pct | Failure rate percentage. |
| status | Pass, watch, or fail. |
| owner | Function responsible for follow-up. |
