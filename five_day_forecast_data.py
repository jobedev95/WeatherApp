from datetime import datetime
from typing import Any
from box_print import box_print_title, box_print_body, box_print_footer


class FiveDayForecastData:
    """Hanterar och printar fem dagars väderprognosdata i lämpligt format."""

    def __init__(self, weather_data: dict, unit: str) -> None:
        self.city: str = weather_data["city"]["name"]  # Sparar stadsnamn
        self.forecast_data: list[Any] = weather_data["list"]  # Sparar en lista med dictionaries
        if unit == "metric":
            self.unit: str = "C"
        else:
            self.unit = "F"

    def print_forecast_data(self, width: int) -> None:
        """Printar ut all prognosdata för dom kommande 120 timmarna tillsammans.
        Varje datum med dess tidsprognoser blir omgivet av en linjeram med en angiven bredd."""
        seen_dates: list[str] = []  # Lista som ska spara alla datum som loopen har gått genom

        # Loopar genom varje värde i den inhämtade prognosdatan
        for index, item in enumerate(self.forecast_data):
            # Hämtar in tidsprognosens datum från varje iteration. Datumet i APIn ser ut på detta sätt: "2024-10-01 12:00:00"
            date = item["dt_txt"][0:10]  # Slicear ut datumet från strängen YYYY-MM-DD
            time = item["dt_txt"][11:16]  # Slicear ut tiden från strängen HH:MM

            # Om datumet i iterationen inte har setts tidigare ska datumet printas utför att inleda en utskriften av ny dag
            if date not in seen_dates:
                seen_dates.append(date)  # Registrera det nya datumet
                box_print_title(date, width)  # Printar datumet

            # Skapar en sträng för varje tidsprognos. Exempel på hur strängen kan komma att se ut: '14:00: 23 °C, Klart väder'
            new_line: str = f"{time}: {item['main']['temp']} °{self.unit}, {item['weather'][0]['description'].capitalize()}"
            box_print_body(new_line, width)

            # Om tiden i iterationen är 23:00 eller om det är den sista iterationen ska en footer printas
            if time == "21:00" or index == len(self.forecast_data) - 1:
                if seen_dates:
                    box_print_footer(width)
