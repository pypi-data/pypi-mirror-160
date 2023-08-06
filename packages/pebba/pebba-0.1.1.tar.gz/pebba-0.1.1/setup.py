# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pebba', 'pebba.analysis', 'pebba.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.1,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'plotly>=5.9.0,<6.0.0',
 'scipy>=1.8.1,<2.0.0',
 'statsmodels>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'pebba',
    'version': '0.1.1',
    'description': 'A tool for ORA meta-analysis',
    'long_description': '<p align="center">\n  <img  src="https://raw.githubusercontent.com/csbl-br/pebba/master/PEBBA_banner.png">\n</p>\n\n---------------------------------------\n\nOver-representation analysis (ORA) is a critical technique to determine if a set of differentially expressed genes (DEGs) is enriched with genes from specific gene sets or pathways. However, the cut-off used to define the number of DEGs that are utilised significantly impacts ORA results. To overcome the arbitrary choice of a cut-off and identify cut-off-independent enriched pathways, we developed PEBBA. This user-friendly tool ranks genes based on their statistical and biological significance and then systematically performs ORA for different cut-offs. There is no need to shortlist genes or waste time fine-tuning parameters. By simplifying ORA, PEBBA can be employed to lighten users’ burdens concerning parameter choice and decrease false positives. By visually exploring the parameter space, users can draw more precise conclusions about their dataset.\n\n## Install\nPEBBA may be installed through pip: `pip install pebba`.\nAlternatively, PEBBA is also available as an online tool at [pebba.sysbio.tools](https://pebba.sysbio.tools/)\n\n\n## Using pebba\nOnce installed, pebba can be used as a standalone module:\n\n`python -m pebba <deg_file> <gmt_file>`\n\n\nFor more options use the --help flag: `python -m pebba --help`\n',
    'author': 'Alan Barzilay',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pebba.sysbio.tools/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
