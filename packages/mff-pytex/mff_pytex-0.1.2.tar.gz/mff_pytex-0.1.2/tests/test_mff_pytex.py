#!/usr/bin/env python

"""Tests for `mff_pytex` package."""

import pytest


from src.mff_pytex import structure


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_create_texfile():
    """Test if texfile is created"""
    assert structure.TexFile().file_path == structure.TEMPLATE
