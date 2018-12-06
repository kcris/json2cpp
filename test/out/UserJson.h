//
// UserJson.h
//
// -- generated file, do NOT edit
//
#pragma once

#include <cppRest/json.h> //json serialization library

namespace UserJson {

/*
 * struct ArrrayItem
 */
struct  ArrrayItem
{
	ArrrayItem() = default;
	ArrrayItem(const web::json::value & jsonValue) : m_jsonValue(jsonValue) {}

	//prop
	web::json::value get_prop_json() const /*throw(web::json::json_exception)*/ {
		return m_jsonValue.at(L"prop");
	}
	std::wstring get_prop(const std::wstring & defaultValue = std::wstring()) const throw() /*noexcept*/ {
		try{
			return m_jsonValue.at(L"prop").as_string();
		}
		catch(web::json::json_exception &) {
			return defaultValue; //missing data
		}
	}
	void set_prop(const std::wstring & x) {
		m_jsonValue.at(L"prop") = web::json::value::string(x);
	}

	//public data
	web::json::value m_jsonValue;
};


/*
 * struct Inner
 */
struct  Inner
{
	Inner() = default;
	Inner(const web::json::value & jsonValue) : m_jsonValue(jsonValue) {}

	//alfa
	web::json::value get_alfa_json() const /*throw(web::json::json_exception)*/ {
		return m_jsonValue.at(L"alfa");
	}
	double get_alfa(const double & defaultValue = double()) const throw() /*noexcept*/ {
		try{
			return m_jsonValue.at(L"alfa").as_double();
		}
		catch(web::json::json_exception &) {
			return defaultValue; //missing data
		}
	}
	void set_alfa(const double & x) {
		m_jsonValue.at(L"alfa") = web::json::value::number(x);
	}
	//beta
	web::json::value get_beta_json() const /*throw(web::json::json_exception)*/ {
		return m_jsonValue.at(L"beta");
	}
	double get_beta(const double & defaultValue = double()) const throw() /*noexcept*/ {
		try{
			return m_jsonValue.at(L"beta").as_double();
		}
		catch(web::json::json_exception &) {
			return defaultValue; //missing data
		}
	}
	void set_beta(const double & x) {
		m_jsonValue.at(L"beta") = web::json::value::number(x);
	}

	//public data
	web::json::value m_jsonValue;
};


/*
 * struct Subobj
 */
struct  Subobj
{
	Subobj() = default;
	Subobj(const web::json::value & jsonValue) : m_jsonValue(jsonValue) {}

	//prop
	web::json::value get_prop_json() const /*throw(web::json::json_exception)*/ {
		return m_jsonValue.at(L"prop");
	}
	double get_prop(const double & defaultValue = double()) const throw() /*noexcept*/ {
		try{
			return m_jsonValue.at(L"prop").as_double();
		}
		catch(web::json::json_exception &) {
			return defaultValue; //missing data
		}
	}
	void set_prop(const double & x) {
		m_jsonValue.at(L"prop") = web::json::value::number(x);
	}
	//inner
	web::json::value get_inner_json() const /*throw(web::json::json_exception)*/ {
		return m_jsonValue.at(L"inner");
	}
	Inner get_inner(const Inner & defaultValue = Inner()) const throw() /*noexcept*/ {
		try{
			return Inner(m_jsonValue.at(L"inner"));
		}
		catch(web::json::json_exception &) {
			return defaultValue; //missing data
		}
	}
	void set_inner(const Inner & x) {
		m_jsonValue.at(L"inner") = x.m_jsonValue; //json object
	}

	//public data
	web::json::value m_jsonValue;
};


/*
 * struct User
 */
struct  User
{
	User() = default;
	User(const web::json::value & jsonValue) : m_jsonValue(jsonValue) {}

