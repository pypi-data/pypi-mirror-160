#!/usr/bin/env python
# encoding: utf-8

"""
Producing then compiling templates
"""

import importlib.util
import os
from pathlib import Path

from bopytex import default_config
from bopytex.scheduler import Scheduler


def orcherstrator(
    options: dict,
    planner,
    dispatcher,
):
    tasks = planner(options)

    scheduler = Scheduler(dispatcher, [options["template"]])
    scheduler.append(tasks)

    for message in scheduler.backlog():
        yield message


def load_module(modulefile: str):
    spec = importlib.util.spec_from_file_location("module.name", modulefile)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clean_vars_keys(
    vars: dict,
    keys: list[str] = [
        "__name__",
        "__doc__",
        "__package__",
        "__loader__",
        "__spec__",
        "__file__",
        "__cached__",
        "__builtins__",
    ],
) -> dict:
    new_dict = vars.copy()
    for k in keys:
        del new_dict[k]
    return new_dict


def config_from_file(filename: str) -> dict:
    if Path(filename).exists():
        local_config = vars(load_module(filename))
        return clean_vars_keys(local_config)
    else:
        return {}


def build_config(options: dict) -> dict:
    """Look for options["configfile"] to load it with default_config and options"""
    config = clean_vars_keys(vars(default_config))

    configfile = ""
    try:
        configfile = options["configfile"]
    except KeyError:
        pass
    try:
        configfile = os.environ["BOPYTEXCONFIG"]
    except KeyError:
        pass
    if configfile:
        local_config = config_from_file(configfile)
        config.update(local_config)

    config.update(options)

    return config


def main(**options):

    config = build_config(options)

    orcherstre = orcherstrator(
        config, planner=default_config.planner, dispatcher=default_config.dispatcher
    )
    for message in orcherstre:
        yield message


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del
