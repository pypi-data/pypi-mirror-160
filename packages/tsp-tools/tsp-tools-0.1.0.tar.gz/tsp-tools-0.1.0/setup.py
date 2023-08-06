# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tsp_tools']

package_data = \
{'': ['*']}

install_requires = \
['PuLP>=2.6,<3.0', 'more-itertools>=8.13,<9.0', 'pandas>=1.4,<2.0']

setup_kwargs = {
    'name': 'tsp-tools',
    'version': '0.1.0',
    'description': '`tsp-tools` is a package for Traveling Salesman Problem for Python.',
    'long_description': '`tsp-tools` is a package for Traveling Salesman Problem for Python.\n\n::\n\n    import tsp_tools\n    t = tsp_tools.tsp([(0,0), (0,1), (1,0), (1,1)])\n    print(t)  # distance, node index list\n    >>>\n    (4, [0, 2, 3, 1])\n\n    mat = [[  0,   1, 1, 1.5],\n           [  1,   0, 1.5, 1],\n           [  1, 1.5,   0, 1],\n           [1.5,   1,   1, 0]]  # Distance Matrix\n    r = range(len(mat))\n    # Dictionary of distance\n    dist = {(i, j): mat[i][j] for i in r for j in r}\n    print(tsp_tools.tsp(r, dist))\n    >>>\n    (4, [0, 2, 3, 1])\n\nNote: When large size, `ortoolpy.ortools_vrp` may be efficient.\n\nSee also https://pypi.org/project/ortoolpy/\n\nRequirements\n------------\n* Python 3\n* more-itertools\n\nFeatures\n--------\n* nothing\n\nSetup\n-----\n::\n\n   $ pip install tsp-tools\n\nHistory\n-------\n0.0.1 (2015-10-2)\n~~~~~~~~~~~~~~~~~~\n* first release\n',
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/tsp-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
