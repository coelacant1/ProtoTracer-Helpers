from PIL import Image

name = "RunningKernel"
fileName = f"Example Files\Boot\{name}.obj"
textureName = "Example Files\Boot\{name}.png"
outputName = f"..\ProtoTracer\lib\ProtoTracer\Assets\Models\OBJ\{name}.h"
numColors = 16

class Vector3D:
    X = 0.0
    Y = 0.0
    Z = 0.0

class Triangle:
    A = 0
    B = 1
    C = 2

def GetHeader():
    return "#pragma once\n\n" + \
           "#include \"..\\..\\..\\Scene\\Materials\\Static\\SimpleMaterial.h\"\n" + \
           "#include \"..\\..\\..\\Scene\\Materials\\Static\\UVMap.h\"\n" + \
           "#include \"..\\..\\..\\Scene\\Objects\\Object3D.h\"\n" + \
           "#include \"..\\..\\..\\Renderer\\Utils\\IndexGroup.h\"\n\n" + \
           "class " + name + " {\nprivate:\n"

def GetHeaderUV():
    return "\n\n#include \"..\Render\Object3D.h\"\n#include \"..\Materials\SimpleMaterial.h\"\n\nclass " + name + "{\nprivate:\n"

def GetVertices(vertices):
    basisVertices = "\tVector3D basisVertices[" + str(int(len(vertices))) + "] = {"

    for i, vertex in enumerate(vertices):
        if i in {len(vertices) - 1}:
            basisVertices += "Vector3D(" + f'{vertex.X:.4f}' + "f," + f'{vertex.Y:.4f}' + "f," + f'{vertex.Z:.4f}' + "f)};\n" #last entry
        else:
            basisVertices += "Vector3D(" + f'{vertex.X:.4f}' + "f," + f'{vertex.Y:.4f}' + "f," + f'{vertex.Z:.4f}' + "f),"

    return basisVertices

def GetIndexes(triangles):
    basisIndexes = "\tIndexGroup basisIndexes[" + str(len(triangles)) + "] = {"

    for i, index in enumerate(triangles):
        if i in {len(triangles) - 1}:
            basisIndexes += "IndexGroup(" + str(index.A) + "," + str(index.B) + "," + str(index.C) + ")};\n"
        else:
            basisIndexes += "IndexGroup(" + str(index.A) + "," + str(index.B) + "," + str(index.C) + "),"

    return basisIndexes

def GetUVVertices(vertices):
    uvVertices = "\tVector2D uvVertices[" + str(int(len(vertices))) + "] = {"

    for i, vertex in enumerate(vertices):
        if i in {len(vertices) - 1}:
            uvVertices += "Vector2D(" + f'{vertex.X:.4f}' + "f," + f'{vertex.Y:.4f}' + "f)};\n" #last entry
        else:
            uvVertices += "Vector2D(" + f'{vertex.X:.4f}' + "f," + f'{vertex.Y:.4f}' + "f),"

    return uvVertices

def GetUVIndexes(triangles):
    basisIndexes = "\tIndexGroup uvIndexGroup[" + str(len(triangles)) + "] = {"

    for i, index in enumerate(triangles):
        if i in {len(triangles) - 1}:
            basisIndexes += "IndexGroup(" + str(index.A) + "," + str(index.B) + "," + str(index.C) + ")};\n"
        else:
            basisIndexes += "IndexGroup(" + str(index.A) + "," + str(index.B) + "," + str(index.C) + "),"

    return basisIndexes

def GetObject(vertices, triangles):
    lines =  "\tTriangleGroup triangleGroup = TriangleGroup(&basisVertices[0], &basisIndexes[0], " + str(int(len(vertices))) + ", " + str(len(triangles)) + ");\n"
    lines += "\tSimpleMaterial simpleMaterial = SimpleMaterial(RGBColor(128, 128, 128));\n"
    return lines + "\tObject3D basisObj = Object3D(&triangleGroup, &simpleMaterial);\n\n"

def GetObjectUV(vertices, triangles, uvVertices):
    lines =  "\tTriangleGroup triangleGroup = TriangleGroup(basisVertices, basisIndexes, uvIndexGroup, uvVertices, " + str(int(len(vertices))) + ", " + str(len(triangles)) + ", " + str(len(uvVertices)) + ");\n"
    lines += "\t" + name + "Tex material = " + name + "Tex(Vector2D(1.0f, 1.0f), Vector2D());\n"
    return lines + "\tObject3D basisObj = Object3D(&triangleGroup, &material);\n\n"

