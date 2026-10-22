# Chart alignment and UI consistency repair — 22 October 2026

## Change scope

| Area | Issue / change | Data handling |
|---|---|---|
| Legacy dashboard ETC reference chart | Dense vertical grouped bars, rotated shipment labels, wrapped legend obscuring bars on small screens. Replaced with horizontal grouped Plotly bars; reserved category space and moved the mobile legend outside the plotting area. | Server-provided ETC, conservative ETC, cutoff balances and no-rate states unchanged, including negative cutoff balances. |
| Legacy truck ready-time chart | Deadline annotations could crowd the upper border and scenario row labels. Adjusted annotation heights and margins; increased row separation. | Uses identical `ready_comparison.py` payload, cutoff and status bands. |
| Manufacturing order status | Three adjacent segments were difficult to distinguish; legend not explicit. Added thin separation, distinct status legend and accessible quantity text. | Counts are still directly calculated from the registered tank records; `good + scrapped + open_wip = total_tanks`. |
| Manufacturing recovery planner | Added an easy-to-read before/after crew comparison with separately aligned bars (not layered/overlapped). Includes **destination and source** station and minimum-safe workforce. | Derives from existing `CENTERS`, scenario workforce and candidate checks; WC1 goes 4 to 5 and WC4 goes 2 to 1 for the fixed, qualified W-012 proposal. No rows, synthetic events, CTQ guide values or historical workbook changed. |
| Forecast copy | Fixed recovery illustration was too easy to confuse with the currently selected what-if scenario. Clearer labels make reference versus selected scenario explicit. | No change to forecast formulas or scenario fixture values. |

## Scope safety

- No changes to routes, database schemas, inspection submission rules, CSV downloads, existing labor computations, forecast engine, or stored shop-floor event history.
- No manufacture of supposedly real output data to aesthetically space the chart.
- The before/after crew preview is **scenario-specific and illustrative**, not a general live resource optimizer. It does not assert any unvalidated production speed-up.

## Validation performed

- `PYTHONPATH=. python scripts/check_manufacturing_templates.py`: 13 manufacturing templates render with strict Jinja variables.
- `PYTHONPATH=. pytest -q tests/test_chart_clarity_20261022.py tests/test_mfg_logic.py tests/test_mfg_render.py tests/test_mfg_schema.py tests/test_shopfloor_logic.py tests/test_reallocation.py`: **76 passed**.
- `python -m compileall -q app.py manufacturing`: syntax passes.
- `node --check static/js/dashboard.js` and `node --check static/js/ready_chart.js`: JavaScript syntax passes.
- Headless Chromium (local Plotly bundle): ETC grouped bar plot rendered successfully at widths 1100 px and 510 px. On narrow view, legend is above bars.
- Headless Chromium (strict Jinja rendered HTML): manufacturing recovery and overview layout inspected at 1440 px and 390 px. Crew bars visually separate, maintain proportional lengths and do not overflow the page.

## Limitations

- Flask is unavailable in this sandbox and package installation is blocked; live GET/POST Flask route smoke tests and interactive end-to-end checks were **not run** here.
- Original legacy truck source database is not populated in this ZIP. Source-dependent historical SMD tests fail on missing tables, unrelated to the presentation-only fixes. The historical SMD app is not wired into the current manufacturing entry point.
- Fixed manufacturing scenario projections remain fictional and are not automatically rescheduled based on supervisor approval. That product limitation remains unchanged.
