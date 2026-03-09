import sys
import logging
from datetime import datetime
from scraper import scrape_products
from ai_analysis import analyze_with_ai
from config import get_config


def setup_logging():
    log_filename = f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.FileHandler(log_filename, encoding="utf-8")],
    )
    return log_filename


def generate_dashboard(csv_file: str):
    try:
        from dashboard import generate_html_dashboard
        generate_html_dashboard(csv_file)
    except Exception as e:
        print(f"[!] No se pudo generar el dashboard: {e}")


def print_banner():
    print("\n" + "=" * 50)
    print("   Jhon Esteban Tellez Gracia - Prueba Tecnica | Kata Middle")
    print("=" * 50)


def main():
    log_file = setup_logging()
    logger = logging.getLogger(__name__)

    print_banner()
    config = get_config()

    categories  = config["categories"]
    pages       = config["pages"]
    model       = config["ai_model"]
    output_file = config["output_file"]

    print(f"\n  Configuración:")
    print(f"    Categorías : {', '.join(categories)}")
    print(f"    Páginas    : {pages} por categoría")
    print(f"    Modelo IA  : {model}")
    print(f"    Salida     : {output_file}")
    print(f"    Log        : {log_file}")

    logger.info(f"Categorías={categories} páginas={pages} modelo={model}")

  
    print(f"\n[1] Scraping de {len(categories)} categoría(s)\n")
    try:
        df = scrape_products(categories, pages, output_file)
        if df.empty:
            print(" Sin datos. Continuando si existe CSV ")
            logger.warning("Scraper retornó vacío")
    except Exception as e:
        logger.error(f"Error crítico en scraper: {e}")
        print(f"[Error scraper] {e}")

   
    print("\n[2] Análisis con IA\n")
    try:
        analyze_with_ai(model, input_file=output_file)
    except Exception as e:
        logger.error(f"Error crítico en IA: {e}")
        print(f"[Error IA] {e}")
        sys.exit(1)

    
    print("\n[3] Generando dashboard\n")
    generate_dashboard(output_file)

    logger.info("Proceso completado")
    print("\n" + "=" * 50)
    print("   Proceso completado")
    print(f"   Datos      : {output_file}")
    print(f"   Análisis   : ai_summary.md")
    print(f"   Dashboard  : dashboard.html")
    print(f"   Log        : {log_file}")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()