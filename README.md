# MINT LAB
**MINT** (**M**athematik, **I**nformatik, **N**aturwissenschaften, **T**echnik)
is the German equivalent to 
**STEM** (**S**cience, **T**echnology, **E**ngineering, **M**athematics)

This is a free to use Software to use with a Raspberry Pi. It contains a number of different Interdisciplinary Educational Experiments created by **MAKE IT MINT** to give people an easy introduction into working with a Raspberry Pi.
The Experiments featured in the **MINT LAB** are part of a wider range of Interdispciplinary Experiments created by **MAKE IT MINT** that aim to help students better understand how MINT Subjects are connected and should not be viewed independently.
For more detailed information you can go to our [Website](https://www.make-it-mint.de). !!!WEBSITE STILL UNDER CONSTRUCTION!!!

##Installing MINT LAB

Running on Raspberry Pi 4/400
Tested On:
- OS Version - Bullseye
- Python Version - 3.9.2

#### Cloning the Repository
Clone the Repository by opening a Terminal on your Raspberry Pi an input the following:
`git clone https://github.com/make-it-mint/mint-lab.git <INSTALLATION_DIRECTORY>`

e.g.: `git clone https://github.com/make-it-mint/mint-lab.git /home/pi/mint-lab`

This clones the repository to your Pi and creates a new directory at `/home/pi/` called `mint-lab` where the repository will be placed. Of course you can choose another place for the repository.

#### Installing required packages
MINT LAB uses PyQt5 which has to be installed manually once.
PyQt5 is a library to create User Interfaces.
It is installed by opening a Terminal and the inputting
`sudo apt-get install python3-pyqt5`

Since the version of the Python library `numpy` that s used here is higher than the one currently provided by Raspbian, it is necessary to install another package for linear algebra calculations
`sudo apt-get install libatlas-base-dev` 

#### Starting MINT LAB
There are multiple options to run Mint LAB after downloading the Repository.
The `main.py` can be run directly, but it will not check if all requirements are met. The `run_mint_lab.sh` script will do this and automatically download required Python Libraries.

Here are two options on how to start MINT LAB

If the instructions above were followed, the `<PATH_TO_REPOSITORY_DIRECTORY>` for the following steps can be substituted by `/home/pi`

To run from the file directly, open a Terminal an input the following command:
`bash <PATH_TO_REPOSITORY_DIRECTORY>/run_mint_lab.sh`

or

Creating and Using a Desktop Icon:
- Create a new Emtpy File on the Desktop
- Insert the following content:
    ```
    [Desktop Entry]
    Name=MINT LAB
    Terminal=true
    Exec=<PATH_TO_REPOSITORY_DIRECTORY>/run_mint_lab.sh
    Type=Application
    Icon=<PATH_TO_REPOSITORY_DIRECTORY>/assets/system/logo.png
    ```

Now you can run it through this Desktop Icon


## For Developers

You are welcome to create your own Experiments! A guide will be created in the future.

For development purposes `run_mint_lab.sh` creates a virtual environment. The current version is tailored for Linux systems.
Except for the `run_mint_lab.sh` file in `main` branch, which is Raspbian specific.

You can also run the `main.py` file directly using Python.