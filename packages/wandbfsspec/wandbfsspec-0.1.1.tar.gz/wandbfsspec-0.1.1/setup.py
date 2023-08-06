# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wandbfsspec']

package_data = \
{'': ['*']}

install_requires = \
['fsspec>=2022.5.0,<2023.0.0', 'wandb>=0.12.20,<0.13.0']

entry_points = \
{'fsspec.specs': ['wandbfs = wandbfsspec.core.WandbFileSystem']}

setup_kwargs = {
    'name': 'wandbfsspec',
    'version': '0.1.1',
    'description': 'fsspec interface for Weights & Biases (wandb)',
    'long_description': '# 🍱 `fsspec` interface for Weights & Biases (wandb)\n\nQuoting Weights and Biases (wandb), "Weights & Biases is the \nmachine learning platform for developers to build better models \nfaster. Use W&B\'s lightweight, interoperable tools to quickly track \nexperiments, version and iterate on datasets, evaluate model performance, \nreproduce models, visualize results and spot regressions, and share \nfindings with colleagues.". Reference at https://docs.wandb.ai/\n\nSo you may be thinking, what does `wandb` have to do with anything\nclose to a File System? Well, it\'s not but it actually provides a way\nto upload/download files and store them in a remote, which makes it somehow\na File System. Also, `wandb` provides an API that lets you interact with\nthat "File System", so this is why `wandbfsspec` makes sense, in order to ease\nthat interface between `wandb`\'s File System and anyone willing to use it.\n\nThe `wandbfsspec` implementation is based on https://github.com/fsspec/filesystem_spec.\n\n## 🔮 Future TODOs\n\nObviously, since `wandb`\'s main purpose is to track and monitor ML experiments,\nit contains an artifact store, so as to dump there the experiment artifacts for data\nversioning and model tracking. More information in https://wandb.ai/site/artifacts.\n\nSo on, a new interface will be implemented in `wandbfsspec` not just to handle the files\nthat can be uploaded/downloaded to/from `wandb`, but also the artifacts. So the next release\nwill implement a new `AbstractFileSystem` class named `WandbArtifactStore` with the protocol\n`wandbas` in order to access the artifact store as if it was a default File System.\n\nSome more notes on how to actually use `wandb`\'s artifact store at https://docs.wandb.ai/guides/artifacts.\n\nOnce that\'s done, we\'ll fill a PR in https://github.com/fsspec/filesystem_spec, so as to\nregister both protocols supported by `wandbfsspec`: `wandbfs` and `wandbas`.\n\n## 🚸 Usage\n\nHere\'s an example on how to locate and open a file:\n\n```python\n>>> from wandbfsspec.core import WandbFileSystem\n>>> fs = WandbFileSystem(api_key="YOUR_API_KEY")\n>>> fs.ls("alvarobartt/wandbfsspec-tests/3s6km7mp")\n[\'alvarobartt/wandbfsspec-tests/3s6km7mp/config.yaml\', \'alvarobartt/wandbfsspec-tests/3s6km7mp/file.yaml\', \'alvarobartt/wandbfsspec-tests/3s6km7mp/files\', \'alvarobartt/wandbfsspec-tests/3s6km7mp/output.log\', \'alvarobartt/wandbfsspec-tests/3s6km7mp/requirements.txt\', \'alvarobartt/wandbfsspec-tests/3s6km7mp/wandb-metadata.json\', \'alvarobartt/wandbfsspec-tests/3s6km7mp/wandb-summary.json\']\n>>> with fs.open("alvarobartt/wandbfsspec-tests/3s6km7mp/file.yaml", "rb") as f:\n...     print(f.read())\nb\'some: data\\nfor: testing\'\n```\n\n📌 Note that it can also be done through `fsspec` as long as `wandbfsspec` is installed:\n\n```python\n>>> import fsspec\n>>> fs = fsspec.filesystem("wandbfs")\n>>> fs.ls("alvarobartt/wandbfsspec-tests/3s6km7mp")\n[\'alvarobartt/wandbfsspec-tests/3s6km7mp/config.yaml\', \'alvarobartt/wandbfsspec-tests/3s6km7mp/file.yaml\', \'alvarobartt/wandbfsspec-tests/3s6km7mp/files\', \'alvarobartt/wandbfsspec-tests/3s6km7mp/output.log\', \'alvarobartt/wandbfsspec-tests/3s6km7mp/requirements.txt\', \'alvarobartt/wandbfsspec-tests/3s6km7mp/wandb-metadata.json\', \'alvarobartt/wandbfsspec-tests/3s6km7mp/wandb-summary.json\']\n>>> with fs.open("alvarobartt/wandbfsspec-tests/3s6km7mp/file.yaml", "rb") as f:\n...     print(f.read())\nb\'some: data\\nfor: testing\'\n```\n\n## 📝 Documentation\n\nComing soon... (https://github.com/mkdocs/mkdocs)\n\n## 🧪 How to test it\n\nIn order to test it, you should first set the following environment variables\nso as to use `wandb` as a file system for the tests.\n\n```\nWANDB_ENTITY = ""\nWANDB_PROJECT = ""\nWANDB_API_KEY = ""\n```\n\nBoth entity and project values can be found in your https://wandb.ai/ account, as\nthe entity name is your account name, and the project name can either be already\ncreated or you can just specify it and it\'ll be created during `pytest` init. Then,\nregarding the API Key, you just need to go to https://wandb.ai/settings, scroll\ndown to Danger Zone -> API Keys, and copy your personal API Key from there.\n\n⚠️ Make sure that you don\'t publish your API Key anywhere, that\'s why we\'re defining\nit as an environment value, so as to avoid potential issues on commiting code with\nthe actual API Key value.\n\nThen, in order to actually run the tests you can either run:\n\n- `poetry run pytest`\n- `poetry run make tests`\n\nOr, if you\'re not using `poetry`, you can just run both those commands without it.',
    'author': 'Alvaro Bartolome',
    'author_email': 'alvarobartt@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alvarobartt/wandbfsspec',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
