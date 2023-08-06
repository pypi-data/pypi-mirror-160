Python package to create report for Frigel machines

# Table of Contents
1. [Project information](README.md#project-information)
2. [Package creation](README.md#package-creation)
2. [Usage](README.md#usage)
3. [Licensing](LICENSE.txt)

# Project information
This tool converts PEMS TCP to PEMS serial

# Package creation
How to create python package and upload it to [pypi](https://pypi.org/)
<pre><code>
pip install --upgrade twine
python setup.py sdist
python setup.py bdist_wheel
python setup.py build
python setup.py install
twine upload --repository pypi dist/*
</code></pre>


# Usage
Check [runs_server.py](#runs_server.py)

