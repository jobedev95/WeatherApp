import requests
import pyinputplus as pyip
from box_print import box_print_title, box_print_body, box_print_footer
from typing import Any


class HistoricalData:
    def __init__(self, data) -> None:
        self.data: dict = data
        self.query: str = self.data["data"]["request"][0]["query"]  # Hämtar vad för stad samt land som datan representerar
        self.date: str = self.data["data"]["weather"][0]["date"]  # Hämtar datum
        self.sun_hours: str = self.data["data"]["weather"][0]["sunHour"]  # Hämtar totala soltimmar
        self.max_temp: str = self.data["data"]["weather"][0]["mintempC"]  # Hämtar max temperatur
        self.min_temp: str = self.data["data"]["weather"][0]["mintempC"]  # Hämtar lägst temperatur

    def print_historical_data(self) -> None:
        """Skriver ut all historisk väderdata som hämtats."""
        border_width: int = 40
        print("\nHere is the data you requested:\n")
        box_print_title(f"{self.query}", border_width)
        box_print_body(f"Date: {self.date}", border_width)
        box_print_body(f"Highest temperature: {self.max_temp}°C", border_width)
        box_print_body(f"Lowest temperature: {self.min_temp}°C", border_width)
        box_print_body(f"Total sun hours: {int(float(self.sun_hours))}h", border_width)
        box_print_footer(border_width)


class HistoricalManager:
    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key

    def get_historical_data(self) -> Any:
        attempt_search = True
        while attempt_search:  # Loop för att kunna söka efter flera städer utan att programmet avslutas
            try:
                city: str = input("\nAnge stad: ")
                date: str = pyip.inputDate(
                    prompt="\nAnge datum som du vill ha historisk väderdata på.\n"
                    "OBS: tidigaste godtagbara datumet är 2008/07/01.\n"
                    "Formatet måste vara i YYYY/MM/DD: "
                )
                result = self.fetch_historical_data(
                    city, date
                )  # Tar input från användaren och skickar upp det till metoden för att kunna skapa API-länken
                return result
            except Exception as e:  # Ifall det inte skulle gå att hämta data som förväntat så kommer denna utskrift att köras.
                print(
                    f"\nEtt fel uppstod när historiska datan skulle hämtas. Vänligen kontrollera att du har en internetanslutning!\nFelmeddelande: {e}"
                )
                if pyip.inputYesNo("\nVill du försöka igen? (y/n): ") == "no":
                    print("Tack för att du använder vår väderapp. Hejdå!")
                    attempt_search = False

    def fetch_historical_data(self, city: str, date: str) -> Any:
        historical_url: str = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={}&format=json&q={}&date={}".format(
            self.api_key, city, date
        )  # Hela API länken
        response: requests.Response = requests.get(historical_url)  # Hämtar API länk och tilldelar den till en variabel

        historical_weather_data = response.json()  # Formaterar om hämtningen till json fil
        return historical_weather_data
