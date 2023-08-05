#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "WYDomain",
    version = "0.0.2",
    keywords = ("pip", "WYDomain", "domain licensed"),
    description = "A tool of check Chinese domain is licensed",
    long_description = "A tool of check Chinese domain is licensed",
    license = "MIT Licence",

    url = "https://github.com/WYTool/wydomain_python",
    author = "WYTool",
    author_email = "wytoolsoft@gmail.com",

    packages = find_packages(),
    include_package_data = True,

    # package_data = { '':['*.txt'], },

    platforms = "any",
)

