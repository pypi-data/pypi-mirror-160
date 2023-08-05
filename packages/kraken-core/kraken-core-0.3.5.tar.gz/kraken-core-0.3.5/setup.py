# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['api', 'core', 'core.loader', 'core.testing']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.6.0,<3.0.0',
 'setuptools>=33.1.0',
 'termcolor>=1.1.0,<2.0.0',
 'typeapi>=0.2.1,<0.3.0']

extras_require = \
{'testing': ['pytest>=6.0.0']}

entry_points = \
{'kraken.core.loader': ['python_script = '
                        'kraken.core.loader.python_script:PythonScriptProjectLoader'],
 'pytest11': ['kraken-testing = kraken.core.testing']}

setup_kwargs = {
    'name': 'kraken-core',
    'version': '0.3.5',
    'description': '',
    'long_description': '# kraken-core\n\n[![Python application](https://github.com/kraken-build/kraken-core/actions/workflows/python-package.yml/badge.svg)](https://github.com/kraken-build/kraken-core/actions/workflows/python-package.yml)\n[![PyPI version](https://badge.fury.io/py/kraken-core.svg)](https://badge.fury.io/py/kraken-core)\n\nThe `kraken-core` package provides the primitives to describe a dependency graph for the purpose of task\norchestration.\n\n__Packages__\n\n* `kraken.api` &ndash; This module can be imported from in a `.kraken.py` build script to get access to the current\n    build context and project.\n* `kraken.core` &ndash; The core API that consists of primitives to describe tasks with dependencies, as well as\n    Pytest fixtures.\n\n## Concepts\n\n* __Context__: The build context is the "root object" which contains a reference to the root project as well as\nthe path to a designated build directory. The context can hold metadata that is addressable globally by the Python\ntype (see `Context.metadata`).\n* __Project__: A project represents a directory on the file system and tasks that are associated with the contents of\nthat directory and the build script loaded from it. A project\'s members are named and either `Task`s or other\n`Project`s. A project is uniquely identified by it\'s "path" which is similar to a filesystem path only that the\nseparator is a colon (`:`). The root project is identifier with just a single colon, while members of a project are\nidentified by concatenating the project path with the member name (such as `:subproject:task`).\n* __Task__: A task is a unit of work that can is related to a project. Tasks can have relationships to other tasks\nthat describe whether it needs to run before or after the related task. The relationship can also be strict (default)\nor optional, in which case only the order of execution is informed. Tasks have properties that when passed to\nproperties of other tasks inform a strict dependency relationship.\n* __Task factory__: A task factory is a function that is a convenient utility for Kraken build scripts to define one\nor more tasks in a project. The `Project.do()` method in particular is often used to create task, allowing users to\nconveniently set task property values directly instead of interfacing with the property API.\n* __Group tasks__: Group tasks are a special kind of task that store a list of tasks as their dependencies, effectively\ngrouping the tasks under their name. There is some special treatment for group tasks when the task graph is constructed,\nbut otherwise they behave like normal tasks that don\'t actually do any work themselves. Every Kraken project always\nhas the following groups by default: `fmt`, `lint`, `build` and `test`.\n* __Property__: A property is a typed container for a value. It can receive a static value or another task\'s property\nto inform a strict dependency relationship between the property owners. Properties have a `.set(value)`, `.get()` and\n`.get_or()` method.\n* __Task graph__: The task graph represents a fully wired graph of the tasks in a *context*. The task graph must only\nbe constructed after `Context.finalize()` was called to allow tasks to perform one final update before nothing can be\nchanged anymore. After constructing a graph from a set of initially required tasks, it only contains the tasks that are\ntransitively required by the initial set. The graph can be further trimmed to remove weakly connected components of the\ngraph (such as group tasks if they were of the initial set or dependencies that are not strictly required by any other\ntask).\n\n## Example\n\nCheck out the [`example/`](./example/) directory.\n\n## Remarks for writing extensions\n\n__Use `typing` aliases when defining Task properties for pre-3.10 compatibility__\n\nThe Kraken code base uses the 3.10+ type union operator `|` for type hints where possible. However, special care needs\nto be taken with this operator when defining properties on Kraken tasks. The annotations on task objects are eveluated\nand will cause errors in Python versions lower than 3.10 when using the union operator `|` even with\n`__future__.annotations` enabled.\n\nThe following code will cause a `TypeError` when executed even when using `from __future__ import annotations`:\n\n```py\nclass MyTask(Task):\n    my_prop: Property[str | Path]  # unsupported operand type(s) for |: \'type\' and \'type\'\n```\n\n__Property value adapters__\n\nProperties only support the types for which there is a value adapter registered. The default adapters registered in\nthe `kraken.core.property` module covert most use cases such as plain data types (`bool`, `int`, `float`, `str`,\n`None`) and containers (`list`, `set`, `dict`) for which (not nested) type checking is implemented. Additionally, the\nvalue adapter for `pathlib.Path` will allow a `str` to be passed and automatically convert it to a path.\n\nBe aware that the order of the union members will play a role: A property declared as `Property[Union[Path, str]]`\nwill always coerce strings to paths, whereas a property declared as `Property[Union[str, Path]]` will accept a string\nand not coerce it to a string.\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
