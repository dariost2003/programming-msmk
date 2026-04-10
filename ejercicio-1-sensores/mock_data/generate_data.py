"""
Generador de datos simulados para sensores de una planta de tratamiento de agua.

Genera 4 archivos CSV (uno por sensor) con ~10,000 lecturas cada uno.
Los datos simulan ~3.5 dias de lecturas cada 30 segundos.

Sensores simulados:
  - Temperatura (20-25 C)
  - pH (6.5-7.5)
  - Turbidez (1-5 NTU)
  - Caudal (100-150 L/min)

Cada archivo incluye patrones diurnos sinusoidales, ruido aleatorio,
picos anomalos (~2%) y valores faltantes (~1%) para simular fallos.
"""

import numpy as np
import pandas as pd
from pathlib import Path

# Semilla para reproducibilidad
SEED = 42
rng = np.random.default_rng(SEED)

# Numero de lecturas por sensor (~3.5 dias a 30 segundos = 10,080 lecturas)
NUM_LECTURAS = 10_080

# Intervalo entre lecturas en segundos
INTERVALO_SEGUNDOS = 30

# Directorio de salida (mismo directorio que este script)
DIR_SALIDA = Path(__file__).parent


def generar_timestamps(num_lecturas: int, intervalo_seg: int) -> pd.DatetimeIndex:
    """Genera una serie de timestamps equiespaciados."""
    inicio = pd.Timestamp("2024-06-01 00:00:00")
    return pd.date_range(start=inicio, periods=num_lecturas, freq=f"{intervalo_seg}s")


def generar_patron_diurno(num_lecturas: int, intervalo_seg: int, amplitud: float) -> np.ndarray:
    """
    Genera un patron sinusoidal con periodo de 24 horas.
    El pico ocurre alrededor de las 14:00 (hora mas calurosa del dia).
    """
    # Tiempo en horas desde el inicio
    horas = np.arange(num_lecturas) * intervalo_seg / 3600.0
    # Periodo de 24 horas, desfasado para que el maximo sea ~14:00
    patron = amplitud * np.sin(2 * np.pi * (horas - 8) / 24.0)
    return patron


def agregar_anomalias(valores: np.ndarray, proporcion: float, magnitud_min: float,
                      magnitud_max: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Agrega picos anomalos aleatorios a una fraccion de las lecturas.

    Retorna:
        - valores modificados
        - mascara booleana indicando cuales son anomalias
    """
    n = len(valores)
    num_anomalias = int(n * proporcion)

    # Seleccionar indices aleatorios para las anomalias
    indices_anomalos = rng.choice(n, size=num_anomalias, replace=False)

    # Generar magnitudes aleatorias (positivas o negativas)
    magnitudes = rng.uniform(magnitud_min, magnitud_max, size=num_anomalias)
    signos = rng.choice([-1, 1], size=num_anomalias)

    valores_modificados = valores.copy()
    valores_modificados[indices_anomalos] += magnitudes * signos

    # Crear mascara de anomalias
    mascara = np.zeros(n, dtype=bool)
    mascara[indices_anomalos] = True

    return valores_modificados, mascara


def agregar_valores_faltantes(valores: np.ndarray, proporcion: float) -> np.ndarray:
    """Reemplaza una fraccion aleatoria de valores con NaN (simulando fallos del sensor)."""
    n = len(valores)
    num_faltantes = int(n * proporcion)
    indices = rng.choice(n, size=num_faltantes, replace=False)
    valores_con_nan = valores.copy()
    valores_con_nan[indices] = np.nan
    return valores_con_nan


def generar_sensor(
    nombre: str,
    sensor_id: str,
    base_min: float,
    base_max: float,
    amplitud_diurna: float,
    ruido_std: float,
    anomalia_magnitud_min: float,
    anomalia_magnitud_max: float,
) -> pd.DataFrame:
    """
    Genera un DataFrame completo para un sensor con:
    - Valor base + patron diurno + ruido gaussiano
    - Anomalias (~2%)
    - Valores faltantes (~1%)
    """
    timestamps = generar_timestamps(NUM_LECTURAS, INTERVALO_SEGUNDOS)

    # Valor base: punto medio del rango
    base = (base_min + base_max) / 2.0

    # Generar valores con patron diurno
    patron = generar_patron_diurno(NUM_LECTURAS, INTERVALO_SEGUNDOS, amplitud_diurna)

    # Agregar ruido gaussiano
    ruido = rng.normal(0, ruido_std, size=NUM_LECTURAS)

    valores = base + patron + ruido

    # Limitar al rango base antes de anomalias (para que el patron normal sea realista)
    valores = np.clip(valores, base_min, base_max)

    # Agregar anomalias (~2%)
    valores, _ = agregar_anomalias(
        valores,
        proporcion=0.02,
        magnitud_min=anomalia_magnitud_min,
        magnitud_max=anomalia_magnitud_max,
    )

    # Agregar valores faltantes (~1%)
    valores = agregar_valores_faltantes(valores, proporcion=0.01)

    # Construir DataFrame
    df = pd.DataFrame({
        "timestamp": timestamps,
        "value": np.round(valores, 4),
        "sensor_id": sensor_id,
    })

    return df


def main():
    """Genera los 4 archivos CSV de datos simulados."""

    # Configuracion de cada sensor
    sensores = {
        "temperatura": {
            "sensor_id": "TEMP-001",
            "base_min": 20.0,
            "base_max": 25.0,
            "amplitud_diurna": 2.0,       # +/- 2 grados por ciclo diurno
            "ruido_std": 0.3,
            "anomalia_magnitud_min": 3.0,  # Picos de al menos 3 grados
            "anomalia_magnitud_max": 8.0,
        },
        "ph": {
            "sensor_id": "PH-001",
            "base_min": 6.5,
            "base_max": 7.5,
            "amplitud_diurna": 0.2,       # Variacion diurna leve
            "ruido_std": 0.08,
            "anomalia_magnitud_min": 0.8,
            "anomalia_magnitud_max": 2.0,
        },
        "turbidez": {
            "sensor_id": "TURB-001",
            "base_min": 1.0,
            "base_max": 5.0,
            "amplitud_diurna": 0.8,
            "ruido_std": 0.4,
            "anomalia_magnitud_min": 3.0,
            "anomalia_magnitud_max": 10.0,
        },
        "caudal": {
            "sensor_id": "FLOW-001",
            "base_min": 100.0,
            "base_max": 150.0,
            "amplitud_diurna": 15.0,      # Variacion significativa de flujo
            "ruido_std": 5.0,
            "anomalia_magnitud_min": 30.0,
            "anomalia_magnitud_max": 60.0,
        },
    }

    for nombre, config in sensores.items():
        print(f"Generando datos para sensor: {nombre}...")
        df = generar_sensor(nombre, **config)

        archivo = DIR_SALIDA / f"{nombre}.csv"
        df.to_csv(archivo, index=False)

        # Estadisticas basicas
        total = len(df)
        nulos = df["value"].isna().sum()
        anomalias_aprox = (
            df["value"].dropna().pipe(
                lambda s: ((s < config["base_min"] * 0.9) | (s > config["base_max"] * 1.1)).sum()
            )
        )
        print(f"  -> {archivo.name}: {total} lecturas, {nulos} NaN, ~{anomalias_aprox} anomalias detectables")

    print("\nGeneracion completada.")


if __name__ == "__main__":
    main()
