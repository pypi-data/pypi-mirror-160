# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ast_monitor']

package_data = \
{'': ['*'], 'ast_monitor': ['icons/*', 'map/*']}

install_requires = \
['PyQt5',
 'PyQtWebEngine>=5.15.5,<6.0.0',
 'geopy',
 'matplotlib',
 'pyqt-feedback-flow',
 'sport-activities-features>=0.2.18,<0.3.0',
 'tcxreader']

setup_kwargs = {
    'name': 'ast-monitor',
    'version': '0.2.1',
    'description': 'AST-Monitor is a wearable Raspberry Pi computer for cyclists',
    'long_description': '# AST-Monitor --- A wearable Raspberry Pi computer for cyclists\n\n---\n\n[![PyPI Version](https://img.shields.io/pypi/v/ast-monitor.svg)](https://pypi.python.org/pypi/ast-monitor)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ast-monitor.svg)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/ast-monitor.svg)\n[![Downloads](https://pepy.tech/badge/ast-monitor)](https://pepy.tech/project/ast-monitor)\n[![GitHub license](https://img.shields.io/github/license/firefly-cpp/ast-monitor.svg)](https://github.com/firefly-cpp/AST-Monitor/blob/master/LICENSE)\n![GitHub commit activity](https://img.shields.io/github/commit-activity/w/firefly-cpp/ast-monitor.svg)\n![GitHub contributors](https://img.shields.io/github/contributors/firefly-cpp/ast-monitor.svg)\n\n[![DOI](https://img.shields.io/badge/DOI-10.1109/ISCMI53840.2021.9654817-blue)](https://doi.org/10.1109/ISCMI53840.2021.9654817)\n[![Fedora package](https://img.shields.io/fedora/v/python3-ast-monitor?color=blue&label=Fedora%20Linux&logo=fedora)](https://src.fedoraproject.org/rpms/python-ast-monitor)\n\n<p align="center">\n  <img width="600" src="https://user-images.githubusercontent.com/73126820/179205064-160bdd44-fd67-4d8d-85dd-badea999885c.png" alt="AST-GUI">\n  <img width="600" src="https://user-images.githubusercontent.com/73126820/179205118-19cbb6e2-f410-4371-a762-c4c77344ab24.png" alt="AST-Map">\n  <img width="600" src="https://user-images.githubusercontent.com/73126820/179205160-edce581c-1ea8-4287-a795-7d05fb7c8ddc.png" alt="AST-Intervals">\n  <img width="600" src="https://user-images.githubusercontent.com/73126820/179205215-e75098f2-0b43-4905-8c1f-0cf488b90ac5.png" alt="AST-Trainings">\n</p>\n\nThis repository is devoted to the AST-monitor, i.e., a low-cost and efficient embedded device for monitoring the realization of sports training sessions that are dedicated to monitoring cycling training sessions.\nAST-Monitor is a part of the Artificial Sport Trainer (AST) system. The first bits of AST-monitor were presented in the following [paper](https://arxiv.org/abs/2109.13334).\n\n## Outline of this repository\n\nThis repository presents basic code regarded to GUI. It was ported from the initial prototype to poetry.\n\n## Hardware outline\n\nThe complete hardware part is shown in the figure from which it can be seen that the AST-computer is split into the following pieces:\n\n* a platform with fixing straps that attach to a bicycle,\n* the Raspberry Pi 4 Model B micro-controller with Raspbian OS installed,\n* a five-inch LCD touch screen display,\n* a USB ANT+ stick,\n* Adafruit\'s Ultimate GPS HAT module.\n\n<p align="center">\n  <img width="600" src="https://raw.githubusercontent.com/firefly-cpp/AST-Monitor/main/.github/img/complete_small.JPG" alt="AST-Monitor">\n</p>\n\n\nA Serial Peripheral Interface (SPI) protocol was dedicated to communication between the Raspberry Pi and the GPS peripheral. A specialized USB ANT+ stick was used to capture the HR signal. The screen display was connected using a modified (physically shortened) HDMI cable, while the touch feedback was implemented using physical wires. The computer was powered during the testing phase using the Trust\'s (5 VDC) power bank. The AST-Monitor prototype is still a little bulky, but a more discrete solution is being searched for, including the sweat drainer of the AST.\n\n## Software outline\n\n### Dependencies\n\nList of dependencies:\n\n| Package      | Version    | Platform |\n| ------------ |:----------:|:--------:|\n| PyQt5        | ^5.15.6    | All      |\n| matplotlib   | ^3.5.1     | All      |\n| geopy        | ^2.2.0     | All      |\n| openant        | v0.4     | All      |\n| pyqt-feedback-flow       | ^0.1.0     | All      |\n| tcxreader       | ^0.3.8     | All      |\n| sport-activities-features       | ^0.2.9     | All      |\n\nNote: openant package should be installed manually. Please follow the [official instructions](https://github.com/Tigge/openant). If you use Fedora OS, you can install openant package using the dnf package manager:\n\n```sh\n$ dnf install python-openant\n```\n\nAdditional note: adafruit-circuitpython-gps package must be installed in order to work with the GPS sensor:\n\n```sh\n$ pip install adafruit-circuitpython-gps\n```\n\n## Installation\n\nInstall AST-Monitor with pip:\n\n```sh\n$ pip install ast-monitor\n```\nIn case you want to install directly from the source code, use:\n\n```sh\n$ git clone https://github.com/firefly-cpp/AST-Monitor.git\n$ cd AST-Monitor\n$ poetry build\n$ python setup.py install\n```\n\nTo install AST-Monitor on Fedora Linux, please use:\n\n```sh\n$ dnf install python3-ast-monitor\n```\n\n## Deployment\n\nOur project was deployed on a Raspberry Pi device using Raspbian OS.\n\n### Run AST-Monitor on startup\n\nAdd the following lines in /etc/profile which ensures to run scripts on startup:\n\n```sh\nsudo python3 /home/user/run_example.py\nsudo nohup python3 /home/user/read_hr_data.py  &\nsudo nohup python3 /home/user/read_gps_data.py  &\n```\n## Examples\n\n### Basic run\n\n```python\nfrom PyQt5 import QtCore, QtGui, uic, QtWidgets\nfrom ast_monitor.model import AST\nimport sys\n\n# provide data locations\n\nhr_data = "sensor_data/hr.txt"\ngps_data = "sensor_data/gps.txt"\n\n\nif __name__ == "__main__":\n    app = QtWidgets.QApplication(sys.argv)\n    window = AST(hr_data, gps_data)\n\n    window.show()\n    sys.exit(app.exec_())\n```\n\n\n## License\n\nThis package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.\n\n## Disclaimer\n\nThis framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!\n\n## References\n\nFister Jr, I., Fister, I., Iglesias, A., Galvez, A., Deb, S., & Fister, D. (2021). On deploying the Artificial Sport Trainer into practice. arXiv preprint [arXiv:2109.13334](https://arxiv.org/abs/2109.13334).\n\nFister Jr, I., Salcedo-Sanz, S., Iglesias, A., Fister, D., Gálvez, A., & Fister, I. (2021). New Perspectives in the Development of the Artificial Sport Trainer. Applied Sciences, 11(23), 11452. DOI: [10.3390/app112311452](https://doi.org/10.3390/app112311452)\n',
    'author': 'Iztok Fister Jr.',
    'author_email': 'iztok@iztok-jr-fister.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
