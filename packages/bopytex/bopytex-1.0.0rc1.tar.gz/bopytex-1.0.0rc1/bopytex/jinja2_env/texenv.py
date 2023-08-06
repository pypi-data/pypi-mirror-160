#!/usr/bin/env python
# encoding: utf-8

import jinja2

__all__ = [
    "texenv",
]

# Definition of jinja syntax for latex
texenv = jinja2.Environment(
    block_start_string=r"\Block{",
    block_end_string="}",
    variable_start_string=r"\Var{",
    variable_end_string="}",
    comment_start_string=r"\#{",
    comment_end_string="}",
    line_statement_prefix="%-",
    line_comment_prefix="%#",
    loader=jinja2.ChoiceLoader(
        [
            jinja2.FileSystemLoader(["./"]),
        ]
    ),
    extensions=["jinja2.ext.do"],
)

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del
