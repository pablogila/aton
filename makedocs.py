"""
This script is used to update the documentation automatically.
Requires pdoc, install it with `pip install pdoc`.
It also requires Aton itself; installation instructions can be found in the README.md file.
Run this script as `python3 makedocs.py`.
"""

import shutil
import aton

readme = './README.md'
temp_readme = './_README_temp.md'
# Update links from the README
fix_dict ={
    '[call](https://pablogila.github.io/Aton/aton/call.html)'                           : '`aton.call`',
    '[alias](https://pablogila.github.io/Aton/aton/alias.html)'                         : '`aton.alias`',
    '[units](https://pablogila.github.io/Aton/aton/units.html)'                         : '`aton.units`',
    '[atoms](https://pablogila.github.io/Aton/aton/atoms.html)'                         : '`aton.atoms`',
    '[elements](https://pablogila.github.io/Aton/aton/elements.html)'                   : '`aton.elements`',
    '[file](https://pablogila.github.io/Aton/aton/file.html)'                           : '`aton.file`',
    '[text](https://pablogila.github.io/Aton/aton/text.html)'                           : '`aton.text`',
    '[text.find](https://pablogila.github.io/Aton/aton/text/find.html)'                 : '`aton.text.find`',
    '[text.extract](https://pablogila.github.io/Aton/aton/text/extract.html)'           : '`aton.text.extract`',
    '[text.edit](https://pablogila.github.io/Aton/aton/text/edit.html)'                 : '`aton.text.edit`',
    '[interface](https://pablogila.github.io/Aton/aton/interface.html)'                 : '`aton.interface`',
    '[interface.qe](https://pablogila.github.io/Aton/aton/interface/qe.html)'           : '`aton.interface.qe`',
    '[interface.phonopy](https://pablogila.github.io/Aton/aton/interface/phonopy.html)' : '`aton.interface.phonopy`',
    '[interface.castep](https://pablogila.github.io/Aton/aton/interface/castep.html)'   : '`aton.interface.castep`',
    '[spectra](https://pablogila.github.io/Aton/aton/spectra.html)'                     : '`aton.spectra`',
    'Check the [full documentation online](https://pablogila.github.io/Aton/).'         : '',
}

# Get the package version as __version__
exec(open('aton/_version.py').read())
print(f'Updating docs to {__version__}...')
# Copy the pics folder
shutil.copytree('pics', 'docs/pics', dirs_exist_ok=True)
# Fix the README
aton.text.edit.from_template(readme, temp_readme, fix_dict)
# Run Pdoc with the dark theme template from the ./css/ folder
aton.call.bash(f"pdoc ./aton/ -o ./docs/ --mermaid --math --footer-text='Aton {__version__} documentation' -t ./css/")
aton.file.remove(temp_readme)

