import bpy
import numpy as np
import math


for index in range(1):
    filepath = 'D:\\fyp\\pinnar\\data\\2022_07_11_12_24_04_l\\test.obj'
    bpy.ops.import_scene.obj(filepath=filepath)
    
    bpy.ops.object.select_all(action='DESELECT')

    for obj in bpy.context.scene.objects[:]:
        bpy.context.view_layer.objects.active = obj
        bpy.data.objects[obj.name].select_set(True)
        obj.name = 'Reference'
        bpy.data.objects['Reference'].rotation_euler[0] = 0.0
        bpy.data.objects['Reference'].scale[0] = 1000.0
        bpy.data.objects['Reference'].scale[1] = 1000.0
        bpy.data.objects['Reference'].scale[2] = 1000.0
        bpy.data.objects['Reference'].location[0] = 5.0
        bpy.ops.object.transform_apply()        
            
    for obj in bpy.context.scene.objects[:]:
        if obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            
            tmphide = obj.hide_get()
            obj.hide_set(False)
            tmphide_select=obj.hide_select
            obj.hide_select=False
            
            for ii in range(1,100):
                bpy.ops.object.material_slot_remove()


            obj.hide_select=tmphide_select     
            obj.hide_set(tmphide)

           
    for material in bpy.data.materials[:]:
        bpy.data.materials.remove(material)

    skin=bpy.data.materials.new('Skin')
    skin.name='Skin'
    skin.diffuse_color[0]=0.8
    skin.diffuse_color[1]=0.6
    skin.diffuse_color[2]=0.4
    left=bpy.data.materials.new('Left ear')
    left.name='Left ear'
    left.diffuse_color[0]=0.8
    left.diffuse_color[1]=0
    left.diffuse_color[2]=0
    right=bpy.data.materials.new('Right ear')
    right.name='Right ear'
    right.diffuse_color[0]=0
    right.diffuse_color[1]=0
    right.diffuse_color[2]=0.8
            
    for obj in bpy.context.scene.objects[:]:
        if obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            
            tmphide = obj.hide_get()
            obj.hide_set(False)
            tmphide_select=obj.hide_select
            obj.hide_select=False
            
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.editmode_toggle()
                
            bpy.ops.object.material_slot_add()
            obj.material_slots[0].material=skin
                
            bpy.ops.object.material_slot_add()
            obj.material_slots[1].material=left
                
            bpy.ops.object.material_slot_add()
            obj.material_slots[2].material=right
            
            obj_data=obj.data
            
            ear=([0,200,0])
            mic=([0])
            for vertex in obj_data.vertices[:]:
                if math.sqrt(vertex.co[0]*vertex.co[0]+vertex.co[2]*vertex.co[2])<3 and vertex.co[1]>0 and vertex.co[0]<0 and vertex.co[2]>0:
                    if vertex.co[1]<ear[1] and math.sqrt(vertex.co[0]*vertex.co[0]+vertex.co[2]*vertex.co[2])<math.sqrt(obj_data.vertices[mic[0]].co[0]**2+obj_data.vertices[mic[0]].co[2]**2):
                        ear[1]=vertex.co[1]
                        mic[0]=vertex.index
            
            for ii in range(0,3):
                for jj in range(0,len(mic)):
                    for triangle in obj_data.polygons[:]:
                        if triangle.vertices[0]==mic[jj] or triangle.vertices[1]==mic[jj] or triangle.vertices[2]==mic[jj]:
                            triangle.material_index=1
                            mic.append(triangle.vertices[0])
                            mic.append(triangle.vertices[1])
                            mic.append(triangle.vertices[2])
                tmpbreak=False
                for jj in range(1,len(mic)):
                    if math.sqrt((obj_data.vertices[mic[jj]].co[0]-obj_data.vertices[mic[0]].co[0])**2+(obj_data.vertices[mic[jj]].co[1]-obj_data.vertices[mic[0]].co[1])**2+(obj_data.vertices[mic[jj]].co[2]-obj_data.vertices[mic[0]].co[2])**2)>1.5:
                        tmpbreak=True
                if tmpbreak:
                    break
            
            ear=([0,-200,0])
            mic=([0])
            for vertex in obj_data.vertices[:]:
                if math.sqrt(vertex.co[0]*vertex.co[0]+vertex.co[2]*vertex.co[2])<3 and vertex.co[1]<0 and vertex.co[0]<0 and vertex.co[2]>0:
                    if vertex.co[1]>ear[1] and math.sqrt(vertex.co[0]*vertex.co[0]+vertex.co[2]*vertex.co[2])<math.sqrt(obj_data.vertices[mic[0]].co[0]**2+obj_data.vertices[mic[0]].co[2]**2):
                        ear[1]=vertex.co[1]
                        mic[0]=vertex.index
            
            for ii in range(0,3):
                for jj in range(0,len(mic)):
                    for triangle in obj_data.polygons[:]:
                        if triangle.vertices[0]==mic[jj] or triangle.vertices[1]==mic[jj] or triangle.vertices[2]==mic[jj]:
                            triangle.material_index=2
                            mic.append(triangle.vertices[0])
                            mic.append(triangle.vertices[1])
                            mic.append(triangle.vertices[2])
                tmpbreak=False
                for jj in range(1,len(mic)):
                    if math.sqrt((obj_data.vertices[mic[jj]].co[0]-obj_data.vertices[mic[0]].co[0])**2+(obj_data.vertices[mic[jj]].co[1]-obj_data.vertices[mic[0]].co[1])**2+(obj_data.vertices[mic[jj]].co[2]-obj_data.vertices[mic[0]].co[2])**2)>1.5:
                        tmpbreak=True
                if tmpbreak:
                    break

            obj.hide_select=tmphide_select     
            obj.hide_set(tmphide)

    bpy.ops.export_mesh2hrtf.inp(
        title="pinna model generated HRTF",
        method="ML-FMM BEM",
        sourceType = "Both ears",
        filepath="D:\\fyp\\pinnar\\test_htrf\\GAN_PINNA_DATA\\"+str(index),              # this is the folder where the Mesh2HRTF project is saved
        programPath="D:\\fyp\\pinnar\\output2hrtf_python\\mesh2hrtf",  # change this to the location of Mesh2HRTF
        pictures=False,
        reference=True,
        computeHRIRs=True,
        unit="mm",
        speedOfSound="346.18",                           # this is passed as a string
        densityOfMedium="1.1839",                        # this is passed as a string
        evaluationGrids="gan_1280",
        materialSearchPaths='None',
        minFrequency=100,
        maxFrequency=16000,
        frequencyVectorType="Num steps",
        frequencyVectorValue=128)

    bpy.ops.object.delete()