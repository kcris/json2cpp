//
// User.h
//
// -- generated file, do NOT edit
//
#pragma once

#include <cppRest/json.h> //cpprest library used for json serialization

#include "subobj.h" //generated
#include "ArrrayItem.h" //generated


struct User
{
	//constructors
	User() = default;
	User(const web::json::value & jsonObject) : User() { load(jsonObject); }

	//operators (see std::rel_ops)
	bool operator==(const User & other) const;
	bool operator<(const User & other) const;

	//json parsing and serializing
	bool load(const web::json::value & jsonObject);
	web::json::value save() const;

	//member data
	bool m_verified;
	Subobj m_subobj;
	double m_weight;
	int m_userid;
	std::vector<ArrrayItem> m_arrray;
	std::vector<int> m_items;
	std::vector<std::wstring> m_games;
	std::wstring m_username;
};