	//verified
	web::json::value get_verified_json() const /*throw(web::json::json_exception)*/ {
		return m_jsonValue.at(L"verified");
	}
	bool get_verified(const bool & defaultValue = bool()) const throw() /*noexcept*/ {
		try{
			return m_jsonValue.at(L"verified").as_bool();
		}
		catch(web::json::json_exception &) {
			return defaultValue; //missing data
		}
	}
	void set_verified(const bool & x) {
		m_jsonValue.at(L"verified") = web::json::value::boolean(x);
	}
	//userid
	web::json::value get_userid_json() const /*throw(web::json::json_exception)*/ {
		return m_jsonValue.at(L"userid");
	}
	double get_userid(const double & defaultValue = double()) const throw() /*noexcept*/ {
		try{
			return m_jsonValue.at(L"userid").as_double();
		}
		catch(web::json::json_exception &) {
			return defaultValue; //missing data
		}
	}
	void set_userid(const double & x) {
		m_jsonValue.at(L"userid") = web::json::value::number(x);
	}
	//weight
	web::json::value get_weight_json() const /*throw(web::json::json_exception)*/ {
		return m_jsonValue.at(L"weight");
	}
	double get_weight(const double & defaultValue = double()) const throw() /*noexcept*/ {
		try{
			return m_jsonValue.at(L"weight").as_double();
		}
		catch(web::json::json_exception &) {
			return defaultValue; //missing data
		}
	}
	void set_weight(const double & x) {
		m_jsonValue.at(L"weight") = web::json::value::number(x);
	}
	//username
	web::json::value get_username_json() const /*throw(web::json::json_exception)*/ {
		return m_jsonValue.at(L"username");
	}
	std::wstring get_username(const std::wstring & defaultValue = std::wstring()) const throw() /*noexcept*/ {
		try{
			return m_jsonValue.at(L"username").as_string();
		}
		catch(web::json::json_exception &) {
			return defaultValue; //missing data
		}
	}
	void set_username(const std::wstring & x) {
		m_jsonValue.at(L"username") = web::json::value::string(x);
	}
	//items
	web::json::value get_items_json() const /*throw(web::json::json_exception)*/ {
		return m_jsonValue.at(L"items");
	}
	std::vector<double> get_items(const std::vector<double> & defaultValue = std::vector<double>()) const throw() /*noexcept*/ {
		try{
			std::vector<double> arr;
			for (const web::json::value & item : m_jsonValue.at(L"items").as_array())
				arr.push_back(item.as_double());
			return arr;
		}
		catch(web::json::json_exception &) {
			return defaultValue; //missing data
		}
	}
	void set_items(const std::vector<double> & x) {
		std::vector<web::json::value> arr;
		for (const auto & item : x)
			arr.push_back(web::json::value::number(item));
		m_jsonValue.at(L"items") = web::json::value::array(arr);
	}
	//games
	web::json::value get_games_json() const /*throw(web::json::json_exception)*/ {
		return m_jsonValue.at(L"games");
	}
	std::vector<std::wstring> get_games(const std::vector<std::wstring> & defaultValue = std::vector<std::wstring>()) const throw() /*noexcept*/ {
		try{
			std::vector<std::wstring> arr;
			for (const web::json::value & item : m_jsonValue.at(L"games").as_array())
				arr.push_back(item.as_string());
			return arr;
		}
		catch(web::json::json_exception &) {
			return defaultValue; //missing data
		}
	}
	void set_games(const std::vector<std::wstring> & x) {
		std::vector<web::json::value> arr;
		for (const auto & item : x)
			arr.push_back(web::json::value::string(item));
		m_jsonValue.at(L"games") = web::json::value::array(arr);
	}
	//arrray
	web::json::value get_arrray_json() const /*throw(web::json::json_exception)*/ {
		return m_jsonValue.at(L"arrray");
	}
	std::vector<ArrrayItem> get_arrray(const std::vector<ArrrayItem> & defaultValue = std::vector<ArrrayItem>()) const throw() /*noexcept*/ {
		try{
			std::vector<ArrrayItem> arr;
			for (const web::json::value & item : m_jsonValue.at(L"arrray").as_array())
				arr.push_back(ArrrayItem(item));
			return arr;
		}
		catch(web::json::json_exception &) {
			return defaultValue; //missing data
		}
	}
	void set_arrray(const std::vector<ArrrayItem> & x) {
		std::vector<web::json::value> arr;
		for (const auto & item : x)
			arr.push_back(item.m_jsonValue); //json objects
		m_jsonValue.at(L"arrray") = web::json::value::array(arr);
	}
	//subobj
	web::json::value get_subobj_json() const /*throw(web::json::json_exception)*/ {
		return m_jsonValue.at(L"subobj");
	}
	Subobj get_subobj(const Subobj & defaultValue = Subobj()) const throw() /*noexcept*/ {
		try{
			return Subobj(m_jsonValue.at(L"subobj"));
		}
		catch(web::json::json_exception &) {
			return defaultValue; //missing data
		}
	}
	void set_subobj(const Subobj & x) {
		m_jsonValue.at(L"subobj") = x.m_jsonValue; //json object
	}

	//public data
	web::json::value m_jsonValue;
};

} //namespace UserJson
