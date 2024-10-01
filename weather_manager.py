import pyinputplus as py
import requests
from requests import Response
import geocoder
import sys
from typing import Any


class WeatherManager:
    """Hanterar inhämtning av extern indata såsom användarens input för typ av prognos, stadsnamn eller postnummer, och IP-adressens koordinater.
    Dessa används sedan för att forma den URL-sträng som behövs för inhämtning av väderprognoserna, antingen nuvarande väder eller en 5-dagars prognos."""

    def __init__(self, openweathermap_api_key: str) -> None:
        self.API_KEY: str = openweathermap_api_key

    def get_forecast_choice(self) -> str:
        """Frågar användaren om vilken typ av väderprognos som ska hämtas.
        Returnerar den relevanta url-strängen för den angivna prognostypen,
        antingen 'weather?' eller 'forecast?'"""

        menu_choices: list[str] = ["Nuvarande Väder", "5 Dagars Prognos", "Historisk Väderinformation"]
        user_choice: str = py.inputMenu(prompt="\nAnge typ av väderprognos:\n", choices=menu_choices, numbered=True)

        return user_choice

    def get_search_choice(self) -> str:
        """Frågar användaren om vilken typ av sökning som ska göras.
        Returnerar den relevanta url-strängen för söktypen,
        exempelvis '&q={city_name}' för en stadssökning."""

        menu_choices: list[str] = ["Stad", "Postnummer", "Nuvarande Plats"]
        user_choice: str = py.inputMenu(prompt="\nAnge typ av sökning:\n", choices=menu_choices, numbered=True)

        type_of_search: str = ""
        match user_choice:
            case "Stad":
                city_name: str = py.inputStr(prompt="\nAnge stad: ")
                type_of_search = f"&q={city_name}"  # Skapar parametersträngen som ska användas i API URL-länken
            case "Postnummer":
                location: Any = self.get_location()  # Hämtar platsinformation baserat på användarens IP-adress
                country_code: str = location.country  # Tar fram landskoden (ex. "SE" för Sverige)
                zip_code: str = self.get_zip_code()  # Hämtar in postnummer från användaren i formatet "xxx xx"
                type_of_search = f"&zip={zip_code},{country_code}"  # Skapar parametersträngen som ska användas i API URL-länken
            case "Nuvarande Plats":
                try:
                    location = self.get_location()  # Hämtar platsinformation baserat på användarens IP-adress
                except Exception:
                    print("Kunde inte hämta platsdata.")
                    sys.exit()
                if location is not None:
                    lat, lon = location.latlng
                    type_of_search = f"&lat={lat}&lon={lon}"  # Skapar parametersträngen som ska användas i API URL-länken
            case _:
                pass

        return type_of_search

    def get_zip_code(self) -> str:
        """Hämtar in postnummer från användaren. Returnerar det i formatet "xxx xx"."""
        while True:
            zip_code: int = py.inputInt(prompt="\nAnge postnummer: ")
            zip_code_string: str = str(zip_code)
            if len(zip_code_string) == 5:
                zip_code_string = f"{zip_code_string[:3]} {zip_code_string[3:]}"
                break
        return zip_code_string

    def get_location(self) -> Any:
        """Hämtar platsinformation genom användaren IP-adress. Returnerar platsinformationen eller None vid fel."""
        try:
            location: Any = geocoder.ip("me")
            return location
        except Exception as e:
            print(f"Kunde inte hämta platsinformation. Felmeddelande: {e}")
            return None

    def fetch_data(self, chosen_forecast: str) -> dict[Any, Any]:
        """Försöker hämta in väderdata från OpenWeatherMap.
        Returnerar JSON-encodad väderdata vid lyckad inhämtning."""

        if chosen_forecast == "Nuvarande Väder":
            forecast_type = "weather?"
        elif chosen_forecast == "5 Dagars Prognos":
            forecast_type = "forecast?"

        attempt_search: bool = True
        while attempt_search:
            try:
                search_type: str = self.get_search_choice()
                url: str = f"https://api.openweathermap.org/data/2.5/{forecast_type}appid={self.API_KEY}&units=metric&lang=sv{search_type}"
                response: Response = requests.get(url)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(
                    f"\nNågot gick fel med sökningen. Kontrollera att du stavade rätt och att du har en internetanslutning!\nFelmeddelande:\n{e}"
                )
                return e
        raise ValueError("\nLyckades inte hämta väderdata!")
