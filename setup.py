#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

setup(
    name="gensory",
    version="0.1.0",
    description="Testing POCP",
    author="Martín",
    author_email = "maj.dagostino@gmail.com",
    license = "GPL v3",
    keywords = "Scraping Crawling Framework Python Twitter",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
    'python-twitter',
	'textblob',
	'elasticsearch',
	'tweepy',
    'monkeylearn',
    'HTMLParser'
    ],
)
