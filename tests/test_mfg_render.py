"""Render all ten manufacturing pages with strict Jinja fixtures (no Flask needed)."""
from pathlib import Path
from runpy import run_path

def test_ten_pages_strict_jinja_render():
    run_path(str(Path(__file__).resolve().parents[1] / 'scripts' / 'check_manufacturing_templates.py'))
