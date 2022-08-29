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

stdout = io.StringIO()

argv = sys.argv

arg_path = argv[argv.index("--") + 1]
arg_mesh = argv[argv.index("--") + 2]
arg_remesh = argv[argv.index("--") + 3]
arg_image = argv[argv.index("--") + 4]
arg_res = argv[argv.index("--") + 5]

def select(label, action):
    if action:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[label].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[label]
    else:
        bpy.data.objects[label].select_set(False)
        bpy.ops.object.select_all(action='DESELECT')
        
def setDir(folder, file, extension):

        target_file = os.path.join(folder, '{}.{}'.format(file, extension))
        return target_file

class Bone():
        
    def __init__(self, name, ear):

        self.name = name
        ear.bones.append(self)
        ear.bonesLookup[self.name] = self
        
        

    def rotate(self, point, axis, val):
        
        if axis == 'W':
            axis_idx = 0
        elif axis == 'X':
            axis_idx = 1
        elif axis == 'Y':
            axis_idx = 2
        elif axis == 'Z':
            axis_idx = 3
        else:
            axis_idx = "error"
        bpy.data.objects["Armature"].pose.bones[self.name + "_" + point].rotation_quaternion[axis_idx] = float(val)
        
    def translate(self, point, axis, val):
                
        if axis == 'X':
            axis_idx = 0
        elif axis == 'Y':
            axis_idx = 1
        elif axis == 'Z':
            axis_idx = 2
        else:
            axis_idx = "error"

        bpy.data.objects["Armature"].pose.bones[self.name + "_" + point].location[axis_idx] = float(val)

