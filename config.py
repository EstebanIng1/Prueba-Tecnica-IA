import argparse

DEFAULT_CONFIG = {
    "categories": [
        "computers/laptops",
        "computers/tablets",
        "phones/touch",
    ],
    "pages": 2,
    "ai_model": "llama3",
    "output_file": "results.csv",
}


def get_config() -> dict:

    parser = argparse.ArgumentParser(description="Prueba Tecnica - Jhon Esteban Tellez Gracia")
    parser.add_argument(
        "--categories",
        type=str,
        nargs="+", 
        default=DEFAULT_CONFIG["categories"],
        help="Categorías a scrapear (separadas por espacio)",
    )
    parser.add_argument("--pages", type=int, default=DEFAULT_CONFIG["pages"],
                        help=f"Número de páginas por categoría (default: {DEFAULT_CONFIG['pages']})")
    parser.add_argument("--model", type=str, default=DEFAULT_CONFIG["ai_model"],
                        help=f"Modelo de IA local (default: {DEFAULT_CONFIG['ai_model']})")
    parser.add_argument("--output", type=str, default=DEFAULT_CONFIG["output_file"],
                        help=f"Archivo de salida (default: {DEFAULT_CONFIG['output_file']})")

    args = parser.parse_args()
    return {
        "categories": args.categories,
        "pages": args.pages,
        "ai_model": args.model,
        "output_file": args.output,
    }


CONFIG = DEFAULT_CONFIG