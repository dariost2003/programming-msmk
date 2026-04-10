"""
Simulador de streaming de datos de sensores.

Carga un archivo CSV y entrega lecturas una por una,
simulando la recepcion de datos en tiempo real.
Permite aplicar factores de calibracion y ruido adicional.
"""

import time
from pathlib import Path

import numpy as np
import pandas as pd

from models import Reading


class SensorSimulator:
    """
    Simulador que lee un CSV de datos de sensor y entrega
    lecturas una por una, como si vinieran en tiempo real.

    Uso basico:
        sim = SensorSimulator("mock_data/temperatura.csv")
        sim.start()
        while True:
            lectura = sim.get_next_reading()
            if lectura is None:
                break
            print(lectura)
    """

    def __init__(
        self,
        csv_path: str | Path,
        speed_factor: float = 1.0,
        noise_std: float = 0.0,
        seed: int | None = None,
    ):
        """
        Inicializa el simulador.

        Args:
            csv_path: Ruta al archivo CSV con los datos del sensor.
            speed_factor: Factor de velocidad de simulacion.
                          1.0 = tiempo real (30s entre lecturas),
                          0.0 = sin espera (lo mas rapido posible),
                          10.0 = 10x mas rapido que tiempo real.
            noise_std: Desviacion estandar del ruido adicional a aplicar.
                       0.0 = sin ruido extra.
            seed: Semilla para el generador de ruido (reproducibilidad).
        """
        self._csv_path = Path(csv_path)
        self._speed_factor = speed_factor
        self._noise_std = noise_std
        self._rng = np.random.default_rng(seed)

        # Factor de calibracion (multiplicativo)
        self._calibration_factor: float = 1.0

        # Estado interno
        self._data: pd.DataFrame | None = None
        self._index: int = 0
        self._started: bool = False

    def start(self) -> None:
        """
        Carga los datos del CSV e inicializa el simulador.
        Debe llamarse antes de get_next_reading().
        """
        if not self._csv_path.exists():
            raise FileNotFoundError(f"No se encontro el archivo: {self._csv_path}")

        self._data = pd.read_csv(self._csv_path, parse_dates=["timestamp"])
        self._index = 0
        self._started = True
        print(f"Simulador iniciado: {len(self._data)} lecturas cargadas desde {self._csv_path.name}")

    def get_next_reading(self) -> Reading | None:
        """
        Obtiene la siguiente lectura del sensor.

        Aplica el factor de calibracion y ruido adicional si estan configurados.
        Respeta el speed_factor para simular el paso del tiempo.

        Returns:
            Un objeto Reading con la lectura, o None si se agotaron los datos.
        """
        if not self._started or self._data is None:
            raise RuntimeError("El simulador no ha sido iniciado. Llama a start() primero.")

        if self._index >= len(self._data):
            return None

        fila = self._data.iloc[self._index]
        self._index += 1

        # Simular espera entre lecturas (si speed_factor > 0)
        if self._speed_factor > 0 and self._index > 1:
            # Intervalo real entre lecturas (30 segundos en los datos)
            espera = 30.0 / self._speed_factor
            # Limitar la espera maxima a 5 segundos para no bloquear demasiado
            espera = min(espera, 5.0)
            time.sleep(espera)

        # Obtener valor original
        valor = fila["value"]

        # Si el valor es NaN, lo pasamos tal cual (simula fallo del sensor)
        if pd.isna(valor):
            is_anomaly = False
        else:
            # Aplicar calibracion
            valor = valor * self._calibration_factor

            # Aplicar ruido adicional
            if self._noise_std > 0:
                valor += self._rng.normal(0, self._noise_std)

            # Redondear a 4 decimales
            valor = round(valor, 4)

            # Marcar como anomalia si el valor es inusual
            # (criterio simple: fuera de 3 desviaciones estandar de la media parcial)
            is_anomaly = False  # El estudiante puede mejorar esta logica

        return Reading(
            timestamp=pd.Timestamp(fila["timestamp"]),
            value=valor if not pd.isna(fila["value"]) else float("nan"),
            sensor_id=fila["sensor_id"],
            is_anomaly=is_anomaly,
        )

    def apply_calibration(self, factor: float) -> None:
        """
        Aplica un factor de calibracion multiplicativo a las lecturas futuras.

        Args:
            factor: Factor de calibracion (ej: 1.05 para +5%, 0.95 para -5%).
        """
        if factor <= 0:
            raise ValueError("El factor de calibracion debe ser positivo.")
        self._calibration_factor = factor
        print(f"Factor de calibracion actualizado: {factor}")

    @property
    def readings_remaining(self) -> int:
        """Numero de lecturas restantes en el dataset."""
        if self._data is None:
            return 0
        return max(0, len(self._data) - self._index)

    @property
    def total_readings(self) -> int:
        """Numero total de lecturas en el dataset."""
        if self._data is None:
            return 0
        return len(self._data)

    @property
    def progress(self) -> float:
        """Progreso de la simulacion como fraccion (0.0 a 1.0)."""
        if self._data is None or len(self._data) == 0:
            return 0.0
        return self._index / len(self._data)

    def reset(self) -> None:
        """Reinicia el simulador al inicio del dataset."""
        self._index = 0
        print("Simulador reiniciado al inicio.")

    def __repr__(self) -> str:
        estado = "activo" if self._started else "no iniciado"
        return (
            f"SensorSimulator(archivo={self._csv_path.name}, "
            f"estado={estado}, "
            f"progreso={self.progress:.1%}, "
            f"calibracion={self._calibration_factor})"
        )
