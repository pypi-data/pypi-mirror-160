# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['psi_score', 'psi_score.linalg']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.1,<2.0.0', 'progressbar2>=4.0.0,<5.0.0', 'scipy>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'psi-score',
    'version': '0.2.0',
    'description': 'Metric of user influence in Online Social Networks',
    'long_description': "# Psi-score\n\n$\\psi$-score: Metric of user influence in Online Social Networks\n\n## Requirements\n* Python >=3.9,<3.11\n\n## Installation\n\n```bash\n$ pip install psi-score\n```\n\n## Usage\n\n```python\n>>> from psi_score import PsiScore\n>>> adjacency = {0: [1, 3], 1: [0, 2], 2: [0, 1, 3], 3: [0]}\n>>> lambdas = [0.23, 0.50, 0.86, 0.19]\n>>> mus = [0.42, 0.17, 0.10, 0.37]\n>>> psiscore = PsiScore()\n>>> scores = psiscore.fit_transform(adjacency, lambdas, mus)\n>>> scores\narray([0.21158803, 0.35253745, 0.28798439, 0.14789014])\n>>> np.round(scores, 2)\narray([0.21, 0.35, 0.29, 0.15])\n```\nYou can use another algorithm and change some parameters:\n```python\n>>> psiscore = PsiScore(solver='power_nf', n_iter=500, tol=1e-3)\n>>> scores = psiscore.fit_transform(adjacency, lambdas, mus, ps=[1], qs=[0, 3])\n```\nThe ``ps`` and ``qs`` parameters allows to have some chosen ``p_i`` and ``q_i`` vectors (only with the ``push`` and ``power_nf`` methods):\n```python\n>>> psiscore.P\n{1: array([0.5333334 , 0.1681094 , 0.46801851, 0.34442264])}\n>>> psiscore.Q\n{0: array([0.46164044, 0.0514935 , 0.02798624, 0.30484491]),\n 3: array([0.13087053, 0.01616898, 0.01850541, 0.42554885])}\n```\n\n## License\n\n`psi-score` was created by Nouamane Arhachoui. It is licensed under the terms of the MIT license.\n\n## References\n\n* Giovanidis, A., Baynat, B., Magnien, C., & Vendeville, A. (2021).\n  Ranking Online Social Users by Their Influence. \n  IEEE/ACM Transactions on Networking, 29(5), 2198–2214. https://doi.org/10.1109/tnet.2021.3085201\n\n* Arhachoui, N., Bautista, E., Danisch, M., & Giovanidis, A. (2022). \n  A Fast Algorithm for Ranking Users by their Influence in Online Social Platforms. \n  arXiv Preprint. https://doi.org/10.48550/ARXIV.2206.09960\n",
    'author': 'Nouamane Arhachoui',
    'author_email': 'nouamane.arhachoui@lip6.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NouamaneA/psi-score',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
