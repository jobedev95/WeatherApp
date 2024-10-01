from typing import Any
import sys
from forecast_data import ForecastData
from current_weather_data import CurrentWeatherData
import logging
from weather_manager import WeatherManager
from historical_data import HistoricalData, HistoricalManager

# from historical_data import HistoricalData.
import logo

# Ställer in konfigurationen för loggning. Den skapar en fil med namnet "my_log.log" som skrivs över varje gång programmet körs.
# Det angivna formatet gör att varje logg har ett datum, namn på modulen som felet härstammar ifrån, loggnivå samt felmeddelandet.
logging.basicConfig(filename="my_log.log", filemode="w", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

#! Lägg till OpenWeatherMap och WorldWeatherOnline API Nycklarna här
OPENWEATHERMAP_API_KEY: str = ""
WORLDWEATHERONLINE_API_KEY: str = ""  # API nyckel klistras in här.


def main() -> None:
    logo.print_logo()  # Printar programloggan.

    # Skapar en ny instans av WeatherManager, som hanterar programlogiken för inhämtning av extern indata.
    weather: WeatherManager = WeatherManager(OPENWEATHERMAP_API_KEY)
    forecast_type: str = weather.get_forecast_choice()  # Hämtar in användarens val för typ av väderprognos.

    # Om användaren har valt att få historisk väderinformation körs koden nedan
    if forecast_type == "Historisk Väderinformation":
        while True:
            historical_weather = HistoricalManager(WORLDWEATHERONLINE_API_KEY)
            try:
                data: Any = historical_weather.get_historical_data()
                historical_data: HistoricalData = HistoricalData(data)
                break
            except Exception:
                print(
                    f"\nKunde inte hämta historisk väderinformation. Kontrollera att stavningen är korrekt och att datumet är rätt formaterat!\n"
                )
        historical_data.print_historical_data()

    # Om användaren har valt att få nuvarande väder eller en femdagarsväderprognos körs koden nedan
    else:
        # Försöker hämta in väderdatan genom OpenWeatherMap API.
        try:
            data: dict = weather.fetch_data(forecast_type)
            # Om användaren enbart ska ha nuvarande väder körs kodblocket nedan.
            if forecast_type == "Nuvarande Väder":
                weather_data: CurrentWeatherData = CurrentWeatherData(data)  # Skapar ett objekt för nuvarande väderprognos.
                weather_data.print_weather()  # Printar ut nuvarande väder.

            # Om användaren ska ha en 5-dagars prognos körs kodblocket nedan.
            else:
                forecast: ForecastData = ForecastData(data)  # Skapar ett objekt för fem dagars väderprognos.
                forecast.print_forecast_data(width=40)  # Printar fem dagars prognosen.
        except Exception:
            # Printar ett felmeddelande om inhämtningen gick fel.
            print("\nKunde inte hämta väderinformation. Kontrollera att stavningen är korrekt eller att postnumret är rätt formaterat!\n")


if __name__ == "__main__":
    main()
