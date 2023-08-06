""" Produce tasks to do

It essentially place things at the right place.

"""
from dataclasses import dataclass


@dataclass
class Task:
    action: str
    args: dict
    deps: list
    output: str


def generate(template: str, meta: dict, output: str):
    """Create a task to generate a subject"""
    return Task(
        action="GENERATE",
        args=meta,
        deps=[template],
        output=output,
    )


def activate_corr_on(src: str, meta: dict, output: str):
    """Create a task to activate correction for src"""
    return Task(
        action="ACTIVATE_CORR",
        args=meta,
        deps=[src],
        output=output,
    )


def compile_pdf(src: str, output: str):
    """Create a task to compile src"""
    return Task(
        action="COMPILE",
        args={},
        deps=[src],
        output=output,
    )


def join_pdfs(pdfs: list, output: str):
    """Create task to join pdf together"""
    return Task(
        action="JOIN",
        args={},
        deps=pdfs,
        output=output,
    )


def clean(files: list):
    """Create task to clean files"""
    return Task(
        action="CLEAN",
        args={},
        deps=files,
        output=None,
    )
