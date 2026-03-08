
## Project Setup
The projects dependencies are managed with uv. To install and get more information about uv, follow this documentation:
```
https://docs.astral.sh/uv/getting-started/installation/
```

To install the dependencies run

```
uv sync --locked
```

To setup the project you need to install requirements.txt and create a database_config.yaml in database package, 
database_config.yaml has to have following structure 

```
url: [ip of InfluxDB instance]
token: [auth token of InfluxDB instance]
org: [organization of InfluxDB instance]
```

## Run Tests
Tests are base on Pytest - run all tests via command line:

```
uv run pytest
```

## Update UAl Commons
To update changes in UAL commons library use this commands:
```
uv lock --upgrade-package ual
uv sync
```











