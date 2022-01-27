import os
import re
import subprocess
import pprint

paks=['Packages/ActionScript/ActionScript.sublime-syntax', 'Packages/AppleScript/AppleScript.sublime-syntax', 'Packages/ASP/ASP.sublime-syntax', 'Packages/ASP/HTML-ASP.sublime-syntax', 'Packages/Batch File/Batch File.sublime-syntax', 'Packages/C#/Build.sublime-syntax', 'Packages/C#/C#.sublime-syntax', 'Packages/C++/C++.sublime-syntax', 'Packages/C++/C.sublime-syntax', 'Packages/Clojure/Clojure.sublime-syntax', 'Packages/CSS/CSS.sublime-syntax', 'Packages/D/D.sublime-syntax', 'Packages/D/DMD Output.sublime-syntax', 'Packages/Diff/Diff.sublime-syntax', 'Packages/Erlang/Erlang.sublime-syntax', 'Packages/Erlang/HTML (Erlang).sublime-syntax', 'Packages/Git Formats/Git Attributes.sublime-syntax', 'Packages/Git Formats/Git Commit.sublime-syntax', 'Packages/Git Formats/Git Common.sublime-syntax', 'Packages/Git Formats/Git Config.sublime-syntax', 'Packages/Git Formats/Git Ignore.sublime-syntax', 'Packages/Git Formats/Git Link.sublime-syntax', 'Packages/Git Formats/Git Log.sublime-syntax', 'Packages/Git Formats/Git Rebase.sublime-syntax', 'Packages/Go/Go.sublime-syntax', 'Packages/Graphviz/DOT.sublime-syntax', 'Packages/Groovy/Groovy.sublime-syntax', 'Packages/Haskell/Haskell.sublime-syntax', 'Packages/Haskell/Literate Haskell.sublime-syntax', 'Packages/HTML/HTML.sublime-syntax', 'Packages/Java/Java Server Pages (JSP).sublime-syntax', 'Packages/Java/Java.sublime-syntax', 'Packages/Java/JavaDoc.sublime-syntax', 'Packages/Java/JavaProperties.sublime-syntax', 'Packages/JavaScript/JavaScript.sublime-syntax', 'Packages/JavaScript/JSON.sublime-syntax', 'Packages/JavaScript/Regular Expressions (JavaScript).sublime-syntax', 'Packages/LaTeX/Bibtex.sublime-syntax', 'Packages/LaTeX/LaTeX Log.sublime-syntax', 'Packages/LaTeX/LaTeX.sublime-syntax', 'Packages/LaTeX/TeX.sublime-syntax', 'Packages/Lisp/Lisp.sublime-syntax', 'Packages/Lua/Lua.sublime-syntax', 'Packages/Makefile/Make Output.sublime-syntax', 'Packages/Makefile/Makefile.sublime-syntax', 'Packages/Markdown/Markdown.sublime-syntax', 'Packages/Markdown/MultiMarkdown.sublime-syntax', 'Packages/Matlab/Matlab.sublime-syntax', 'Packages/Objective-C/Objective-C++.sublime-syntax', 'Packages/Objective-C/Objective-C.sublime-syntax', 'Packages/OCaml/camlp4.sublime-syntax', 'Packages/OCaml/OCaml.sublime-syntax', 'Packages/OCaml/OCamllex.sublime-syntax', 'Packages/OCaml/OCamlyacc.sublime-syntax', 'Packages/Pascal/Pascal.sublime-syntax', 'Packages/Perl/Perl.sublime-syntax', 'Packages/PHP/PHP Source.sublime-syntax', 'Packages/PHP/PHP.sublime-syntax', 'Packages/PHP/Regular Expressions (PHP).sublime-syntax', 'Packages/Python/Python.sublime-syntax', 'Packages/Python/Regular Expressions (Python).sublime-syntax', 'Packages/R/R Console.sublime-syntax', 'Packages/R/R.sublime-syntax', 'Packages/R/Rd (R Documentation).sublime-syntax', 'Packages/Rails/HTML (Rails).sublime-syntax', 'Packages/Rails/JavaScript (Rails).sublime-syntax', 'Packages/Rails/Ruby Haml.sublime-syntax', 'Packages/Rails/Ruby on Rails.sublime-syntax', 'Packages/Rails/SQL (Rails).sublime-syntax', 'Packages/Regular Expressions/RegExp.sublime-syntax', 'Packages/RestructuredText/reStructuredText.sublime-syntax', 'Packages/Ruby/Ruby.sublime-syntax', 'Packages/Rust/Cargo.sublime-syntax', 'Packages/Rust/Rust.sublime-syntax', 'Packages/Scala/Scala.sublime-syntax', 'Packages/ShellScript/Bash.sublime-syntax', 'Packages/ShellScript/commands-builtin-shell-bash.sublime-syntax', 'Packages/ShellScript/Shell-Unix-Generic.sublime-syntax', 'Packages/SQL/SQL.sublime-syntax', 'Packages/TCL/HTML (Tcl).sublime-syntax', 'Packages/TCL/Tcl.sublime-syntax', 'Packages/Textile/Textile.sublime-syntax', 'Packages/XML/XML.sublime-syntax', 'Packages/YAML/YAML.sublime-syntax', 'Packages/CMake/CMake C Header.sublime-syntax', 'Packages/CMake/CMake C++ Header.sublime-syntax', 'Packages/CMake/CMake.sublime-syntax', 'Packages/CMake/CMakeCache.sublime-syntax', 'Packages/CMake/CMakeCommands.sublime-syntax']
# 4.0
paks=['Packages/ActionScript/ActionScript.sublime-syntax', 'Packages/AppleScript/AppleScript.sublime-syntax', 'Packages/ASP/ASP.sublime-syntax', 'Packages/ASP/HTML (ASP).sublime-syntax', 'Packages/Batch File/Batch File.sublime-syntax', 'Packages/C#/Build.sublime-syntax', 'Packages/C#/C#.sublime-syntax', 'Packages/C++/C++.sublime-syntax', 'Packages/C++/C.sublime-syntax', 'Packages/Clojure/Clojure.sublime-syntax', 'Packages/Clojure/ClojureScript.sublime-syntax', 'Packages/CSS/CSS.sublime-syntax', 'Packages/D/D.sublime-syntax', 'Packages/D/DMD Output.sublime-syntax', 'Packages/Diff/Diff.sublime-syntax', 'Packages/Erlang/Erlang.sublime-syntax', 'Packages/Erlang/HTML (Erlang).sublime-syntax', 'Packages/Git Formats/Git Attributes.sublime-syntax', 'Packages/Git Formats/Git Commit.sublime-syntax', 'Packages/Git Formats/Git Common.sublime-syntax', 'Packages/Git Formats/Git Config.sublime-syntax', 'Packages/Git Formats/Git Ignore.sublime-syntax', 'Packages/Git Formats/Git Link.sublime-syntax', 'Packages/Git Formats/Git Log.sublime-syntax', 'Packages/Git Formats/Git Mailmap.sublime-syntax', 'Packages/Git Formats/Git Rebase.sublime-syntax', 'Packages/Go/Go.sublime-syntax', 'Packages/Graphviz/DOT.sublime-syntax', 'Packages/Groovy/Groovy.sublime-syntax', 'Packages/Haskell/Haskell.sublime-syntax', 'Packages/Haskell/Literate Haskell.sublime-syntax', 'Packages/HTML/HTML (Plain).sublime-syntax', 'Packages/HTML/HTML.sublime-syntax', 'Packages/Java/Java Server Pages (JSP).sublime-syntax', 'Packages/Java/Java.sublime-syntax', 'Packages/Java/JavaDoc.sublime-syntax', 'Packages/Java/JavaProperties.sublime-syntax', 'Packages/JavaScript/JavaScript.sublime-syntax', 'Packages/JavaScript/JSX.sublime-syntax', 'Packages/JavaScript/Regular Expressions (JavaScript).sublime-syntax', 'Packages/JavaScript/TSX.sublime-syntax', 'Packages/JavaScript/TypeScript.sublime-syntax', 'Packages/JSON/JSON.sublime-syntax', 'Packages/LaTeX/Bibtex.sublime-syntax', 'Packages/LaTeX/LaTeX Log.sublime-syntax', 'Packages/LaTeX/LaTeX.sublime-syntax', 'Packages/LaTeX/TeX.sublime-syntax', 'Packages/Lisp/Lisp.sublime-syntax', 'Packages/Lua/Lua.sublime-syntax', 'Packages/Makefile/Make Output.sublime-syntax', 'Packages/Makefile/Makefile Shell.sublime-syntax', 'Packages/Makefile/Makefile.sublime-syntax', 'Packages/Markdown/Markdown.sublime-syntax', 'Packages/Markdown/MultiMarkdown.sublime-syntax', 'Packages/Matlab/Matlab.sublime-syntax', 'Packages/Objective-C/Objective-C++.sublime-syntax', 'Packages/Objective-C/Objective-C.sublime-syntax', 'Packages/OCaml/camlp4.sublime-syntax', 'Packages/OCaml/OCaml.sublime-syntax', 'Packages/OCaml/OCamllex.sublime-syntax', 'Packages/OCaml/OCamlyacc.sublime-syntax', 'Packages/Pascal/Pascal.sublime-syntax', 'Packages/Perl/Perl.sublime-syntax', 'Packages/PHP/PHP Source.sublime-syntax', 'Packages/PHP/PHP.sublime-syntax', 'Packages/PHP/Regular Expressions (PHP).sublime-syntax', 'Packages/Python/Python.sublime-syntax', 'Packages/Python/Regular Expressions (Python).sublime-syntax', 'Packages/R/R Console.sublime-syntax', 'Packages/R/R.sublime-syntax', 'Packages/R/Rd (R Documentation).sublime-syntax', 'Packages/Rails/HTML (Rails).sublime-syntax', 'Packages/Rails/JavaScript (Rails).sublime-syntax', 'Packages/Rails/Ruby Haml.sublime-syntax', 'Packages/Rails/Ruby on Rails.sublime-syntax', 'Packages/Rails/SQL (Rails).sublime-syntax', 'Packages/Regular Expressions/File Pattern.sublime-syntax', 'Packages/Regular Expressions/Regex Replace.sublime-syntax', 'Packages/Regular Expressions/RegExp.sublime-syntax', 'Packages/RestructuredText/reStructuredText.sublime-syntax', 'Packages/Ruby/Ruby.sublime-syntax', 'Packages/Rust/Cargo.sublime-syntax', 'Packages/Rust/Rust.sublime-syntax', 'Packages/Scala/Scala.sublime-syntax', 'Packages/ShellScript/Bash.sublime-syntax', 'Packages/ShellScript/commands-builtin-shell-bash.sublime-syntax', 'Packages/ShellScript/Shell-Unix-Generic.sublime-syntax', 'Packages/SQL/SQL.sublime-syntax', 'Packages/TCL/HTML (Tcl).sublime-syntax', 'Packages/TCL/Tcl.sublime-syntax', 'Packages/Textile/Textile.sublime-syntax', 'Packages/XML/DTD.sublime-syntax', 'Packages/XML/XML.sublime-syntax', 'Packages/XML/XSL.sublime-syntax', 'Packages/YAML/YAML.sublime-syntax']
# paks=sublime.find_resources('*.sublime-syntax')

