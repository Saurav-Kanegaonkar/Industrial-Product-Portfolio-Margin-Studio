-- Illustrative checks for Industrial Product Portfolio Margin Studio
select signal, owner, risk
from source_events
where risk in ('High', 'Medium');
