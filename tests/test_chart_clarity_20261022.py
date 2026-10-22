"""Chart/UI regression: safe source-to-destination staff counts and independent bars."""
from pathlib import Path

from manufacturing.model import CENTERS, reference_transfer_crew, verify_candidate

ROOT = Path(__file__).resolve().parents[1]


def test_recovery_chart_conserves_workers_and_meets_minimum_crews():
    data = reference_transfer_crew()
    assert data['feasible'] == verify_candidate('W-012', 'combined', '10:55')['feasible']
    assert data['scenario'] == 'combined' and data['reference_time'] == '10:55'
    by_station = {r['id']: r for r in data['rows']}
    assert by_station['WC1']['before'] == 4 and by_station['WC1']['after'] == 5
    assert by_station['WC4']['before'] == 2 and by_station['WC4']['after'] == 1
    assert sum(r['before'] for r in data['rows']) == sum(r['after'] for r in data['rows'])
    assert all(r['safe'] and r['after'] >= r['minimum'] for r in data['rows'])
    for row in data['rows']:
        assert row['planned'] == next(c['planned'] for c in CENTERS if c['id'] == row['id'])
        assert all(0 <= row[p] / row['scale'] <= 1 for p in ('before', 'after'))


def test_recovery_preview_is_labelled_and_not_a_new_production_forecast():
    tpl = (ROOT / 'templates/mfg/recovery.html').read_text()
    assert 'Staffing before and after the proposed transfer' in tpl
    assert 'not a live reassignment' in tpl
    assert "center[point]" in tpl and "center.scale" in tpl
    assert 'minimum {{center.minimum}}' in tpl
    assert 'crew-fill {{point}}' in tpl
    mfg_css = (ROOT / 'static/css/manufacturing.css').read_text()
    assert '.crew-row{display:grid' in mfg_css
    assert '.crew-groups{display:grid' in mfg_css


def test_truck_reference_bars_grouped_horizontally_not_overlaid():
    js = (ROOT / 'static/js/dashboard.js').read_text()
    assert "orientation:'h'" in js
    assert "offsetgroup:'etc'" in js and "offsetgroup:'cutoff'" in js
    assert "barmode:'group'" in js and 'bargap:0.34' in js
    assert "type:'scatter',mode:'markers',name:'Conservative ETC (h)'" in js
    assert "x:valid.map(x=>x.etc)" in js
    assert "x:valid.map(x=>x.cutoff)" in js
    ready_js = (ROOT / 'static/js/ready_chart.js').read_text()
    assert "barmode: 'group'" in ready_js
    assert '1.025' in ready_js and '1.105' in ready_js


def test_order_status_segments_keep_live_counts_not_hardcoded():
    tpl = (ROOT / 'templates/mfg/dashboard.html').read_text()
    for key in ('good', 'open_wip', 'scrapped'):
        assert f'stats.{key} / stats.total_tanks' in tpl
    assert 'Reference case · before recovery' in tpl
    assert "9 if asof>=" not in tpl
