"""
================================================================================
SISTEMA DE GESTION DE POLICIAS VOLUNTARIOS - MANAGUA
================================================================================
Conceptos de programacion aplicados:
    - Variables y tipos de datos (str, int, float, bool, list, dict)
    - Entrada/salida de datos (input, print)
    - Operadores aritmeticos, relacionales y logicos
    - Estructuras condicionales (if, elif, else)
    - Estructuras repetitivas (for, while)
    - Funciones (con y sin parametros, con y sin retorno)
    - Listas y diccionarios
    - Clases y objetos (POO)
    - Encapsulamiento, herencia, polimorfismo
    - Manejo de excepciones (try, except)
    - Modulos y funcion principal (__main__)
================================================================================
"""

import os
import re
import datetime


# ==============================================================================
# EXCEPCIONES PERSONALIZADAS
# ==============================================================================
class EntradaInvalidaError(Exception):
    """Se lanza cuando el usuario ingresa un dato fuera de rango o invalido."""
    pass


# ==============================================================================
# CLASE BASE (HERENCIA / ENCAPSULAMIENTO)
# ==============================================================================
class Persona:
    """Clase base que representa a una persona con datos generales."""

    def __init__(self, nombre, edad, telefono):
        # Atributos "protegidos" -> encapsulamiento
        self._nombre = nombre
        self._edad = edad
        self._telefono = telefono

    # ---- Propiedades (getters) ----
    @property
    def nombre(self):
        return self._nombre

    @property
    def edad(self):
        return self._edad

    @property
    def telefono(self):
        return self._telefono

    def mostrar_info(self):
        """Metodo que sera sobrescrito (polimorfismo)."""
        return f"Nombre: {self._nombre} | Edad: {self._edad} | Telefono: {self._telefono}"


# ==============================================================================
# CLASE HIJA (HERENCIA + POLIMORFISMO)
# ==============================================================================
class PoliciaVoluntario(Persona):
    """Representa a un candidato a policia voluntario de Managua."""

    # Diccionario de distritos de Managua (dato de clase)
    DISTRITOS = {
        1: "Distrito I",
        2: "Distrito II",
        3: "Distrito III",
        4: "Distrito IV",
        5: "Distrito V",
        6: "Distrito VI",
        7: "Distrito VII",
        8: "Distrito VIII",
        9: "Distrito IX",
        10: "Distrito X",
    }

    def __init__(self, nombre, edad, telefono, distrito):
        super().__init__(nombre, edad, telefono)  # herencia
        self._distrito = distrito
        self._condicion_fisica = None      # 1 - 10
        self._enfermedades = []            # lista de enfermedades seleccionadas
        self._gravedad_otros = None        # 1 - 10 (solo si eligio "Otros")
        self._clasificacion = None         # "SEMANA" o "FIN DE SEMANA"
        self._fecha_registro = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    # ---- Setters controlados (encapsulamiento) ----
    def set_condicion_fisica(self, valor):
        self._condicion_fisica = valor

    def set_enfermedades(self, lista_enfermedades):
        self._enfermedades = lista_enfermedades

    def set_gravedad_otros(self, valor):
        self._gravedad_otros = valor

    def set_clasificacion(self, texto):
        self._clasificacion = texto

    def get_distrito_nombre(self):
        return self.DISTRITOS.get(self._distrito, "Desconocido")

    # ---- Polimorfismo: sobrescribe el metodo de la clase padre ----
    def mostrar_info(self):
        info_base = super().mostrar_info()
        return (f"{info_base} | Distrito: {self.get_distrito_nombre()} | "
                f"Condicion fisica: {self._condicion_fisica}/10 | "
                f"Clasificacion: {self._clasificacion}")


