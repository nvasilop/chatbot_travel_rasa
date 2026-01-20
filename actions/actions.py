from rasa_sdk import Action, Tracker
from datetime import datetime, timedelta
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List, Text
import requests

class ActionShowDestinations(Action):

    def name(self):
        return "action_show_destinations"

    def run(self, dispatcher, tracker, domain):

        destinations = ["Paris", "Rome", "Barcelona", "London", "Athens", "Berlin", "Amsterdam"]

        dispatcher.utter_message(
            text=f"Here are some destinations in Europe: {', '.join(destinations)}"
        )

        return []


class ActionAskWeather(Action):

    def name(self):
        return "action_ask_weather"

    def run(self, dispatcher, tracker, domain):

        city = tracker.get_slot("city")

        if not city:
            dispatcher.utter_message(
                text="Please tell me which city you want the weather for."
            )
            return []

        api_key = "c49c0bd2e4cad5bfded2dd267fc28019"

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )

        try:
            response = requests.get(url, timeout=5)
            data = response.json()

            if response.status_code != 200:
                dispatcher.utter_message(
                    text=f"Sorry, I couldn't find weather data for {city}."
                )
                return []

            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]

            dispatcher.utter_message(
                text=f"The weather in {city} is {temperature}°C with {description}."
            )

        except Exception:
            dispatcher.utter_message(
                text="Sorry, the weather service is currently unavailable."
            )

        return []

class ActionEventsCity(Action):

    def name(self) -> Text:
        return "action_events_city"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")

        if not city:
            dispatcher.utter_message(
                text="Please tell me which city you are interested in."
            )
            return []

        # ✅ City → Country mapping
        city_country = {
            "rome": "IT",
            "athens": "GR",
            "paris": "FR",
            "barcelona": "ES",
            "london": "GB",
            "berlin": "DE",
            "amsterdam": "NL"
        }

        country_code = city_country.get(city.lower())

        api_key = "GyOVkw2IzILfDhhOnh1hbwMI4neSEtLI"
        url = "https://app.ticketmaster.com/discovery/v2/events.json"

        params = {
            "apikey": api_key,
            "city": city,
            "countryCode": country_code,
            "size": 5,
            "sort": "date,asc"
        }

        try:
            response = requests.get(url, params=params, timeout=6)
            data = response.json()

            # If API returns no events at all
            events = data.get("_embedded", {}).get("events", [])

            message = f"🎉 Upcoming events in {city.title()}:\n"
            found = False

            for event in events:
                venue = event["_embedded"]["venues"][0]
                venue_country = venue.get("country", {}).get("countryCode", "")

                # ✅ filter wrong-country cities
                if country_code and venue_country != country_code:
                    continue

                name = event.get("name", "Unknown event")
                date = event["dates"]["start"].get("localDate", "Unknown date")
                venue_name = venue.get("name", "Unknown venue")

                message += (
                    f"\n• {name}"
                    f"\n  📅 {date}"
                    f"\n  📍 {venue_name}"
                )

                found = True

            if not found:
                dispatcher.utter_message(
                    text=(
                        f"Ticketmaster currently has no available events "
                        f"for {city.title()}.\n"
                        f"This depends on event organizer coverage."
                    )
                )
                return []

            dispatcher.utter_message(text=message)

        except Exception as e:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve events right now."
            )

        return []

class ActionAskLocalTime(Action):

    def name(self) -> Text:
        return "action_ask_local_time"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")

        if not city:
            dispatcher.utter_message(
                text="Please tell me which city you want the local time for."
            )
            return []

        api_key = "c49c0bd2e4cad5bfded2dd267fc28019"

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )

        try:
            response = requests.get(url, timeout=6)
            data = response.json()

            if response.status_code != 200:
                dispatcher.utter_message(
                    text=f"I couldn't find time information for {city.title()}."
                )
                return []

            timezone_offset = data.get("timezone")

            if timezone_offset is None:
                dispatcher.utter_message(
                    text="Timezone data is not available for this city."
                )
                return []

            utc_time = datetime.utcnow()
            local_time = utc_time + timedelta(seconds=timezone_offset)

            dispatcher.utter_message(
                text=(
                    f"🕒 Local time in {city.title()} is "
                    f"{local_time.strftime('%H:%M')}."
                )
            )

        except Exception as e:
            dispatcher.utter_message(
                text="Sorry, the time service is currently unavailable."
            )

        return []
