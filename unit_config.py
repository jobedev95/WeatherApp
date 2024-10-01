import pyinputplus as py


class UnitConfig:
    def __init__(self) -> None:
        self.unit: str = "metric"  # Standard enhetssystem är metric

    def get_unit(self) -> str:
        """Tillåter användaren att välja mellan Celsius eller Fahrenheit. Returnerar sedan vald enhet."""
        # Användaren får välja system
        menu_choices: list[str] = ["Metriskt (Celsius)", "Imperial (Fahrenheit)"]
        choice: str = py.inputMenu(prompt="\nVälj enhetssystem:\n", choices=menu_choices, numbered=True)

        # Om användaren valt imperial ändras enhetsystemet
        if choice == "Metriskt (Celsius)":
            print("Enhetssystem inställd på metrisk (Celsius).")
        else:
            self.unit = "imperial"  # Ändrar enheten till imperial om användaren väljer 2
            print("Enhetssystem inställd på imperial (Fahrenheit).")

        return self.unit  # Enheten returneras
