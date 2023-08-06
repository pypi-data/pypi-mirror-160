# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytemppack']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3', 'pandas>=1.4.2']

setup_kwargs = {
    'name': 'pytemppack',
    'version': '0.0.0',
    'description': 'A python package template with poetry',
    'long_description': '.. |pic1| image:: https://img.shields.io/badge/python-3.8%20%7C%203.9-blue\n.. |pic2| image:: https://img.shields.io/badge/security-bandit-yellow.svg\n.. |pic3| image:: https://img.shields.io/github/license/mashape/apistatus.svg\n.. |pic4| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n.. |pic5| image:: http://www.mypy-lang.org/static/mypy_badge.svg\n.. |pic6| image:: https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey\n.. |pic7| image:: https://github.com/AndresAlgaba/pytemppack/actions/workflows/testing.yml/badge.svg\n.. |pic8| image:: https://img.shields.io/readthedocs/pytemppack\n.. |pic9| image:: https://img.shields.io/pypi/v/pytemppack\n.. |pic10| image:: https://img.shields.io/badge/isort-checked-yellow\n\n.. _pytemppack: https://github.com/AndresAlgaba/pytemppack/tree/main/pytemppack\n.. _examples: https://github.com/AndresAlgaba/pytemppack/tree/main/examples\n.. _contribute: https://github.com/AndresAlgaba/pytemppack/blob/main/CONTRIBUTING.rst\n\n.. _poetry: https://python-poetry.org/docs/\n.. _pip: https://mypy.readthedocs.io/en/stable/config_file.html#the-mypy-configuration-file\n\n.. _black: https://black.readthedocs.io/en/stable/index.html\n.. _pytest: https://docs.pytest.org/en/stable/index.html\n.. _pytest-cov: https://pytest-cov.readthedocs.io/en/stable/index.html\n.. _mypy: https://mypy.readthedocs.io/en/stable/index.html\n.. _shields: https://shields.io/\n.. _README: https://www.makeareadme.com/\n.. _Sphinx: https://www.sphinx-doc.org/en/master/\n.. _Read the Docs: https://readthedocs.org/\n.. _isort: https://pycqa.github.io/isort/index.html\n.. _templates: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates\n\n.. _changelog: https://keepachangelog.com/en/1.0.0/\n.. _code of conduct: https://www.contributor-covenant.org/version/1/4/code-of-conduct/\n\n.. _Twitter: https://twitter.com/DataLabBE\n.. _website: https://data.research.vub.be/\n.. _papers: https://researchportal.vub.be/en/organisations/data-analytics-laboratory/publications/\n\n.. _repo: https://github.com/JamesALeedham/Sphinx-Autosummary-Recursion\n\npytemppack\n==========\n\n|pic3| |pic6| |pic1| |pic9|\n\n|pic4| |pic5| |pic10| |pic2|\n\n|pic7| |pic8|\n\nThis is a template for Python packages with `poetry`_ with additional tools for development, such as autoformatting, type checking, and more.\n\nThe `pytemppack`_ folder contains the python module, and we have some `examples`_.\n\nAs best practices are always changing, and people have different experiences, we encourage you to `contribute`_ to this project!\n\n\nFeatures\n--------\n\n* Arranging imports with `isort`_.\n* Autoformatting with `black`_.\n* Boilerplate `README`_ with `shields`_.\n* Documentation with `Sphinx`_ and `Read the Docs`_.\n* Issue and pull request `templates`_.\n* Templates for `changelog`_, `code of conduct`_ and `contribute`_.\n* Testing with `pytest`_ and coverage with `pytest-cov`_.\n* Static type-checking with `mypy`_.\n\n\nInstallation\n------------\n\nUse the package manager `pip`_ to install ``pytemppack`` from PyPi.\n\n.. code-block:: bash\n\n    pip install pytemppack\n\nFor development install, see `contribute`_.\n\n\nUsage\n-----\n\nTransform a ``np.ndarray`` into a ``pd.DataFrame``.\n\n.. code-block:: python\n\n    from pytemppack import PyPack\n    from pytemppack.utils import generate_random_array\n\n    data = generate_random_array((5, 5))\n    columns = [\'a\', \'b\', \'c\', \'d\', \'e\']\n\n    pypack = PyPack(data)\n    pypack.transform_results(columns)\n\n    pypack.results.head()\n\n            a\t            b\t            c\t            d\t            e\n    0\t0.976700\t0.118091\t0.441006\t0.659874\t0.060139\n    1\t0.380196\t0.241766\t0.609871\t0.735758\t0.683689\n    2\t0.923246\t0.318534\t0.863621\t0.222754\t0.671238\n    3\t0.261692\t0.964079\t0.863758\t0.172066\t0.611018\n    4\t0.319097\t0.263650\t0.674881\t0.870415\t0.060137\n\n\nCommunity\n---------\n\nIf you are interested in cross-disciplinary research related to machine learning, you can:\n\n* Follow DataLab on `Twitter`_.\n* Check the `website`_.\n* Read our `papers`_.\n\n\nDisclaimer\n----------\n\nThe package and the code is provided "as-is" and there is NO WARRANTY of any kind. \nUse it only if the content and output files make sense to you.\n\n\nAcknowledgements\n----------------\n\nThis README contains many embedded links from which inspiration was drawn. We suggest to check them out!\nEspecially, this `repo`_ was a great help for autosummary recurssion to document the API.\n',
    'author': 'Andres Algaba',
    'author_email': 'andres.algaba@vub.be',
    'maintainer': 'Andres Algaba',
    'maintainer_email': 'andres.algaba@vub.be',
    'url': 'https://www.andresalgaba.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
