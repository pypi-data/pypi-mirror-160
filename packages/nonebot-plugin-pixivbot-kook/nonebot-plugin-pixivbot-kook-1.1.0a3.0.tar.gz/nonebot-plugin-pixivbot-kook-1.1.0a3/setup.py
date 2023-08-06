# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nonebot_plugin_pixivbot_kook',
 'nonebot_plugin_pixivbot_kook.protocol_dep',
 'nonebot_plugin_pixivbot_kook.utils']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-kaiheila>=0.0.4,<0.0.5',
 'nonebot-plugin-pixivbot==1.1.0-alpha.3',
 'nonebot2>=2.0.0-beta.4,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-pixivbot-kook',
    'version': '1.1.0a3',
    'description': 'Nonebot Plugin Pixivbot (KOOK)',
    'long_description': 'nonebot-plugin-pixivbot-kook\n=====\n\nKOOK (原开黑啦) 协议版本的PixivBot\n\n## TODO\n\n1. [ ] 服务器/频道权限管理（schedule功能目前暂无权限管理）\n\n## Special Thanks\n\n[Mikubill/pixivpy-async](https://github.com/Mikubill/pixivpy-async)\n\n[nonebot/nonebot2](https://github.com/nonebot/nonebot2)\n\n\n## LICENSE\n\n```\nMIT License\n\nCopyright (c) 2022 ssttkkl\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\n```\n',
    'author': 'ssttkkl',
    'author_email': 'huang.wen.long@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ssttkkl/nonebot-plugin-pixivbot-kook',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
