# MINT LAB
**MINT** (**M**athematik, **I**nformatik, **N**aturwissenschaften, **T**echnik)
is the German equivalent to 
**STEM** (**S**cience, **T**echnology, **E**ngineering, **M**athematics)

This is a free to use Software to use with a Raspberry Pi. It contains a number of different Interdisciplinary Educational Experiments created by **MAKE IT MINT** to give people an easy introduction into working with a Raspberry Pi.
The Experiments featured in the **MINT LAB** are part of a wider range of Interdispciplinary Experiments created by **MAKE IT MINT** that aim to help students better understand how MINT topics are connected and should not be viewed independently.
For more detailed information you can go to our [Website](https://www.make-it-mint.de).

##Installing MINT LAB

Running on Raspberry Pi 4/400 and Linux
Tested On:
- Raspban Bullseye
- Ubuntu 20.04 & 22.04
- Python Version - 3.9.2


#### Starting MINT LAB

The `"YOUR_SYSTEM"` placeholder can be replaced by one of the following:
`linux` for Ubuntu or another Linux OS
`rpi` for Raspberry Pi
e.g. `run_mint_lab_rpi.sh`

`<PATH_TO_REPOSITORY_DIRECTORY>` should be something similar to
`/home/pi`
##### Option 1
Click the `run_mint_lab_"YOUR_SYSTEM".sh` file that matches your operating system

##### Option 2
To run from the file directly, open a Terminal, navigate to the rpository an execute the following statement, matching your operating system:
`./run_mint_lab_"YOUR_SYSTEM".sh`

##### Option 3
Creating and Using a Desktop Icon:
- Create a new Emtpy File on the Desktop
- Insert the following content:
    ```
    [Desktop Entry]
    Name=MINT LAB
    Terminal=true
    Exec=<PATH_TO_REPOSITORY_DIRECTORY>/run_mint_lab_"YOUR_SYSTEM".sh
    Type=Application
    Icon=<PATH_TO_REPOSITORY_DIRECTORY>/assets/system/logo.png
    ```

Now you can run it through this Desktop Icon


## For Developers

You are welcome to create your own Experiments! 
There is a directory called **for_developers**. Copy the template for example into the `topics/basics` directory and change the files according to the template.
A detailed guide will be created in the future.
