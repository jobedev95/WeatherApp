from typing import Any
import sys
from forecast_data import ForecastData
from current_weather_data import CurrentWeatherData
import logging
from weather_manager import WeatherManager
import logo

# Ställer in konfigurationen för loggning. Den skapar en fil med namnet "my_log.log" som skrivs över varje gång programmet körs.
# Det angivna formatet gör att varje logg har ett datum, namn på modulen som felet härstammar ifrån, loggnivå samt felmeddelandet.
logging.basicConfig(filename="my_log.log", filemode="w", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

#! Lägg till OpenWeatherMap API Nyckeln här
OPENWEATHERMAP_API_KEY: str = ""


def main() -> None:
    logo.print_logo()  # Printar programloggan
    weather: Any = WeatherManager(OPENWEATHERMAP_API_KEY)
    forecast_type: str = weather.get_forecast_choice()

    # Försöker hämta in väderdatan genom OpenWeatherMap API
    try:
        data: dict[Any, Any] = weather.attempt_search(forecast_type)
    except ValueError as e:
        # Printar ett felmeddelande om inhämtningen gick fel och avslutar programmet.
        print(e)
        sys.exit()

    # Om användaren enbart ska ha nuvarande väder körs kodblocket nedan
    if forecast_type == "weather?":
        weather_data = CurrentWeatherData(data)  # Skapar ett objekt för nuvarande väderprognos
        weather_data.print_weather()  # Printar ut nuvarande väder

    # Om användaren ska ha en 5-dagars prognos körs kodblocket nedan
    else:
        forecast = ForecastData(data)  # Skapar ett objekt för fem dagars väderprognos
        forecast.print_full_day_forecasts()  # Printar ut femdagars-prognosen


if __name__ == "__main__":
    main()
