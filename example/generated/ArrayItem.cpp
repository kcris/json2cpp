//
// ArrrayItem.cpp
//
// -- generated class for jsoncpp
//
#include "ArrrayItem.h"

//equals operator
bool ArrrayItem::operator==(const ArrrayItem & other) const
{
	return
		std::tie(m_prop)
		==
		std::tie(other.m_prop);
}

//lessThan operator
bool ArrrayItem::operator<(const ArrrayItem & other) const
{
	return
		std::tie(m_prop)
		<
		std::tie(other.m_prop);
}

// parse
bool ArrrayItem::load(const web::json::value & jsonObject)
{
	try
	{
		m_prop = jsonObject.at(L"prop").as_string();
	}
	catch(web::json::json_exception &) { return false; }

	return true;
}

// serialize
web::json::value ArrrayItem::save() const
{
	web::json::value jsonObject;

	jsonObject[L"prop"] = web::json::value::string(m_prop);

	return jsonObject;
}
