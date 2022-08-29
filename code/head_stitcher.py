import bpy
import os

basepath = bpy.path.abspath("//")

for index in range(1,2):
    bpy.ops.import_scene.obj(filepath=os.path.join(basepath, str(index)+"_l.obj"))
    bpy.ops.import_scene.obj(filepath=os.path.join(basepath, str(index)+"_r.obj"))

    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]

    bpy.context.view_layer.objects.active.scale = (1, 1, -1)
    
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.editmode_toggle()

    bpy.ops.object.select_by_type(type="MESH")

    bpy.ops.object.join()
    
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.mark_sharp(clear=True)
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.editmode_toggle()
    
    for obj in bpy.context.scene.objects[:]:
        for idx in range(3):
            bpy.data.objects[obj.name].scale[idx] = 0.001



    bpy.ops.export_scene.obj(axis_forward='Y', axis_up='Z', filepath = os.path.join(basepath, str(index)+".obj"))

    bpy.ops.object.delete(use_global=True)