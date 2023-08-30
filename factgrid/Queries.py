import constants
from config import Configuration


class Queries:

    def get_agent(self, agent_id, lang="DE"):
        return f"""SELECT ?item
		?itemLabel
		?itemDescription
		?Date_of_birth
		?Gender
		?GenderLabel
		?Place_of_address
		?Place_of_addressLabel
		?From
		?FromLabel
		?Place_of_birth
		?Place_of_birthLabel
		?Date_of_birth_precision
		?Date_of_birth_calendar
		?Date_of_death
		?Image
		?Place_of_Death
		?Place_of_DeathLabel
		?Date_of_death_precision
		?Date_of_death_calendar
		?Date_of_baptism
		?Date_of_baptism_precision
		?Date_of_baptism_calendar
		?GND_ID
		?Surname
		?SurnameLabel
		?Place_of_baptism
		?Place_of_baptismLabel
		?Grave
		?GraveLabel        
		?Date_of_burial
		?Date_of_burial_precision
		?Date_of_burial_calendar
		?Mother
		?MotherLabel
		?Father
		?FatherLabel
		?Date_of_confirmation
		?Date_of_confirmation_precision
		?Date_of_confirmation_calendar
		WHERE {{
		VALUES ?item {{ wd:{agent_id} }}
		SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{lang},[AUTO_LANGUAGE]". }}
		OPTIONAL {{ ?item wdt:P77 ?Date_of_birth. }}
		OPTIONAL {{ ?item p:P77/psv:P77 [ wikibase:timePrecision ?Date_of_birth_precision; wikibase:timeCalendarModel ?Date_of_birth_calendar] }}
		OPTIONAL {{ ?item wdt:P154 ?Gender. }}
		OPTIONAL {{ ?item wdt:P83 ?Place_of_address. }}
		OPTIONAL {{ ?item wdt:P295 ?From. }}
		OPTIONAL {{ ?item wdt:P82 ?Place_of_birth. }}
		OPTIONAL {{ ?item wdt:P38 ?Date_of_death. }}
		OPTIONAL {{ ?item p:P38/psv:P38 [ wikibase:timePrecision ?Date_of_death_precision; wikibase:timeCalendarModel ?Date_of_death_calendar] }}
		OPTIONAL {{ ?item wdt:P84 ?Married_to. }} 
		OPTIONAL {{ ?item wdt:P189 ?Image. }} 
		OPTIONAL {{ ?item wdt:P182 ?Date_of_confirmation. }}
		OPTIONAL {{ ?item p:P182/psv:P182 [ wikibase:timePrecision ?Date_of_confirmation_precision; wikibase:timeCalendarModel ?Date_of_confirmation_calendar] }}
		OPTIONAL {{ ?item wdt:P168 ?Place_of_Death. }}
		OPTIONAL {{ ?item wdt:P37 ?Date_of_baptism. }}
		OPTIONAL {{ ?item p:P37/psv:P37 [ wikibase:timePrecision ?Date_of_baptism_precision; wikibase:timeCalendarModel ?Date_of_baptism_calendar] }}
		OPTIONAL {{ ?item wdt:P76 ?GND_ID. }}
		OPTIONAL {{ ?item wdt:P247 ?Surname. }}
		OPTIONAL {{ ?item wdt:P169 ?Place_of_baptism. }}
		OPTIONAL {{ ?item wdt:P79 ?Grave. }}
		OPTIONAL {{ ?item wdt:P40 ?Date_of_burial. }}
		OPTIONAL {{ ?item p:P40/psv:P40 [ wikibase:timePrecision ?Date_of_burial_precision; wikibase:timeCalendarModel ?Date_of_burial_calendar] }}
		OPTIONAL {{ ?item wdt:P142 ?Mother. }}
		OPTIONAL {{ ?item wdt:P141 ?Father. }} }} LIMIT 1"""

    def get_geo_property(self, agent_id, property_id, lang="DE"):
        return f"""SELECT ?item ?Place ?PlaceLabel ?Latitude ?Longitude
        WHERE {{ VALUES ?item {{ wd:{agent_id} }}
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{lang},[AUTO_LANGUAGE]". }}
        ?item wdt:{property_id} ?Place.
        ?Place p:P48/psv:P48 [ wikibase:geoLatitude ?Latitude; wikibase:geoLongitude ?Longitude] }}"""

    def get_list(self, agent_id, property_id, lang="DE"):
        return f"""SELECT ?item ?property ?propertyLabel
        WHERE {{ VALUES ?item {{ wd:{agent_id} }}
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{lang},[AUTO_LANGUAGE]". }}
        OPTIONAL {{ ?item wdt:{property_id} ?property. }} }}"""

    def get_relations(self, agent_id, relation_id, lang="DE"):
        return f"""SELECT ?item ?property ?propertyLabel
        WHERE {{ VALUES ?item {{ wd:{agent_id} }}
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{lang},[AUTO_LANGUAGE]". }}
        ?item p:P703 ?properties.
        ?properties ps:P703 ?property.
        ?properties pq:P820 wd:{relation_id}. }}"""

    def get_agents(self, keyword, birth_from, birth_to, lang="DE"):
        # Not in use yet
        keyword_filter_string = ""
        birth_filter_string = """OPTIONAL {{ ?item wdt:P77 ?Date_of_birth. }}"""
        if len(keyword):
            keyword_filter_string = """FILTER regex(?itemLabel, "{keyword}", "i") """

        if len(birth_from)==4 and len(birth_to)==4:
            print(birth_to, birth_from)
            if 1000 < int(birth_from) < 2100 and 1000 < int(birth_to) < 2100:
                birth_filter_string = f"""?item wdt:P77 ?Date_of_birth  
                . FILTER (?Date_of_birth >= "{birth_from}-01-01"^^xsd:dateTime && ?Date_of_birth <= "{birth_to}-12-31"^^xsd:dateTime)"""

        return f"""SELECT DISTINCT ?item ?itemLabel ?itemDescription ?Date_of_birth ?Date_of_birth_precision ?Date_of_birth_calendar ?Place_of_birth ?Place_of_addressLabel ?Date_of_death ?Date_of_death_precision ?Date_of_death_calendar WHERE {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{lang},[AUTO_LANGUAGE]". }}
        ?item (wdt:P165) wd:{constants.PROJECT_ITEM}; (wdt:P2) wd:Q7.
        {birth_filter_string}
        OPTIONAL {{ ?item p:P77/psv:P77 [ wikibase:timePrecision ?Date_of_birth_precision; wikibase:timeCalendarModel ?Date_of_birth_calendar] }}
        OPTIONAL {{ ?item wdt:P82 ?Place_of_address. }}
        OPTIONAL {{ ?item wdt:P38 ?Date_of_death. }}
        OPTIONAL {{ ?item p:P38/psv:P38 [ wikibase:timePrecision ?Date_of_death_precision; wikibase:timeCalendarModel ?Date_of_death_calendar] }}
        {keyword_filter_string} }}
        ORDER BY (?itemLabel)
        LIMIT 1000"""

    def get_project_items(self):
        return f"""SELECT ?item WHERE {{
        ?item (wdt:P131) wd:{constants.PROJECT_ITEM}.
        }}"""

    def get_courts(self, lang="DE"):
        return f"""SELECT DISTINCT ?item ?itemLabel ?itemDescription ?Latitude ?Longitude ?Image WHERE {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{lang},[AUTO_LANGUAGE]". }}
        ?item (wdt:P2) wd:Q504686; (wdt:P131) wd:Q499340. 
         OPTIONAL {{ ?item p:P48/psv:P48 [ wikibase:geoLatitude ?Latitude; wikibase:geoLongitude ?Longitude] }}
         OPTIONAL {{ ?item wdt:P189 ?Image }}
         }}
        ORDER BY (?itemLabel)
        LIMIT 1000"""

    def get_court_details(self, court_id, lang="DE"):
        return f"""SELECT DISTINCT ?item ?itemLabel ?itemDescription WHERE {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{lang},[AUTO_LANGUAGE]". }}
        ?item (wdt:P165) wd:Q464939; wdt:P2 wd:Q7; wdt:P165 ?role .
        {{ ?item p:P165 ?courts . }} UNION {{ ?item p:P296 ?courts . }}
        {{ ?courts pq:P267 wd:{court_id} . }} UNION {{ ?courts pq:P47 wd:{court_id} . }}
        OPTIONAL {{ ?item wdt:P77 ?Date_of_birth. }}
        OPTIONAL {{ ?item p:P77/psv:P77 [ wikibase:timePrecision ?Date_of_birth_precision; wikibase:timeCalendarModel ?Date_of_birth_calendar] }}
        }}
        ORDER BY ASC(?Date_of_birth)
        LIMIT 1000"""
