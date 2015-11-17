//
// Subobj.cpp
//
// -- generated class for jsoncpp
//
#include "Subobj.h"

//equals operator
bool Subobj::operator==(const Subobj & other) const
{
	return
		std::tie(m_prop)
		==
		std::tie(other.m_prop);
}

//lessThan operator
bool Subobj::operator<(const Subobj & other) const
{
	return
		std::tie(m_prop)
		<
		std::tie(other.m_prop);
}

// parse
bool Subobj::load(const web::json::value & jsonObject)
{
	try
	{
		m_prop = jsonObject.at(L"prop").as_integer();
	}
	catch(web::json::json_exception &) { return false; }

	return true;
}

// serialize
web::json::value Subobj::save() const
{
	web::json::value jsonObject;

	jsonObject[L"prop"] = web::json::value::number(m_prop);

	return jsonObject;
}
