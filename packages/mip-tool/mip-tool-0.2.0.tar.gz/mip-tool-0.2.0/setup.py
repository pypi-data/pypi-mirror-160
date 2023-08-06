# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mip_tool', 'mip_tool.func']

package_data = \
{'': ['*']}

install_requires = \
['mip>=1.14.0,<2.0.0', 'more-itertools>=8.13.0,<9.0.0', 'pandas>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'mip-tool',
    'version': '0.2.0',
    'description': '`mip-tool` is a package for Python-MIP.',
    'long_description': '# MIP-Tool\n\nMIP-Tool is a package for [Python-MIP](https://www.python-mip.com/).\n\n## Installation\n\n```\npip install pandas\npip install mip-tool\n```\n\n## Example\n\n### Non-convex piecewise linear constraint\n\nMaximize y which is on points of (-2, 6), (-1, 7), (2, -2), (4, 5).\n\n```python\nimport numpy as np\nfrom mip import INF, Model, OptimizationStatus\nfrom mip_tool import add_lines, show_model\n\nm = Model()\nx = m.add_var("x", lb=-INF)\ny = m.add_var("y", obj=-1)\ncurve = np.array([[-2, 6], [-1, 7], [2, -2], [4, 5]])\nadd_lines(m, curve, x, y)\nm.verbose = 0\nm.optimize()\nassert m.status == OptimizationStatus.OPTIMAL\nassert (x.x, y.x) == (-1, 7)\nshow_model(m)\n```\n\n*Output*\n\n```\n\\Problem name: \n\nMinimize\nOBJROW: - y\nSubject To\nconstr(0):  - x + w_0 + w_1 + w_2 = 2\nconstr(1):  - y + w_0 -3 w_1 + 3.50000 w_2 = -6\nconstr(2):  - w_0 + z_0 <= -0\nconstr(3):  w_0 <= 1\nconstr(4):  - w_1 + 3 z_1 <= -0\nconstr(5):  - w_1 + 3 z_0 >= -0\nconstr(6):  - w_2 + 2 z_1 >= -0\nBounds\n x Free\n 0 <= z_0 <= 1\n 0 <= z_1 <= 1\nIntegers\nz_0 z_1 \nEnd\n```\n\n## F example\n\nEasy to understand using F.\n\nattention: Change Model and Var when using mip_tool.func.\n\n```python\nfrom mip_tool.func import F\n\nm = Model()\nx = m.add_var("x")\ny = m.add_var("y", obj=-1)\nm += y <= F([[0, 2], [1, 3], [2, 2]], x)\nm.verbose = 0\nm.optimize()\nprint(x.x, y.x)  # 1.0 3.0\n```\n\n- `y <= F(curve, x)` and `y >= F(curve, x)` call `add_lines_conv`.\n- `y == F(curve, x)` calls `add_lines`.\n\n\n## pandas.DataFrame example\n\nattention: Change Seies when using mip_tool.func.\n\n```python\nimport pandas as pd\nfrom mip import Model, maximize, xsum\nfrom mip_tool.func import addvars\n\nA = pd.DataFrame([[1, 2], [3, 1]])\nb = pd.Series([16, 18])\nm = Model()\nx = addvars(m, A, "")\nm.objective = maximize(xsum(x))\nm += A @ x <= b\nm.verbose = 0\nm.optimize()\nprint(x.astype(float))  # [4. 6.]\n```\n\nExpression `m += A.T.apply(lambda row: xsum(row * x)) <= b` may be faster than `m += A @ x <= b`.\n',
    'author': 'Saito Tsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/mip-tool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
