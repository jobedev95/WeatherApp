from typing import Any
from box_print import box_print_title, box_print_body, box_print_footer


class CurrentWeatherData:
    """Hanterar och printar nuvarande väderprognosdata i lämpligt format."""

    def __init__(self, weather_data: dict) -> None:
        self.city: str = weather_data["name"]  # Sparar stadsnamn
        self.temperature: float = weather_data["main"]["temp"]  # Sparar temperatur
        self.feels_like: float = weather_data["main"]["feels_like"]  # Sparar känns-som temperatur
        self.weather_description: str = weather_data["weather"][0]["description"]  # Sparar väderbeskrivning
        self.weather_id: int = weather_data["weather"][0]["id"]  # Sparar väder-id

    def print_weather(self, width: int) -> None:
        """Printar prognosdatan med en omgivande linjeram."""
        weather_icon: str = f"{self.get_weather_icon()}"  # Hämtar väderikonen som motsvarar väderid-numret
        print(weather_icon.center(width))  # Printa väderikonen

        title: str = self.city  # Sparar stadsnamnet
        box_print_title(title, width)  # Printa rubriken med en överkant

        # Printar f-strängarna med sidolinjer
        line1: str = f"Temperatur: {self.temperature} °C, {self.weather_description.capitalize()}"
        line2: str = f"Känns som: {self.feels_like} °C"
        box_print_body(line1, width)  # Printar line1
        box_print_body(line2, width)  # Printar line2
        box_print_footer(width)  # Printa nedre kant

    def get_weather_icon(self) -> str:
        """Returnerar en väderikon (emoji) som motsvarar prognosdatans väderkod."""

        symbol: str = ""
        # Match-case som söker efter en matchning med den första siffran i väder-id:t
        match str(self.weather_id)[0]:
            case "2":
                # Åska
                symbol = "⚡️⚡️"
            case "3" | "5":
                # Duggregn / Regn
                symbol = "🌧️"
            case "6":
                # Snö
                symbol = "🌨️"
            case "7":
                # Atmosfär (dimma)
                symbol = "🌁"
            case "8":
                if self.weather_id == 800:
                    # Klart väder
                    symbol = "🌞"
                else:
                    # Molnigt
                    symbol = "🌤️"
            case _:
                pass
        return symbol
