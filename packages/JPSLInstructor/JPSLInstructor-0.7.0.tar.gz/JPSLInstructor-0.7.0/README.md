## JPSLInstructor
(aka Jupyter Physical Science Lab Instructor package)

This package installs all of the packages in the 
[Jupyter Physical Science lab suite](https://github.com/JupyterPhysSciLab), 
their dependencies and the [Algebra_with_SymPy](https://github.com/gutow/Algebra_with_Sympy)
package into the current python environment. The packages can then be used 
in a Jupyter notebook to construct assignments. See the overall 
documentation and the descriptions of each package for more details.

If you have an example notebook to upload you can try it on binder:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JupyterPhysSciLab/JPSLInstructor.git/HEAD?urlpath=/tree/)

#### Installation
1. Install python3+ on your system, if you have not. See 
   [python.org](https://python.org) for instructions.
1. Install a tool for managing and using virtual environments. This 
   allows you to have multiple independent sets (virtual environments)
   of python packages installed. I recommend you use this so
   that you can have both an "instructor" and "student" environment for
   testing. I personally like using
   [pipenv](https://pipenv.pypa.io/en/latest/). You can install it using
   the command `$ pip3 --user install pipenv`. See the website for more
   information.
1. Once you have the correct python and a virtual environment system,
   create a directory for your "Instructor" environment. Navigate into
   the directory. Then:
   * Create the empty virtual environment `$ pipenv shell`. This will
    create the environment, activate it and leave you inside it.
   * Still within the environment use pip to install this package
    `$ pip install JPSLInstructor`. This will take a while to run. There
     are a lot of packages to download and install.
1. To exit the virtual environment just type "exit" on the command line
   `$ exit`.
1. To enter the virtual environment: first make sure you are in the proper 
   directory; then issue the command `$ pipenv shell`.
1. To update you must be in the virtual environment. Use 
   `$ pip install -U JPSLInstructor`.