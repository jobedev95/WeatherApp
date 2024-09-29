from typing import Any
import sys
from forecast_data import ForecastData
from weather_data import WeatherData
import logging
from weather_history_manager import WeatherHistoryManager
from history_data import HistoryData
from weather_manager import WeatherManager
import logo

logging.basicConfig(filename="my_log.log", filemode="w", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

OPENWEATHERMAP_API_KEY = ""


def main() -> None:
    logo.print_logo()
    weather: Any = WeatherManager(OPENWEATHERMAP_API_KEY)
    forecast_type: str = weather.get_forecast_choice()
    try:
        data: dict[Any, Any] = weather.attempt_search(forecast_type)
    except ValueError as e:
        print(e)
        sys.exit()

    # Om användaren enbart ska ha nuvarande väder
    if forecast_type == "weather?":
        weather_data = WeatherData(data)
        weather_data.print_weather()

    # Om användaren ska ha en 5-dagars prognos
    else:
        forecast = ForecastData(data)
        forecast.prepare_forecast()


if __name__ == "__main__":
    main()