# Parsing yaml is overkill, just find the first scope entry with regex
# grep -r 'hidden: tru'
rehidden = re.compile(r'\s*hidden:\s*true')
rescope = re.compile(r'\s*scope:\s*([\w.+-]+)')

# Main format is listed as first entry
# A good way to find out which formats are used by vim, run:
# grep -r -l 'runtime.*xml.vim' vim81

vim_mapping = {
	#'source.actionscript.2': (),
	#'source.applescript': (),
	#'source.asp': (),
	'source.c': ('c', 'ch', 'cmod', 'dtrace', 'nasm', 'rpcgen', 'splint', 'xs'),
	'source.c++': ('cpp', 'arduino', 'cuda', 'cynlib', 'esqlc', 'kwt'),
	'source.camlp4.ocaml': ('ocaml'),
	'source.clojure': ('clojure'),
	'source.cs': ('cs'),
	'source.css': ('css', 'less', 'sass', 'typescript'),
	'source.d': ('d'),
	'source.diff': ('diff'),
	'source.dosbatch': ('dosbatch'),
	'source.dot': ('dot'),
	'source.erlang': ('erlang'),
	'source.go': ('go'),
	'source.groovy': ('groovy'),
	'source.haskell': ('haskell', 'chaskell'),
	'source.java': ('java', 'antlr', 'javacc'),
	#'source.java-props': (),
	'source.js': ('javascript', 'javascriptreact', 'tt2js', 'typescript'),
	#'source.js.rails': (),
	'source.json': ('json', 'typescript'),
	'source.lisp': ('lisp'),
	'source.lua': ('lua'),
	'source.makefile': ('make', 'automake'),
	'source.matlab': ('matlab'),
	#'source.nant-build': (),
	'source.objc': ('objc'),
	'source.objc++': ('objcpp'),
	'source.ocaml': ('ocaml'),
	#'source.ocamllex': (),
	#'source.ocamlyacc': (),
	'source.pascal': ('pascal'),
	'source.perl': ('perl'),
	'source.python': ('python', 'bzl', 'conaryrecipe', 'pyrex'),
	'source.r': ('r'),
	#'source.r-console': (),
	#'source.regexp': (),
	'source.ruby': ('ruby'),
	#'source.ruby.rails': (),
	'source.rust': ('rust'),
	'source.scala': ('scala', 'sbt'),
	'source.shell.bash': ('bash', 'zsh', 'sh'),
	'source.sql': ('sql'),
	'source.sql.ruby': ('ruby'),
	'source.tcl': ('tcl', 'sdc'),
	'source.yaml': ('yaml'),
	#'text.bibtex': (),
	#'text.git.attributes': (),
	#'text.git.commit': (),
	#'text.git.config': (),
	#'text.git.ignore': (),
	#'text.git.link': (),
	#'text.git.log': (),
	#'text.git.rebase': (),
	'text.haml': ('haml'),
	#'text.html.asp': (),
	'text.html.basic': ('html', 'aspperl', 'aspvbs', 'cf', 'dtml', 'gsp', 'htmlcheetah', 'htmldjango', 'htmlm4', 'htmlos', 'mason', 'msql', 'plp', 'smarty', 'spyce', 'template', 'tt2html', 'vue', 'webmacro', 'wml', 'xhtml'),
	#'text.html.erlang.yaws': (),
	'text.html.jsp': ('jsp'),
	'text.html.markdown': ('markdown', 'rmd'),
	#'text.html.markdown.multimarkdown': (),
	'text.html.ruby': ('ruby'),
	'text.html.tcl': ('tcl', 'sdc'),
	#'text.html.textile': (),
	#'text.log.latex': (),
	'text.restructuredtext': ('rst', 'rrst'),
	'text.tex': ('tex', 'cweb', 'lhaskell', 'rnoweb'),
	#'text.tex.latex': (),
	'text.tex.latex.haskell': ('haskell', 'chaskell'),
	#'text.tex.latex.rd': (),
	'text.xml': ('xml', 'ant', 'dsl', 'papp', 'svg', 'wsh', 'xbl', 'xquery', 'xsd', 'xslt'),

	# External Packages

	# https://github.com/zyxar/Sublime-CMakeLists
	'source.cmake': ('cmake'),
}

