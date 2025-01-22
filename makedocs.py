"""
This script is used to update the documentation automatically.
Requires pdoc, install it with `pip install pdoc`.
It also requires ATON itself; installation instructions can be found in the README.md file.
Run this script as `python3 makedocs.py`.
"""

import shutil
import aton

readme = './README.md'
temp_readme = './_README_temp.md'
# Update links from the README
fix_dict ={
    '[ATON](https://pablogila.github.io/ATON/)'                                         : '**ATON**',
    '[aton.st](https://pablogila.github.io/ATON/aton/st.html)'                          : '`aton.st`',
    '[st.call](https://pablogila.github.io/ATON/aton/st/call.html)'                     : '`aton.st.call`',
    '[st.file](https://pablogila.github.io/ATON/aton/st/file.html)'                     : '`aton.st.file`',
    '[st.alias](https://pablogila.github.io/ATON/aton/st/alias.html)'                   : '`aton.st.alias`',
    '[aton.phys](https://pablogila.github.io/ATON/aton/phys.html)'                      : '`aton.phys`',
    '[phys.units](https://pablogila.github.io/ATON/aton/phys/units.html)'               : '`aton.phys.units`',
    '[phys.atoms](https://pablogila.github.io/ATON/aton/phys/atoms.html)'               : '`aton.phys.atoms`',
    '[phys.functions](https://pablogila.github.io/ATON/aton/phys/functions.html)'       : '`aton.phys.functions`',
    '[aton.txt](https://pablogila.github.io/ATON/aton/txt.html)'                        : '`aton.txt`',
    '[txt.find](https://pablogila.github.io/ATON/aton/txt/find.html)'                   : '`aton.txt.find`',
    '[txt.extract](https://pablogila.github.io/ATON/aton/txt/extract.html)'             : '`aton.txt.extract`',
    '[txt.edit](https://pablogila.github.io/ATON/aton/txt/edit.html)'                   : '`aton.txt.edit`',
    '[aton.interface](https://pablogila.github.io/ATON/aton/interface.html)'            : '`aton.interface`',
    '[interface.qe](https://pablogila.github.io/ATON/aton/interface/qe.html)'           : '`aton.interface.qe`',
    '[interface.phonopy](https://pablogila.github.io/ATON/aton/interface/phonopy.html)' : '`aton.interface.phonopy`',
    '[interface.castep](https://pablogila.github.io/ATON/aton/interface/castep.html)'   : '`aton.interface.castep`',
    '[interface.slurm](https://pablogila.github.io/ATON/aton/interface/slurm.html)'     : '`aton.interface.slurm`',
    '[aton.spx](https://pablogila.github.io/ATON/aton/spx.html)'                        : '`aton.spx`',
    '[spx.classes](https://pablogila.github.io/ATON/aton/spx/classes.html)'             : '`aton.spx.classes`',
    '[spx.fit](https://pablogila.github.io/ATON/aton/spx/fit.html)'                     : '`aton.spx.fit`',
    '[spx.normalize](https://pablogila.github.io/ATON/aton/spx/normalize.html)'         : '`aton.spx.normalize`',
    '[spx.plot](https://pablogila.github.io/ATON/aton/spx/plot.html)'                   : '`aton.spx.plot`',
    '[spx.deuterium](https://pablogila.github.io/ATON/aton/spx/deuterium.html)'         : '`aton.spx.deuterium`',
    '[spx.samples](https://pablogila.github.io/ATON/aton/spx/samples.html)'             : '`aton.spx.samples`',
    '[aton.qrotor](https://pablogila.github.io/ATON/aton/qrotor.html)'                  : '`aton.qrotor`',
    '[qrotor.classes](https://pablogila.github.io/ATON/aton/qrotor/classes.html)'       : '`aton.qrotor.classes`',
    '[qrotor.constants](https://pablogila.github.io/ATON/aton/qrotor/constants.html)'   : '`aton.qrotor.constants`',
    '[qrotor.rotate](https://pablogila.github.io/ATON/aton/qrotor/rotate.html)'         : '`aton.qrotor.rotate`',
    '[qrotor.potential](https://pablogila.github.io/ATON/aton/qrotor/potential.html)'   : '`aton.qrotor.potential`',
    '[qrotor.solve](https://pablogila.github.io/ATON/aton/qrotor/solve.html)'           : '`aton.qrotor.solve`',
    '[qrotor.plot](https://pablogila.github.io/ATON/aton/qrotor/plot.html)'             : '`aton.qrotor.plot`',
    'Check the [full documentation online](https://pablogila.github.io/ATON/).'         : '',
}

# Get the package version as __version__
exec(open('aton/_version.py').read())
print(f'Updating docs to {__version__}...')
# Copy the pics folder
shutil.copytree('pics', 'docs/pics', dirs_exist_ok=True)
# Fix the README
aton.txt.edit.from_template(readme, temp_readme, fix_dict)
# Run Pdoc with the dark theme template from the ./css/ folder
aton.st.call.bash(f"pdoc ./aton/ -o ./docs/ --mermaid --math --footer-text='ATON {__version__} documentation' -t ./css/")
aton.st.file.remove(temp_readme)

