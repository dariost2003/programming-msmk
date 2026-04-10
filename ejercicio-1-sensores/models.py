"""
Modelos de datos para el sistema de monitoreo de sensores.

Define las estructuras principales usando dataclasses:
- SensorConfig: configuracion de un sensor (umbrales, unidades, calibracion)
- Reading: una lectura individual de un sensor
- Alert: una alerta generada cuando un valor excede un umbral
"""

from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd


@dataclass
class SensorConfig:
    """
    Configuracion de un sensor industrial.

    Attributes:
        name: Nombre descriptivo del sensor (ej: "Temperatura del agua").
        unit: Unidad de medida (ej: "C", "NTU", "L/min").
        min_threshold: Umbral minimo aceptable. Valores por debajo generan alerta.
        max_threshold: Umbral maximo aceptable. Valores por encima generan alerta.
        calibration_factor: Factor multiplicativo de calibracion (1.0 = sin ajuste).
    """
    name: str
    unit: str
    min_threshold: float
    max_threshold: float
    calibration_factor: float = 1.0

    def is_within_range(self, value: float) -> bool:
        """Verifica si un valor esta dentro del rango aceptable."""
        return self.min_threshold <= value <= self.max_threshold

    def get_severity(self, value: float) -> str | None:
        """
        Determina la severidad de una desviacion.

        Returns:
            None si esta en rango, "warning" si esta cerca del limite,
            "critical" si lo excede significativamente.
        """
        if self.is_within_range(value):
            return None

        # Calcular que tan lejos esta del rango
        rango = self.max_threshold - self.min_threshold
        margen_critico = rango * 0.5  # 50% del rango fuera = critico

        if value < self.min_threshold:
            desviacion = self.min_threshold - value
        else:
            desviacion = value - self.max_threshold

        if desviacion > margen_critico:
            return "critical"
        return "warning"


@dataclass
class Reading:
    """
    Una lectura individual de un sensor.

    Attributes:
        timestamp: Momento en que se tomo la lectura.
        value: Valor numerico de la lectura (puede ser NaN si fallo el sensor).
        sensor_id: Identificador unico del sensor (ej: "TEMP-001").
        is_anomaly: Indica si la lectura fue marcada como anomala.
    """
    timestamp: pd.Timestamp | datetime
    value: float
    sensor_id: str
    is_anomaly: bool = False

    def __str__(self) -> str:
        valor_str = f"{self.value:.4f}" if not pd.isna(self.value) else "NaN"
        anomalia_str = " [ANOMALIA]" if self.is_anomaly else ""
        return f"[{self.timestamp}] {self.sensor_id}: {valor_str}{anomalia_str}"


@dataclass
class Alert:
    """
    Una alerta generada cuando un sensor reporta un valor fuera de rango.

    Attributes:
        timestamp: Momento en que se genero la alerta.
        sensor_id: Identificador del sensor que genero la alerta.
        value: Valor que provoco la alerta.
        threshold_exceeded: Descripcion del umbral excedido (ej: "max: 25.0").
        severity: Nivel de severidad ("warning" o "critical").
    """
    timestamp: pd.Timestamp | datetime
    sensor_id: str
    value: float
    threshold_exceeded: str
    severity: str = "warning"  # "warning" o "critical"

    def __post_init__(self):
        """Valida que la severidad sea valida."""
        severidades_validas = {"warning", "critical"}
        if self.severity not in severidades_validas:
            raise ValueError(
                f"Severidad '{self.severity}' no valida. "
                f"Opciones: {severidades_validas}"
            )

    def __str__(self) -> str:
        icono = "!!" if self.severity == "critical" else "!"
        return (
            f"[{icono} ALERTA {self.severity.upper()}] "
            f"{self.timestamp} - {self.sensor_id}: "
            f"valor={self.value:.4f}, umbral excedido: {self.threshold_exceeded}"
        )


# --- Configuraciones predefinidas para los sensores de la planta ---

SENSOR_CONFIGS: dict[str, SensorConfig] = {
    "TEMP-001": SensorConfig(
        name="Temperatura del agua",
        unit="C",
        min_threshold=18.0,
        max_threshold=28.0,
        calibration_factor=1.0,
    ),
    "PH-001": SensorConfig(
        name="pH del agua",
        unit="pH",
        min_threshold=6.0,
        max_threshold=8.0,
        calibration_factor=1.0,
    ),
    "TURB-001": SensorConfig(
        name="Turbidez del agua",
        unit="NTU",
        min_threshold=0.0,
        max_threshold=8.0,
        calibration_factor=1.0,
    ),
    "FLOW-001": SensorConfig(
        name="Caudal de entrada",
        unit="L/min",
        min_threshold=50.0,
        max_threshold=200.0,
        calibration_factor=1.0,
    ),
}
