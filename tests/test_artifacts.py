from pathlib import Path
import hashlib
import io
import json
import tokenize
from html.parser import HTMLParser
import nbformat
import pandas as pd
import pytest
from bike_analysis import prepare_trips, load_clean

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('name,expected', [('Part_I_exploration_template',12), ('Part_II_explanatory_template',4)])
def test_saved_notebooks_have_exact_plot_evidence(name, expected):
    nb = nbformat.read(ROOT / (name+'.ipynb'),4)
    code = [cell for cell in nb.cells if cell.cell_type == 'code' and cell.source.strip()]
    assert code and all(cell.execution_count is not None for cell in code)
    assert not any(out.output_type == 'error' for cell in code for out in cell.outputs)
    images = sum('image/png' in out.get('data',{}) for cell in code for out in cell.outputs)
    assert images == expected
    assert not any(marker in cell.source for cell in nb.cells for marker in ['Your answer here', 'Rubric Tip', 'your name here', 'Dataset Exploration Title'])
    assert any(token.type == tokenize.COMMENT for cell in code for token in tokenize.generate_tokens(io.StringIO(cell.source).readline))
    if expected == 12:
        for index,cell in enumerate(nb.cells):
            if cell.metadata.get('chart_id'):
                assert 'Question' in nb.cells[index-1].source
                assert 'Observations' in nb.cells[index+1].source


class Images(HTMLParser):
    def __init__(self): super().__init__(); self.embedded=0; self.alts=[]
    def handle_starttag(self,tag,attrs):
        if tag=='img' and dict(attrs).get('src','').startswith('data:image/png;base64,'):
            self.embedded+=1
            self.alts.append(dict(attrs).get('alt',''))


@pytest.mark.parametrize('name,count',[('Part_I_exploration_template',12), ('Part_II_explanatory_template',4)])
def test_html_reports_embed_all_figures(name,count):
    parser=Images()
    parser.feed((ROOT/(name+'.html')).read_text())
    assert parser.embedded==count
    assert all(alt and 'No description' not in alt for alt in parser.alts)


def test_explanatory_html_has_a_report_title_and_hides_runtime_diagnostics():
    html=(ROOT/'Part_II_explanatory_template.html').read_text()
    assert '<title>Ford GoBike — Explanatory Findings</title>' in html
    assert 'Verified shared analysis population:' not in html
    assert 'https://s3.amazonaws.com/baywheels-data/201902-fordgobike-tripdata.csv.zip' in html


@pytest.mark.parametrize('name',['Part_I_exploration_template','Part_II_explanatory_template'])
def test_generated_html_has_no_trailing_whitespace(name):
    lines=(ROOT/(name+'.html')).read_text().splitlines()
    assert all(line == line.rstrip() for line in lines)


def test_data_provenance_and_clean_reconstruction():
    metadata=json.loads((ROOT/'data/raw/provenance.json').read_text())
    path=ROOT/'data/raw/201902-fordgobike-tripdata.csv'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==metadata['csv_sha256']
    rebuilt,audit=prepare_trips(pd.read_csv(path))
    stored=load_clean(ROOT/'data/cleaned/february_2019_trips.csv')
    pd.testing.assert_frame_equal(rebuilt,stored)
    assert audit['input_rows']==183412 and audit['output_rows']==183412
    assert stored.duration_min.max()>1000
