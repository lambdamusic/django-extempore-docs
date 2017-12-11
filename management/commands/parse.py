#!/usr/bin/env python


"""
# extracts functions code from xtm source code, returns a structure consisting of a list of metadata dictionaries (one per function)

USAGE

python parse.py > data.json


2016-03-07: changes for working against 'HEAD'
2016-01-26: this is a duplicate of /code/extempore/xtm-utils-public/etc..

"""


import os, sys

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


# get this path
_dirname, _filename = os.path.split(os.path.abspath(__file__))
# for dynamic links generation
GITHUB_BASE_URL = "https://github.com/digego/extempore/tree/0.7.0/"
# location of extempore src
DEFAULT_XTMDIR = ['/Applications/-Other-Apps/2-Music/_synthesys/extempore/']
# DEFAULT_XTMDIR = ['/usr/local/Cellar/extempore/HEAD/share/extempore/']



##
### main functions
##


def parse_extempore_src(_DIRS=DEFAULT_XTMDIR, noexamples=True, notests=True):
	"""
	recursive src files browser & extractor

	<noexamples, notests>: flags to avoid parsing those folders
	<aot-cache> : skipped by default (compiled stuff)
	"""

	index = []
	for path in _DIRS:
		print >> sys.stderr, "******** Extracting documentation from: \n=> " + _DIRS[0] + " ==\n********"
		for root, dirs, files in os.walk(path):
			for file in files:
				if noexamples and "/share/extempore/examples" in root:
					continue
				elif notests and "/share/extempore/tests" in root:
					continue
				elif "aot-cache" in root:
					continue
				else:
					if file.endswith(".xtm"):
						print >> sys.stderr, root + "/" + file
						index += _parse_onefile(root + "/" + file, path)

	index = sorted(index, key=lambda x: x['name'])
	return index






def _parse_onefile(f, original_path, IGNORE_CONSTANTS=True, IGNORE_SYMBOLS=True):
	"""
	extract definitions
	eg (define *gm-kick* 35)

	returns a list of dicts
	[{'name' : titlebuffer, 'codepygments' : linebuffer, 'file' : f, 'url' : url, 'functiontype' : functiontype, 'group' : group}]

	@todo: extract also the fun comments

	"""
	output = []
	lines = open(f).read().splitlines()

	functiontype = None
	titlebuffer = None
	linebuffer = []

	def _genData(linebuffer, titlebuffer, f, original_path, functiontype):
		"""wrapping common func"""
		# add pygments
		lexer = get_lexer_by_name("scheme", stripall=True)
		result = highlight(linebuffer, lexer, HtmlFormatter())
		# hardcode github url
		url = f.replace(original_path, GITHUB_BASE_URL)
		return [{'name' : titlebuffer,
				# 'code' : _saveSpaces(linebuffer),
				'codepygments' : result,
				'file' : f,
				'functiontype' : functiontype,
				'url' : url,
				'group' : inferGroup(titlebuffer) }]


	for line in lines:
		# print line
		if titlebuffer and linebuffer and not line:
			# it's a definition delimited by an empty line => save
			output += _genData(linebuffer, titlebuffer, f, original_path, functiontype)
			functiontype = None
			titlebuffer = None
			linebuffer = []

		elif line.startswith("(define ") or \
			 line.startswith("(bind-func ") or \
			 line.startswith("(define-macro ") or \
			 line.startswith("(macro "):
			# it's a definition delimited by a new def => save
			# but of course the first time round <linebuffer> is empty
			#
			if linebuffer:

				output += _genData(linebuffer, titlebuffer, f, original_path, functiontype)

			lline = line.split()

			# get function name
			functiontype = _getType(lline[0])
			# get function name
			titlebuffer = _getTitle(lline[1])
			# titlebuffer = _remove_parenthesis(lline[1])

			if IGNORE_CONSTANTS and titlebuffer.startswith("*"):
				functiontype = None
				titlebuffer = None
				linebuffer = None
			else:
				linebuffer = line
		else:
			# print line + "/n/n"
			if titlebuffer:
					# HACK...
				if not line[0] == "(":
					#note: very weak way to determine two definitions without empty line
					# in such a case we just skip it - assuming the good coding convention
					# this refers to cases like {bind-val etc...}
					linebuffer += "\n" + line

	return output











# ;;;;;;;;;;;;;;;;;;;;;;;;
# ;;;;;;; UTILS ;;;;;;;;
# ;;;;;;;;;;;;;;;;;;;;;;;;;;



def _getTitle(s):
	s = _remove_parenthesis(s)

	if "[" and "]" in s:
		# eg (bind-func qbuf_push:[void,QBuffer*,!a]*
		s = s.split(":")[0]

	return s


def _getType(s):
	"""classify the type of a function definition """

	s = _remove_parenthesis(s.strip())

	if "define-macro" in s or "macro" in s:
		return "macro"
	elif "define" in s:
		return "scheme"
	elif "bind-func" in s:
		return "xtlang"
	else:
		return "unknown"



def _remove_parenthesis(s):
	s = s.replace("(", "")
	s = s.replace(")", "")
	return s


def _saveSpaces(line):
	return line.replace(" ", "&nbsp;")


def inferGroup(titlebuffer):
	"""infers the function prefix"""
	if titlebuffer[0] == "*":
		return "*var*"
	if titlebuffer[0] in ["-", "_"]:  #["*", "-", "_"]
		#strip first letter
		titlebuffer = titlebuffer[1:]

	if titlebuffer.startswith("glfw"):
		return "glfw:"

	idx = titlebuffer.rfind(":")
	# print idx, titlebuffer[:idx+1]
	if idx > 0:
		return titlebuffer[:idx+1]
	else:
		return "" # default








# ;;;;;;;;;;;;;;;;;;;;;;;;
# ;;;;;;; main Caller ;;;;;;;;
# ;;;;;;;;;;;;;;;;;;;;;;;;;;



def main(args):

	if len(args) < 2:
		# DEFAULT - IMPORTANT: if not starting at ../share/extempore/ level the links to GitHub will be broken
		DIRS = DEFAULT_XTMDIR
	else:
		_dir = args[1]
		if _dir[-1] != "/": # ps: must end with slash
			_dir += "/"
		DIRS = [_dir]

	if os.path.isdir(DIRS[0]):

		##
		print parse_extempore_src(DIRS)
		##

	else:
		print >> sys.stderr, "Directory does not exist"





if __name__ == '__main__':
	import sys
	try:
		main(sys.argv)
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e
