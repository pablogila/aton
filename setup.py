from setuptools import find_packages, setup
import re

DESCRIPTION = "Aton is an all-in-one Python package that provides powerful and comprehensive tools for cutting-edge materials research."

with open('aton/__init__.py', 'r') as f:
    content = f.read()
    version_match = re.search(r"__version__\s*=\s*'([^']+)'", content)
    if not version_match:
        raise RuntimeError("Unable to find version.")
    VERSION = version_match.group(1)

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='aton', 
    version=VERSION,
    author='Pablo Gila-Herranz',
    author_email='pgila001@ikasle.ehu.eus',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=['aton'],
    install_requires=['pandas'],
    extras_requires={
        'dev': ['pytest', 'twine']
        },
    python_requires='>=3',
    license='AGPL-3.0',
    keywords=['Aton', 'Neutron', 'Neutron research', 'Spectra', 'Inelastic Neutron Scattering', 'INS', 'Ab-initio', 'DFT', 'Density Functional Theory', 'MD', 'Molecular Dynamics', 'Quantum ESPRESSO', 'Phonopy', 'CASTEP'],
    classifiers= [
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Other OS",
    ]
)
