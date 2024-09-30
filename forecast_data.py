from datetime import datetime
from typing import Any


class ForecastData:
    """Hanterar och printar fem dagars väderprognosdata i lämpligt format."""

    def __init__(self, weather_data: dict[Any, Any]) -> None:
        self.forecast_data: list[Any] = []
        self.city: str = weather_data["city"]["name"]  # Sparar stadsnamn

        # Loopar genom varje tidpunkt i väderprognosen
        for item in weather_data["list"]:
            # Konverterar UNIX-tidsstämpel till datetime objekt
            datetime_object: datetime = datetime.fromtimestamp(item["dt"])

            self.forecast_data.append(
                {
                    "date": datetime_object,  # Sparar datumet
                    "feels_like": item["main"]["feels_like"],  # Sparar känns-som temperatur
                    "temp": item["main"]["temp"],  # Sparar temperaturen
                    "temp_min": item["main"]["temp_min"],  # Sparar minimum temperaturen
                    "temp_max": item["main"]["temp_max"],  # Sparar maximum temperaturen
                    "weather_description": item["weather"][0]["description"],  # Sparar väderbeskrivning
                    "weather_id": item["weather"][0]["id"],  # Sparar väder-id
                }
            )

    def _prepare_forecast_data(self) -> list[dict[Any, Any]]:
        """Förbereder väderprognosdata för fem dagar genom att organisera och dela upp
        prognosdatan i fem separata delar efter datum. Skapar och returnerar en lista med fem dictionaries
        där varje dictionary innehåller alla väderprognoser för en specifik dag.

        OpenWeatherMaps API ger en fem dagars väderprognos som innehåller 40 tidpunkter,
        en för var tredje timme, över en period av totalt 120 timmar. Man måste därför på något
        sätt gruppera ihop de tidpunkter som tillhör samma datum, vilket är syftet med denna metod.
        """

        # Lista som ska samla in alla väderkoder från alla dagar, viktigt för väderikonerna ska printas
        weather_ids: dict[str, list[int]] = {}

        # Lista som ska samla in alla strängar som ska printas ut
        forecast_lines: dict[str, list[str]] = {}

        # För varje tidpunkt i prognosdatan, skapa en ny nyckel för en dictionary och initialisera en lista
        for time_forecast in self.forecast_data:
            # Hämtar in tidsprognosens datum från varje iteration,
            # strftime() funktionen extraherar det i formatet YYYY-MM-DD respektive HH:MM som strängar
            date = time_forecast["date"].strftime("%Y-%m-%d")
            time = time_forecast["date"].strftime("%H:%M")

            # Om datumet inte är en nyckel som existerar ännu i forecast_lines så initieras en
            # ny dictionary där nyckeln är datumet som just hämtades. Värdet den får är en tom lista.
            if date not in forecast_lines:
                forecast_lines[date] = []  # Behövs för att spara alla tidsprognossträngar
                weather_ids[date] = []

            # Skapar en sträng för varje tidsprognos. Exempel på hur strängen kan komma att se ut: '14:00: 23 °C, Klart väder'
            new_line: str = f"{time}: " + f'{time_forecast['temp']} °C, {time_forecast["weather_description"].capitalize()}'
            forecast_lines[date].append(new_line)
            weather_ids[date].append(time_forecast["weather_id"])

        prepared_forecast_data: list[dict[Any, Any]] = []
        for date in forecast_lines.keys():
            # Hämtar väderkodens motsvarande väderikon (emoji) och sparar den i header
            avg_weather_id: int = self.get_average_weather_id(weather_ids[date])
            header: str = f"{self.get_weather_icon(avg_weather_id)}"

            # Ställer in rubrik
            title: str = date

            # Ställer in värdet för underrubriken
            subheader: str = self.city

            prepared_forecast_data.append(
                {"header": header, "title": title, "subheader": subheader, "time_forecasts": forecast_lines[date]}
            )

        return prepared_forecast_data

    def print_full_day_forecasts(self) -> None:
        """Printar ut femdagarsprognosen i ett särskilt format där den första dagen visas separat,
        och de resterande fyra dagarna printas ut i par sida vid sida. Varje prognos omges av sin egen linjeram."""

        # Anropar en funktion som förbereder den inhämtade datan genom att organisera alla tidsprognoser
        full_day_forecast: list = self._prepare_forecast_data()
        border_width = 45

        #!                                       PRINTAR DAGENS PROGNOS (Index 0)

        # Printar väderikonen över rubriken
        header: str = f'{full_day_forecast[0]['header']}'
        self._print_header(header, border_width, should_center=True)

        # Printar övre kant med hörn för en ruta med rubrik
        title: str = f"{full_day_forecast[0]['title']}"
        self._print_title(title, border_width, should_center=True)

        # Printar underrubrik med kanter på sidorna
        subheader: str = f"{full_day_forecast[0]['subheader']}"
        self._print_subheader(subheader, border_width, should_center=True)

        # Printar hela dagens väderprognos med kanter
        for value in full_day_forecast[0]["time_forecasts"]:
            body: str = f"{value}"
            self._print_body(body, border_width, should_center=True)

        # Printar nedre kant med hörn
        self._print_footer(border_width, should_center=True)

        #!                         PRINTAR RESTERANDE DAGARS PROGNOSER SIDA VID SIDA - TVÅ ÅT GÅNGEN
        # Loop för dag 2-4 (motsvarar index 1-4) med en step på 2 eftersom att det ska printas parvis (varje iteration hanterar två dagar åt gången)
        for i in range(1, 5, 2):
            # Printar väderikonerna över rubriken
            header1: str = f"{full_day_forecast[i]['header']}"
            header2: str = f"{full_day_forecast[i+1]['header']}"
            self._print_header(header1, border_width)
            self._print_header(header2, border_width)
            print()

            # Printar rubriker ihop med de övre kanterna för två rutor
            title1: str = f'{full_day_forecast[i]["title"]}'
            title2: str = f'{full_day_forecast[i+1]["title"]}'
            self._print_title(title1, border_width)
            self._print_title(title2, border_width)
            print()

            # Printar underrubrikerna med kanter på sidorna
            subheader1: str = f"{full_day_forecast[i]['subheader']}"
            subheader2: str = f"{full_day_forecast[i+1]['subheader']}"
            self._print_subheader(subheader1, border_width)
            self._print_subheader(subheader2, border_width)
            print()

            # Printar varje tidsprognos för båda dagarna,
            # Loopar genom tidsprognoserna och printar ut en tidsprognos åt gången med kanter på båda sidorna.
            # Variabeln time_forecast innehåller en ny tidsprognosen för varje iteration,
            # medan j är indexet vilket används för att komma åt nästkommande dags tidsprognoser
            for j, time_forecast in enumerate(full_day_forecast[i]["time_forecasts"]):
                body1: str = time_forecast
                body2: str = full_day_forecast[i + 1]["time_forecasts"][j]
                self._print_body(body1, border_width)
                self._print_body(body2, border_width)
                print()

            # Printar nedre kanterna med hörn
            self._print_footer(border_width)
            self._print_footer(border_width)
            print()

    def _print_header(self, header: str, width: int, should_center: bool = False) -> None:
        """Printar en header. Centrerar om should_center=True"""
        if should_center:
            print(header.rjust(width + 2))
        else:
            print(header.center(width + 3), end="")

    def _print_title(self, title: str, width: int, should_center: bool = False) -> None:
        """Printar en rubrik ihop med en överkantlinje och hörn. Centrerar om should_center=True"""
        if should_center:
            print("┌".rjust(width // 2 + 2) + f"  IDAG - {title}  ".center(width, "─") + "┐")
        else:
            print("┌" + f"  {title}  ".center(width, "─") + "┐", end="")

    def _print_subheader(self, subheader: str, width: int, should_center: bool = False) -> None:
        """Printar en underrubrik ihop med en sidolinjer. Centrerar om should_center=True"""
        if should_center:
            print("│".rjust(width // 2 + 2) + f"{subheader}".center(width) + "│")
        else:
            print("│" + f"{subheader}".center(width) + "│", end="")

    def _print_body(self, body: str, width: int, should_center: bool = False) -> None:
        """Printar brödtexten eller innehållet för en ruta ihop med sidolinjer. Centrerar om should_center=True"""
        if should_center:
            print("│".rjust(width // 2 + 2) + f" {body}".ljust(width) + "│")
        else:
            print(f"│ {body}".ljust(width) + " │", end="")

    def _print_footer(self, width: int, should_center: bool = False) -> None:
        """Printar en underkant ihop med en hörn. Centrerar om should_center=True"""
        if should_center:
            print("└".rjust(width // 2 + 2) + "─" * width + "┘")
        else:
            print("└" + "─" * width + "┘", end="")

    def get_average_weather_id(self, weather_ids: list[int]) -> int:
        """Räknar ut vilken väderkod som förekommer flest antal gånger i listan.
        Returnerar det mest förekommande värdet."""

        # Dictionary som ska hålla räkningen på alla väderkoder,
        # den innehåller inga nycklar än utan dessa skapas i loopen
        counter: dict[int, int] = {}

        # Loopar genom alla väderkoder i strängen
        for weather_id in weather_ids:
            # För varje väderkod skapas en ny nyckel med värdet 1 om den inte redan finns, annars adderas det direkt med 1
            # om nyckeln redan skapats i en tidigare iteration
            if weather_id not in counter:
                counter[weather_id] = 1
            else:
                counter[weather_id] += 1

        # Returnerar det högsta värdet i dictionary med max() funktionen
        # key=counter.get gör att funktionen jämför värdena i stället för nycklarna
        return max(counter, key=counter.get)  # type: ignore

    def get_weather_icon(self, weather_id: int) -> str:
        """Tar emot en väderkod. Returnerar motsvarande väderikon (emoji)."""

        symbol: str = ""
        # Hittar matchningen med första siffran i väderkoden
        match str(weather_id)[0]:
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
                if weather_id == 800:
                    # Klart väder
                    symbol = "🌞"
                else:
                    # Molnigt
                    symbol = "🌤️"
            case _:
                pass
        return symbol
