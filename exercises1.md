## Solución: Crear dos cuentas

```python
class CuentaBancaria:
	def __init__(self, titular, saldo=0):
		self.titular = titular
		self.saldo = saldo

	def depositar(self, cantidad):
		if cantidad > 0:
			self.saldo += cantidad

	def retirar(self, cantidad):
		if 0 < cantidad <= self.saldo:
			self.saldo -= cantidad
			return True
		return False

	def __repr__(self):
		return f"CuentaBancaria(titular={self.titular!r}, saldo={self.saldo})"

# Crear dos cuentas
cuenta1 = CuentaBancaria("Alex", 500)
cuenta2 = CuentaBancaria("Santiago", 100)

print(cuenta1)
print(cuenta2)
```
