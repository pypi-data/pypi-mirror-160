# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['strmath']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'strmath',
    'version': '1.0',
    'description': 'A module for evaluating math expressions without eval()',
    'long_description': '# strmath\n\n![tests](https://github.com/Exenifix/strmath/actions/workflows/test.yml/badge.svg)\n\nA module for evaluating math expressions without eval(). Currently the module supports only simple math operations (eg.\nmultiplication, subtraction, division, %) but in the future there will be functions support.\n\n## Installation\nThe module is available for installation from PyPI\n```shell\n$ pip install strmath\n```\n\n## Basic Usage\n```python\nfrom strmath import evaluate\n\n\nresult = evaluate("(90 + 2) // 4")\nprint(result)\n```\n\n## Accuracy\nAs [tests](https://github.com/Exenifix/strmath/actions/workflows/test.yml) show, the library is 100% accurate with python native evaluation:\n```\n+----------------+--------+---------+-----+-----------+-------------+\n|                | Python | StrMath | PEE | Mathparse | InfixParser |\n+----------------+--------+---------+-----+-----------+-------------+\n| Failures       | 0      | 0       | 61  | 150       | 91          |\n| Failures (%)   | 0%     | 0%      | 30% | 75%       | 45%         |\n+----------------+--------+---------+-----+-----------+-------------+\n```\nIn the test above, 198 randomly generated samples were submitted to Python `eval()` and several other parsing libraries, including `strmath`. \nAs you can see, the library has 0 failures and almost same speed with native python. You can see test implementation [here](https://github.com/Exenifix/strmath/blob/master/tests/test_expressions.py).\n\n## Features\n### Currently Supported\n- basic math operations (+, -, /, //, *, **, %) eg. `"2 + 5 * 2" --> 12`\n- float operations\n- braces eg. `"(2 + 5) * 2" --> 20`\n\n### Planned for Future\n- math functions\n- custom functions registration\n- correct `-` operator as neg (eg. `50+-30`)\n\n## Principle\n1. Tokenize expression (split it into operators and numbers)\n2. Apply operations order\n3. Build evaluation binary tree\n4. Evaluate the tree\n\n## License\nThis repository is licensed under MIT license. See [LICENSE](https://github.com/Exenifix/strmath/blob/master/LICENSE) for details.\n',
    'author': 'Exenifix',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Exenifix/strmath',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