vimpath='/usr/share/vim/vim82/syntax'
vimpath='/tmp/vim-8.2.3111/runtime/syntax'

subltovim = {
	'source.c++': 'cpp',
	'source.js': 'javascript',
	'source.makefile': 'make',
	'source.objc++': 'objcpp',
	'text.html.basic': 'html',
	'text.restructuredtext': 'rst',
	'text.git.config': '',
	'source.cmake.config.c': '',
	'source.cmake.config.c++': '',
}
sublextramap = {
	'bash': ['zsh']
}
sublremmap = {
	'c': ['nasm', 'xs']
}
foundmarkups=set()
finaltable={}
packagemap={}
for p in paks:
	try:
		with open(os.path.join('/tmp', p)) as f:
			data= f.read()
			if not rehidden.search(data):
				m = rescope.search(data)
				fmt=m.group(1)
				packagemap[m.group(1)]=p
				fmt = subltovim.get(fmt, fmt.rpartition('.')[2])
				if os.path.isfile(os.path.join(vimpath, fmt + '.vim')):
					addname=set()
					if fmt in sublextramap:
						addname = addname.union(sublextramap[fmt])

					try:
						additional = subprocess.check_output(['grep', '-r', '-l', 'runtime.*\\b' + fmt + '.vim', vimpath], universal_newlines=True)
						for addfmt in additional.split():
							addname.add(os.path.basename(addfmt)[:-len('.vim')])
					except subprocess.CalledProcessError:
						pass
					foundmarkups.add(fmt)
					if fmt in sublremmap:
						addname = addname.difference(sublremmap[fmt])

					finaltable[m.group(1)] = [fmt] + list(addname)

				else:
					finaltable[m.group(1)] = []
				# print(m.group(1), p)
	except Exception as e:
		raise(e)
		print("Cant parse", p, e)

print('vim_mapping = {')
skeys = list(finaltable)
skeys.sort()
vimtypes={}
vmmap={}
for key in list(skeys):
	value = finaltable[key]
	if value:
		for v in value:
			vimtypes[v] = key
		mainfmt = value[0];
		uniquelist=list(set(value).difference(foundmarkups))
		uniquelist.sort();
		print('\t\'%s\': (\'%s\'),' % (key, '\', \''.join([mainfmt] + uniquelist)))
	else:
		print('\t#\'%s\': (),' % key)

print('\n\t# External Packages\n\n\t# https://github.com/zyxar/Sublime-CMakeLists\n\t\'source.cmake\': (\'cmake\'),\n}')

pprint.pprint(vimtypes)
pprint.pprint(packagemap)
