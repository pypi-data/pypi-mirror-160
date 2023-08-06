# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_panel', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['coverage>=6.4.2,<7.0.0',
 'panel>=0.12',
 'plum-dispatch',
 'pydantic',
 'pytest-cov>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'pydantic-panel',
    'version': '0.1.5',
    'description': 'Top-level package for pydantic-panel.',
    'long_description': "==============\npydantic-panel\n==============\n\n\n.. image:: https://img.shields.io/pypi/v/pydantic_panel.svg\n        :target: https://pypi.python.org/pypi/pydantic_panel\n\n.. image:: https://img.shields.io/travis/jmosbacher/pydantic_panel.svg\n        :target: https://travis-ci.com/jmosbacher/pydantic_panel\n\n.. image:: https://readthedocs.org/projects/pydantic-panel/badge/?version=latest\n        :target: https://pydantic-panel.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\nEdit pydantic models with panel.\n\nThis is just a small little project i made mostly for my own use and decided to share.\nIts limited in scope and probably still has bugs, USE AT YOUR OWN RISK.\n\nI will continue to add support for more types as I need them but feel free to \nopen issues with feature requests or better yet PRs with implementations.\n\n\n* Free software: MIT\n* Documentation: https://pydantic-panel.readthedocs.io.\n\nGetting Started\n---------------\n\nStep 1 - Install \n\n.. code-block::\n\n    pip install pydantic-panel\n\n\nStep 2 - Import pydantic_panel and add your models to layouts!\n\n.. code-block:: python\n    \n    import pydantic\n    import panel as pn\n    import pydantic_panel\n\n    class SomeModel(pydantic.BaseModel):\n        name: str\n        value: float\n\n    widget = pn.panel(SomeModel)\n\n    layout = pn.Column(widget, widget.json)\n    layout.servable()\n\n\nNow edit \n\nBasic Usage\n-----------\n\nIf you import `pydantic_panel`, it will register the widget automatically using the `panel.BasePane.applies` interface.\nAfter importing, calling `panel.panel(model)` will return a `panel.CompositeWidget` whos value is the model.\nWhen you change one of the sub-widget values, the new value is validated/coerced using the corresponding pydantic\nfield and if it passes validation/coercion the new value is set on the model itself.\nBy default this is a one-way sync, if the model field values are changed via code, it does not sync the widgets.\nIf you want biderectional sync, you can pass `bidirectional = True` to the widget constructor, this will patch the model \nto sync changes to the widgets but this may break without warning if pydantic change the internals of \ntheir `__setattr__` method.\n\n\n.. code-block:: python\n\n    import panel as pn\n    import pydantic_panel\n\n    class SomeModel(pydantic.BaseModel):\n        name: str\n        value: float\n\n    # when passing a model class, \n    # all widget values will be None including the composite widget value\n    w = pn.panel(SomeModel)\n    \n    # if you pass a model instance \n    # widget values will be the same as the model instance\n    inst = SomeModel(name='meaning', value=42)\n    w = pn.panel(inst)\n\n    # This will display widgets to e.g. edit the model in a notebook\n    w\n\n    # This will return True\n    inst is w.value\n\n    # This will be None if the widgets have not yet been set to values\n    # if all the required fields have been set, this will be an instance of SomeModel\n    # with the validated attribute values from the widgets\n    w.value\n\n\nThe `pn.panel` method will return a widget which can be used as part of a larger application or as just \na user friendly way to edit your model data in the notebook.\n\nCustomizing widgets\n-------------------\n\nYou can add or change the widgets used for a given type by hooking into the dispatch\nmechanism (we use plum-dispatch). This can be used to override the widget used for a supported\ntype or to add supprt for a new type.\n\n\n.. code-block:: python\n\n    from pydantic_panel import get_widget\n    from pydantic import FieldInfo\n\n    # precedence > 0 will ensure this function will be called\n    # instead of the default which has precedence = 0\n    @get_widget.dispatch(precedence=1)\n    def get_widget(value: MY_TYPE, field: FieldInfo, **kwargs):\n        # extract relavent info from the pydantic field info here.\n\n        # return your favorite widget\n        return MY_FAVORITE_WIDGET(value=value, **kwargs)\n\n\nSupported types\n---------------\n\n* int\n* float\n* str\n* list\n* tuple\n* dict\n* datetime.datetime\n* BaseModel\n* List[BaseModel]\n* pandas.Interval\n* numpy.ndarray\n\nFAQ\n---\n\nQ: Why did you decide to use CompositWidget instead of Pane like Param uses?\n\nA: Nested models. This is a recursive problem, so I was looking for a recursive solution. By using a Widget to\ndisplay models, all fields are treated equally. A field of type BaseModel is edited with a widget that has a `.value` \nattribute just like any other field and therefore requires no special treatment. When the parent collects the values of its children \nit just reads the `widget.value` attribute and does not need to check whether the value is nested or not. At every level \nof the recursion the widget only has to care about the fields on its model class and watch only the `.value` attribute of\nits children widgets for changes.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n",
    'author': 'Yossi Mosbacher',
    'author_email': 'joe.mosbacher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmosbacher/pydantic_panel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
