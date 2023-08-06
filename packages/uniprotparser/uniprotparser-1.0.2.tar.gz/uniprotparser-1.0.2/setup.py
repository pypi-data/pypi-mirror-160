# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uniprotparser']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'uniprotparser',
    'version': '1.0.2',
    'description': 'Getting Uniprot Data from Uniprot Accession ID through Uniprot REST API',
    'long_description': 'UniProt Database Web Parser Project\n--\n\nTLDR: This parser can be used to parse UniProt accession id and obtain related data from the UniProt web database.\n\nTo parse UniProt accession\n\n```python\nfrom uniprotparser.parser import UniprotSequence\n\nprotein_id = "seq|P06493|swiss"\n\nacc_id = UniprotSequence(protein_id, parse_acc=True)\n\n#Access ACCID\nacc_id.accession\n\n#Access isoform id\nacc_id.isoform\n```\n\nTo get additional data from UniProt online database\n\n```python\nfrom uniprotparser.parser import UniprotParser\nfrom io import StringIO\n#Install pandas first to handle tabulated data\nimport pandas as pd\n\nprotein_accession = "P06493"\n\nparser = UniprotParser([protein_accession])\n\n#To get tabulated data\nresult = []\nfor i in parser.parse("tab"):\n    tab_data = pd.read_csv(i, sep="\\t")\n    last_column_name = tab_data.columns[-1]\n    tab_data.rename(columns={last_column_name: "query"}, inplace=True)\n    result.append(tab_data)\nfin = pd.concat(result, ignore_index=True)\n\n#To get fasta sequence\nwith open("fasta_output.fasta", "wt") as fasta_output:\n    for i in parser.parse():\n        fasta_output.write(i)\n```\n\n',
    'author': 'Toan K. Phung',
    'author_email': 'toan.phungkhoiquoctoan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
