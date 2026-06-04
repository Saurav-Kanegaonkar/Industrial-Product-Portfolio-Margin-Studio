-- SQL-style checks for a warehouse implementation of this artifact.

-- 1. Product family rows should have all scoring inputs.
select
  count(*) as missing_scoring_inputs
from product_portfolio
where annual_revenue_k is null
  or gross_margin_pct is null
  or cost_inflation_pct is null
  or lead_time_days is null
  or customer_need_score is null
  or data_confidence is null;

-- 2. Business cases should point to valid product families.
select
  c.action_id,
  c.family_id
from pricing_obsolescence_cases c
left join product_portfolio p
  on c.family_id = p.family_id
where p.family_id is null;

-- 3. Gate candidates should have a positive value case.
select
  concept_id,
  estimated_annual_value_k,
  investment_required_k
from npd_gate_candidates
where estimated_annual_value_k <= 0
   or investment_required_k <= 0;

-- 4. Source controls with high failure rates should be visible.
select
  source_system,
  control,
  failure_rate_pct,
  status
from source_quality_controls
where failure_rate_pct >= 10
order by failure_rate_pct desc;
