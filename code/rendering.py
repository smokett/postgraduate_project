print("Blender Loaded")
print("Initialising Scripts... ", end="", flush=True)
import bpy
import os
import glob
import sys
import io
import numpy as np
import math
import random
from contextlib import redirect_stdout

arg_depth_col_dep_exr = "16"
arg_depth_comp_exr = 15
arg_depth_codec_exr = 'ZIP'
arg_depth_col_dep_png = "16"
arg_depth_comp_png = 15

def setDir(folder, file, extension):
    target_file = os.path.join(folder, '{}.{}'.format(file, extension))
    return target_file

def hsv_to_rgb(h, s, v):
    if s == 0.0: return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)


def get_depth(name):
    # Scene-render settings
    bpy.context.scene.render.engine = 'CYCLES' # BLENDER_EEVEE, CYCLES
    bpy.context.scene.render.use_compositing = True
    
    # Enable nodes
    bpy.context.scene.use_nodes = True
    
    path = "D:\\fyp\\pinnar\\test_depth"

    tree = bpy.context.scene.node_tree
    links = tree.links

    # Clear default nodes
    for n in tree.nodes:
        tree.nodes.remove(n)

    # Create render-layers node
    render_layer = tree.nodes.new(type='CompositorNodeRLayers')

    # Create map-range node
    map = tree.nodes.new(type='CompositorNodeMapRange')
    
    # Set map maximum to Euclidian distance of camera to origin
    cam = bpy.data.objects['Camera']
    dist_l2 = math.sqrt(cam.location.x**2 + cam.location.y**2 + cam.location.z**2)
    map.inputs[1].default_value = 0 # map minimum in Blender units
    map.inputs[2].default_value = dist_l2 # map maximum in Blender units

    # Map values between 1 (white) and zero (black)
    map.inputs[3].default_value = 1 # map minimum in normalised units (linear steps when using OPEN_EXR)
    map.inputs[4].default_value = 0 # map minimum in normalised units (linear steps when using OPEN_EXR)

    # Create a file-output node, set the path, and file format
    fileOutput = tree.nodes.new(type='CompositorNodeOutputFile')
    fileOutput.base_path = "D:\\fyp\\pinnar\\test_depth"
    fileOutput.format.file_format = "OPEN_EXR"
    fileOutput.file_slots[0].path = name + "_depth." + fileOutput.format.file_format # file name with appended frame idx
    fileOutput.format.color_depth = arg_depth_col_dep_exr
    fileOutput.format.compression = int(arg_depth_comp_exr)
    fileOutput.format.exr_codec = arg_depth_codec_exr # [‘NONE’, ‘PXR24’, ‘ZIP’, ‘PIZ’, ‘RLE’, ‘ZIPS’, ‘B44’, ‘B44A’, ‘DWAA’, ‘DWAB’], default ‘NONE’

    # Link output of render-layers node to input of map node
    links.new(render_layer.outputs['Depth'], map.inputs['Value'])

    # Link output of map node to input of compositor-output node (exr)
    links.new(map.outputs['Value'], fileOutput.inputs['Image'])

    fileOutput_png = tree.nodes.new(type='CompositorNodeOutputFile')
    fileOutput_png.base_path = "D:\\fyp\\pinnar\\test_depth"
    fileOutput_png.format.file_format = "PNG" # "OPEN_EXR", "PNG"
    fileOutput_png.file_slots[0].path = name + "_depth." + fileOutput_png.format.file_format # file name with appended frame idx
    fileOutput_png.format.color_depth = arg_depth_col_dep_png
    fileOutput_png.format.compression = int(arg_depth_comp_png)

    # Link output of map node to input of compositor-output node (png)
    links.new(map.outputs['Value'], fileOutput_png.inputs['Image'])

    # Render
    target_file = "D:\\fyp\\pinnar\\test_depth\\" + name + ".png"
    bpy.context.scene.render.filepath = target_file
    bpy.ops.render.render(write_still=True)

    # Remove previous results with same file name and extension
    if (os.path.exists(setDir(path, name + "_depth","EXR"))):
        os.remove(setDir(path, name + "_depth", "exr"))

    if (os.path.exists(setDir(path, name + "_depth", fileOutput_png.format.file_format))):
        os.remove(setDir(path, name + "_depth", fileOutput_png.format.file_format))

    # rename current files by removing automatically appended frame index
    if (os.path.exists(setDir(path, name + "_depth." + fileOutput.format.file_format 
        + "0000", "exr"))):
        os.rename(setDir(path, name + "_depth." + fileOutput.format.file_format 
            + "0000", "exr"), setDir(path, name + "_depth", "exr"))

    if (os.path.exists(setDir(path, name + "_depth." + fileOutput_png.format.file_format 
        + "0000", "png"))):
        os.rename(setDir(path, name + "_depth." + fileOutput_png.format.file_format
            + "0000",fileOutput_png.format.file_format), 
            setDir(path, name + "_depth", "png"))

    bpy.context.scene.render.use_compositing = False

