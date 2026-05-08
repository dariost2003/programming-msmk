
class CuentaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self.saldo = saldo

    def consultar(self):
        print(f"\n--- Info de Cuenta ---")
        print(f"Titular: {self.titular}")
        print(f"Saldo actual: ${self.saldo}")
        print("----------------------")

    def depositar(self, cantidad):
        try:
            if cantidad <= 0:
                raise ValueError("La cantidad a depositar debe ser mayor a $0.")
            self.saldo += cantidad
            print(f"Depósito exitoso: +${cantidad}")
        except ValueError as e:
            print(f"Error en depósito: {e}")

    def retirar(self, cantidad):
        try:
            if cantidad <= 0:
                raise ValueError("La cantidad a retirar debe ser mayor a $0.")
            if cantidad > self.saldo:
                raise RuntimeError("Fondos insuficientes.")
            
            self.saldo -= cantidad
            print(f"Retiro exitoso: -${cantidad}")
        except (ValueError, RuntimeError) as e:
            print(f"Error en retiro: {e}")

    def transferir(self, cantidad, otra_cuenta):
        print(f"\nIniciando transferencia de {self.titular} a {otra_cuenta.titular}...")
        try:
            if cantidad <= 0:
                raise ValueError("La cantidad a transferir debe ser mayor a $0.")
            if cantidad > self.saldo:
                raise RuntimeError("No tienes saldo suficiente para transferir.")
            
            # Si pasa las validaciones, procedemos
            self.saldo -= cantidad
            otra_cuenta.saldo += cantidad
            print(f"Transferencia de ${cantidad} realizada con éxito.")
        except (ValueError, RuntimeError) as e:
            print(f"Error en transferencia: {e}")

#  PRUEBAS DEL SISTEMA 

# 1. Crear dos cuentas
cuenta1 = CuentaBancaria("Alex", 500)
cuenta2 = CuentaBancaria("Santiago", 100)

# 2. Consultar estados iniciales
cuenta1.consultar()
cuenta2.consultar()

# 3. Operaciones normales
cuenta1.depositar(200)
cuenta1.retirar(100)

# 4. Transferencia exitosa
cuenta1.transferir(150, cuenta2)

# 5. PRUEBA DE ERROR INTENCIONADO (Retirar más de lo disponible)
print("\n--- Intento de retiro excesivo (Error intencionado) ---")
cuenta2.retirar(1000)

# 6. Consultar estados finales
cuenta1.consultar()
cuenta2.consultar()