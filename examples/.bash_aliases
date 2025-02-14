# This file can be placed in your Linux HOME folder
# to use custom terminal commands with ATON

# Your $HOME/.bashrc file must contain the following lines,
# add them uncommented if not present already:
#if [ -f ~/.bash_aliases ]; then
#    . ~/.bash_aliases
#fi

# Create a python virtual environment with:
# python3 -m venv venv
# And add the path to this environment below.
# (Default is $HOME/venv)
if [ -d "$HOME/venv" ] ; then
    alias venv='source $HOME/venv/bin/activate'
fi

# Try to activate your environment running 'venv' in your terminal.
# Remember to do so in a new terminal so that everything is loaded properly.
# Install or upgrade ATON in your environment with:
# pip install aton -U
# Now, to open the ATON command line interface, you just have to type 'aton'
alias aton='venv && python3 -i -c "import aton; import aton.qrotor as qr; from aton import interface; from aton import txt; from aton import spx; from aton import st; import numpy as np; import pandas as pd; import scipy; import matplotlib.pyplot as plt; import math; print(aton.version)"'

