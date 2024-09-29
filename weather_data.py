from typing import Any


class WeatherData:
    """Hanterar och printar dagens väderprognosdata i lämpligt format."""

    def __init__(self, weather_data: dict[Any, Any]) -> None:
        self.city: str = weather_data["name"]  # Sparar stadsnamn
        self.temperature: float = weather_data["main"]["temp"]  # Sparar temperatur
        self.feels_like: float = weather_data["main"]["feels_like"]  # Sparar känns-som temperatur
        self.weather_description: str = weather_data["weather"][0]["description"]  # Sparar väderbeskrivning
        self.weather_id: int = weather_data["weather"][0]["id"]  # Sparar väder-id

    def print_weather(self) -> None:
        """Förbereder den inhämtade väderdatan för att printas och printar den sedan med en omgivande linjeram."""
        header, title, lines = self._prepare_for_print()
        self._print_with_border(header, title, lines)

    def _prepare_for_print(self) -> tuple[str, str, list[str]]:
        """Förbereder väderdatan för att printas genom att formatera strängar i ett visst format."""
        # Skapar rubriken med stadsnamn och väderikon
        header: str = f"{self.get_weather_icon()}"
        title: str = f"{self.city}"
        lines: list[str] = []

        # Skapar de olika meningarna som ska printas ut och lägger dem i en lista
        lines.append(f"Temperatur: {self.temperature} °C, {self.weather_description.capitalize()}")
        lines.append(f"Känns som: {self.feels_like} °C")
        return (header, title, lines)

    def _print_with_border(self, header: str, title: str, lines: list[str]) -> None:
        """Printar den angivna prognosdatan med en omgivande linjeram."""
        border_width = 45
        # Printa väderikonen
        print(header.center(border_width))
        # Printa rubrik med linjer och hörn
        print("┌" + f"  {title}  ".center(border_width - 1, "─") + "┐")

        # Printa alla meningar tillsammans med kantlinjer
        for sentence in lines:
            print(f"│ {sentence}".ljust(border_width) + "│")

        # Printa nedre linje med hörn
        print("└" + "─" * (border_width - 1) + "┘")

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
