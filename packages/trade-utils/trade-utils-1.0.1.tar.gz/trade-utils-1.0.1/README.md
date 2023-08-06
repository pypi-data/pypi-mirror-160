# algo
Set of tools for algorithmic trading

# Contributing 
To get started [install pipenv](https://pipenv.pypa.io/en/latest/install/#crude-installation-of-pipenv)

Install dependencies
```
pipenv install --dev
```

Active environment
```
pipenv shell
```

To use VSCode `Pyhton: Select Interpreter` and choose suggested PipEnv environment.

At this point version update is manual. 

# Building And uploading
```sh
python -m build
twine upload ./dist/* --verbose
```

# Local run for dev

```sh
docker compose up
pipenv shell
export CONFIG_FILE=~/config-container/config.yml
python -m algo

```

TODO: 
  * make it run standalon (now it raises errors about the log format)
  * add tests [important] way to many things are dangling on the `expectations` of valid functioning ie: caching and valid rehidration
  * make config retry loading config file ie do not assign empty config on fail
    Now it raises error only once on the first attempt to access config. Then it returns empty/default values
  

DONE:
  * `11/07/22`: make `install_requires` dynamic based on `Pipfile`
  * `10/07/22`: implement multiprocess caches see :synccache: mark. In order to make only one process to call the data retrieval function. to do so: done 
    1. keep the temporary cache value as a global lock aka '{cache_key}-loading' its presense mean that one process is loading the data and cache will be available soon
    1. main: loading process should create this special value and start loading data
    1. others: on this cache availability should sleep before the data will become available
    1. main: after data is loaded set cache value and remove the locking entry
    1. others: should poll until there is no such value in the table then read the cached data or take the role of main process