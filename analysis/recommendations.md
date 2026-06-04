# Analytical Recommendations

## What Stands Out

- Obsolescence risk is highest where low-margin SKUs still absorb sales training and inventory attention.
- Customer feedback and supplier constraints point to different priorities unless weighted through business-case value.
- A simple gate score exposes which launch ideas have enough evidence to enter NPD discovery.

## Recommended Operating Moves

- Retire low-margin, low-demand SKUs after mapping customer substitution paths and sales enablement needs.
- Prioritize NPD concepts that improve both portfolio fit and supply-chain feasibility before gate review.
- Create a recurring KPI readout that ties pricing, product availability, and customer feedback to roadmap choices.

## How I Would Use The Data

1. Start with `daily_metrics.csv` to identify entities with worsening priority scores.
2. Join `source_events.csv` to separate true business movement from freshness or definition issues.
3. Use `stakeholder_requirements.csv` to confirm whether the dashboard is answering a decision, not just visualizing a number.
4. Use `data_quality_checks.csv` to block recommendations where the source is unreliable.
5. Push the final action queue from `recommended_actions.csv` into roadmap or operating review follow-up.
