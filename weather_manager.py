import pyinputplus as py
import requests
from requests import Response
import geocoder
from typing import Any


class WeatherManager:
    """Hanterar inhämtning av extern indata såsom användarens input för typ av prognos, stadsnamn eller postnummer, och IP-adressens koordinater.
    Dessa används sedan för att forma den URL-sträng som behövs för inhämtning av väderprognoserna, antingen nuvarande väder eller en 5-dagars prognos."""

    def __init__(self, openweathermap_api_key: str) -> None:
        self.API_KEY: str = openweathermap_api_key  # Tilldelar den angivna API-nyckeln

    def get_forecast_choice(self) -> str:
        """Frågar användaren om vilken typ av väderprognos som ska hämtas.
        Returnerar den relevanta url-strängen för den angivna prognostypen,
        antingen 'weather?' eller 'forecast?'"""

        menu_choices: list[str] = ["Nuvarande Väder", "5 Dagars Prognos", "Historisk Väderinformation"]
        user_choice: str = py.inputMenu(prompt="\nAnge typ av väderprognos:\n", choices=menu_choices, numbered=True)

        return user_choice

    def get_search_choice(self) -> str:
        """Frågar användaren om vilken typ av sökning som ska göras.
        Returnerar den parametersträng som krävs för söktypen i API URL-länken,
        exempelvis '&q={city_name}' för en stadssökning."""

        menu_choices: list[str] = ["Stad", "Postnummer", "Nuvarande Plats"]
        user_choice: str = py.inputMenu(prompt="\nAnge typ av sökning:\n", choices=menu_choices, numbered=True)

        type_of_search: str = ""
        match user_choice:
            case "Stad":
                city_name: str = py.inputStr(prompt="\nAnge stad: ")
                type_of_search = f"&q={city_name}"  # Skapar parametersträngen som ska användas i API URL-länken
            case "Postnummer":
                try:
                    location: Any = self.get_location()  # Hämtar platsinformation baserat på användarens IP-adress
                except Exception:
                    print("Kunde inte hämta platsdata.")

                country_code: str = location.country  # Tar fram landskoden (ex. "SE" för Sverige)
                zip_code: str = self.get_zip_code()  # Hämtar in postnummer från användaren i formatet "xxx xx"
                type_of_search = f"&zip={zip_code},{country_code}"  # Skapar parametersträngen som ska användas i API URL-länken
            case "Nuvarande Plats":
                try:
                    location = self.get_location()  # Hämtar platsinformation baserat på användarens IP-adress
                    lat, lon = location.latlng  # Hämtar latitud och longitud koordinaterna från den inhämtade platsinformationen
                    type_of_search = f"&lat={lat}&lon={lon}"  # Skapar parametersträngen som ska användas i API URL-länken
                except Exception:
                    print("Kunde inte hämta platsdata.")
            case _:
                pass
        return type_of_search  # Returnerar parametersträngen

    def get_zip_code(self) -> str:
        """Hämtar in postnummer från användaren. Returnerar det i formatet "xxx xx"."""

        # En while-loop som loopar så länge användaren inte anger ett femsiffrigt nummer
        while True:
            zip_code: int = py.inputInt(prompt="\nAnge postnummer: ")  # Hämtar in postnumret i form av heltal
            zip_code_string: str = str(zip_code)  # Konverterar värdet till en sträng

            if len(zip_code_string) == 5:  # Kontrollerar att det angivna postnumret är 5 siffror långt
                zip_code_string = f"{zip_code_string[:3]} {zip_code_string[3:]}"  # Gör om formatet av siffrorna till "xxx xx"
                break  # Breakar loopen
        return zip_code_string  # Returnerar postnumret

    def get_location(self) -> Any:
        """Hämtar platsinformation genom användaren IP-adress. Returnerar platsinformationen eller None vid fel."""
        try:
            location: Any = geocoder.ip("me")  # Hämtar platsinformation med hjälp av geocoder-modulen och dess ip() funktion
            return location  # Returnerar platsinformationen
        except Exception as e:
            print(f"Kunde inte hämta platsinformation. Felmeddelande: {e}")
            return None

    def fetch_data(self, chosen_forecast: str) -> Any:
        """Försöker hämta in väderdata från OpenWeatherMap.
        Returnerar JSON-encodad väderdata vid lyckad inhämtning."""

        # If-sats som avgör vilken sträng som ska användas i URL-länken.
        if chosen_forecast == "Nuvarande Väder":
            forecast_type = "weather?"
        elif chosen_forecast == "5 Dagars Prognos":
            forecast_type = "forecast?"

        attempt_search: bool = True
        while attempt_search:
            try:
                # Anropar metoden get_search_choice() för att inhämta URL-strängen för söktyp
                search_type: str = self.get_search_choice()

                # Skapar URL-länken
                url: str = f"https://api.openweathermap.org/data/2.5/{forecast_type}appid={self.API_KEY}&units=metric&lang=sv{search_type}"

                # Försöker hämta in json-datan från URL-länken
                response: Response = requests.get(url)  # Hämtar API datan och tilldelar den till en variabel

                # Kontrollerar att inhämtningen gick bra
                response.raise_for_status()

                # Konverterar json-datan och returnerar värdet
                return response.json()
            except Exception as e:
                print(
                    f"\nNågot gick fel med sökningen. Kontrollera att du stavade rätt och att du har en internetanslutning!\nFelmeddelande:\n{e}\n"
                )
                if py.inputYesNo("\nVill du försöka igen? (y/n): ") == "no":
                    print("Tack för att du använder vår väderapp. Hejdå!")
                    attempt_search = False
