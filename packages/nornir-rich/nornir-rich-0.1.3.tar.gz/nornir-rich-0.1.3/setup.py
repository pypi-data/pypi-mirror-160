# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_rich']

package_data = \
{'': ['*']}

install_requires = \
['nornir>=3,<4', 'rich>=12,<13']

setup_kwargs = {
    'name': 'nornir-rich',
    'version': '0.1.3',
    'description': "Collection of 'nice looking' functions with rich for nornir",
    'long_description': '# nornir_rich\n\n## Install\n\n```bash\npip install nornir-rich\n```\n\n## Usage\n\nFeatures\n\n- Print functions\n  - `print_result`\n  - `print_failed_hosts`\n  - `print_inventory`\n- Processors\n  - `progressbar`\n\n\n### Print example\n\n```python\nfrom nornir_rich.functions import print_result\n\nresults = nr.run(\n    task=hello_world\n)\n\nprint_result(results)\nprint_result(results, vars=["diff", "result", "name", "exception", "severity_level"])\n```\n\n### Progress bar example\n\n```python\nfrom time import sleep\nfrom nornir_rich.progress_bar import RichProgressBar\n\n\ndef random_sleep(task: Task) -> Result:\n    delay = randrange(10)\n    sleep(delay)\n    return Result(host=task.host, result=f"{delay} seconds delay")\n\n\nnr_with_processors = nr.with_processors([RichProgressBar()])\nresult = nr_with_processors.run(task=random_sleep)\n```\n\n\n## Images\n\n### Print Inventory\n\n![Print inventory](https://raw.githubusercontent.com/InfrastructureAsCode-ch/nornir-rich/main/docs/imgs/print_inventory.png)\n\n### Print Result\n\n![Print Result](https://raw.githubusercontent.com/InfrastructureAsCode-ch/nornir-rich/main/docs/imgs/print_result.png)\n\n### Progress Bar\n\n![Progress Bar](https://raw.githubusercontent.com/InfrastructureAsCode-ch/nornir-rich/main/docs/imgs/progressbar.png)\n\n\nMore [examples](https://raw.githubusercontent.com/InfrastructureAsCode-ch/nornir-rich/main/docs/imgs/print_functions.ipynb)',
    'author': 'ubaumann',
    'author_email': 'github@m.ubaumann.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/InfrastructureAsCode-ch/nornir-rich',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
