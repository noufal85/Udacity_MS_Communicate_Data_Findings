"""Execute both notebooks in new kernels and export self-contained figure reports."""
from pathlib import Path
import os
import sys
import tempfile
import copy
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from jupyter_client import KernelManager

root=Path(__file__).resolve().parent
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'communicate-findings-mpl'))
os.environ.setdefault('MPLBACKEND','Agg')
os.environ.setdefault('IPYTHONDIR',str(Path(tempfile.gettempdir())/'communicate-findings-ipython'))

for name in ['Part_I_exploration_template','Part_II_explanatory_template']:
    path=root/(name+'.ipynb')
    notebook=nbformat.read(path,4)
    manager=KernelManager(kernel_name='python3')
    manager.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
    NotebookClient(notebook,km=manager,timeout=240,resources={'metadata':{'path':str(root)}}).execute()
    nbformat.write(notebook,path)
    report=copy.deepcopy(notebook)
    if name.startswith('Part_II'):
        report.cells=[cell for cell in report.cells if 'report_setup' not in cell.metadata.get('tags',[])]
    exporter=HTMLExporter(template_name='classic')
    exporter.exclude_input=name.startswith('Part_II')
    exporter.exclude_input_prompt=True
    exporter.exclude_output_prompt=True
    exporter.embed_images=True
    title='Ford GoBike — '+('Explanatory Findings' if name.startswith('Part_II') else 'Exploratory Analysis')
    body,_=exporter.from_notebook_node(report,resources={'metadata':{'name':title}})
    body='\n'.join(line.rstrip() for line in body.splitlines())+'\n'
    (root/(name+'.html')).write_text(body,encoding='utf-8')
    print('Executed and exported:',name,flush=True)
