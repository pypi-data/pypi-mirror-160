#!/usr/bin/env python

"""Tests for `mff_pytex` package."""

import pytest
from src.mff_pytex import structure


def test_create_texfile():
    """Test if texfile is created"""
    assert structure.TexFile().file_path == structure.TEMPLATE

# def test_document():
#     figure = structure.Document()
#     figure.clearpage()
#     f = open('tests/temp2.tex', 'w')
#     f.write(str(figure))
#     f.close()
#     assert cmp('tests/temp2.tex', 'tests/temp.tex')

def test_command_makefile():
    """Test if command makefile works properly"""
    assert structure.command('makefile') == "\\makefile"

def test_command_begin_document():
    """Test if command begin works properly"""
    assert structure.command('begin', 'document') == "\\begin{document}"

def test_command_usepackage():
    """Test if command usepackage properly"""
    assert structure.command('usepackage', 'inputenc', 'utf8') == "\\usepackage[utf8]{inputenc}"
