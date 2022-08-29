import bpy

f = open("bad.txt", "w")

for i in range(1,1001):
    filepath = 'D:\\fyp\\pinnar\\data\\2022_07_11_13_03_06_l\\'+str(i)+"_meshgrading"+".obj"
    bpy.ops.import_scene.obj(filepath=filepath)

    for obj in bpy.context.scene.objects[:]:
        if obj.name.startswith(str(i)):
            n = obj.name
            break
        
    data = obj.data

    # FACES, TRIANGLES
    total_triangles = 0

    for face in data.polygons:
        vertices = face.vertices
        triangles = len(vertices) - 2
        total_triangles += triangles

    print(total_triangles)
    if total_triangles < 15000:
        f.write(str(i)+"\n")
    
        
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    bpy.data.objects[obj.name].select_set(True)
    bpy.ops.object.delete()

f.close()