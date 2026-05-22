
def celsius_a_fahrenheit(celsius):
    return (celsius * 9/5) + 32

entrada = input("Introduce la temperatura en grados Celsius: ")

try:
    grados_c = float(entrada)

    grados_f = celsius_a_fahrenheit(grados_c)
    print(f"El resultado de la conversión es: {grados_f}°F")

except ValueError:

    print("Error: Por favor, introduce un número válido.")
