//
// ArrrayItem.h
//
// -- generated file, do NOT edit
//
#pragma once

#include <cppRest/json.h> //cpprest library used for json serialization



struct ArrrayItem
{
	//constructors
	ArrrayItem() = default;
	ArrrayItem(const web::json::value & jsonObject) : ArrrayItem() { load(jsonObject); }

	//operators (see std::rel_ops)
	bool operator==(const ArrrayItem & other) const;
	bool operator<(const ArrrayItem & other) const;

	//json parsing and serializing
	bool load(const web::json::value & jsonObject);
	web::json::value save() const;

	//member data
	std::wstring m_prop;
};