f = open("bad.txt","r")

for line in f:
    file_index = int(line.strip())
    azimuth = [-10.0,-5.0,0.0,5.0,10.0]
    elevation = [-10.0,-5.0,0.0,5.0,10.0]
    bpy.context.scene.render.image_settings.color_mode = 'BW'
    bpy.context.scene.render.image_settings.color_depth = '16'
    bpy.context.scene.render.image_settings.compression = 100

    filepath = 'D:\\fyp\\pinnar\\data\\2022_07_11_13_03_06_l\\'+str(file_index)+".obj"
    bpy.ops.import_scene.obj(filepath=filepath)
    for obj in bpy.context.scene.objects[:]:
        if obj.name.startswith('ARI_PPM'):
            n = obj.name
            break
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    bpy.data.objects[obj.name].select_set(True)
    bpy.context.object.active_material_index = 1
    bpy.ops.object.material_slot_remove()

        
    bpy.data.objects[n].rotation_euler[0] = 0.0
    bpy.data.objects[n].scale[0] = 1000.0
    bpy.data.objects[n].scale[1] = 1000.0
    bpy.data.objects[n].scale[2] = 1000.0
    bpy.data.objects[n].location[0] = 5.0
        
    obj.material_slots[0].material = bpy.data.materials['S']

    H = np.clip(np.random.normal(0.05, 0.0167, 1)[0], 0.0, 0.1)
    S = np.clip(np.random.normal(0.5, 0.1, 1)[0], 0.2, 0.8)
    V = np.clip(np.random.normal(0.5, 0.33, 1)[0], 0.0, 1.0)
    RGB = hsv_to_rgb(H,S,V)
    bpy.data.materials['S'].node_tree.nodes["Group.001"].inputs[1].default_value[0] = RGB[0]
    bpy.data.materials['S'].node_tree.nodes["Group.001"].inputs[1].default_value[1] = RGB[1]
    bpy.data.materials['S'].node_tree.nodes["Group.001"].inputs[1].default_value[2] = RGB[2]
    bpy.data.materials['S'].node_tree.nodes["Group.001"].inputs[1].default_value[3] = 1.0

    index = 0

    bpy.data.objects['Camera'].location[1] = 200.0
    bpy.data.objects['Camera'].rotation_euler[2] = math.radians(180.0)

    for e in elevation:
        for a in azimuth:
            bpy.data.objects[n].rotation_euler[0] = math.radians(e)
            bpy.data.objects[n].rotation_euler[2] = math.radians(a)
            get_depth(str(file_index)+'_L_'+str(index))
            index += 1

    index = 0

    bpy.data.objects['Camera'].location[1] = -200.0
    bpy.data.objects['Camera'].rotation_euler[2] = math.radians(0.0)

    for e in elevation:
        for a in azimuth:
            bpy.data.objects[n].rotation_euler[0] = math.radians(e)
            bpy.data.objects[n].rotation_euler[2] = math.radians(a)
            get_depth(str(file_index)+'_R_'+str(index))
            index += 1
    file_index += 1
    
    for obj in bpy.context.scene.objects[:]:
        if obj.name.startswith('ARI_PPM'):
            n = obj.name
            break
        
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    bpy.data.objects[obj.name].select_set(True)
    bpy.ops.object.delete()

f.close()

