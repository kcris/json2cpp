//
// User.cpp
//
// -- generated class for jsoncpp
//
#include "User.h"

//equals operator
bool User::operator==(const User & other) const
{
	return
		std::tie(m_verified, m_subobj, m_weight, m_userid, m_arrray, m_items, m_games, m_username)
		==
		std::tie(other.m_verified, other.m_subobj, other.m_weight, other.m_userid, other.m_arrray, other.m_items, other.m_games, other.m_username);
}

//lessThan operator
bool User::operator<(const User & other) const
{
	return
		std::tie(m_verified, m_subobj, m_weight, m_userid, m_arrray, m_items, m_games, m_username)
		<
		std::tie(other.m_verified, other.m_subobj, other.m_weight, other.m_userid, other.m_arrray, other.m_items, other.m_games, other.m_username);
}

// parse
bool User::load(const web::json::value & jsonObject)
{
	try
	{
		m_verified = jsonObject.at(L"verified").as_bool();
		m_subobj.load(jsonObject.at(L"subobj")); //json object
		m_weight = jsonObject.at(L"weight").as_double();
		m_userid = jsonObject.at(L"userid").as_integer();
		
		for (const web::json::value & item : jsonObject.at(L"arrray").as_array())
			m_arrray.push_back(ArrrayItem(item)); //json objects
		
		for (const web::json::value & item : jsonObject.at(L"items").as_array())
			m_items.push_back(item.as_integer());
		
		for (const web::json::value & item : jsonObject.at(L"games").as_array())
			m_games.push_back(item.as_string());
		m_username = jsonObject.at(L"username").as_string();
	}
	catch(web::json::json_exception &) { return false; }

	return true;
}

// serialize
web::json::value User::save() const
{
	web::json::value jsonObject;

	jsonObject[L"verified"] = web::json::value::boolean(m_verified);
	jsonObject[L"subobj"] = m_subobj.save(); //json object
	jsonObject[L"weight"] = web::json::value::number(m_weight);
	jsonObject[L"userid"] = web::json::value::number(m_userid);
	
	std::vector<web::json::value> t_arrray;
	for (const auto & item : m_arrray)
		t_arrray.push_back(item.save()); //json objects
	jsonObject[L"arrray"] = web::json::value::array(t_arrray);
	
	std::vector<web::json::value> t_items;
	for (const auto & item : m_items)
		t_items.push_back(web::json::value::number(item));
	jsonObject[L"items"] = web::json::value::array(t_items);
	
	std::vector<web::json::value> t_games;
	for (const auto & item : m_games)
		t_games.push_back(web::json::value::string(item));
	jsonObject[L"games"] = web::json::value::array(t_games);
	jsonObject[L"username"] = web::json::value::string(m_username);

	return jsonObject;
}
