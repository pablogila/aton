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
    '[ATON](https://pablogila.github.io/aton/)'                                         : '**ATON**',
    '[aton.call](https://pablogila.github.io/aton/aton/call.html)'                      : '`aton.call`',
    '[aton.file](https://pablogila.github.io/aton/aton/file.html)'                      : '`aton.file`',
    '[aton.alias](https://pablogila.github.io/aton/aton/alias.html)'                    : '`aton.alias`',
    '[aton.phys](https://pablogila.github.io/aton/aton/phys.html)'                      : '`aton.phys`',
    '[phys.units](https://pablogila.github.io/aton/aton/phys/units.html)'               : '`aton.phys.units`',
    '[phys.atoms](https://pablogila.github.io/aton/aton/phys/atoms.html)'               : '`aton.phys.atoms`',
    '[phys.isotope](https://pablogila.github.io/aton/aton/phys/isotope.html)'           : '`aton.phys.isotope`',
    '[phys.export_atoms](https://pablogila.github.io/aton/aton/phys/export_atoms.html)' : '`aton.phys.export_atoms`',
    '[aton.txt](https://pablogila.github.io/aton/aton/txt.html)'                        : '`aton.txt`',
    '[txt.find](https://pablogila.github.io/aton/aton/txt/find.html)'                   : '`aton.txt.find`',
    '[txt.extract](https://pablogila.github.io/aton/aton/txt/extract.html)'             : '`aton.txt.extract`',
    '[txt.edit](https://pablogila.github.io/aton/aton/txt/edit.html)'                   : '`aton.txt.edit`',
    '[aton.api](https://pablogila.github.io/aton/aton/api.html)'                        : '`aton.api`',
    '[api.qe](https://pablogila.github.io/aton/aton/api/qe.html)'                       : '`aton.api.qe`',
    '[api.phonopy](https://pablogila.github.io/aton/aton/api/phonopy.html)'             : '`aton.api.phonopy`',
    '[api.castep](https://pablogila.github.io/aton/aton/api/castep.html)'               : '`aton.api.castep`',
    '[api.slurm](https://pablogila.github.io/aton/aton/api/slurm.html)'                 : '`aton.api.slurm`',
    'Check the [full documentation online](https://pablogila.github.io/aton/).'         : '',
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

