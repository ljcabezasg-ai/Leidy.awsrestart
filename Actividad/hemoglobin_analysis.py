# hemoglobin_analysis.py
# Descripción: Análisis básico de la secuencia de la hemoglobina beta humana.
# Contenido:
# - Cargar la secuencia desde hemoglobin_clean.txt
# - Mostrar información básica (longitud, primeros/últimos residuos)
# - Calcular la composición de aminoácidos
# - Calcular el peso molecular usando pesos por aminoácido
# - Refactorizar el peso en una función reutilizable
# - Guardar resultados en JSON (hemoglobin_results.json)
# - Calcular el porcentaje de aminoácidos hidrofóbicos (A, V, I, L, M, F, W, Y)

from pathlib import Path
import json

# Directorio base donde está este script
BASE_DIR = Path(__file__).parent

# Archivo de entrada con la secuencia de aminoácidos
SECUENCIA_FILE = BASE_DIR / "hemoglobin_clean.txt"

# Pesos moleculares aproximados por aminoácido (en Daltons)
PESO_AMINOACIDO = {
    'A': 89.09, 'R': 174.20, 'N': 132.12, 'D': 133.10, 'C': 121.15,
    'Q': 146.15, 'E': 147.13, 'G': 75.07, 'H': 155.16, 'I': 131.18,
    'L': 131.18, 'K': 146.19, 'M': 149.21, 'F': 165.19, 'P': 115.13,
    'S': 105.09, 'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15,
}

# Aminoácidos hidrofóbicos
HIDROFOBICOS = set(['A','V','I','L','M','F','W','Y'])

def cargar_secuencia(ruta):
    """Carga la secuencia desde un archivo y la devuelve como string sin saltos de línea."""
    path = Path(ruta)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo {ruta}")
    with path.open("r", encoding="utf-8") as f:
        texto = f.read()
    return "".join(texto.split())

def mostrar_informacion(secuencia):
    """Imprime información básica de la secuencia."""
    longitud = len(secuencia)
    print("Longitud de la secuencia:", longitud)
    print("Secuencia (primeros 20 residuos):", secuencia[:20])
    print("Secuencia (últimos 20 residuos):", secuencia[-20:])

def contar_aminoacidos(secuencia):
    """Devuelve un diccionario con conteo por aminoácido presente en la secuencia."""
    conteo = {aa: 0 for aa in PESO_AMINOACIDO.keys()}
    for aa in secuencia:
        if aa in conteo:
            conteo[aa] += 1
        else:
            print(f"Advertencia: aminoácido desconocido '{aa}' encontrado y omitido.")
    return conteo

def calcular_peso(secuencia, pesos=PESO_AMINOACIDO):
    """Calcula el peso molecular total de la secuencia sumando pesos por residuo."""
    total = 0.0
    for aa in secuencia:
        if aa in pesos:
            total += pesos[aa]
        else:
            print(f"Advertencia: peso para '{aa}' no encontrado; se omite.")
    return total

def calcular_peso_promedio(secuencia, pesos=PESO_AMINOACIDO):
    """Devuelve el peso promedio por residuo."""
    if len(secuencia) == 0:
        return 0.0
    return calcular_peso(secuencia, pesos) / len(secuencia)

def porcentaje_hidrofobico(secuencia):
    """Calcula el porcentaje de aminoácidos hidrofóbicos en la secuencia."""
    if len(secuencia) == 0:
        return 0.0
    hidro_count = sum(1 for aa in secuencia if aa in HIDROFOBICOS)
    return (hidro_count / len(secuencia)) * 100.0

def guardar_json(ruta, datos):
    """Guarda los datos en un archivo JSON."""
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def main():
    # Cargar la secuencia limpia
    secuencia = cargar_secuencia(SECUENCIA_FILE)

    print("=== Información de la Secuencia ===")
    mostrar_informacion(secuencia)

    # Conteo de aminoácidos
    conteo = contar_aminoacidos(secuencia)
    print("\nConteo de aminoácidos (solo los presentes):")
    for aa, c in conteo.items():
        if c > 0:
            print(f"{aa}: {c}")

    longitud = len(secuencia)

    # Peso total y promedio
    peso_total = calcular_peso(secuencia)
    peso_promedio = calcular_peso_promedio(secuencia)

    print("\nPeso molecular total (aprox.):", peso_total)
    print("Peso molecular promedio por residuo:", peso_promedio)

    # Porcentaje hidrofóbico
    porcentaje_hidro = porcentaje_hidrofobico(secuencia)
    print("\nPorcentaje de aminoácidos hidrofóbicos:", round(porcentaje_hidro, 2), "%")

    # Datos para JSON
    datos_json = {
        "nombre_proteina": "hemoglobina beta humana (Homo sapiens)",
        "longitud_sec": longitud,
        "conteo_aminoacidos": {aa: c for aa, c in conteo.items() if c > 0},
        "peso_molecular_total": peso_total,
        "peso_molecular_promedio_por_residuo": peso_promedio,
        "porcentaje_hidrofobico": porcentaje_hidro
    }

    # Guardar resultados
    guardar_json(BASE_DIR / "hemoglobin_results.json", datos_json)
    print("\nResultados guardados en hemoglobin_results.json")

if __name__ == "__main__":
    main()