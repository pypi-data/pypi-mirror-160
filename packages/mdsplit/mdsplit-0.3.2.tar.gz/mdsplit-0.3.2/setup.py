# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mdsplit']
entry_points = \
{'console_scripts': ['mdsplit = mdsplit:main']}

setup_kwargs = {
    'name': 'mdsplit',
    'version': '0.3.2',
    'description': 'Split markdown files at headings',
    'long_description': "# mdsplit\n\n`mdsplit` is a python command line tool to\n**split markdown files** into chapters\n**at a given [heading level](https://spec.commonmark.org/0.30/#atx-headings)**.\n\nEach chapter (or subchapter) is written to its own file,\nwhich is named after the heading title.\nThese files are written to subdirectories representing the document's structure.\n\n**Note:**\n- *Code blocks* (`` ``` ``)are detected (and headers inside ignored)\n- The output is *guaranteed to be identical* with the input\n  (except for the separation into multiple files of course)\n    - This means: no touching of whitespace or changing `-` to `*` of your lists\n      like some viusual markdown editors tend to do\n- Text before the first heading is written to a file with the same name as the markdown file\n- Chapters with the same heading name are written to the same file.\n- Reading from `stdin` is supported\n- Can easily handle large files,\n  e.g. a 1 GB file is split into 30k files in 35 seconds on my 2015 Thinkpad (with an SSD)\n\n**Limitations:**\n- Only [ATX headings](https://spec.commonmark.org/0.30/#atx-headings) \n  such as `# Heading 1` are supported.\n  [Setext headings](https://spec.commonmark.org/0.30/#setext-headings)\n  (underlined headings) are not recognised.\n\n## Installation\n\nEither use pip:\n\n    pip install mdsplit\n    mdsplit\n\nOr simply download [mdsplit.py](mdsplit.py) and run it (it does not use any dependencies but python itself):\n\n    python3 mdsplit.py\n\n## Usage\n\n**Split a file at level 1 headings**, e.g. `# This Heading`, and write results to an output folder based on the input name:\n\n```bash\nmdsplit in.md\n```\n\n```mermaid\n%%{init: {'themeVariables': { 'fontFamily': 'Monospace', 'text-align': 'left'}}}%%\nflowchart LR\n    subgraph in.md\n        SRC[# Heading 1<br>lorem ipsum<br><br># HeadingTwo<br>dolor sit amet<br><br>## Heading 2.1<br>consetetur sadipscing elitr]\n    end\n    SRC --> MDSPLIT(mdsplit in.md)\n    MDSPLIT --> SPLIT_A\n    MDSPLIT --> SPLIT_B\n    subgraph in/HeadingTwo.md\n        SPLIT_B[# HeadingTwo<br>dolor sit amet<br><br>## Heading 2.1<br>consetetur sadipscing elitr]\n    end\n    subgraph in/Heading 1.md\n        SPLIT_A[# Heading 1<br>lorem ipsum<br><br>]\n    end\n    style SRC text-align:left\n    style SPLIT_A text-align:left\n    style SPLIT_B text-align:left\n    style MDSPLIT fill:#000,color:#0F0\n```\n\n**Split a file at level 2 headings** and higher, e.g. `# This Heading` and `## That Heading`, and write to a specific output directory:\n\n```bash\nmdsplit in.md --max-level 2 --output out\n```\n\n```mermaid\n%%{init: {'themeVariables': { 'fontFamily': 'Monospace', 'text-align': 'left'}}}%%\nflowchart LR\n    subgraph in.md\n        SRC[# Heading 1<br>lorem ipsum<br><br># HeadingTwo<br>dolor sit amet<br><br>## Heading 2.1<br>consetetur sadipscing elitr]\n    end\n    SRC --> MDSPLIT(mdsplit in.md -l 2 -o out)\n    subgraph out/HeadingTwo/Heading 2.1.md\n        SPLIT_C[## Heading 2.1<br>consetetur sadipscing elitr]\n    end\n    subgraph out/HeadingTwo.md\n        SPLIT_B[# HeadingTwo<br>dolor sit amet<br><br>]\n    end\n    subgraph out/Heading 1.md\n        SPLIT_A[# Heading 1<br>lorem ipsum<br><br>]\n    end\n    MDSPLIT --> SPLIT_A\n    MDSPLIT --> SPLIT_B\n    MDSPLIT --> SPLIT_C\n    style SRC text-align:left\n    style SPLIT_A text-align:left\n    style SPLIT_B text-align:left\n    style MDSPLIT fill:#000,color:#0F0\n```\n\n**Split markdown from stdin**:\n\n```bash\ncat in.md | mdsplit --output out\n```\n\n## Development (Ubuntu 22.04)\n\nAdd the [deadsnakes PPA](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa)\nand install additional python versions for testing\n\n    sudo add-apt-repository ppa:deadsnakes/ppa\n    sudo apt install python3.7 python3.7-distutils\n    sudo apt install python3.8 python3.8-distutils\n    sudo apt install python3.9 python3.9-distutils\n\nInstall [poetry](https://python-poetry.org)\n\nPrepare virtual environment and download dependencies\n\n    poetry install\n\nRun tests (for the default python version)\n\n    poetry run pytest\n\nRun tests for all supported python versions\n\n    tox\n\nRelease new version\n\n    poetry build\n    poetry publish\n\n[Download statistics](https://pypistats.org/packages/mdsplit)\n",
    'author': 'Markus Straub',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/markusstraub/mdsplit',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
