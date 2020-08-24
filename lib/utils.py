#!/usr/bin/python
#-*- coding:utf-8 -*-

from os import listdir, walk, getcwd, chdir
from os.path import isfile, join, dirname, abspath, expanduser

class cd:
	"""https://stackoverflow.com/a/13197763/12469275
	tnx Brian M. Hunt"""
	"""Context manager for changing the current working directory"""
	def __init__(self, newPath):
		self.newPath = expanduser(newPath)

	def __enter__(self):
		self.savedPath = getcwd()
		chdir(self.newPath)

	def __exit__(self, etype=None, value=None, traceback=None):
		chdir(self.savedPath)

def gotofile(relpath = __file__):
	cd(dirname(abspath(relpath))).__enter__()
	return(abspath(""))
