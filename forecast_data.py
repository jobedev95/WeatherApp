from datetime import datetime
from typing import Any


class ForecastData:
    """Hanterar och printar fem dagars väderprognosdata i lämpligt format."""

    def __init__(self, weather_data: dict[Any, Any]) -> None:
        self.forecast_data: list[Any] = []
        self.city: str = weather_data["city"]["name"]  # Sparar stadsnamn
        self.forecast_data = weather_data["list"]  # Sparar en lista med dictionary

    def print_forecast_data(self, width: int) -> None:
        """Printar ut all prognosdata för dom kommande 120 timmarna tillsammans.
        Varje datum med dess tidsprognoser blir omgivet av en linjeram med en angiven bredd."""
        seen_dates: list[str] = []  # Lista som ska spara alla datum som loopen har gått genom

        # Loopar genom varje värde i den inhämtade prognosdatan
        for index, item in enumerate(self.forecast_data):
            # Konverterar UNIX-tidsstämpel till datetime objekt
            datetime_object: datetime = datetime.fromtimestamp(item["dt"])

            # Hämtar in tidsprognosens datum från varje iteration,
            # strftime() funktionen extraherar det i formatet YYYY-MM-DD respektive HH:MM som strängar
            date: str = datetime_object.strftime("%Y-%m-%d")
            time: str = datetime_object.strftime("%H:%M")

            # Om datumet i iterationen inte har setts tidigare ska datumet printas utför att inleda en utskriften av ny dag
            if date not in seen_dates:
                seen_dates.append(date)  # Registrera det nya datumet
                self._print_title(date, width)  # Printar datumet

            # Skapar en sträng för varje tidsprognos. Exempel på hur strängen kan komma att se ut: '14:00: 23 °C, Klart väder'
            new_line: str = time + f'{item['main']['temp']} °C, {item["weather"][0]["description"].capitalize()}'
            self._print_body(new_line, width)

            # Om tiden i iterationen är 23:00 eller om det är den sista iterationen ska en footer printas
            if time == "23:00" or index == len(self.forecast_data) - 1:
                if seen_dates:
                    self._print_footer(width)

    def _print_title(self, title: str, width: int) -> None:
        """Printar en rubrik ihop med en överkantlinje och hörn. Centrerar om should_center=True"""
        print("┌" + f"  {title}  ".center(width, "─") + "┐")

    def _print_body(self, body: str, width: int) -> None:
        """Printar brödtexten eller innehållet för en ruta ihop med sidolinjer. Centrerar om should_center=True"""
        print(f"│ {body}".ljust(width) + " │")

    def _print_footer(self, width: int) -> None:
        """Printar en underkant ihop med en hörn. Centrerar om should_center=True"""
        print("└" + "─" * width + "┘")
