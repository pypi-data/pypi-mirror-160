# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'packages'}

packages = \
['ipcq']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ipcq',
    'version': '1.1.3',
    'description': '',
    'long_description': "# ipcq\n\nA simple inter-process communication (IPC) Queue built on top of the built-in library [multiprocessing](https://docs.python.org/3/library/multiprocessing.html).\n\n![](examples/showcase.gif)\n\n* [Quick Start](#quick-start)\n* [API](#api)\n    + [class ipcq.**QueueManagerServer**(*address*: Optional[str], *authkey*: Optional[bytes])](#class-ipcqqueuemanagerserveraddress-optionalstr-authkey-optionalbytes)\n        - [def **get_queue**(*ident*: Union[AnyStr, int, type(None)] = None) -> queue.Queue](#def-get_queueident-unionanystr-int-typenone--none---queuequeue)\n    + [class ipcq.**QueueManagerClient**(*address*: Optional[str], *authkey*: Optional[bytes])](#class-ipcqqueuemanagerclientaddress-optionalstr-authkey-optionalbytes)\n        - [def **get_queue**(*ident*: Union[AnyStr, int, type(None)] = None) -> queue.Queue](#def-get_queueident-unionanystr-int-typenone--none---queuequeue-1)\n\n## Quick Start\n\n**Server**\n\n```\nimport ipcq\n\n\nwith ipcq.QueueManagerServer(address=ipcq.Address.DEFAULT, authkey=ipcq.AuthKey.DEFAULT) as server:\n    server.get_queue().get()\n```\n\n**Client**\n\n```\nimport ipcq\n\n\nclient = ipcq.QueueManagerClient(address=ipcq.Address.DEFAULT, authkey=ipcq.AuthKey.DEFAULT)\nclient.get_queue().put('a message')\n```\n\nPlease checkout out the [examples](examples) folder for more examples.\n\n## API\n\n### class ipcq.**QueueManagerServer**(*address*: Optional[str], *authkey*: Optional[bytes])\n\nThis class inherits [multiprocessing.managers.BaseManager](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.managers.BaseManager).\n\n*address* can be `ipcq.Address.AUTO`, `ipcq.Address.CWD` or any other path described in `str`.\nWhen it's given `ipcq.Address.AUTO`, a random address will be chosen.\n`ipcq.Address.CWD` means using a file that lives in the current working directory.\n\n*authkey* is just like the password for authentication. It can be `ipcq.AuthKey.AUTO`, `ipcq.AuthKey.DEFAULT`, `ipcq.AuthKey.EMPTY` or any other arbitrary `bytes`.\n\n#### def **get_queue**(*ident*: Union[AnyStr, int, type(None)] = None) -> queue.Queue\n\nThe method returns a `queue.Queue` corresponding with *ident*.\nThe returned queue is shared between the server and the client.\nSo both the server and the client access to the same queue.\n\n*ident* is the identity, it can be any string-like object, `int` or `None`.\nThe default is `None`.\nIt is used for differetiate the obtained queues.\nDifferent *ident*s refer to different queues.\n\n### class ipcq.**QueueManagerClient**(*address*: Optional[str], *authkey*: Optional[bytes])\n\nThis class inherits [multiprocessing.managers.BaseManager](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.managers.BaseManager).\n\n*address* can be `ipcq.Address.CWD` or any other path described in `str`.\nWhen the server is set with `ipcq.Address.CWD` and the client is running in the same CWD that the server runs, the client can be set with `ipcq.Address.CWD` as well.\nOtherwise, it should be the same with the *address* field in the server instance.\n\n*authkey* is just like the password for authentication. It has to be the same with what's set on the server .\nIf the server was set with `ipcq.AuthKey.DEFAULT` or `ipcq.AuthKey.EMPTY`, the client can just be set with the same.\n\n#### def **get_queue**(*ident*: Union[AnyStr, int, type(None)] = None) -> queue.Queue\n\nThe method returns a `queue.Queue` corresponding with *ident*.\nThe returned queue is shared between the server and the client.\nSo both the server and the client access to the same queue.\n\n*ident* is the identity, it can be any string-like object, `int` or `None`.\nThe default is `None`.\nIt is used for differetiate the obtained queues.\nDifferent *ident*s refer to different queues.\n",
    'author': 'Johann Chang',
    'author_email': 'mr.changyuheng@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/changyuheng/ipcq.py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
