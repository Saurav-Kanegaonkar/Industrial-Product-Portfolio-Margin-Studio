const artifact = window.portfolioArtifact;

const money = (value) => `$${Number(value).toLocaleString(undefined, { maximumFractionDigits: 0 })}k`;
const pct = (value) => `${Number(value).toFixed(1)}%`;
const node = (tag, className, html = "") => {
  const element = document.createElement(tag);
  if (className) element.className = className;
  element.innerHTML = html;
  return element;
};

const statusClass = (status) => {
  const normalized = String(status).toLowerCase().replaceAll(" ", "-");
  return `status ${normalized}`;
};

const table = (columns, rows) => `
  <div class="table-shell">
    <table>
      <thead>
        <tr>${columns.map((column) => `<th>${column.label}</th>`).join("")}</tr>
      </thead>
      <tbody>
        ${rows.map((row) => `
          <tr>
            ${columns.map((column) => `<td>${column.render ? column.render(row) : row[column.key]}</td>`).join("")}
          </tr>
        `).join("")}
      </tbody>
    </table>
  </div>
`;

const renderCards = () => {
  const grid = document.querySelector("#metric-grid");
  grid.replaceChildren(...artifact.cards.map((card) => node("article", "metric", `
    <span>${card.label}</span>
    <strong>${card.value}</strong>
    <small>${card.note}</small>
  `)));
};

const renderStageMix = () => {
  const total = Object.values(artifact.stageCounts).reduce((sum, value) => sum + value, 0);
  const labels = Object.entries(artifact.stageCounts).map(([stage, count]) => {
    const width = Math.round((count / total) * 100);
    return `
      <div class="stage-row">
        <div class="stage-label"><span>${stage}</span><strong>${count}</strong></div>
        <div class="track"><div class="fill ${stage}" style="width: ${width}%"></div></div>
      </div>
    `;
  });
  document.querySelector("#stage-mix").innerHTML = labels.join("");
};

const renderPlatformBars = () => {
  const maxRevenue = Math.max(...artifact.platforms.map((row) => row.revenue_k));
  const rows = artifact.platforms.map((row) => `
    <div class="bar-row">
      <div class="bar-label">
        <strong>${row.platform}</strong>
        <span>${money(row.revenue_k)} revenue, ${pct(row.gross_margin_pct)} margin</span>
      </div>
      <div class="track"><div class="fill score" style="width: ${Math.max(8, row.revenue_k / maxRevenue * 100)}%"></div></div>
      <div class="score-grid">
        <span>Transition ${pct(row.avg_transition_urgency)}</span>
        <span>Pricing ${pct(row.avg_pricing_confidence)}</span>
        <span>NPD ${pct(row.avg_npd_gate_score)}</span>
      </div>
    </div>
  `);
  document.querySelector("#platform-bars").innerHTML = rows.join("");
};

const renderPortfolioTable = () => {
  document.querySelector("#portfolio-table").innerHTML = table([
    { label: "Family", render: (row) => `<strong>${row.family_name}</strong><small>${row.region_scope}</small>` },
    { label: "Stage", key: "lifecycle_stage" },
    { label: "Margin", render: (row) => pct(row.gross_margin_pct) },
    { label: "Lead Time", render: (row) => `${row.lead_time_days} days` },
    { label: "Transition", render: (row) => pct(row.transition_urgency) },
    { label: "Action Score", render: (row) => `<span class="score-pill">${pct(row.portfolio_action_score)}</span>` },
  ], artifact.topProducts);
};

const renderCases = () => {
  const cards = artifact.businessCases.map((item) => node("article", "case-card", `
    <div class="case-header">
      <span>${item.action_type}</span>
      <strong>${money(item.annual_margin_lift_k)}</strong>
    </div>
    <h3>${item.family_name}</h3>
    <p>${item.region_scope}. ${item.rationale}.</p>
    <dl>
      <div><dt>Revenue at risk</dt><dd>${money(item.revenue_at_risk_k)}</dd></div>
      <div><dt>Owner</dt><dd>${item.cross_functional_owner}</dd></div>
      <div><dt>Confidence</dt><dd><span class="${statusClass(item.confidence)}">${item.confidence}</span></dd></div>
      <div><dt>Time to value</dt><dd>${item.time_to_value_months} months</dd></div>
    </dl>
    <footer>${item.next_gate}</footer>
  `));
  document.querySelector("#case-grid").replaceChildren(...cards);
};

const renderNpd = () => {
  document.querySelector("#npd-table").innerHTML = table([
    { label: "Concept", render: (row) => `<strong>${row.concept_name}</strong><small>${row.platform}</small>` },
    { label: "Value", render: (row) => money(row.estimated_annual_value_k) },
    { label: "Investment", render: (row) => money(row.investment_required_k) },
    { label: "Payback", render: (row) => `${row.payback_months} months` },
    { label: "Gate Score", render: (row) => `<span class="score-pill">${pct(row.gate_score)}</span>` },
    { label: "Evidence", render: (row) => `<span class="${statusClass(row.evidence_status)}">${row.evidence_status}</span>` },
  ], artifact.npdConcepts);

  document.querySelector("#role-fit").replaceChildren(...artifact.roleFit.map((item) => node("div", "check-item", `
    <span>OK</span>
    <p>${item}</p>
  `)));
};

const renderQuality = () => {
  document.querySelector("#quality-table").innerHTML = table([
    { label: "Source", render: (row) => `<strong>${row.source_system}</strong><small>${row.owner}</small>` },
    { label: "Control", key: "control" },
    { label: "Records", render: (row) => Number(row.records_checked).toLocaleString() },
    { label: "Failures", render: (row) => Number(row.failed_records).toLocaleString() },
    { label: "Failure Rate", render: (row) => pct(row.failure_rate_pct) },
    { label: "Status", render: (row) => `<span class="${statusClass(row.status)}">${row.status}</span>` },
  ], artifact.qualityControls);
};

const bindTabs = () => {
  document.querySelectorAll(".tab").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".tab").forEach((tab) => tab.classList.remove("is-active"));
      document.querySelectorAll(".surface").forEach((surface) => surface.classList.remove("is-visible"));
      button.classList.add("is-active");
      document.querySelector(`#surface-${button.dataset.surface}`).classList.add("is-visible");
    });
  });
};

renderCards();
renderStageMix();
renderPlatformBars();
renderPortfolioTable();
renderCases();
renderNpd();
renderQuality();
bindTabs();
