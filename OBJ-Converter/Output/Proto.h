#pragma once

#include "..\Materials\UVMap.h"

class ProtoTex : public UVMap{
private:
	static const uint8_t rgbMemory[];

public:
	ProtoTex(Vector2D size, Vector2D offset) : UVMap(Image::RGB, rgbMemory, 512, 512) {
		SetSize(size);
		SetPosition(offset);
	}
};



#include "..\Render\Object3D.h"
#include "..\Materials\SimpleMaterial.h"

class Proto{
private:
	TriangleGroup triangleGroup = TriangleGroup(basisVertices, basisIndexes, uvIndexGroup, uvVertices, 3578, 3348, 4115);
	ProtoTex material = ProtoTex(Vector2D(1.0f, 1.0f), Vector2D());
	Object3D basisObj = Object3D(&triangleGroup, &material);

public:
	Proto(){}

	Object3D* GetObject(){
		return &basisObj;
	}
};