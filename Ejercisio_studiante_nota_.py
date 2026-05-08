class Estudiante:
    def __init__(self, nombre):
        self.nombre = nombre
        self.notas = [] 

    def añadir_nota(self, asignatura, valor_nota):
        try:
            
            if not (0 <= valor_nota <= 10):
                raise ValueError(f"La nota {valor_nota} no es válida. Debe ser de 0 a 10.")
            
            # Guardamos la nota (podemos imprimir la materia para que se entienda)
            self.notas.append(valor_nota)
            print(f" Nota de {asignatura} ({valor_nota}) registrada para {self.nombre}.")
            
        except ValueError as e:
            print(f" Error en {asignatura}: {e}")

    def media(self):
        try:
            if not self.notas:
                raise ValueError("No hay notas para calcular el promedio.")
            
            promedio = sum(self.notas) / len(self.notas)
            print(f"\n El promedio general de {self.nombre} es: {promedio:.2f}")
            return promedio
        except ValueError as e:
            print(f" Aviso: {e}")

    def aprobado(self):
        try:
            if not self.notas:
                raise ValueError("No hay notas suficientes para evaluar.")
            
            promedio = sum(self.notas) / len(self.notas)
            if promedio >= 5:
                print(f" {self.nombre}, has APROBADO.")
            else:
                print(f" {self.nombre}, has REPROBADO.")
        except ValueError as e:
            print(f" Error: {e}")

# 1. Creamos el objeto estudiante
estudiante_ferney = Estudiante("Ferney")

print(f"Iniciando gestor de notas para: {estudiante_ferney.nombre}\n")

# 2. materias y notas
estudiante_ferney.añadir_nota("Programación", 9.5)
estudiante_ferney.añadir_nota("Cálculo", 7.0)
estudiante_ferney.añadir_nota("Física", 6.5)
estudiante_ferney.añadir_nota("Matemáticas", 8.0)

# 3.  nota errónea
estudiante_ferney.añadir_nota("Química", 12)

# 4. Resultados finales
estudiante_ferney.media()
estudiante_ferney.aprobado()