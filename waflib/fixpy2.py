#!/usr/bin/env python
# encoding: utf-8
# Thomas Nagy, 2010-2016 (ita)

import os

all_modifs = {}

def fixdir(dir):
	"""Call all substitution functions on Waf folders"""
	global all_modifs
	for k in all_modifs:
		for v in all_modifs[k]:
			modif(os.path.join(dir, 'waflib'), k, v)

def modif(dir, name, fun):
	"""Call a substitution function"""
	if name == '*':
		lst = []
		for y in '. Tools extras'.split():
			for x in os.listdir(os.path.join(dir, y)):
				if x.endswith('.py'):
					lst.append(y + os.sep + x)
		for x in lst:
			modif(dir, x, fun)
		return

	filename = os.path.join(dir, name)
	f = open(filename, 'r')
	try:
		txt = f.read()
	finally:
		f.close()

	txt = fun(txt)

	f = open(filename, 'w')
	try:
		f.write(txt)
	finally:
		f.close()

def subst(*k):
	"""register a substitution function"""
	def do_subst(fun):
		global all_modifs
		for x in k:
			try:
				all_modifs[x].append(fun)
			except KeyError:
				all_modifs[x] = [fun]
		return fun
	return do_subst

@subst('*')
def r1(code):
	"utf-8 fixes for python < 2.6"
	code = code.replace('as e:', ',e:')
	code = code.replace(".decode(sys.stdout.encoding or'iso8859-1',replace=True)", '')
	return code.replace('.encode()', '')

@subst('Runner.py')
def r4(code):
	"generator syntax"
	return code.replace('next(self.biter)', 'self.biter.next()')

@subst('Context.py')
def r5(code):
	return code.replace("('Execution failure: %s'%str(e),ex=e)", "('Execution failure: %s'%str(e),ex=e),None,sys.exc_info()[2]")

