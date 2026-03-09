import pandas as pd
import ollama
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def build_compact_summary(df: pd.DataFrame) -> str:
    
    lines = []
    for _, row in df.iterrows():
        lines.append(f"- {row.get('name','?')} | {row.get('price_raw','?')} | rating:{row.get('rating','N/A')}")

    valid_prices = []
    for p in df.get("price_raw", []):
        try:
            valid_prices.append(float(str(p).replace("$","").replace(",","").strip()))
        except:
            pass

    stats = ""
    if valid_prices:
        stats = (
            f"Total:{len(df)} | "
            f"Min:${min(valid_prices)} | "
            f"Max:${max(valid_prices)} | "
            f"Promedio:${round(sum(valid_prices)/len(valid_prices),2)}"
        )

    return f"STATS: {stats}\n" + "\n".join(lines)


def analyze_with_ai(model: str, input_file: str = "results.csv", output_file: str = "ai_summary.md") -> None:

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {input_file}")
        print(f"[Error] No se encontró '{input_file}'.")
        return
    except pd.errors.EmptyDataError:
        print(f"[Error] '{input_file}' está vacío.")
        return

    if df.empty:
        print("[Advertencia] Sin datos para analizar.")
        return

    logger.info(f"Analizando {len(df)} productos con '{model}' (1 sola llamada)")
    print(f"\n Modelo: {model} | Productos: {len(df)}")
    print(" Enviando consulta única...")

    data = build_compact_summary(df)


    prompt = f"""Analiza estos productos y responde EXACTAMENTE en este formato, en español, con máximo 4 bullets por sección:

## RESUMEN
- (total de productos, rango de precios, rating promedio, top 2 productos)

## ANOMALIAS
- (precios extremos, ratings sospechosos o datos raros)

## RECOMENDACIONES
- (top 3 mejor calidad-precio con justificación breve)

## PRODUCTOS NO COMPRAR
-(Dame el producto con el cual tenga el ratings bajo y una mala descripción)

DATOS:
{data}"""

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            options={
                "num_predict": 500,  
                "temperature": 0.2, 
            }
        )
        result = response["message"]["content"]
        logger.info("Consulta única completada")
        print(" Respuesta recibida")

    except ollama.ResponseError as e:
        logger.error(f"Ollama error: {e}")
        result = f"[Error Ollama] {e}"
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        result = f"[Error] {e}"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Analisis Realizado con IA - Jhon Esteban Tellez Gracia - Prueba Tecnica\n\n")
        f.write(f"> **Generado:** {timestamp}  \n")
        f.write(f"> **Modelo:** `{model}`  \n")
        f.write(f"> **Fuente:** `{input_file}` ({len(df)} productos)  \n\n")
        f.write("---\n\n")
        f.write(result)
        f.write("\n\n---\n\n")
        f.write("##  Datos Crudos\n\n```\n")
        f.write(df.to_string(index=False))
        f.write("\n```\n")

    logger.info(f"Guardado: {output_file}")
    print(f" Guardado en '{output_file}'")