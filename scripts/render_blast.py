import sys

import bpy
import math
import numpy as np
from math import sin, cos, pi
import mathutils

import os

sys.path.insert(0, '/home/jzhang72/PycharmProjects/blasts_w_blender')
from scripts.simple_sphere import rainbow_lights

# Check if script is executed in Blender and get absolute path of current folder
if bpy.context.space_data is not None:
    filesDir = os.path.dirname(bpy.context.space_data.text.filepath)
else:
    filesDir = os.path.dirname(os.path.abspath(__file__))

# Remove all elements
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

# Set cursor to (0, 0, 0)
bpy.context.scene.cursor.location = (0, 0, 0)

# Create camera object
bpy.ops.object.add(type='CAMERA', location=(0, 0, 0))
camera = bpy.context.object
camera.data.lens = 35
camera.rotation_euler = mathutils.Euler((pi / 2, 0, 0), 'XYZ')

# Make this the current camera
bpy.context.scene.camera = camera

'''Blast'''
blend_file_path = filesDir + '/' + '../projects/blast_final.blend'

# Load the .blend file
bpy.ops.wm.open_mainfile(filepath=blend_file_path)
''''''

'''Built-in object'''
# bpy.ops.mesh.primitive_monkey_add(
#     size=2.0, calc_uvs=True, enter_editmode=False, align='WORLD',
#     location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0),
#     scale=(0.0, 0.0, 0.0))
# obj = bpy.context.object
#
# # Add subsurf modifier
# modifier = obj.modifiers.new('Subsurf', 'SUBSURF')
# modifier.levels = 2
# modifier.render_levels = 2
#
# # Smooth surface
# for p in obj.data.polygons:
#     p.use_smooth = True
#
# # Add Glossy BSDF material
# mat = bpy.data.materials.new('Material')
# mat.use_nodes = True
# node = mat.node_tree.nodes[0]
# node.inputs[0].default_value = (0.8, 0.8, 0.8, 1)  # Base color
# node.inputs[4].default_value = 0.5  # Metalic
# node.inputs[7].default_value = 0.5  # Roughness
# obj.data.materials.append(mat)
#
# # Create lamps
# rainbow_lights(5, 100, 2, energy=100)
''''''

bpy.context.scene.render.resolution_x = 640
bpy.context.scene.render.resolution_y = 480
bpy.context.scene.render.resolution_percentage = 100

# Render settings
bpy.context.scene.render.engine = 'CYCLES'

# Set the device_type
bpy.context.preferences.addons[
    "cycles"
].preferences.compute_device_type = "CUDA"  # or "OPENCL"
bpy.context.scene.cycles.device = 'GPU'
bpy.context.preferences.addons["cycles"].preferences.get_devices()
print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)

for d in bpy.context.preferences.addons["cycles"].preferences.devices:
    d["use"] = 1  # Using all devices, include GPU and CPU
    print(d["name"], d["use"])

# set camera locations
radius = 2.0
camera_locations = {
    0: (1.0, -radius, 1.0),
    1: (0, -radius, 1.0)
}

focus_point = mathutils.Vector((0.0, 0.0, 0.0))  # set to the 3D position of the object
frames = range(12, 20)  # frames = range(bpy.context.scene.frame_start, bpy.context.scene.frame_end)
for el in range(0, 91, 45):  # (0, 91, 45)
    for az in range(0, 360, 45):  # (0, 360, 45)
        el_rad = el / 180.0 * np.pi
        az_rad = az / 180.0 * np.pi
        z = radius * sin(el_rad)
        x = radius * cos(el_rad) * cos(az_rad)
        y = radius * cos(el_rad) * sin(az_rad)
        bpy.context.scene.camera.location = (x, -y, z)
        # Option 1:
        bpy.context.scene.camera.rotation_euler = mathutils.Euler((math.radians(90 - el), math.radians(0), math.radians(90 - az)), 'XYZ')
        # print('euler angles = ({}, {}, {})'.format(90-el, 0, 90-az))
        # Option 2 (doesn't work well, will align the camera up in a strange way when camera is point down):
        # looking_direction = focus_point - bpy.context.scene.camera.location
        # Q = looking_direction.to_track_quat('-Z', 'Y')
        # bpy.context.scene.camera.rotation_euler = Q.to_euler()

        for frame in frames:
            # Set the current frame or a specific frame to the start of the animation
            bpy.context.scene.frame_set(frame)

            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.context.scene.render.filepath = (filesDir + '/' + '../outputs/blast/' + "r_{}_az_{}_el_{}".format(radius, az, el)
                                                 + "/frame_" + str(frame).zfill(4) + '.png')

            # set animation to True for saving the entire animation, otherwise it will only save the specified frame
            bpy.ops.render.render(animation=False, write_still=True)

print("Done")