class Ear():
    
    def __init__(self, name):
        
        self.name = name
        self.path = str(arg_path)
        self.bones = []
        self.bonesLookup = {}
        
    def modifiers(self, state):
        if arg_remesh == 'TRUE':
            bpy.data.objects["ARI_PPM_v1"].modifiers["DataTransfer"].show_render = state
            bpy.data.objects["ARI_PPM_v1"].modifiers["DataTransfer"].show_viewport = state
            bpy.data.objects["ARI_PPM_v1"].modifiers["DataTransfer"].show_in_editmode = state
            bpy.data.objects["ARI_PPM_v1"].modifiers["DataTransfer"].show_on_cage = state
            bpy.data.objects["ARI_PPM_v1"].modifiers["Decimate"].show_render = state
            bpy.data.objects["ARI_PPM_v1"].modifiers["Decimate"].show_viewport = state
    
    def scale(self):
        for name in self.bendy_bone_names:
            val = np.clip(np.random.normal(0.0, 0.1, 1)[0], -0.3, 0.3)
            for axis_idx in range(0,3):
                bpy.data.objects["Armature"].pose.bones[name].scale[axis_idx] += val
        
    def shapeKey(self, name, val):
        
        bpy.data.shape_keys["Key.002"].key_blocks[name].value = float(val)


    def export(self, name):
    
        target_file = setDir(self.path, name, "obj")
        select('ARI_PPM_v1', True)
        with redirect_stdout(stdout):
            bpy.ops.export_scene.obj(filepath=target_file, use_selection=True, use_materials=True)
        select('ARI_PPM_v1', False)
        
    def hsv_to_rgb(self, h, s, v):
        if s == 0.0: return (v, v, v)
        i = int(h*6.) # XXX assume int() truncates!
        f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)

    def render(self, name):
        #camera_translation = np.clip(np.random.normal(0.0, 1.0, 1)[0], -3.0, 3.0)
        #bpy.data.objects['Camera'].location[0] += camera_translation
        #camera_translation = np.clip(np.random.normal(0.0, 1.0, 1)[0], -3.0, 3.0)
        #bpy.data.objects['Camera'].location[1] += camera_translation
        #camera_translation = np.clip(np.random.normal(0.0, 1.0, 1)[0], -3.0, 3.0)
        #bpy.data.objects['Camera'].location[2] += camera_translation
        #camera_rotation = math.radians(np.clip(np.random.normal(0.0, 1.0, 1)[0], -3.0, 3.0))
        #bpy.data.objects['Camera'].rotation_euler[0] += camera_rotation
        #camera_rotation = math.radians(np.clip(np.random.normal(0.0, 1.0, 1)[0], -3.0, 3.0))
        #bpy.data.objects['Camera'].rotation_euler[1] += camera_rotation
        #camera_rotation = math.radians(np.clip(np.random.normal(0.0, 1.0, 1)[0], -3.0, 3.0))
        #bpy.data.objects['Camera'].rotation_euler[2] += camera_rotation
        
        H = np.clip(np.random.normal(0.05, 0.0167, 1)[0], 0.0, 0.1)
        S = np.clip(np.random.normal(0.5, 0.1, 1)[0], 0.2, 0.8)
        V = np.clip(np.random.normal(0.5, 0.33, 1)[0], 0.0, 1.0)
        RGB = self.hsv_to_rgb(H,S,V)
        bpy.data.materials['S'].node_tree.nodes["Group.001"].inputs[1].default_value[0] = RGB[0]
        bpy.data.materials['S'].node_tree.nodes["Group.001"].inputs[1].default_value[1] = RGB[1]
        bpy.data.materials['S'].node_tree.nodes["Group.001"].inputs[1].default_value[2] = RGB[2]
        bpy.data.materials['S'].node_tree.nodes["Group.001"].inputs[1].default_value[3] = 1.0
        
        
        bpy.data.scenes["Scene"].render.resolution_x = int(arg_res)
        bpy.data.scenes["Scene"].render.resolution_y = int(arg_res)
        
        target_file = setDir(self.path, name, "png")
        bpy.context.scene.render.filepath = target_file
        bpy.ops.render.render(write_still = True)
  
    def reset(self, name):
        
        target_file = setDir(self.path, name, "txt")
        file = open(target_file, 'r')
        lines = file.readlines()
        lines.reverse()
        
        for line in lines:
            transform = line.split(',')[0]

            if transform == "R":          
                self.bonesLookup[line.split(',')[1].split('-')[0]].rotate(line.split(',')[1].split('-')[1], line.split(',')[2], 0)
            elif transform == "T":
                self.bonesLookup[line.split(',')[1].split('-')[0]].translate(line.split(',')[1].split('-')[1], line.split(',')[2], 0)
            elif transform == "K":
                self.shapeKey(line.split(',')[1], 0) 
            else:
                print("Reset: skipped line")
                pass
          
    def load(self, name):
        
        target_file = setDir(self.path, name, "txt")
        file = open(target_file, 'r')
        lines = file.readlines()
        for line in lines:
            
            transform = line.split(',')[0]
            
            if transform == "R":          
                self.bonesLookup[line.split(',')[1].split('-')[0]].rotate(line.split(',')[1].split('-')[1], line.split(',')[2], line.split(',')[3])
            elif transform == "T":
                self.bonesLookup[line.split(',')[1].split('-')[0]].translate(line.split(',')[1].split('-')[1], line.split(',')[2], line.split(',')[3])
            elif transform == "K":
                self.shapeKey(line.split(',')[1], line.split(',')[3]) 
            else:
                print("Reset: skipped line")
                pass
        
            
    def loadAll(self):
        self.bendy_bone_names = ["Lobulo_Start", "Lobulo_End", "Helix_low_Start", "Helix_low_End", "Helix_middle_Start", "Helix_middle_End", "Helix_up_Start", "Helix_up_End", "Tragus_Start", "Tragus_End", "Antitragus_Start", "Antitragus_End", "Antihelix_Start", "Antihelix_End", "Crus_Inferius_Anthelicis_Start", "Crus_Inferius_Anthelicis_End", "Crus_Superius_Anthelicis_Start", "Crus_Superius_Anthelicis_End"]
        self.shape_key_names = ["Antitragus inside crease", "Cavum Concha Depth", "Cymba Concha Depth", "Crus Helicis Prominence", "Upper Helix Depth", "Middle Helix Depth", "Lower Helix Depth", "Lobulo Attachment", "Scapha Depth", "Fossa Triangularis Depth", "Crus Inferius Anthelicis lower crease", "Crus Inferius Anthelicis upper crease", "Crus Superius Anthelicis lower crease", "Crus Superius Anthelicis upper crease", "Tragus Upper Dent", "Crus Helicis upper dent", "Crus Helicis lower dent", "Ear canal diameter"]
        self.bendy_bone_scale_names = ['Lobulo_Bendy','Helix_low_Bendy','Helix_middle_Bendy','Helix_up_Bendy','Tragus_Bendy','Antitragus_Bendy','Antihelix_Bendy','Crus_Inferius_Anthelicis_Bendy','Crus_Superius_Anthelicis_Bendy']
        self.axis_t = ['X', 'Y', 'Z']
        self.axis_r = ['W', 'X', 'Y' ,'Z']
        
        self.original_shape_keys_values = {}
        for skn in self.shape_key_names:
            self.original_shape_keys_values[skn] = bpy.data.shape_keys["Key.002"].key_blocks[skn].value
        
        
        
        
        self.bendy_bone_translate_values = {}
        self.bendy_bone_rotate_values = {}
        self.bendy_bone_scale_values = {}
        self.bendy_bone_translate_values_r = {}
        self.bendy_bone_rotate_values_r = {}
        self.bendy_bone_scale_values_r = {}
        for bbn in self.bendy_bone_names:
            self.bendy_bone_translate_values[bbn] = {}
            self.bendy_bone_translate_values[bbn]["X"] = [0.0]*2
            self.bendy_bone_translate_values[bbn]["Y"] = [0.0]*2
            self.bendy_bone_translate_values[bbn]["Z"] = [0.0]*2
            self.bendy_bone_rotate_values[bbn] = {}
            self.bendy_bone_rotate_values[bbn]["W"] = [1.0]*2
            self.bendy_bone_rotate_values[bbn]["X"] = [0.0]*2
            self.bendy_bone_rotate_values[bbn]["Y"] = [0.0]*2
            self.bendy_bone_rotate_values[bbn]["Z"] = [0.0]*2
            self.bendy_bone_scale_values[bbn] = 1.0
            self.bendy_bone_translate_values_r[bbn] = {}
            self.bendy_bone_translate_values_r[bbn]["X"] = [0.0]*2
            self.bendy_bone_translate_values_r[bbn]["Y"] = [0.0]*2
            self.bendy_bone_translate_values_r[bbn]["Z"] = [0.0]*2
            self.bendy_bone_rotate_values_r[bbn] = {}
            self.bendy_bone_rotate_values_r[bbn]["W"] = [1.0]*2
            self.bendy_bone_rotate_values_r[bbn]["X"] = [0.0]*2
            self.bendy_bone_rotate_values_r[bbn]["Y"] = [0.0]*2
            self.bendy_bone_rotate_values_r[bbn]["Z"] = [0.0]*2
            self.bendy_bone_scale_values_r[bbn] = 1.0
            
        self.shape_key_values = {}
        self.shape_key_values_r = {}
        for skn in self.shape_key_names:
            self.shape_key_values[skn] = [bpy.data.shape_keys["Key.002"].key_blocks[skn].value,bpy.data.shape_keys["Key.002"].key_blocks[skn].value]
            self.shape_key_values_r[skn] = [bpy.data.shape_keys["Key.002"].key_blocks[skn].value,bpy.data.shape_keys["Key.002"].key_blocks[skn].value]
        
        
        self.bendy_bone_translate_values['Lobulo_Start']['X'] = [-1.2423,1.0809]
        self.bendy_bone_translate_values['Lobulo_Start']['Y'] = [-0.7318,1.6893]
        self.bendy_bone_translate_values['Lobulo_Start']['Z'] = [0.3389,1.8973]
        self.bendy_bone_rotate_values['Lobulo_Start']['W'] = [0.9763,0.0473]
        self.bendy_bone_rotate_values['Lobulo_Start']['X'] = [0.0241,0.1435]
        self.bendy_bone_rotate_values['Lobulo_Start']['Y'] = [0.0164,0.1325]
        self.bendy_bone_rotate_values['Lobulo_Start']['Z'] = [0.0157,0.0924]
        
        self.bendy_bone_translate_values['Lobulo_End']['X'] = [-0.9800,1.4209]
        self.bendy_bone_translate_values['Lobulo_End']['Y'] = [0.1269,1.0466]
        self.bendy_bone_translate_values['Lobulo_End']['Z'] = [-0.1247,1.0025]
        self.bendy_bone_rotate_values['Lobulo_End']['W'] = [0.9960,0.0085]
        self.bendy_bone_rotate_values['Lobulo_End']['X'] = [-0.0085,0.0557]
        self.bendy_bone_rotate_values['Lobulo_End']['Y'] = [-0.0042,0.0292]
        self.bendy_bone_rotate_values['Lobulo_End']['Z'] = [-0.0192,0.0630]
        
        self.bendy_bone_translate_values['Helix_low_Start']['X'] = [-0.4013,1.0896]
        self.bendy_bone_translate_values['Helix_low_Start']['Y'] = [0.2291,1.0015]
        self.bendy_bone_translate_values['Helix_low_Start']['Z'] = [-0.4267,0.8884]
        self.bendy_bone_rotate_values['Helix_low_Start']['W'] = [0.9964,0.0081]
        self.bendy_bone_rotate_values['Helix_low_Start']['X'] = [-0.0063,0.0245]
        self.bendy_bone_rotate_values['Helix_low_Start']['Y'] = [0.0254,0.0602]
        self.bendy_bone_rotate_values['Helix_low_Start']['Z'] = [0.0171,0.0480]
        
        self.bendy_bone_translate_values['Helix_low_End']['X'] = [0.4265,0.9114]
        self.bendy_bone_translate_values['Helix_low_End']['Y'] = [0.4223,1.1215]
        self.bendy_bone_translate_values['Helix_low_End']['Z'] = [-0.6337,0.9977]
        self.bendy_bone_rotate_values['Helix_low_End']['W'] = [0.9939,0.0137]
        self.bendy_bone_rotate_values['Helix_low_End']['X'] = [-0.0007,0.0395]
        self.bendy_bone_rotate_values['Helix_low_End']['Y'] = [0.0130,0.0312]
        self.bendy_bone_rotate_values['Helix_low_End']['Z'] = [-0.0362,0.0925]
        
        self.bendy_bone_translate_values['Helix_middle_Start']['X'] = [0.6806,0.8833]
        self.bendy_bone_translate_values['Helix_middle_Start']['Y'] = [0.4046,0.9029]
        self.bendy_bone_translate_values['Helix_middle_Start']['Z'] = [-0.3757,0.8971]
        self.bendy_bone_rotate_values['Helix_middle_Start']['W'] = [0.9940,0.0115]
        self.bendy_bone_rotate_values['Helix_middle_Start']['X'] = [0.0044,0.0093]
        self.bendy_bone_rotate_values['Helix_middle_Start']['Y'] = [0.0159,0.0409]
        self.bendy_bone_rotate_values['Helix_middle_Start']['Z'] = [-0.0443,0.0919]
        
        self.bendy_bone_translate_values['Helix_middle_End']['X'] = [0.3823,0.8477]
        self.bendy_bone_translate_values['Helix_middle_End']['Y'] = [0.1159,1.0605]
        self.bendy_bone_translate_values['Helix_middle_End']['Z'] = [1.3038,1.0485]
        self.bendy_bone_rotate_values['Helix_middle_End']['W'] = [0.9979,0.0049]
        self.bendy_bone_rotate_values['Helix_middle_End']['X'] = [-0.0067,0.0355]
        self.bendy_bone_rotate_values['Helix_middle_End']['Y'] = [0.0047,0.0324]
        self.bendy_bone_rotate_values['Helix_middle_End']['Z'] = [0.0154,0.0404]
        
        self.bendy_bone_translate_values['Helix_up_Start']['X'] = [0.4491,0.6676]
        self.bendy_bone_translate_values['Helix_up_Start']['Y'] = [0.1750,0.6997]
        self.bendy_bone_translate_values['Helix_up_Start']['Z'] = [0.9194,0.9426]
        self.bendy_bone_rotate_values['Helix_up_Start']['W'] = [0.9730,0.0971]
        self.bendy_bone_rotate_values['Helix_up_Start']['X'] = [0.0333,0.0887]
        self.bendy_bone_rotate_values['Helix_up_Start']['Y'] = [0.0533,0.1873]
        self.bendy_bone_rotate_values['Helix_up_Start']['Z'] = [-0.0064,0.0184]
        
        self.bendy_bone_translate_values['Helix_up_End']['X'] = [0.1064,0.5297]
        self.bendy_bone_translate_values['Helix_up_End']['Y'] = [0.1837,0.8550]
        self.bendy_bone_translate_values['Helix_up_End']['Z'] = [0.2367,0.8882]
        self.bendy_bone_rotate_values['Helix_up_End']['W'] = [0.9992,0.0022]
        self.bendy_bone_rotate_values['Helix_up_End']['X'] = [-0.0048,0.0351]
        self.bendy_bone_rotate_values['Helix_up_End']['Y'] = [-0.0064,0.0175]
        self.bendy_bone_rotate_values['Helix_up_End']['Z'] = [-0.0019,0.0052]
        
        self.bendy_bone_translate_values['Tragus_Start']['X'] = [0.0529,1.0343]
        self.bendy_bone_translate_values['Tragus_Start']['Y'] = [-1.1829,1.2812]
        self.bendy_bone_translate_values['Tragus_Start']['Z'] = [0.4275,0.9874]
        self.bendy_bone_rotate_values['Tragus_Start']['W'] = [0.9872,0.0346]
        self.bendy_bone_rotate_values['Tragus_Start']['X'] = [0.0087,0.1158]
        self.bendy_bone_rotate_values['Tragus_Start']['Y'] = [-0.0055,0.0765]
        self.bendy_bone_rotate_values['Tragus_Start']['Z'] = [0.0152,0.0786]
        
        self.bendy_bone_translate_values['Tragus_End']['X'] = [0.0377,0.7606]
        self.bendy_bone_translate_values['Tragus_End']['Y'] = [0.2836,1.5361]
        self.bendy_bone_translate_values['Tragus_End']['Z'] = [0.4472,0.7468]
        self.bendy_bone_rotate_values['Tragus_End']['W'] = [0.9773,0.0778]
        self.bendy_bone_rotate_values['Tragus_End']['X'] = [0.0269,0.1770]
        self.bendy_bone_rotate_values['Tragus_End']['Y'] = [0.0016,0.0465]
        self.bendy_bone_rotate_values['Tragus_End']['Z'] = [-0.0248,0.0832]
        
        self.bendy_bone_translate_values['Antitragus_Start']['X'] = [-0.1493,0.5318]
        self.bendy_bone_translate_values['Antitragus_Start']['Y'] = [0.1728,0.9953]
        self.bendy_bone_translate_values['Antitragus_Start']['Z'] = [-0.2904,0.7304]
        self.bendy_bone_rotate_values['Antitragus_Start']['W'] = [0.9719,0.0598]
        self.bendy_bone_rotate_values['Antitragus_Start']['X'] = [-0.0941,0.1963]
        self.bendy_bone_rotate_values['Antitragus_Start']['Y'] = [-0.0033,0.0628]
        self.bendy_bone_rotate_values['Antitragus_Start']['Z'] = [-0.0012,0.0609]
        
        self.bendy_bone_translate_values['Antitragus_End']['X'] = [-0.2312,0.5447]
        self.bendy_bone_translate_values['Antitragus_End']['Y'] = [0.1388,0.9335]
        self.bendy_bone_translate_values['Antitragus_End']['Z'] = [-0.5844,0.6058]
        self.bendy_bone_rotate_values['Antitragus_End']['W'] = [0.9681,0.0740]
        self.bendy_bone_rotate_values['Antitragus_End']['X'] = [0.0470,0.1993]
        self.bendy_bone_rotate_values['Antitragus_End']['Y'] = [-0.0153,0.0610]
        self.bendy_bone_rotate_values['Antitragus_End']['Z'] = [-0.0379,0.1183]
        
        self.bendy_bone_translate_values['Antihelix_Start']['X'] = [-0.2367,1.0071]
        self.bendy_bone_translate_values['Antihelix_Start']['Y'] = [-0.1188,1.1425]
        self.bendy_bone_translate_values['Antihelix_Start']['Z'] = [-0.6758,0.5983]
        self.bendy_bone_rotate_values['Antihelix_Start']['W'] = [0.9931,0.0161]
        self.bendy_bone_rotate_values['Antihelix_Start']['X'] = [-0.0130,0.1110]
        self.bendy_bone_rotate_values['Antihelix_Start']['Y'] = [-0.0097,0.0422]
        self.bendy_bone_rotate_values['Antihelix_Start']['Z'] = [-0.0002,0.0008]
        
        self.bendy_bone_translate_values['Antihelix_End']['X'] = [-0.0384,0.7625]
        self.bendy_bone_translate_values['Antihelix_End']['Y'] = [0.3530,0.5225]
        self.bendy_bone_translate_values['Antihelix_End']['Z'] = [-0.4241,0.7102]
        self.bendy_bone_rotate_values['Antihelix_End']['W'] = [0.9903,0.0233]
        self.bendy_bone_rotate_values['Antihelix_End']['X'] = [0.0290,0.1085]
        self.bendy_bone_rotate_values['Antihelix_End']['Y'] = [0.0112,0.0336]
        self.bendy_bone_rotate_values['Antihelix_End']['Z'] = [-0.0312,0.0712]
        
        self.bendy_bone_translate_values['Crus_Inferius_Anthelicis_Start']['X'] = [0.0387,0.5821]
        self.bendy_bone_translate_values['Crus_Inferius_Anthelicis_Start']['Y'] = [0.3415,0.7798]
        self.bendy_bone_translate_values['Crus_Inferius_Anthelicis_Start']['Z'] = [0.0240,0.9202]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_Start']['W'] = [0.9719,0.1032]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_Start']['X'] = [-0.0053,0.0341]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_Start']['Y'] = [0.0362,0.1171]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_Start']['Z'] = [0.0460,0.1733]
        
        self.bendy_bone_translate_values['Crus_Inferius_Anthelicis_End']['X'] = [0.1737,0.8253]
        self.bendy_bone_translate_values['Crus_Inferius_Anthelicis_End']['Y'] = [-0.0754,1.0781]
        self.bendy_bone_translate_values['Crus_Inferius_Anthelicis_End']['Z'] = [0.2698,0.9613]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_End']['W'] = [0.9388,0.1445]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_End']['X'] = [0.1258,0.2527]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_End']['Y'] = [-0.0400,0.1321]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_End']['Z'] = [-0.0179,0.0760]
        
        self.bendy_bone_translate_values['Crus_Superius_Anthelicis_Start']['X'] = [-0.1536,0.6328]
        self.bendy_bone_translate_values['Crus_Superius_Anthelicis_Start']['Y'] = [0.3908,0.6331]
        self.bendy_bone_translate_values['Crus_Superius_Anthelicis_Start']['Z'] = [-0.5878,0.6121]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_Start']['W'] = [0.9944,0.0151]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_Start']['X'] = [-0.0033,0.0392]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_Start']['Y'] = [0.0030,0.0288]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_Start']['Z'] = [-0.0078,0.0953]
        
        self.bendy_bone_translate_values['Crus_Superius_Anthelicis_End']['X'] = [0.4884,0.5171]
        self.bendy_bone_translate_values['Crus_Superius_Anthelicis_End']['Y'] = [0.3039,0.3964]
        self.bendy_bone_translate_values['Crus_Superius_Anthelicis_End']['Z'] = [-0.5013,0.8171]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_End']['W'] = [0.9823,0.0454]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_End']['X'] = [0.0002,0.0763]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_End']['Y'] = [-0.0047,0.0437]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_End']['Z'] = [0.0084,0.1658]
        
        self.shape_key_values['Antitragus inside crease'] = [0.2122,0.5000]
        self.shape_key_values['Cavum Concha Depth'] = [-0.1575,0.3198]
        self.shape_key_values['Cymba Concha Depth'] = [0.2871,0.3435]
        self.shape_key_values['Crus Helicis Prominence'] = [0.0627,0.7069]
        self.shape_key_values['Upper Helix Depth'] = [0.6867,0.3936]
        self.shape_key_values['Middle Helix Depth'] = [0.7287,0.2999]
        self.shape_key_values['Lower Helix Depth'] = [0.4887,0.4370]
        self.shape_key_values['Lobulo Attachment'] = [0.5152,0.4013]
        self.shape_key_values['Scapha Depth'] = [0.4585,0.3311]
        self.shape_key_values['Fossa Triangularis Depth'] = [-0.1884,0.4453]
        self.shape_key_values['Crus Inferius Anthelicis lower crease'] = [0.2925,0.2763]
        self.shape_key_values['Crus Inferius Anthelicis upper crease'] = [0.0556,0.0719]
        self.shape_key_values['Crus Superius Anthelicis lower crease'] = [0.0943,0.1710]
        self.shape_key_values['Crus Superius Anthelicis upper crease'] = [0.2001,0.2386]
        self.shape_key_values['Tragus Upper Dent'] = [-0.1582,0.4597]
        self.shape_key_values['Crus Helicis upper dent'] = [0.0746,0.1289]
        self.shape_key_values['Crus Helicis lower dent'] = [0.0815,0.2077]
        self.shape_key_values['Ear canal diameter'] = [0.1807,0.4307]
        
        self.bendy_bone_scale_values['Lobulo_Bendy'] = [0.9300,0.2772]
        self.bendy_bone_scale_values['Helix_low_Bendy'] = [0.9857,0.3402]
        self.bendy_bone_scale_values['Helix_middle_Bendy'] = [0.9149,0.2320]
        self.bendy_bone_scale_values['Helix_up_Bendy'] = [1.0646,0.4903]
        self.bendy_bone_scale_values['Tragus_Bendy'] = [0.9898,0.4251]
        self.bendy_bone_scale_values['Antitragus_Bendy'] = [1.0277,0.1703]
        self.bendy_bone_scale_values['Antihelix_Bendy'] = [0.8060,0.3611]
        self.bendy_bone_scale_values['Crus_Inferius_Anthelicis_Bendy'] = [0.9628,0.3345]
        self.bendy_bone_scale_values['Crus_Superius_Anthelicis_Bendy'] = [0.9437,0.3378]
        
        
        #-----------------------------------------------------------------------------------
        
        
        
        self.bendy_bone_translate_values['Lobulo_Start']['X'] = [0.0,1.0809]
        self.bendy_bone_translate_values['Lobulo_Start']['Y'] = [0.0,1.6893]
        self.bendy_bone_translate_values['Lobulo_Start']['Z'] = [0.0,1.8973]
        self.bendy_bone_rotate_values['Lobulo_Start']['W'] = [1.0,0.0473]
        self.bendy_bone_rotate_values['Lobulo_Start']['X'] = [0.0,0.1435]
        self.bendy_bone_rotate_values['Lobulo_Start']['Y'] = [0.0,0.1325]
        self.bendy_bone_rotate_values['Lobulo_Start']['Z'] = [0.0,0.0924]
        
        self.bendy_bone_translate_values['Lobulo_End']['X'] = [0.0,1.4209]
        self.bendy_bone_translate_values['Lobulo_End']['Y'] = [0.0,1.0466]
        self.bendy_bone_translate_values['Lobulo_End']['Z'] = [0.0,1.0025]
        self.bendy_bone_rotate_values['Lobulo_End']['W'] = [1.0,0.0085]
        self.bendy_bone_rotate_values['Lobulo_End']['X'] = [0.0,0.0557]
        self.bendy_bone_rotate_values['Lobulo_End']['Y'] = [0.0,0.0292]
        self.bendy_bone_rotate_values['Lobulo_End']['Z'] = [0.0,0.0630]
        
        self.bendy_bone_translate_values['Helix_low_Start']['X'] = [0.0,1.0896]
        self.bendy_bone_translate_values['Helix_low_Start']['Y'] = [0.0,1.0015]
        self.bendy_bone_translate_values['Helix_low_Start']['Z'] = [0.0,0.8884]
        self.bendy_bone_rotate_values['Helix_low_Start']['W'] = [1.0,0.0081]
        self.bendy_bone_rotate_values['Helix_low_Start']['X'] = [0.0,0.0245]
        self.bendy_bone_rotate_values['Helix_low_Start']['Y'] = [0.0,0.0602]
        self.bendy_bone_rotate_values['Helix_low_Start']['Z'] = [0.0,0.0480]
        
        self.bendy_bone_translate_values['Helix_low_End']['X'] = [0.0,0.9114]
        self.bendy_bone_translate_values['Helix_low_End']['Y'] = [0.0,1.1215]
        self.bendy_bone_translate_values['Helix_low_End']['Z'] = [0.0,0.9977]
        self.bendy_bone_rotate_values['Helix_low_End']['W'] = [1.0,0.0137]
        self.bendy_bone_rotate_values['Helix_low_End']['X'] = [0.0,0.0395]
        self.bendy_bone_rotate_values['Helix_low_End']['Y'] = [0.0,0.0312]
        self.bendy_bone_rotate_values['Helix_low_End']['Z'] = [0.0,0.0925]
        
        self.bendy_bone_translate_values['Helix_middle_Start']['X'] = [0.0,0.8833]
        self.bendy_bone_translate_values['Helix_middle_Start']['Y'] = [0.0,0.9029]
        self.bendy_bone_translate_values['Helix_middle_Start']['Z'] = [0.0,0.8971]
        self.bendy_bone_rotate_values['Helix_middle_Start']['W'] = [1.0,0.0115]
        self.bendy_bone_rotate_values['Helix_middle_Start']['X'] = [0.0,0.0093]
        self.bendy_bone_rotate_values['Helix_middle_Start']['Y'] = [0.0,0.0409]
        self.bendy_bone_rotate_values['Helix_middle_Start']['Z'] = [0.0,0.0919]
        
        self.bendy_bone_translate_values['Helix_middle_End']['X'] = [0.0,0.8477]
        self.bendy_bone_translate_values['Helix_middle_End']['Y'] = [0.0,1.0605]
        self.bendy_bone_translate_values['Helix_middle_End']['Z'] = [0.0,1.0485]
        self.bendy_bone_rotate_values['Helix_middle_End']['W'] = [1.0,0.0049]
        self.bendy_bone_rotate_values['Helix_middle_End']['X'] = [0.0,0.0355]
        self.bendy_bone_rotate_values['Helix_middle_End']['Y'] = [0.0,0.0324]
        self.bendy_bone_rotate_values['Helix_middle_End']['Z'] = [0.0,0.0404]
        
        self.bendy_bone_translate_values['Helix_up_Start']['X'] = [0.0,0.6676]
        self.bendy_bone_translate_values['Helix_up_Start']['Y'] = [0.0,0.6997]
        self.bendy_bone_translate_values['Helix_up_Start']['Z'] = [0.0,0.9426]
        self.bendy_bone_rotate_values['Helix_up_Start']['W'] = [1.0,0.0971]
        self.bendy_bone_rotate_values['Helix_up_Start']['X'] = [0.0,0.0887]
        self.bendy_bone_rotate_values['Helix_up_Start']['Y'] = [0.0,0.1873]
        self.bendy_bone_rotate_values['Helix_up_Start']['Z'] = [0.0,0.0184]
        
        self.bendy_bone_translate_values['Helix_up_End']['X'] = [0.0,0.5297]
        self.bendy_bone_translate_values['Helix_up_End']['Y'] = [0.0,0.8550]
        self.bendy_bone_translate_values['Helix_up_End']['Z'] = [0.0,0.8882]
        self.bendy_bone_rotate_values['Helix_up_End']['W'] = [1.0,0.0022]
        self.bendy_bone_rotate_values['Helix_up_End']['X'] = [0.0,0.0351]
        self.bendy_bone_rotate_values['Helix_up_End']['Y'] = [0.0,0.0175]
        self.bendy_bone_rotate_values['Helix_up_End']['Z'] = [0.0,0.0052]
        
        self.bendy_bone_translate_values['Tragus_Start']['X'] = [0.0,1.0343]
        self.bendy_bone_translate_values['Tragus_Start']['Y'] = [0.0,1.2812]
        self.bendy_bone_translate_values['Tragus_Start']['Z'] = [0.0,0.9874]
        self.bendy_bone_rotate_values['Tragus_Start']['W'] = [1.0,0.0346]
        self.bendy_bone_rotate_values['Tragus_Start']['X'] = [0.0,0.1158]
        self.bendy_bone_rotate_values['Tragus_Start']['Y'] = [0.0,0.0765]
        self.bendy_bone_rotate_values['Tragus_Start']['Z'] = [0.0,0.0786]
        
        self.bendy_bone_translate_values['Tragus_End']['X'] = [0.0,0.7606]
        self.bendy_bone_translate_values['Tragus_End']['Y'] = [0.0,1.5361]
        self.bendy_bone_translate_values['Tragus_End']['Z'] = [0.0,0.7468]
        self.bendy_bone_rotate_values['Tragus_End']['W'] = [1.0,0.0778]
        self.bendy_bone_rotate_values['Tragus_End']['X'] = [0.0,0.1770]
        self.bendy_bone_rotate_values['Tragus_End']['Y'] = [0.0,0.0465]
        self.bendy_bone_rotate_values['Tragus_End']['Z'] = [0.0,0.0832]
        
        self.bendy_bone_translate_values['Antitragus_Start']['X'] = [0.0,0.5318]
        self.bendy_bone_translate_values['Antitragus_Start']['Y'] = [0.0,0.9953]
        self.bendy_bone_translate_values['Antitragus_Start']['Z'] = [0.0,0.7304]
        self.bendy_bone_rotate_values['Antitragus_Start']['W'] = [1.0,0.0598]
        self.bendy_bone_rotate_values['Antitragus_Start']['X'] = [0.0,0.1963]
        self.bendy_bone_rotate_values['Antitragus_Start']['Y'] = [0.0,0.0628]
        self.bendy_bone_rotate_values['Antitragus_Start']['Z'] = [0.0,0.0609]
        
        self.bendy_bone_translate_values['Antitragus_End']['X'] = [0.0,0.5447]
        self.bendy_bone_translate_values['Antitragus_End']['Y'] = [0.0,0.9335]
        self.bendy_bone_translate_values['Antitragus_End']['Z'] = [0.0,0.6058]
        self.bendy_bone_rotate_values['Antitragus_End']['W'] = [1.0,0.0740]
        self.bendy_bone_rotate_values['Antitragus_End']['X'] = [0.0,0.1993]
        self.bendy_bone_rotate_values['Antitragus_End']['Y'] = [0.0,0.0610]
        self.bendy_bone_rotate_values['Antitragus_End']['Z'] = [0.0,0.1183]
        
        self.bendy_bone_translate_values['Antihelix_Start']['X'] = [0.0,1.0071]
        self.bendy_bone_translate_values['Antihelix_Start']['Y'] = [0.0,1.1425]
        self.bendy_bone_translate_values['Antihelix_Start']['Z'] = [0.0,0.5983]
        self.bendy_bone_rotate_values['Antihelix_Start']['W'] = [1.0,0.0161]
        self.bendy_bone_rotate_values['Antihelix_Start']['X'] = [0.0,0.1110]
        self.bendy_bone_rotate_values['Antihelix_Start']['Y'] = [0.0,0.0422]
        self.bendy_bone_rotate_values['Antihelix_Start']['Z'] = [0.0,0.0008]
        
        self.bendy_bone_translate_values['Antihelix_End']['X'] = [0.0,0.7625]
        self.bendy_bone_translate_values['Antihelix_End']['Y'] = [0.0,0.5225]
        self.bendy_bone_translate_values['Antihelix_End']['Z'] = [0.0,0.7102]
        self.bendy_bone_rotate_values['Antihelix_End']['W'] = [1.0,0.0233]
        self.bendy_bone_rotate_values['Antihelix_End']['X'] = [0.0,0.1085]
        self.bendy_bone_rotate_values['Antihelix_End']['Y'] = [0.0,0.0336]
        self.bendy_bone_rotate_values['Antihelix_End']['Z'] = [0.0,0.0712]
        
        self.bendy_bone_translate_values['Crus_Inferius_Anthelicis_Start']['X'] = [0.0,0.5821]
        self.bendy_bone_translate_values['Crus_Inferius_Anthelicis_Start']['Y'] = [0.0,0.7798]
        self.bendy_bone_translate_values['Crus_Inferius_Anthelicis_Start']['Z'] = [0.0,0.9202]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_Start']['W'] = [1.0,0.1032]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_Start']['X'] = [0.0,0.0341]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_Start']['Y'] = [0.0,0.1171]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_Start']['Z'] = [0.0,0.1733]
        
        self.bendy_bone_translate_values['Crus_Inferius_Anthelicis_End']['X'] = [0.0,0.8253]
        self.bendy_bone_translate_values['Crus_Inferius_Anthelicis_End']['Y'] = [0.0,1.0781]
        self.bendy_bone_translate_values['Crus_Inferius_Anthelicis_End']['Z'] = [0.0,0.9613]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_End']['W'] = [1.0,0.1445]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_End']['X'] = [0.0,0.2527]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_End']['Y'] = [0.0,0.1321]
        self.bendy_bone_rotate_values['Crus_Inferius_Anthelicis_End']['Z'] = [0.0,0.0760]
        
        self.bendy_bone_translate_values['Crus_Superius_Anthelicis_Start']['X'] = [0.0,0.6328]
        self.bendy_bone_translate_values['Crus_Superius_Anthelicis_Start']['Y'] = [0.0,0.6331]
        self.bendy_bone_translate_values['Crus_Superius_Anthelicis_Start']['Z'] = [0.0,0.6121]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_Start']['W'] = [1.0,0.0151]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_Start']['X'] = [0.0,0.0392]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_Start']['Y'] = [0.0,0.0288]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_Start']['Z'] = [0.0,0.0953]
        
        self.bendy_bone_translate_values['Crus_Superius_Anthelicis_End']['X'] = [0.0,0.5171]
        self.bendy_bone_translate_values['Crus_Superius_Anthelicis_End']['Y'] = [0.0,0.3964]
        self.bendy_bone_translate_values['Crus_Superius_Anthelicis_End']['Z'] = [0.0,0.8171]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_End']['W'] = [1.0,0.0454]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_End']['X'] = [0.0,0.0763]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_End']['Y'] = [0.0,0.0437]
        self.bendy_bone_rotate_values['Crus_Superius_Anthelicis_End']['Z'] = [0.0,0.1658]
        
        self.shape_key_values['Antitragus inside crease'] = [0.2122,0.5000]
        self.shape_key_values['Cavum Concha Depth'] = [-0.1575,0.3198]
        self.shape_key_values['Cymba Concha Depth'] = [0.2871,0.3435]
        self.shape_key_values['Crus Helicis Prominence'] = [0.0627,0.7069]
        self.shape_key_values['Upper Helix Depth'] = [0.6867,0.3936]
        self.shape_key_values['Middle Helix Depth'] = [0.7287,0.2999]
        self.shape_key_values['Lower Helix Depth'] = [0.4887,0.4370]
        self.shape_key_values['Lobulo Attachment'] = [0.5152,0.4013]
        self.shape_key_values['Scapha Depth'] = [0.4585,0.3311]
        self.shape_key_values['Fossa Triangularis Depth'] = [-0.1884,0.4453]
        self.shape_key_values['Crus Inferius Anthelicis lower crease'] = [0.2925,0.2763]
        self.shape_key_values['Crus Inferius Anthelicis upper crease'] = [0.0556,0.0719]
        self.shape_key_values['Crus Superius Anthelicis lower crease'] = [0.0943,0.1710]
        self.shape_key_values['Crus Superius Anthelicis upper crease'] = [0.2001,0.2386]
        self.shape_key_values['Tragus Upper Dent'] = [-0.1582,0.4597]
        self.shape_key_values['Crus Helicis upper dent'] = [0.0746,0.1289]
        self.shape_key_values['Crus Helicis lower dent'] = [0.0815,0.2077]
        self.shape_key_values['Ear canal diameter'] = [0.1807,0.4307]
        
        self.bendy_bone_scale_values['Lobulo_Bendy'] = [1.0,0.2772]
        self.bendy_bone_scale_values['Helix_low_Bendy'] = [1.0,0.3402]
        self.bendy_bone_scale_values['Helix_middle_Bendy'] = [1.0,0.2320]
        self.bendy_bone_scale_values['Helix_up_Bendy'] = [1.0,0.4903]
        self.bendy_bone_scale_values['Tragus_Bendy'] = [1.0,0.4251]
        self.bendy_bone_scale_values['Antitragus_Bendy'] = [1.0,0.1703]
        self.bendy_bone_scale_values['Antihelix_Bendy'] = [1.0,0.3611]
        self.bendy_bone_scale_values['Crus_Inferius_Anthelicis_Bendy'] = [1.0,0.3345]
        self.bendy_bone_scale_values['Crus_Superius_Anthelicis_Bendy'] = [1.0,0.3378]
        
        #-------------------------------------------------------------------------
        
        self.bendy_bone_translate_values_r['Lobulo_Start']['X'] = [0.0,1.0809]
        self.bendy_bone_translate_values_r['Lobulo_Start']['Y'] = [0.0,1.6893]
        self.bendy_bone_translate_values_r['Lobulo_Start']['Z'] = [0.0,1.8973]
        self.bendy_bone_rotate_values_r['Lobulo_Start']['W'] = [1.0,0.0473]
        self.bendy_bone_rotate_values_r['Lobulo_Start']['X'] = [0.0,0.1435]
        self.bendy_bone_rotate_values_r['Lobulo_Start']['Y'] = [0.0,0.1325]
        self.bendy_bone_rotate_values_r['Lobulo_Start']['Z'] = [0.0,0.0924]
        
        self.bendy_bone_translate_values_r['Lobulo_End']['X'] = [0.0,1.4209]
        self.bendy_bone_translate_values_r['Lobulo_End']['Y'] = [0.0,1.0466]
        self.bendy_bone_translate_values_r['Lobulo_End']['Z'] = [0.0,1.0025]
        self.bendy_bone_rotate_values_r['Lobulo_End']['W'] = [1.0,0.0085]
        self.bendy_bone_rotate_values_r['Lobulo_End']['X'] = [0.0,0.0557]
        self.bendy_bone_rotate_values_r['Lobulo_End']['Y'] = [0.0,0.0292]
        self.bendy_bone_rotate_values_r['Lobulo_End']['Z'] = [0.0,0.0630]
        
        self.bendy_bone_translate_values_r['Helix_low_Start']['X'] = [0.0,1.0896]
        self.bendy_bone_translate_values_r['Helix_low_Start']['Y'] = [0.0,1.0015]
        self.bendy_bone_translate_values_r['Helix_low_Start']['Z'] = [0.0,0.8884]
        self.bendy_bone_rotate_values_r['Helix_low_Start']['W'] = [1.0,0.0081]
        self.bendy_bone_rotate_values_r['Helix_low_Start']['X'] = [0.0,0.0245]
        self.bendy_bone_rotate_values_r['Helix_low_Start']['Y'] = [0.0,0.0602]
        self.bendy_bone_rotate_values_r['Helix_low_Start']['Z'] = [0.0,0.0480]
        
        self.bendy_bone_translate_values_r['Helix_low_End']['X'] = [0.0,0.9114]
        self.bendy_bone_translate_values_r['Helix_low_End']['Y'] = [0.0,1.1215]
        self.bendy_bone_translate_values_r['Helix_low_End']['Z'] = [0.0,0.9977]
        self.bendy_bone_rotate_values_r['Helix_low_End']['W'] = [1.0,0.0137]
        self.bendy_bone_rotate_values_r['Helix_low_End']['X'] = [0.0,0.0395]
        self.bendy_bone_rotate_values_r['Helix_low_End']['Y'] = [0.0,0.0312]
        self.bendy_bone_rotate_values_r['Helix_low_End']['Z'] = [0.0,0.0925]
        
        self.bendy_bone_translate_values_r['Helix_middle_Start']['X'] = [0.0,0.8833]
        self.bendy_bone_translate_values_r['Helix_middle_Start']['Y'] = [0.0,0.9029]
        self.bendy_bone_translate_values_r['Helix_middle_Start']['Z'] = [0.0,0.8971]
        self.bendy_bone_rotate_values_r['Helix_middle_Start']['W'] = [1.0,0.0115]
        self.bendy_bone_rotate_values_r['Helix_middle_Start']['X'] = [0.0,0.0093]
        self.bendy_bone_rotate_values_r['Helix_middle_Start']['Y'] = [0.0,0.0409]
        self.bendy_bone_rotate_values_r['Helix_middle_Start']['Z'] = [0.0,0.0919]
        
        self.bendy_bone_translate_values_r['Helix_middle_End']['X'] = [0.0,0.8477]
        self.bendy_bone_translate_values_r['Helix_middle_End']['Y'] = [0.0,1.0605]
        self.bendy_bone_translate_values_r['Helix_middle_End']['Z'] = [0.0,1.0485]
        self.bendy_bone_rotate_values_r['Helix_middle_End']['W'] = [1.0,0.0049]
        self.bendy_bone_rotate_values_r['Helix_middle_End']['X'] = [0.0,0.0355]
        self.bendy_bone_rotate_values_r['Helix_middle_End']['Y'] = [0.0,0.0324]
        self.bendy_bone_rotate_values_r['Helix_middle_End']['Z'] = [0.0,0.0404]
        
        self.bendy_bone_translate_values_r['Helix_up_Start']['X'] = [0.0,0.6676]
        self.bendy_bone_translate_values_r['Helix_up_Start']['Y'] = [0.0,0.6997]
        self.bendy_bone_translate_values_r['Helix_up_Start']['Z'] = [0.0,0.9426]
        self.bendy_bone_rotate_values_r['Helix_up_Start']['W'] = [1.0,0.0971]
        self.bendy_bone_rotate_values_r['Helix_up_Start']['X'] = [0.0,0.0887]
        self.bendy_bone_rotate_values_r['Helix_up_Start']['Y'] = [0.0,0.1873]
        self.bendy_bone_rotate_values_r['Helix_up_Start']['Z'] = [0.0,0.0184]
        
        self.bendy_bone_translate_values_r['Helix_up_End']['X'] = [0.0,0.5297]
        self.bendy_bone_translate_values_r['Helix_up_End']['Y'] = [0.0,0.8550]
        self.bendy_bone_translate_values_r['Helix_up_End']['Z'] = [0.0,0.8882]
        self.bendy_bone_rotate_values_r['Helix_up_End']['W'] = [1.0,0.0022]
        self.bendy_bone_rotate_values_r['Helix_up_End']['X'] = [0.0,0.0351]
        self.bendy_bone_rotate_values_r['Helix_up_End']['Y'] = [0.0,0.0175]
        self.bendy_bone_rotate_values_r['Helix_up_End']['Z'] = [0.0,0.0052]
        
        self.bendy_bone_translate_values_r['Tragus_Start']['X'] = [0.0,1.0343]
        self.bendy_bone_translate_values_r['Tragus_Start']['Y'] = [0.0,1.2812]
        self.bendy_bone_translate_values_r['Tragus_Start']['Z'] = [0.0,0.9874]
        self.bendy_bone_rotate_values_r['Tragus_Start']['W'] = [1.0,0.0346]
        self.bendy_bone_rotate_values_r['Tragus_Start']['X'] = [0.0,0.1158]
        self.bendy_bone_rotate_values_r['Tragus_Start']['Y'] = [0.0,0.0765]
        self.bendy_bone_rotate_values_r['Tragus_Start']['Z'] = [0.0,0.0786]
        
        self.bendy_bone_translate_values_r['Tragus_End']['X'] = [0.0,0.7606]
        self.bendy_bone_translate_values_r['Tragus_End']['Y'] = [0.0,1.5361]
        self.bendy_bone_translate_values_r['Tragus_End']['Z'] = [0.0,0.7468]
        self.bendy_bone_rotate_values_r['Tragus_End']['W'] = [1.0,0.0778]
        self.bendy_bone_rotate_values_r['Tragus_End']['X'] = [0.0,0.1770]
        self.bendy_bone_rotate_values_r['Tragus_End']['Y'] = [0.0,0.0465]
        self.bendy_bone_rotate_values_r['Tragus_End']['Z'] = [0.0,0.0832]
        
        self.bendy_bone_translate_values_r['Antitragus_Start']['X'] = [0.0,0.5318]
        self.bendy_bone_translate_values_r['Antitragus_Start']['Y'] = [0.0,0.9953]
        self.bendy_bone_translate_values_r['Antitragus_Start']['Z'] = [0.0,0.7304]
        self.bendy_bone_rotate_values_r['Antitragus_Start']['W'] = [1.0,0.0598]
        self.bendy_bone_rotate_values_r['Antitragus_Start']['X'] = [0.0,0.1963]
        self.bendy_bone_rotate_values_r['Antitragus_Start']['Y'] = [0.0,0.0628]
        self.bendy_bone_rotate_values_r['Antitragus_Start']['Z'] = [0.0,0.0609]
        
        self.bendy_bone_translate_values_r['Antitragus_End']['X'] = [0.0,0.5447]
        self.bendy_bone_translate_values_r['Antitragus_End']['Y'] = [0.0,0.9335]
        self.bendy_bone_translate_values_r['Antitragus_End']['Z'] = [0.0,0.6058]
        self.bendy_bone_rotate_values_r['Antitragus_End']['W'] = [1.0,0.0740]
        self.bendy_bone_rotate_values_r['Antitragus_End']['X'] = [0.0,0.1993]
        self.bendy_bone_rotate_values_r['Antitragus_End']['Y'] = [0.0,0.0610]
        self.bendy_bone_rotate_values_r['Antitragus_End']['Z'] = [0.0,0.1183]
        
        self.bendy_bone_translate_values_r['Antihelix_Start']['X'] = [0.0,1.0071]
        self.bendy_bone_translate_values_r['Antihelix_Start']['Y'] = [0.0,1.1425]
        self.bendy_bone_translate_values_r['Antihelix_Start']['Z'] = [0.0,0.5983]
        self.bendy_bone_rotate_values_r['Antihelix_Start']['W'] = [1.0,0.0161]
        self.bendy_bone_rotate_values_r['Antihelix_Start']['X'] = [0.0,0.1110]
        self.bendy_bone_rotate_values_r['Antihelix_Start']['Y'] = [0.0,0.0422]
        self.bendy_bone_rotate_values_r['Antihelix_Start']['Z'] = [0.0,0.0008]
        
        self.bendy_bone_translate_values_r['Antihelix_End']['X'] = [0.0,0.7625]
        self.bendy_bone_translate_values_r['Antihelix_End']['Y'] = [0.0,0.5225]
        self.bendy_bone_translate_values_r['Antihelix_End']['Z'] = [0.0,0.7102]
        self.bendy_bone_rotate_values_r['Antihelix_End']['W'] = [1.0,0.0233]
        self.bendy_bone_rotate_values_r['Antihelix_End']['X'] = [0.0,0.1085]
        self.bendy_bone_rotate_values_r['Antihelix_End']['Y'] = [0.0,0.0336]
        self.bendy_bone_rotate_values_r['Antihelix_End']['Z'] = [0.0,0.0712]
        
        self.bendy_bone_translate_values_r['Crus_Inferius_Anthelicis_Start']['X'] = [0.0,0.5821]
        self.bendy_bone_translate_values_r['Crus_Inferius_Anthelicis_Start']['Y'] = [0.0,0.7798]
        self.bendy_bone_translate_values_r['Crus_Inferius_Anthelicis_Start']['Z'] = [0.0,0.9202]
        self.bendy_bone_rotate_values_r['Crus_Inferius_Anthelicis_Start']['W'] = [1.0,0.1032]
        self.bendy_bone_rotate_values_r['Crus_Inferius_Anthelicis_Start']['X'] = [0.0,0.0341]
        self.bendy_bone_rotate_values_r['Crus_Inferius_Anthelicis_Start']['Y'] = [0.0,0.1171]
        self.bendy_bone_rotate_values_r['Crus_Inferius_Anthelicis_Start']['Z'] = [0.0,0.1733]
        
        self.bendy_bone_translate_values_r['Crus_Inferius_Anthelicis_End']['X'] = [0.0,0.8253]
        self.bendy_bone_translate_values_r['Crus_Inferius_Anthelicis_End']['Y'] = [0.0,1.0781]
        self.bendy_bone_translate_values_r['Crus_Inferius_Anthelicis_End']['Z'] = [0.0,0.9613]
        self.bendy_bone_rotate_values_r['Crus_Inferius_Anthelicis_End']['W'] = [1.0,0.1445]
        self.bendy_bone_rotate_values_r['Crus_Inferius_Anthelicis_End']['X'] = [0.0,0.2527]
        self.bendy_bone_rotate_values_r['Crus_Inferius_Anthelicis_End']['Y'] = [0.0,0.1321]
        self.bendy_bone_rotate_values_r['Crus_Inferius_Anthelicis_End']['Z'] = [0.0,0.0760]
        
        self.bendy_bone_translate_values_r['Crus_Superius_Anthelicis_Start']['X'] = [0.0,0.6328]
        self.bendy_bone_translate_values_r['Crus_Superius_Anthelicis_Start']['Y'] = [0.0,0.6331]
        self.bendy_bone_translate_values_r['Crus_Superius_Anthelicis_Start']['Z'] = [0.0,0.6121]
        self.bendy_bone_rotate_values_r['Crus_Superius_Anthelicis_Start']['W'] = [1.0,0.0151]
        self.bendy_bone_rotate_values_r['Crus_Superius_Anthelicis_Start']['X'] = [0.0,0.0392]
        self.bendy_bone_rotate_values_r['Crus_Superius_Anthelicis_Start']['Y'] = [0.0,0.0288]
        self.bendy_bone_rotate_values_r['Crus_Superius_Anthelicis_Start']['Z'] = [0.0,0.0953]
        
        self.bendy_bone_translate_values_r['Crus_Superius_Anthelicis_End']['X'] = [0.0,0.5171]
        self.bendy_bone_translate_values_r['Crus_Superius_Anthelicis_End']['Y'] = [0.0,0.3964]
        self.bendy_bone_translate_values_r['Crus_Superius_Anthelicis_End']['Z'] = [0.0,0.8171]
        self.bendy_bone_rotate_values_r['Crus_Superius_Anthelicis_End']['W'] = [1.0,0.0454]
        self.bendy_bone_rotate_values_r['Crus_Superius_Anthelicis_End']['X'] = [0.0,0.0763]
        self.bendy_bone_rotate_values_r['Crus_Superius_Anthelicis_End']['Y'] = [0.0,0.0437]
        self.bendy_bone_rotate_values_r['Crus_Superius_Anthelicis_End']['Z'] = [0.0,0.1658]
        
        self.shape_key_values_r['Antitragus inside crease'] = [0.0,0.5000]
        self.shape_key_values_r['Cavum Concha Depth'] = [0.0,0.3198]
        self.shape_key_values_r['Cymba Concha Depth'] = [0.0,0.3435]
        self.shape_key_values_r['Crus Helicis Prominence'] = [0.0,0.7069]
        self.shape_key_values_r['Upper Helix Depth'] = [0.0,0.3936]
        self.shape_key_values_r['Middle Helix Depth'] = [0.0,0.2999]
        self.shape_key_values_r['Lower Helix Depth'] = [0.0,0.4370]
        self.shape_key_values_r['Lobulo Attachment'] = [0.0,0.4013]
        self.shape_key_values_r['Scapha Depth'] = [0.0,0.3311]
        self.shape_key_values_r['Fossa Triangularis Depth'] = [0.0,0.4453]
        self.shape_key_values_r['Crus Inferius Anthelicis lower crease'] = [0.0,0.2763]
        self.shape_key_values_r['Crus Inferius Anthelicis upper crease'] = [0.0,0.0719]
        self.shape_key_values_r['Crus Superius Anthelicis lower crease'] = [0.0,0.1710]
        self.shape_key_values_r['Crus Superius Anthelicis upper crease'] = [0.0,0.2386]
        self.shape_key_values_r['Tragus Upper Dent'] = [0.0,0.4597]
        self.shape_key_values_r['Crus Helicis upper dent'] = [0.0,0.1289]
        self.shape_key_values_r['Crus Helicis lower dent'] = [0.0,0.2077]
        self.shape_key_values_r['Ear canal diameter'] = [0.0,0.4307]
        
        self.bendy_bone_scale_values_r['Lobulo_Bendy'] = [1.0,0.2772]
        self.bendy_bone_scale_values_r['Helix_low_Bendy'] = [1.0,0.3402]
        self.bendy_bone_scale_values_r['Helix_middle_Bendy'] = [1.0,0.2320]
        self.bendy_bone_scale_values_r['Helix_up_Bendy'] = [1.0,0.4903]
        self.bendy_bone_scale_values_r['Tragus_Bendy'] = [1.0,0.4251]
        self.bendy_bone_scale_values_r['Antitragus_Bendy'] = [1.0,0.1703]
        self.bendy_bone_scale_values_r['Antihelix_Bendy'] = [1.0,0.3611]
        self.bendy_bone_scale_values_r['Crus_Inferius_Anthelicis_Bendy'] = [1.0,0.3345]
        self.bendy_bone_scale_values_r['Crus_Superius_Anthelicis_Bendy'] = [1.0,0.3378]
        

        
        
        
        
        
        print("Locating instructions... ", end="", flush=True)
        os.chdir(self.path)
        print("Done")
        print("Loaded Instructions from {}".format(self.path))
        print("Exporting to {}".format(self.path))
        for file in glob.glob("*.txt"):
            name = file.split('.')[0]
            print("Ear {}... ".format(name), end="", flush=True)

            logfile = 'blender_render.log'
            open(logfile, 'a').close()
            old = os.dup(1)
            sys.stdout.flush()
            os.close(1)
            os.open(logfile, os.O_WRONLY)
            
            
            for bn in self.bendy_bone_names:
                if bn.endswith("_Start"):
                    
                    for ar in self.axis_r:
                        if ar == 'W':
                            offset = 1
                        else:
                            offset = 0
                        v = np.clip(np.random.normal(self.bendy_bone_rotate_values[bn][ar][0], self.bendy_bone_rotate_values[bn][ar][1], 1)[0], -3*self.bendy_bone_rotate_values[bn][ar][1]+offset, 3*self.bendy_bone_rotate_values[bn][ar][1]+offset)
                        self.bendy_bone_rotate_values_r[bn][ar][0] = np.clip(v + np.random.normal(0.0,0.33,1)[0]*self.bendy_bone_rotate_values[bn][ar][1]*3*0.2, -3*self.bendy_bone_rotate_values[bn][ar][1]+offset, 3*self.bendy_bone_rotate_values[bn][ar][1]+offset)
                        self.bonesLookup[bn.removesuffix("_Start")].rotate("Start",ar,v)
                        
                    for at in self.axis_t:
                        v = np.clip(np.random.normal(self.bendy_bone_translate_values[bn][at][0], self.bendy_bone_translate_values[bn][at][1], 1)[0], -3*self.bendy_bone_translate_values[bn][at][1], 3*self.bendy_bone_translate_values[bn][at][1])
                        self.bendy_bone_translate_values_r[bn][at][0] = np.clip(v + np.random.normal(0.0,0.33,1)[0]*self.bendy_bone_translate_values[bn][at][1]*3*0.2, -3*self.bendy_bone_translate_values[bn][at][1]+offset, 3*self.bendy_bone_translate_values[bn][at][1]+offset)
                        self.bonesLookup[bn.removesuffix("_Start")].translate("Start",at,v)        
                    
                        
                elif bn.endswith("_End"):
                    for ar in self.axis_r:
                        if ar == 'W':
                            offset = 1
                        else:
                            offset = 0
                        v = np.clip(np.random.normal(self.bendy_bone_rotate_values[bn][ar][0], self.bendy_bone_rotate_values[bn][ar][1], 1)[0], -3*self.bendy_bone_rotate_values[bn][ar][1]+offset, 3*self.bendy_bone_rotate_values[bn][ar][1]+offset)
                        self.bendy_bone_rotate_values_r[bn][ar][0] = np.clip(v + np.random.normal(0.0,0.33,1)[0]*self.bendy_bone_rotate_values[bn][ar][1]*3*0.2, -3*self.bendy_bone_rotate_values[bn][ar][1]+offset, 3*self.bendy_bone_rotate_values[bn][ar][1]+offset)
                        self.bonesLookup[bn.removesuffix("_End")].rotate("End",ar,v)
                    
                    for at in self.axis_t:
                        v = np.clip(np.random.normal(self.bendy_bone_translate_values[bn][at][0], self.bendy_bone_translate_values[bn][at][1], 1)[0], -3*self.bendy_bone_translate_values[bn][at][1], 3*self.bendy_bone_translate_values[bn][at][1])
                        self.bendy_bone_translate_values_r[bn][at][0] = np.clip(v + np.random.normal(0.0,0.33,1)[0]*self.bendy_bone_translate_values[bn][at][1]*3*0.2, -3*self.bendy_bone_translate_values[bn][at][1]+offset, 3*self.bendy_bone_translate_values[bn][at][1]+offset)
                        self.bonesLookup[bn.removesuffix("_End")].translate("End",at,v)        
                    
                        
            for bn in self.bendy_bone_scale_names:
                val = np.clip(np.random.normal(self.bendy_bone_scale_values[bn][0], self.bendy_bone_scale_values[bn][1], 1)[0], -3*self.bendy_bone_scale_values[bn][1]+1.0, 3*self.bendy_bone_scale_values[bn][1]+1.0)
                self.bendy_bone_scale_values_r[bn][0] = np.clip(val + np.random.normal(0.0,0.33,1)[0]*self.bendy_bone_scale_values[bn][1]*3*0.2, -3*self.bendy_bone_scale_values[bn][1]+1.0, 3*self.bendy_bone_scale_values[bn][1]+1.0)
                for axis_idx in range(0,3):
                    bpy.data.objects["Armature"].pose.bones[bn].scale[axis_idx] = val
                    #bpy.data.objects["Armature"].pose.bones[bn].bbone_scalein[axis_idx] = val
                    #bpy.data.objects["Armature"].pose.bones[bn].bbone_scaleout[axis_idx] = val
            
            for skn in self.shape_key_names:
                v = np.clip(np.random.normal(self.shape_key_values[skn][0], self.shape_key_values[skn][1], 1)[0], self.shape_key_values[skn][0]-3*self.shape_key_values[skn][1], self.shape_key_values[skn][0]+3*self.shape_key_values[skn][1])
                self.shape_key_values_r[skn][0] = np.clip(v + np.random.normal(0.0,0.33,1)[0]*self.shape_key_values[skn][1]*3*0.2, self.shape_key_values[skn][0]-3*self.shape_key_values[skn][1], self.shape_key_values[skn][0]+3*self.shape_key_values[skn][1])
                bpy.data.shape_keys["Key.002"].key_blocks[skn].value = v
                
            

                    

            #self.load(name)
            #self.scale()
                
            if arg_mesh == 'TRUE' or arg_image =='TRUE':
                self.modifiers(True)
                if arg_mesh == 'TRUE':
                    self.export(name+'_l')
                if arg_image == 'TRUE':
                    self.render(name+'_l')
                self.modifiers(False)
            
            parameter_file = open(name+"_parameters_l.txt", 'w')
            parameter_file.write('Size_Bendy,'+'Location,'+'X,'+str(0.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Location,'+'Y,'+str(0.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Location,'+'Z,'+str(0.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Rotation,'+'W,'+str(1.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Rotation,'+'X,'+str(0.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Rotation,'+'Y,'+str(0.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Rotation,'+'Z,'+str(0.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Scale,'+'W,'+str(1.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Scale,'+'W,'+str(1.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Scale,'+'W,'+str(1.0)+'\n')
            for s in self.shape_key_names:
                parameter_file.write(s+",ShapeKey,"+str(bpy.data.shape_keys["Key.002"].key_blocks[s].value)+'\n')
                
            for b in self.bendy_bone_names:
                for idx in range(0,3):
                    parameter_file.write(b+",Location,"+self.axis_t[idx]+','+str(bpy.data.objects["Armature"].pose.bones[b].location[idx])+'\n')
                for idx in range(0,4):
                    parameter_file.write(b+",Rotation,"+self.axis_r[idx]+','+str(bpy.data.objects["Armature"].pose.bones[b].rotation_quaternion[idx])+'\n')
            
            for s in self.bendy_bone_scale_names:
                parameter_file.write(s+",Scale,"+str(bpy.data.objects["Armature"].pose.bones[s].scale[axis_idx])+'\n')
                
            

            
            parameter_file.close()     
            
            
            
            
            
            for bn in self.bendy_bone_names:
                if bn.endswith("_Start"):
                    
                    for ar in self.axis_r:
                        if ar == 'W':
                            offset = 1
                        else:
                            offset = 0
                        v = self.bendy_bone_rotate_values_r[bn][ar][0]
                        self.bonesLookup[bn.removesuffix("_Start")].rotate("Start",ar,v)
                        
                    for at in self.axis_t:
                        v = self.bendy_bone_translate_values_r[bn][at][0]
                        self.bonesLookup[bn.removesuffix("_Start")].translate("Start",at,v)        
                    
                        
                elif bn.endswith("_End"):
                    for ar in self.axis_r:
                        if ar == 'W':
                            offset = 1
                        else:
                            offset = 0
                        v = self.bendy_bone_rotate_values_r[bn][ar][0]
                        self.bonesLookup[bn.removesuffix("_End")].rotate("End",ar,v)
                    
                    for at in self.axis_t:
                        v = self.bendy_bone_translate_values_r[bn][at][0]
                        self.bonesLookup[bn.removesuffix("_End")].translate("End",at,v)        
                    
                        
            for bn in self.bendy_bone_scale_names:
                val = self.bendy_bone_scale_values_r[bn][0]
                for axis_idx in range(0,3):
                    bpy.data.objects["Armature"].pose.bones[bn].scale[axis_idx] = val
                    #bpy.data.objects["Armature"].pose.bones[bn].bbone_scalein[axis_idx] = val
                    #bpy.data.objects["Armature"].pose.bones[bn].bbone_scaleout[axis_idx] = val
            
            for skn in self.shape_key_names:
                v = self.shape_key_values_r[skn][0]
                bpy.data.shape_keys["Key.002"].key_blocks[skn].value = v
                
            

                    

            #self.load(name)
            #self.scale()
                
            if arg_mesh == 'TRUE' or arg_image =='TRUE':
                self.modifiers(True)
                if arg_mesh == 'TRUE':
                    self.export(name+'_r')
                if arg_image == 'TRUE':
                    self.render(name+'_r')
                self.modifiers(False)
            
            parameter_file = open(name+"_parameters_r.txt", 'w')
            parameter_file.write('Size_Bendy,'+'Location,'+'X,'+str(0.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Location,'+'Y,'+str(0.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Location,'+'Z,'+str(0.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Rotation,'+'W,'+str(1.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Rotation,'+'X,'+str(0.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Rotation,'+'Y,'+str(0.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Rotation,'+'Z,'+str(0.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Scale,'+'W,'+str(1.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Scale,'+'W,'+str(1.0)+'\n')
            parameter_file.write('Size_Bendy,'+'Scale,'+'W,'+str(1.0)+'\n')
            for s in self.shape_key_names:
                parameter_file.write(s+",ShapeKey,"+str(bpy.data.shape_keys["Key.002"].key_blocks[s].value)+'\n')
                
            for b in self.bendy_bone_names:
                for idx in range(0,3):
                    parameter_file.write(b+",Location,"+self.axis_t[idx]+','+str(bpy.data.objects["Armature"].pose.bones[b].location[idx])+'\n')
                for idx in range(0,4):
                    parameter_file.write(b+",Rotation,"+self.axis_r[idx]+','+str(bpy.data.objects["Armature"].pose.bones[b].rotation_quaternion[idx])+'\n')
            
            for s in self.bendy_bone_scale_names:
                parameter_file.write(s+",Scale,"+str(bpy.data.objects["Armature"].pose.bones[s].scale[axis_idx])+'\n')
                
            

            
            parameter_file.close()                           
            #self.reset(name)
            
            
            os.close(1)
            os.dup(old)
            os.close(old)
            
            print("Done")

Ear = Ear("Ear")

Lobulo = Bone("Lobulo", Ear)
Helix_low = Bone("Helix_low", Ear)
Helix_middle = Bone("Helix_middle", Ear)
Helix_up = Bone("Helix_up", Ear)
Tragus = Bone("Tragus", Ear)
Antitragus = Bone("Antitragus", Ear)
Antihelix = Bone("Antihelix", Ear)
Crus_Inferius_Anthelicis = Bone("Crus_Inferius_Anthelicis", Ear)
Crus_Superius_Anthelicis = Bone("Crus_Superius_Anthelicis", Ear)

print("Done")

Ear.loadAll()

print("Task Complete")