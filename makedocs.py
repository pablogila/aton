'''
This script is used to update Aton documentation automatically.
Requires pdoc, install it with `pip install pdoc`.
It also requires Aton itself; installation instructions can be found in the README.md file.
Run this script as `python3 makedocs.py`.
'''

import aton

readme = './README.md'
temp_readme = './_README_temp.md'
exec(open('aton/_version.py').read())

fix_dict ={
    '[call](https://pablogila.github.io/Aton/aton/call.html)'                   : '`aton.call`',
    '[file](https://pablogila.github.io/Aton/aton/file.html)'                   : '`aton.file`',
    '[find](https://pablogila.github.io/Aton/aton/text/find.html)'              : '`aton.text.find`',
    '[extract](https://pablogila.github.io/Aton/aton/text/extract.html)'        : '`aton.text.extract`',
    '[text](https://pablogila.github.io/Aton/aton/text/edit.html)'              : '`aton.text.edit`',
    '[qe](https://pablogila.github.io/Aton/aton/interface/qe.html)'             : '`aton.interface.qe`',
    '[phonopy](https://pablogila.github.io/Aton/aton/interface/phonopy.html)'   : '`aton.interface.phonopy`',
    '[castep](https://pablogila.github.io/Aton/aton/interface/castep.html)'     : '`aton.interface.castep`',
    'Check the [full documentation online](https://pablogila.github.io/Aton/).' : '',
    '<p align="center"><img width="50.0%" src="aton.svg"></p>'                  : ''
}

print(f'Updating docs to {__version__}...')
#th.text.replace_line(readme, '# ThotPy v', f'# ThotPy {version}', 1)
aton.file.from_template(readme, temp_readme, fix_dict)
aton.call.bash(f"pdoc ./aton/ -o ./docs --mermaid --math --footer-text='Aton {__version__} documentation'")
aton.file.remove(temp_readme)