def GetFooter():
    publicFunctions = "public:\n"
    publicFunctions += "\t" + name + "(){}\n\n"
    publicFunctions += "\tObject3D* GetObject(){\n\t\treturn &basisObj;\n\t}\n};\n"

    return publicFunctions

def ReadVertices(data):
    lines = data.splitlines()
    vectors = []

    for line in lines:
        if line.find("v ") >= 0:
            spaces = line.split(" ")

            print(spaces)

            v = Vector3D()

            v.X = float(spaces[1])
            v.Y = float(spaces[2])
            v.Z = float(spaces[3])

            vectors.append(v)
    
    return vectors


def ReadIndexes(data):
    lines = data.splitlines()
    indexes = []

    for line in lines:
        if line.find("f ") >= 0:
            spaces = line.split(" ")

            print(spaces)

            t = Triangle()

            t.A = int(spaces[1].split("/")[0]) - 1
            t.B = int(spaces[2].split("/")[0]) - 1
            t.C = int(spaces[3].split("/")[0]) - 1

            indexes.append(t)
    
    return indexes

def ReadUVVertices(data):
    lines = data.splitlines()
    vectors = []

    for line in lines:
        if line.find("vt ") >= 0:
            spaces = line.split(" ")

            print(spaces)

            v = Vector3D()

            v.X = float(spaces[1])
            v.Y = float(spaces[2])
            #v.Z = float(spaces[3])

            vectors.append(v)
    
    return vectors

def ReadUVIndexes(data):
    lines = data.splitlines()
    indexes = []

    for line in lines:
        if line.find("f ") >= 0:
            spaces = line.split(" ")

            print(spaces)

            t = Triangle()

            t.A = int(spaces[1].split("/")[1]) - 1
            t.B = int(spaces[2].split("/")[1]) - 1
            t.C = int(spaces[3].split("/")[1]) - 1

            indexes.append(t)
    
    return indexes

def GetTexture(className, file):
    image = Image.open(file).convert("P", palette = Image.ADAPTIVE, colors = numColors)
    w, h = image.size
    
    image.seek(0)
    pal = image.getpalette()

    data = "#pragma once\n\n"
    data += "#include \"..\Materials\\UVMap.h\"\n\n"
    data += "class " + className + "Tex : public UVMap{\n"
    data += "private:\n"
    data += "\tstatic const uint8_t rgbMemory[];\n"
    data += "\tstatic const uint8_t rgbColors[];\n\n"
    data += "public:\n"
    data += "\t" + className + "Tex(Vector2D size, Vector2D offset) : UVMap(rgbMemory, rgbColors, " + str(w) + ", " + str(h) + ", " + str(int(len(pal) / 3) - 1) + ") {\n"
    data += "\t\tSetSize(size);\n"
    data += "\t\tSetPosition(offset);\n"
    data += "\t}\n};\n\n"

    data += "const uint8_t " + className + "Tex::rgbMemory[] PROGMEM = {"
    
    for i in range(h):
        for j in range(w):
            index = image.getpixel((j, i))

            data += str(index)
            
            if i == h - 1 and j == w - 1:
                data += "};\n\n"
            else:
                data += ","

    data += "const uint8_t " + className + "Tex::rgbColors[] PROGMEM = {"

    for i in range(numColors):
        r = pal[i * 3]
        g = pal[i * 3 + 1]
        b = pal[i * 3 + 2]

        data += str(r) + "," + str(g) + "," + str(b)
        
        if i == numColors - 1:
            data += "};\n"
        else:
            data += ","

    return data

with open(fileName, 'r') as file:
    data = file.read()
    output = ""

    uvVertices = ReadUVVertices(data)

    if len(uvVertices) > 1:
        uvIndexes = ReadUVIndexes(data)
        vertices = ReadVertices(data)
        indexes = ReadIndexes(data)

        output += GetTexture(name, textureName) + GetHeaderUV() + GetVertices(vertices) + GetIndexes(indexes) + GetUVVertices(uvVertices) + GetUVIndexes(uvIndexes) + GetObjectUV(vertices, indexes, uvVertices) + GetFooter()
    else:
        vertices = ReadVertices(data)
        indexes = ReadIndexes(data)

        output += GetHeader() + GetVertices(vertices) + GetIndexes(indexes) + GetObject(vertices, indexes) + GetFooter()

    print(output)
    f = open(outputName, "w")
    f.write(output)
    f.close()
    