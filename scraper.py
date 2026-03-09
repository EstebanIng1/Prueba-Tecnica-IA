import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

logger = logging.getLogger(__name__)


def fetch_with_retry(url: str, retries: int = 3, delay: float = 2.0):
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"GET {url} (intento {attempt}/{retries})")
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            logger.warning(f"HTTP Error intento {attempt}: {e}")
        except requests.exceptions.ConnectionError:
            logger.warning(f"Connection Error intento {attempt}")
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout intento {attempt}")
        except Exception as e:
            logger.error(f"Error inesperado intento {attempt}: {e}")

        if attempt < retries:
            logger.info(f"Reintentando en {delay}s...")
            time.sleep(delay)

    logger.error(f"Todos los intentos fallaron: {url}")
    return None


def scrape_page(url: str) -> list:
    response = fetch_with_retry(url)
    if not response:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select(".thumbnail")

    if not products:
        logger.warning(f"Sin productos en {url}")
        return []

    page_results = []
    for p in products:
        try:
            name = p.select_one(".title")
            price_tag = p.select_one(".price")
            rating_tag = p.select(".ratings p[data-rating]")
            description_tag = p.select_one(".description")

            if not name or not price_tag:
                continue

            price_text = price_tag.text.strip()

            page_results.append({
                "name": name.text.strip(),
                "price_raw": price_text,
                "rating": rating_tag[0]["data-rating"] if rating_tag else "N/A",
                "description": description_tag.text.strip() if description_tag else "N/A",
            })

        except Exception as e:
            logger.error(f"Error al parsear producto: {e}")

    return page_results


def scrape_products(categories, pages: int, output_file: str = "results.csv") -> pd.DataFrame:

    if isinstance(categories, str):
        categories = [categories]

    all_results = []
    sep = "=" * 50

    for category in categories:
        logger.info(f"Scraping: {category}, páginas={pages}")
        print(f"\n{sep}")
        print(f"  Categoría : {category}")
        print(f"  Páginas   : {pages}")
        print(f"{sep}\n")

        for page in range(1, pages + 1):
            url = f"{BASE_URL}/{category}?page={page}"
            print(f"[Página {page}/{pages}] {url}")
            page_data = scrape_page(url)

            if page_data:
                for item in page_data:
                    item["category"] = category
                all_results.extend(page_data)
                print(f"   {len(page_data)} productos encontrados")
                logger.info(f"{category} p{page}: {len(page_data)} productos")
            else:
                print(f"   Sin datos, pero proceso sigue")

        cat_count = sum(1 for r in all_results if r.get("category") == category)
        print(f"  Subtotal '{category}': {cat_count} productos")

    if not all_results:
        logger.warning("Sin productos en ninguna categoría")
        print("\n[Advertencia] No se encontraron productos.")
        return pd.DataFrame()

    df = pd.DataFrame(all_results)

    before_dedup = len(df)
    df = df.drop_duplicates(subset=["name", "price_raw", "category"])
    removed = before_dedup - len(df)
    if removed:
        print(f"  Duplicados eliminados: {removed}")

    df.to_csv(output_file, index=False, encoding="utf-8")
    logger.info(f"CSV guardado: {output_file} ({len(df)} productos)")

    print(f"\n{sep}")
    print(f"   TOTAL: {len(df)} productos guardados en '{output_file}'")
    print(f"  Categorías encontradas: {len(categories)}")
    print(f"{sep}\n")

    return df