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
                    "main_temp": item["main"]["temp"],  # Sparar temperaturen
                    "temp_min": item["main"]["temp_min"],  # Sparar minimum temperaturen
                    "temp_max": item["main"]["temp_max"],  # Sparar maximum temperaturen
                    "weather_description": item["weather"][0]["description"],  # Sparar väderbeskrivning
                    "weather_id": item["weather"][0]["id"],  # Sparar väder-id
                }
            )

    def print_full_day_forecasts(self) -> None:
        """Printar ut femdagarsprognosen i ett särskilt format där den första dagen visas separat,
        och de resterande fyra dagarna printas ut i par sida vid sida. Varje prognos omges av sin egen linjeram."""

        # Anropar en funktion som förbereder den inhämtade datan genom att organisera alla tidsprognoser
        full_day_forecast: list = self._prepare_forecast_data()
        border_width = 45

        #                                       PRINTAR DAGENS PROGNOS (Index 0)
        # Printar väderikonen över rubriken
        print(f'{full_day_forecast[0]['header']}'.rjust(border_width + 2))

        # Printar övre kant med hörn för en ruta med rubrik
        print("┌".rjust(border_width // 2 + 2) + f"  IDAG - {full_day_forecast[0]['title']}  ".center(border_width, "─") + "┐")

        # Printar underrubrik med kanter på sidorna
        print("│".rjust(border_width // 2 + 2) + f"{full_day_forecast[0]['subheader']}".center(border_width) + "│")

        # Printar hela dagens väderprognos med kanter
        for value in full_day_forecast[0]["time_forecasts"]:
            print("│".rjust(border_width // 2 + 2) + f" {value}".ljust(border_width) + "│")

        # Printar nedre kant med hörn
        print("└".rjust(border_width // 2 + 2) + "".center(border_width, "─") + "┘")

        #                   PRINTAR RESTERANDE DAGARS PROGNOSER SIDA VID SIDA - TVÅ ÅT GÅNGEN
        # Loop för dag 2-4 (motsvarar index 1-4) med en step på 2 eftersom att det ska printas parvis (varje iteration hanterar två dagar åt gången)
        for i in range(1, 5, 2):
            # Printar väderikonerna över rubriken
            print(
                f"  {full_day_forecast[i]['header']}  ".center(border_width + 2)
                + f"  {full_day_forecast[i+1]['header']}  ".center(border_width + 1)
            )

            # Printar övre kant för två rutor med rubrik
            print(
                "┌" + f"  {full_day_forecast[i]['title']}  ".center(border_width, "─") + "┐"
                "┌" + f"  {full_day_forecast[i+1]['title']}  ".center(border_width, "─") + "┐"
            )

            # Printar underrubrikerna med kanter på sidorna
            print(
                "│" + f"{full_day_forecast[i]['subheader']}".center(border_width) + "│"
                "│" + f"{full_day_forecast[i+1]['subheader']}".center(border_width) + "│"
            )

            # Printar varje tidsprognos för båda dagarna,
            # Loopar genom tidsprognoserna och printar ut en tidsprognos åt gången med kanter på båda sidorna.
            # Variabeln time_forecast innehåller en ny tidsprognosen för varje iteration,
            # medan j är indexet vilket används för att komma åt nästkommande dags tidsprognoser
            for j, time_forecast in enumerate(full_day_forecast[i]["time_forecasts"]):
                print(
                    f"│ {time_forecast}".ljust(border_width)
                    + " │"
                    + f"│ {full_day_forecast[i+1]['time_forecasts'][j]}".ljust(border_width)
                    + " │"
                )
            # Printar nedre kanterna med hörn
            print("└" + "".center(border_width, "─") + "┘" + "└" + "".center(border_width, "─") + "┘")


    def _prepare_forecast_data(self) -> list[dict[str, str | list[str]]]:
        """Förbereder väderprognosdata för fem dagar genom att organisera och dela upp
        prognosen i fem separata delar efter datum. Skapar och returnerar en lista med fem dictionaries där varje
        dictionary innehåller väderprognoserna för de olika tidpunkterna från varje dag."""

        # Lista för att spara alla prognos-strängar från varje iteration
        forecast_lines: list[str] = []

        # Lista som ska samla in alla fem dagars prognoser
        full_day_forecasts: list[dict[str, str | list[str]]] = []

        # Lista för att spara alla fem väderkoder från varje prognos
        weather_ids: list[int] = []

        title: str = ""
        subheader: str = ""

        # För varje prognos i prognosdatan
        for i, item in enumerate(self.forecast_data):
            # Spara datum och tid. (Konverterar datetimeobjektet till en vanliga datum- och tidsträngar)
            date: str = item["date"].strftime("%Y-%m-%d")
            time: str = item["date"].strftime("%H:%M")

            # Om det är en ny dag i iterationen eller om det är den första iterationen ska en
            # rubrik med datumet sparas och weather_lines (listan med prognossträngar) samt weather_ids återställas
            if time == "02:00" or i == 0:
                weather_ids = []
                forecast_lines = []
                title = f"{date}"

            # Lägg till väderkoden för varje iteration i listan
            weather_ids.append(item["weather_id"])

            # Skapar en sträng från den insamlade prognosdatan från varje iteration och sparar strängen i en lista
            # Exempel på hur varje sträng kommer att se ut: "03:00: 23 °C Klart väder"
            forecast_lines.append(f"{time}: " + f'{item['main_temp']} °C, {item["weather_description"].capitalize()}')

            # När all data från en hel dag har samlats in och organiserats körs detta kodblock
            if time == "23:00":
                # Ställer in värdet underrubriken
                subheader = self.city

                # Hämtar in den mest förekommande väderkoden för dagen
                avg_weather_id: int = self.get_average_weather_id(weather_ids)

                # Hämtar väderkodens motsvarande väderikon (emoji) och sparar den i header
                header: str = f"{self.get_weather_icon(avg_weather_id)}"

                # Lägger till dagsprognosen i prognoslistan
                full_day_forecasts.append({"header": header, "title": title, "subheader": subheader, "time_forecasts": forecast_lines})

        return full_day_forecasts

    
    def get_average_weather_id(self, weather_icons: list[int]) -> int:
        """Räknar ut vilken väderkod som förekommer flest antal gånger i listan.
        Returnerar det mest förekommande värdet."""

        # Dictionary som ska hålla räkningen på alla väderkoder,
        # den innehåller inga nycklar än utan dessa skapas i loopen
        counter: dict[int, int] = {}

        # Loopar genom alla väderkoder i strängen
        for weather_id in weather_icons:
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
