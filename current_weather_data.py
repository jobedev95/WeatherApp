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

    def print_weather(self) -> None:
        """Printar prognosdatan med en omgivande linjeram."""
        weather_icon, title, lines = self._prepare_for_print()

        border_width: int = 45  # Ange bredden på linjeramen
        print(weather_icon.center(border_width))  # Printa väderikonen
        box_print_title(title, border_width)  # Printa rubriken med en överkant

        # Loop som printar ut alla strängar i variabeln lines med sidolinjer
        for line in lines:
            box_print_body(line, border_width)
        box_print_footer(border_width)  # Printa nedre kant

    def _prepare_for_print(self) -> tuple[str, str, list[str]]:
        """Förbereder väderdatan för att printas genom att formatera strängar i ett visst format."""
        weather_icon: str = f"{self.get_weather_icon()}"  # Hämtar väderikonen som motsvarar väderid-numret
        title: str = self.city  # Sparar stadsnamnet

        # Skapar de olika meningarna som ska printas ut och lägger dem i en lista
        lines: list[str] = []
        lines.append(f"Temperatur: {self.temperature} °C, {self.weather_description.capitalize()}")
        lines.append(f"Känns som: {self.feels_like} °C")
        return (weather_icon, title, lines)  # Returnerar alla tre värden i en tuple

    def get_weather_icon(self) -> str:
        """Returnerar en väderikon (emoji) som motsvarar prognosdatans väderkod."""
        symbol: str = ""
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
