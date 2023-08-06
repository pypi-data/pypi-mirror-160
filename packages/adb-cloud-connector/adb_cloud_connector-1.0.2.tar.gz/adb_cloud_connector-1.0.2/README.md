# ArangoDB Cloud Connector

[![build](https://github.com/arangodb/adb_cloud_connector/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/arangodb/adb_cloud_connector/actions/workflows/build.yml)
[![CodeQL](https://github.com/arangodb/adb_cloud_connector/actions/workflows/analyze.yml/badge.svg?branch=master)](https://github.com/arangodb/adb_cloud_connector/actions/workflows/analyze.yml)
[![Last commit](https://img.shields.io/github/last-commit/arangodb/adb_cloud_connector)](https://github.com/arangodb/adb_cloud_connector/commits/master)
<!-- [![Coverage Status](https://coveralls.io/repos/github/arangodb/adb_cloud_connector/badge.svg?branch=master)](https://coveralls.io/github/arangodb/adb_cloud_connector) -->

[![PyPI version badge](https://img.shields.io/pypi/v/adb_cloud_connector?color=3775A9&style=for-the-badge&logo=pypi&logoColor=FFD43B)](https://pypi.org/project/adb_cloud_connector/)
[![Python versions badge](https://img.shields.io/pypi/pyversions/adb_cloud_connector?color=3776AB&style=for-the-badge&logo=python&logoColor=FFD43B)](https://pypi.org/project/adb_cloud_connector/)

[![License](https://img.shields.io/github/license/arangodb/adb_cloud_connector?color=9E2165&style=for-the-badge)](https://github.com/arangodb/adb_cloud_connector/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/static/v1?style=for-the-badge&label=code%20style&message=black&color=black)](https://github.com/psf/black)
[![Downloads](https://img.shields.io/badge/dynamic/json?style=for-the-badge&color=282661&label=Downloads&query=total_downloads&url=https://api.pepy.tech/api/projects/adb_cloud_connector)](https://pepy.tech/project/adb_cloud_connector)

<a href="https://cloud.arangodb.com/" rel="cloud.arangodb.com"><img width=15% src="https://www.arangodb.com/wp-content/uploads/2019/10/ArangoDB-Oasis-Logo.png"/></a>

Provides access to temporary ArangoDB Cloud instance provisioning, for graph and beyond. 

## Installation

#### Latest Release
```
pip install adb-cloud-connector
```
#### Current State
```
pip install git+https://github.com/arangodb/adb_cloud_connector.git
```

## Quickstart

```py
from adb_cloud_connector import get_temp_credentials

con = get_temp_credentials()

print(con)
```

##  Development & Testing

1. `git clone https://github.com/arangodb/adb_cloud_connector.git`
2. `cd adb_cloud_connector`
3. (create virtual environment of choice)
4. `pip install -e .[dev]`
6. `pytest`
