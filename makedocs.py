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
    '[aton.call](https://pablogila.github.io/ATON/aton/call.html)'                      : '`aton.call`',
    '[aton.file](https://pablogila.github.io/ATON/aton/file.html)'                      : '`aton.file`',
    '[aton.alias](https://pablogila.github.io/ATON/aton/alias.html)'                    : '`aton.alias`',
    '[aton.phys](https://pablogila.github.io/ATON/aton/phys.html)'                      : '`aton.phys`',
    '[phys.units](https://pablogila.github.io/ATON/aton/phys/units.html)'               : '`aton.phys.units`',
    '[phys.atoms](https://pablogila.github.io/ATON/aton/phys/atoms.html)'               : '`aton.phys.atoms`',
    '[phys.functions](https://pablogila.github.io/ATON/aton/phys/functions.html)'       : '`aton.phys.functions`',
    '[aton.txt](https://pablogila.github.io/ATON/aton/txt.html)'                        : '`aton.txt`',
    '[txt.find](https://pablogila.github.io/ATON/aton/txt/find.html)'                   : '`aton.txt.find`',
    '[txt.extract](https://pablogila.github.io/ATON/aton/txt/extract.html)'             : '`aton.txt.extract`',
    '[txt.edit](https://pablogila.github.io/ATON/aton/txt/edit.html)'                   : '`aton.txt.edit`',
    '[aton.api](https://pablogila.github.io/ATON/aton/api.html)'            : '`aton.api`',
    '[api.qe](https://pablogila.github.io/ATON/aton/api/qe.html)'           : '`aton.api.qe`',
    '[api.phonopy](https://pablogila.github.io/ATON/aton/api/phonopy.html)' : '`aton.api.phonopy`',
    '[api.castep](https://pablogila.github.io/ATON/aton/api/castep.html)'   : '`aton.api.castep`',
    '[api.slurm](https://pablogila.github.io/ATON/aton/api/slurm.html)'     : '`aton.api.slurm`',
    '[aton.spx](https://pablogila.github.io/ATON/aton/spx.html)'                        : '`aton.spx`',
    '[spx.classes](https://pablogila.github.io/ATON/aton/spx/classes.html)'             : '`aton.spx.classes`',
    '[spx.fit](https://pablogila.github.io/ATON/aton/spx/fit.html)'                     : '`aton.spx.fit`',
    '[spx.normalize](https://pablogila.github.io/ATON/aton/spx/normalize.html)'         : '`aton.spx.normalize`',
    '[spx.plot](https://pablogila.github.io/ATON/aton/spx/plot.html)'                   : '`aton.spx.plot`',
    '[spx.deuterium](https://pablogila.github.io/ATON/aton/spx/deuterium.html)'         : '`aton.spx.deuterium`',
    '[spx.samples](https://pablogila.github.io/ATON/aton/spx/samples.html)'             : '`aton.spx.samples`',
    '[aton.qrotor](https://pablogila.github.io/ATON/aton/qrotor.html)'                  : '`aton.qrotor`',
    '[qrotor.system](https://pablogila.github.io/ATON/aton/qrotor/system.html)'         : '`aton.qrotor.system`',
    '[qrotor.systems](https://pablogila.github.io/ATON/aton/qrotor/systems.html)'       : '`aton.qrotor.systems`',
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
aton.call.bash(f"pdoc ./aton/ -o ./docs/ --mermaid --math --footer-text='ATON {__version__} documentation' -t ./css/")
aton.file.remove(temp_readme)
# Include google search verification
search_verification_tag = '    <meta name="google-site-verification" content="u0Be1NUH4ztGm5rr5f_YFt6hqoqMJ-j9h7rk3wEJAUo" />'
aton.txt.edit.insert_under('docs/aton.html', '<head>', search_verification_tag)

