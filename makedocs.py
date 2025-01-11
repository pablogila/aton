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
    '[Aton](https://pablogila.github.io/Aton/)'                                         : '**Aton**',
    '[aton.st](https://pablogila.github.io/Aton/aton/st.html)'                          : '`aton.st`',
    '[st.call](https://pablogila.github.io/Aton/aton/st/call.html)'                     : '`aton.st.call`',
    '[st.file](https://pablogila.github.io/Aton/aton/st/file.html)'                     : '`aton.st.file`',
    '[st.alias](https://pablogila.github.io/Aton/aton/st/alias.html)'                   : '`aton.st.alias`',
    '[aton.phys](https://pablogila.github.io/Aton/aton/phys.html)'                      : '`aton.phys`',
    '[phys.units](https://pablogila.github.io/Aton/aton/phys/units.html)'               : '`aton.phys.units`',
    '[phys.atoms](https://pablogila.github.io/Aton/aton/phys/atoms.html)'               : '`aton.phys.atoms`',
    '[phys.functions](https://pablogila.github.io/Aton/aton/phys/functions.html)'       : '`aton.phys.functions`',
    '[aton.text](https://pablogila.github.io/Aton/aton/text.html)'                      : '`aton.text`',
    '[text.find](https://pablogila.github.io/Aton/aton/text/find.html)'                 : '`aton.text.find`',
    '[text.extract](https://pablogila.github.io/Aton/aton/text/extract.html)'           : '`aton.text.extract`',
    '[text.edit](https://pablogila.github.io/Aton/aton/text/edit.html)'                 : '`aton.text.edit`',
    '[aton.interface](https://pablogila.github.io/Aton/aton/interface.html)'            : '`aton.interface`',
    '[interface.qe](https://pablogila.github.io/Aton/aton/interface/qe.html)'           : '`aton.interface.qe`',
    '[interface.phonopy](https://pablogila.github.io/Aton/aton/interface/phonopy.html)' : '`aton.interface.phonopy`',
    '[interface.castep](https://pablogila.github.io/Aton/aton/interface/castep.html)'   : '`aton.interface.castep`',
    '[aton.spx](https://pablogila.github.io/Aton/aton/spx.html)'                        : '`aton.spx`',
    '[spx.classes](https://pablogila.github.io/Aton/aton/spx/classes.html)'             : '`aton.spx.classes`',
    '[spx.fit](https://pablogila.github.io/Aton/aton/spx/fit.html)'                     : '`aton.spx.fit`',
    '[spx.normalize](https://pablogila.github.io/Aton/aton/spx/normalize.html)'         : '`aton.spx.normalize`',
    '[spx.plot](https://pablogila.github.io/Aton/aton/spx/plot.html)'                   : '`aton.spx.plot`',
    '[spx.deuterium](https://pablogila.github.io/Aton/aton/spx/deuterium.html)'         : '`aton.spx.deuterium`',
    '[spx.samples](https://pablogila.github.io/Aton/aton/spx/samples.html)'             : '`aton.spx.samples`',
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
aton.st.call.bash(f"pdoc ./aton/ -o ./docs/ --mermaid --math --footer-text='Aton {__version__} documentation' -t ./css/")
aton.st.file.remove(temp_readme)

