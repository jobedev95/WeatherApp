def box_print_title(title: str, width: int) -> None:
    """Printar en rubrik ihop med en överkantlinje och hörn."""
    print("┌" + f"  {title}  ".center(width, "─") + "┐")


def box_print_body(body: str, width: int) -> None:
    """Printar brödtexten eller innehållet för en ruta ihop med sidolinjer."""
    print(f"│ {body}".ljust(width) + " │")


def box_print_footer(width: int) -> None:
    """Printar en underkant ihop med hörn."""
    print("└" + "─" * width + "┘")
