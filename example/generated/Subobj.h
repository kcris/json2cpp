//
// Subobj.h
//
// -- generated file, do NOT edit
//
#pragma once

#include <cppRest/json.h> //cpprest library used for json serialization



struct Subobj
{
	//constructors
	Subobj() = default;
	Subobj(const web::json::value & jsonObject) : Subobj() { load(jsonObject); }

	//operators (see std::rel_ops)
	bool operator==(const Subobj & other) const;
	bool operator<(const Subobj & other) const;

	//json parsing and serializing
	bool load(const web::json::value & jsonObject);
	web::json::value save() const;

	//member data
	int m_prop;
};
