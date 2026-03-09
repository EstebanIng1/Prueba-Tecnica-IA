
## Prueba Tecnica - Jhon Esteban Tellez Gracia

El reto que se desarrollo consta de la extracción automatizada de datos de un sitio de prueba
donde se guardan en un csv y utiliza ollama llama3 para analizar y darnos un leve resumen de los datos, adicionalmente se genera un dashboard para visualizar los datos de una manera mas sencilla.


## Como preparar entorno 

-Instalar Python 3.12
-Crear entorno
-Instalar Ollama localmente ([text](https://ollama.com/download/windows))
- Instalar dependencias

> Crear entorno
-python -m venv venv 

>Activar entrno
- .venv\Scripts\actívate (Windows)
-Source .venv/bin/actívate (Linux)

>Instala las dependencias 
-pip install requests beautifulsoup4 pandas ollama
- pip install -r requirements.txt

## Como se usa el proyecto

-python main.py


Se deja correr tienen un logging por consola que nos va diciendo en que punto va del proceso

## Archivos creados


-results.csv — todos los productos con nombre, precio, rating, descripción y categoría
-ai_summary.md   — el análisis de la IA: resumen, anomalías y recomendaciones
–dashboard.html  — Dashboard con datos 
–scraper_*.log   — log completo de la ejecución con timestamps


# Estructura del proyecto

├── main.py              ← orquestador principal

├── scraper.py           ← extracción de datos 

├── ai_analysis.py       ← análisis con modelo local via Ollama

├── dashboard.py         ← generación del dashboard HTML

├── config.py            ← configuración 

├── requirements.txt

└── static/
    ├── estilos/
    │   └── dashboard.css
    └── js/
        ├── charts.js    ← gráficas Chart.js
        └── table.js     ← filtros y ordenamiento



 
