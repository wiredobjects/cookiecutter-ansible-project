# -*- coding: utf-8 -*-

# import stdlibs
import os
import re
# import third party libs
import pytest
# import local libs


@pytest.fixture
def context():
    return {
        "author_name": "Sven Wilhelm",
        "email": "refnode@gmail.com",
        "github_username": "refnode",
        "license": "Apache Software License 2.0",
    }


#def test_default_configuration(cookies, context):
def test_default_configuration(cookies):
    #result = cookies.bake(extra_context=context)
    result = cookies.bake()
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'ansible-project'
    assert result.project.isdir()
