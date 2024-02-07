# Blender_Image_Generator
Python scripts to save visual data (image, video) from observation poses on a hemisphere. 
Blender 4.1 (in development as of 02/07/2024) and associated Python module are required.

## Installation
The virtual environment and python module (3.11.7) to use this project can be found 
[here](https://drive.google.com/drive/folders/1my-VlOTwRzVt0p3lgpAk8mmYbXjFu5_D?usp=drive_link). 
An example Blender project which creates a blast is also provided. To use it, download the three
folders in the project folder.

Change the symbolic link of the python in the virtual environment.
```
cd $(Project_Folder_Path)/venv/bin
ln -sfn $(Project_Folder_Path)/python3.11.7/bin/python3.11 python
ln -sfn python python3
ln -sfn python python3.11
```
If you have a different path for the downloaded python module and virtual environment, then you will need to modify the virtual environment configuration file accordingly. 
To do that, go to *$(Project_Folder_Path)/venv/pyvenv.cfg* and change the paths there.

## Usage
Make sure you have Blender 4.1 built and compiled on your computer as this project requires Blender 4.1. 
For other versions of Blender, you can modify the configuration accordingly.

To run the example image generation for a sphere object, use the following command
```
python $(Project_Folder_Path)/run_script.py
```
To run the image generation for the Blender blast project, use the following command
```
/bin/bash $(Project_Folder_Path)/scripts/run_blast_script.sh
```
In *$(Project_Folder_Path)/scripts/render_blast.py*, comment in line 44-69 if you want to render a Suzanne monkey object (static) instead of the provide blast.
Camera pose can be changed by modifying line 92 (observation radius), 96 (elevation), and 97 (azimuth).