# ==============================================================================
# CLASE PARA LA EVALUACION MEDICA (SELECCION MULTIPLE)
# ==============================================================================
class EvaluacionMedica:
    """Contiene la logica de las preguntas de seleccion multiple y clasificacion."""

    ENFERMEDADES_COMUNES = [
        "Diabetes",
        "Hipertension",
        "Problemas cardiacos",
        "Asma",
        "Problemas renales",
        "Obesidad",
        "Epilepsia",
        "Otros",
        "Ninguno",
    ]

    # Enfermedades que por si solas obligan al curso fin de semana
    ENFERMEDADES_GRAVES = [
        "Diabetes",
        "Problemas cardiacos",
        "Asma",
        "Problemas renales",
        "Epilepsia",
    ]

    # Enfermedades que NO sacan al candidato del curso entre semana,
    # pero generan un mensaje de advertencia para tener cuidado con el candidato
    ENFERMEDADES_ADVERTENCIA = [
        "Hipertension",
        "Obesidad",
    ]

    UMBRAL_GRAVEDAD = 5       # gravedad >= 5 en "Otros" se considera riesgo
    UMBRAL_CONDICION_FISICA = 5  # condicion fisica < 5 se considera riesgo

    # Reglas de edad
    EDAD_MINIMA = 18            # menor a esto -> no apto para ninguna opcion
    EDAD_MAXIMA = 70            # mayor a esto -> no apto para ninguna opcion
    EDAD_MAYOR_RIESGO = 55      # de aqui hasta EDAD_MAXIMA -> directo a fin de semana

    def __init__(self, policia: PoliciaVoluntario):
        self.policia = policia

    # ---- Funcion con retorno: valida un numero dentro de un rango ----
    @staticmethod
    def pedir_numero(mensaje, minimo, maximo):
        while True:
            try:
                valor = int(input(mensaje))
                if valor < minimo or valor > maximo:
                    raise EntradaInvalidaError(f"Debe ingresar un numero entre {minimo} y {maximo}.")
                return valor
            except ValueError:
                print(">> Entrada invalida. Debe ingresar solo numeros.")
            except EntradaInvalidaError as e:
                print(f">> {e}")

    def preguntar_condicion_fisica(self):
        print("\n--- PREGUNTA 1: Estado fisico ---")
        print("En una escala del 1 al 10, ¿como calificaria su condicion fisica actual?")
        print("(1 = muy mala, 10 = excelente)")
        valor = self.pedir_numero("Seleccione un numero (1-10): ", 1, 10)
        self.policia.set_condicion_fisica(valor)

    def preguntar_enfermedades(self):
        print("\n--- PREGUNTA 2: Enfermedades cronicas ---")
        print("Seleccione TODAS las opciones que apliquen (separadas por coma).")
        for indice, enfermedad in enumerate(self.ENFERMEDADES_COMUNES, start=1):
            print(f"  {indice}. {enfermedad}")

        seleccionadas = []
        while True:
            try:
                entrada = input("Ingrese los numeros de sus opciones (ej: 1,3): ").strip()
                numeros = [int(n.strip()) for n in entrada.split(",")]

                for n in numeros:
                    if n < 1 or n > len(self.ENFERMEDADES_COMUNES):
                        raise EntradaInvalidaError("Hay un numero fuera del rango de opciones.")

                seleccionadas = [self.ENFERMEDADES_COMUNES[n - 1] for n in numeros]

                # Regla logica: "Ninguno" no se puede combinar con otras opciones
                if "Ninguno" in seleccionadas and len(seleccionadas) > 1:
                    print(">> Si selecciona 'Ninguno' no puede marcar otra enfermedad.")
                    continue
                break
            except ValueError:
                print(">> Entrada invalida. Use numeros separados por coma.")
            except EntradaInvalidaError as e:
                print(f">> {e}")

        self.policia.set_enfermedades(seleccionadas)

        # Si eligio "Otros", preguntar la gravedad
        if "Otros" in seleccionadas:
            print("\n--- PREGUNTA 3: Gravedad de la enfermedad 'Otros' ---")
            gravedad = self.pedir_numero(
                "Del 1 al 10, ¿que tan grave es esa condicion? (1 = leve, 10 = muy grave): ", 1, 10
            )
            self.policia.set_gravedad_otros(gravedad)

    # ---- Funcion sin parametros que usa logica condicional y operadores logicos ----
    def clasificar_candidato(self):
        edad = self.policia.edad
        enfermedades = self.policia._enfermedades  # uso interno controlado
        gravedad_otros = self.policia._gravedad_otros
        condicion_fisica = self.policia._condicion_fisica

        tiene_enfermedad_grave = any(e in self.ENFERMEDADES_GRAVES for e in enfermedades)
        tiene_otro_grave = (
            "Otros" in enfermedades
            and gravedad_otros is not None
            and gravedad_otros >= self.UMBRAL_GRAVEDAD
        )
        baja_condicion_fisica = condicion_fisica is not None and condicion_fisica < self.UMBRAL_CONDICION_FISICA
        edad_mayor_riesgo = edad >= self.EDAD_MAYOR_RIESGO

        es_riesgo = tiene_enfermedad_grave or tiene_otro_grave or baja_condicion_fisica or edad_mayor_riesgo

        if es_riesgo:
            self.policia.set_clasificacion("CURSO FIN DE SEMANA (Sabado y Domingo)")
        else:
            self.policia.set_clasificacion("CURSO ENTRE SEMANA (Lunes a Viernes)")

        return self.policia._clasificacion

    # ---- Funcion con retorno: devuelve la lista de enfermedades de advertencia presentes ----
    def obtener_advertencias(self):
        enfermedades = self.policia._enfermedades
        return [e for e in enfermedades if e in self.ENFERMEDADES_ADVERTENCIA]

    def ejecutar_evaluacion_completa(self):
        self.preguntar_condicion_fisica()
        self.preguntar_enfermedades()
        return self.clasificar_candidato()


