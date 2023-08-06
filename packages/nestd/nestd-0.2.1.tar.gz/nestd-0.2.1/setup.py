# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nestd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nestd',
    'version': '0.2.1',
    'description': 'A package to extract your nested functions!',
    'long_description': '# nested\n\nExtract your nested functions!\n\n## Installation\n\n```python3\n    pip install nestd\n```\n\n\n## Usage\n\n```python3\nfrom nestd import nested, get_all_nested\n\n\ndef dummy_function():\n    test_variable = "hello, world"\n    def inner_function():\n        nonlocal test_variable\n        return test_variable\n\n\ndef dummy_function_with_two_inner_functions():\n    test_variable = "hello, world"\n    test_array = [1, 2, 3]\n    def inner_function():\n        nonlocal test_variable\n        return test_variable\n\n    def inner_function_2():\n        nonlocal test_array\n        return test_array[1:]\n\n\ndef test_nested_function():\n    inner_function = nested(dummy_function, "inner_function", test_variable="hello" )\n    assert "hello" == inner_function()\n\ndef test_2_nested_functions():\n    all_inner_functions = get_all_nested(dummy_function_with_two_inner_functions, "hello_world", [1,2])\n    inner_function, inner_function_2 = all_inner_functions\n\n    assert inner_function[0] == "inner_function"\n    assert inner_function[1]() == "hello_world"\n\n    assert inner_function_2[0] == "inner_function_2"\n    assert inner_function_2[1]() == [2]\n```\n\n## Contributor Guidelines\n\nFeel free to open an issue for any clarification or for any suggestions.\n\n\n## To Develop Locally\n\n1. `poetry install` to install the dependencies\n2. `pytest tests` to run the tests\n',
    'author': 'Sanskar Jethi',
    'author_email': 'sansyrox@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