# ==============================================================================
# CLASE DEL SISTEMA (CONTROLADOR PRINCIPAL)
# ==============================================================================
class SistemaGestion:
    def __init__(self):
        self._policias = []  # lista de objetos PoliciaVoluntario

    @staticmethod
    def limpiar_pantalla():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def pedir_texto_no_vacio(mensaje):
        while True:
            valor = input(mensaje).strip()
            if valor == "":
                print(">> Este campo no puede quedar vacio.")
                continue
            return valor

    # ---- Funcion con retorno: valida que el nombre solo tenga letras (como en cedula) ----
    @staticmethod
    def pedir_nombre(mensaje):
        patron_nombre = re.compile(r"^[A-Za-zÁÉÍÓÚÑÜáéíóúñü\s]+$")
        while True:
            valor = input(mensaje).strip()
            if valor == "":
                print(">> Este campo no puede quedar vacio.")
                continue
            if not patron_nombre.match(valor):
                print(">> Nombre invalido. Solo se permiten letras y espacios "
                      "(sin numeros ni simbolos), tal como aparece en la cedula.")
                continue
            return valor

    def pedir_distrito(self):
        print("\nDistritos disponibles de Managua:")
        for numero, nombre in PoliciaVoluntario.DISTRITOS.items():
            print(f"  {numero}. {nombre}")
        return EvaluacionMedica.pedir_numero("Seleccione el numero de su distrito (1-10): ", 1, 10)

    def registrar_policia(self):
        print("\n" + "=" * 78)
        print("REGISTRO DE NUEVO CANDIDATO A POLICIA VOLUNTARIO")
        print("=" * 78)

        nombre = self.pedir_nombre("Nombre completo (tal como aparece en su cedula): ")
        edad = EvaluacionMedica.pedir_numero("Edad: ", 1, 120)

        # Regla de edad: fuera de 18-70 -> no apto para ninguna opcion
        if edad < EvaluacionMedica.EDAD_MINIMA or edad > EvaluacionMedica.EDAD_MAXIMA:
            print("\n" + "=" * 78)
            print(f">>> {nombre} NO ES APTO PARA NINGUNA DE LAS DOS OPCIONES DE CURSO <<<")
            print(f">>> (La edad debe estar entre {EvaluacionMedica.EDAD_MINIMA} y "
                  f"{EvaluacionMedica.EDAD_MAXIMA} anios) <<<")
            print("=" * 78)
            return

        telefono = self.pedir_texto_no_vacio("Numero de telefono: ")
        distrito = self.pedir_distrito()

        nuevo_policia = PoliciaVoluntario(nombre, edad, telefono, distrito)
        self._policias.append(nuevo_policia)

        print("\nDatos registrados correctamente. Ahora responda la evaluacion medica.")
        evaluacion = EvaluacionMedica(nuevo_policia)
        clasificacion = evaluacion.ejecutar_evaluacion_completa()

        print("\n" + "=" * 78)
        if clasificacion == "CURSO ENTRE SEMANA (Lunes a Viernes)":
            print(f">>> {nombre} ES APTO PARA EL CURSO ENTRE SEMANA (LUNES A VIERNES) <<<")
            advertencias = evaluacion.obtener_advertencias()
            if advertencias:
                lista_adv = ", ".join(advertencias)
                print(f">>> ADVERTENCIA: el candidato padece {lista_adv}. "
                      f"Tener cuidado y dar seguimiento durante el curso. <<<")
        else:
            print(f">>> {nombre} FUE CLASIFICADO PARA EL CURSO FIN DE SEMANA (SABADO Y DOMINGO) <<<")
            if edad >= EvaluacionMedica.EDAD_MAYOR_RIESGO:
                print(f">>> Motivo: tiene {edad} anios (55 a 70 anios va directo a fin de semana). <<<")
            print(f">>> El dia que se presente debe llevar su epicrisis medica. <<<")
        print("=" * 78)

    def listar_policias(self):
        print("\n" + "=" * 78)
        print("LISTADO DE POLICIAS VOLUNTARIOS REGISTRADOS")
        print("=" * 78)
        if not self._policias:
            print("Aun no hay candidatos registrados.")
            return
        for indice, policia in enumerate(self._policias, start=1):
            print(f"{indice}. {policia.mostrar_info()}")

    # ---- Menu principal con bucle while ----
    def menu_principal(self):
        opcion = ""
        while opcion != "3":
            print("\n" + "#" * 78)
            print("SISTEMA DE GESTION DE POLICIAS VOLUNTARIOS - MANAGUA")
            print("#" * 78)
            print("1. Agregar candidato")
            print("2. Ver lista de candidatos")
            print("3. Salir")

            opcion = input("Seleccione una opcion: ").strip()

            if opcion == "1":
                self.registrar_policia()
            elif opcion == "2":
                self.listar_policias()
            elif opcion == "3":
                print("\nSaliendo del sistema. ¡Gracias por su servicio voluntario!")
            else:
                print(">> Opcion invalida, intente de nuevo.")


# ==============================================================================
# FUNCION PRINCIPAL / PUNTO DE ENTRADA DEL MODULO
# ==============================================================================
def main():
    sistema = SistemaGestion()
    sistema.menu_principal()


if __name__ == "__main__":
    main()
