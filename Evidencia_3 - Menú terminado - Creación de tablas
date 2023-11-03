#-------------------------------------------------------------------------------------------------------------------------------
#MÓDULOS:
import os
from unidecode import unidecode
import re
import datetime as dt
from tabulate import tabulate
import numpy as np
import sqlite3
from sqlite3 import Error
import sys

#-------------------------------------------------------------------------------------------------------------------------------
#FUNCIONES AUXILIARES:

#Limpia la pantalla.
def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

#Imprime 50 guiones para hacer una separación entre mensajes.
def guiones_separadores():
    return print('-' * 50)

#Imprime la cantidad de guiones que le mandemos como parámetro.
def guiones(longitud):
    return '-' * longitud

def aviso(mensaje, longitud):
    print(f"\n{guiones(longitud)} {mensaje} {guiones(longitud)}\n".upper()) 

def indicarEnter():
    input("\n\nDe clic en Enter para continuar.")

def fechaActual():
    fecha_actual = dt.date.today()
    return fecha_actual

'''Formatear texto:'''
#Elimina números y caracteres especiales si se indica como True el segundo y tercer parámetro.
#Por defecto:
#-Quita espacios del principio y del final.
#-Convierte a mayúscula.
#-Convierte letras con acento a sin acento.
#-Quita espacios entre palabras en caso de que haya más de un espacio, por ejemplo: "ANA     XIMENA" a "ANA XIMENA".
def darFormatoATexto(texto, eliminarNumeros = False, eliminarCaracteresEspeciales = False):
    if eliminarNumeros:
        texto = re.sub(r'\d', '', texto)

    if eliminarCaracteresEspeciales:
        texto = re.sub(r'[^A-Za-z0-9 ]', '', texto)

    texto = unidecode(texto).strip().upper()
    texto = re.sub(r'\s+', ' ', texto)

    return texto

#Valida que haya ingresado únicamente letras y espacios.
def validarUnicamenteTexto(texto):
    if texto.replace(' ', '').isalpha():
        return True
    return False

def respuestaSINO():
    while True:
        respuesta = darFormatoATexto(input('\tRespuesta: '))

        if respuesta == 'SI' or respuesta == 'NO':
            break
        else:
            print('\n\tIngrese una respuesta válida (Sí/No).')
    return respuesta

def validarOpcionesNumericas(opcionMin, opcionMax):
    while True:
        try:
            opcionValida = int(input(f"Opción: "))
            if opcionValida >= opcionMin and opcionValida <= opcionMax:
                return opcionValida
            else:
                print(f"\nIngrese un número válido ({opcionMin}-{opcionMax}).")
        except ValueError:
            print(f"\nIngrese un número válido ({opcionMin}-{opcionMax}).")

def validarContinuarOpcion():
    continuarOpcion = None
    while continuarOpcion != "0" and continuarOpcion != "":
        continuarOpcion = input(f"Pulse Enter para continuar la opción actual o ingrese 0 para volver al menú principal. ").strip()
    if continuarOpcion == "0":
        return True

def contarCantidadOpcionesDeMenu(listaActual):
    cantidad = len(listaActual) - 1
    return cantidad

def mostrarOpcionesDeMenu(listaActual):
    print('Ingrese el número de la opción que desee realizar:')
    print(tabulate(listaActual, headers = 'firstrow', tablefmt = 'pretty'))

def mostrarValidarMenu(ubicacion, opcion, lista):
    mostrarTitulo(ubicacion, True)
    
    mostrarOpcionesDeMenu(lista)

    opcion = validarOpcionesNumericas(1, contarCantidadOpcionesDeMenu(lista))

    limpiar_consola() 
    
    if not opcion == contarCantidadOpcionesDeMenu(lista):
            ubicacion.append(lista[opcion][1])

    return opcion, ubicacion

def mostrarTitulo(ubicacion, esMenu = False):
    print(f'Ubicación: {" / ".join(ubicacion)}')
    
    if esMenu == True:
        aviso(f'MENÚ {ubicacion[-1]}', 20)
    
    else:
        aviso(f'{ubicacion[-1]}', 20)
        return


#-------------------------------------------------------------------------------------------------------------------------------
#FUNCIONES DE MENÚS:
#--------------------------------------------------------------------------
#MENÚ PRINCIPAL:
#menuPrincipal.
def menuPrincipal():
    opcion = 0

    while True:    
        ubicacion = ['Menú principal']
        if opcion == 0:
            aviso('TALLER MECÁNICO DON HAMBLETON', 20)
            print('¡Bienvenido al menú principal!\n')
            mostrarOpcionesDeMenu(lmenu_principal)

            opcion = validarOpcionesNumericas(1, contarCantidadOpcionesDeMenu(lmenu_principal))

        if not opcion == contarCantidadOpcionesDeMenu(lmenu_principal):
            ubicacion.append(lmenu_principal[opcion][1])
            limpiar_consola()

        #Menú Notas:
        if opcion == 1:
            menuNotas(ubicacion)

        #Menú Clientes:
        elif opcion == 2:
            menuClientes(ubicacion)            

        #Menú Servicios:
        elif opcion == 3:
            menuServicios(ubicacion)
        
        #Salir.
        else:
            print('\n¿Está seguro que desea salir? (Sí/No)')
            respuesta = respuestaSINO()

            if respuesta == 'SI':
                aviso("Archivo cerrado correctamente.", 15)
                aviso("Gracias por usar nuestro sistema, hasta la próxima.", 15)
                break
            else:
                limpiar_consola()
                opcion = 0

        opcion = 0
        continue

#--------------------------------------------------------------------------
#NOTAS:
#menuPrincipal/menuNotas.
def menuNotas(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:    
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarValidarMenu(ubicacion, opcion, lmenu_notas)

        #Registrar una nota:
        if opcion == 1:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Cancelar una nota:
        elif opcion == 2:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Recuperar una nota:
        elif opcion == 3:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Consultas y reportes:
        elif opcion == 4:
            notas_consultasYReportes(ubicacion)

        #Volver al menú anterior.
        else:
            break

        opcion = 0
        limpiar_consola()
        continue

#menuPrincipal/menuNotas/consultasYReportes.
def notas_consultasYReportes(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarValidarMenu(ubicacion, opcion, lmenu_notas_consultasYReportes)
        
        #Consulta por período:
        if opcion == 1:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Consulta por folio:
        elif opcion == 2:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Volver al menú anterior.
        else:
            break

        opcion = 0
        limpiar_consola()
        continue

#--------------------------------------------------------------------------
#CLIENTES:
#menuPrincipal/menuClientes.
def menuClientes(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:    
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarValidarMenu(ubicacion, opcion, lmenu_clientes)

        #Agregar un cliente:
        if opcion == 1:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Consultas y reportes:
        elif opcion == 2:
            clientes_consultasYReportes(ubicacion)

        #Volver al menú anterior.
        else:
            break

        opcion = 0
        limpiar_consola()
        continue

#menuPrincipal/menuClientes/consultasYReportes.
def clientes_consultasYReportes(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarValidarMenu(ubicacion, opcion, lmenu_clientes_consultasYReportes)
        
        #Listado de clientes registrados:
        if opcion == 1:
            clientes_consultasYReportes_listadoDeClientesRegistrados(ubicacion)

        #Búsqueda por clave:
        elif opcion == 2:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Búsqueda por nombre:
        elif opcion == 3:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Volver al menú anterior.
        else:
            break

        opcion = 0
        limpiar_consola()
        continue

#menuPrincipal/menuClientes/consultasYReportes/listadoDeClientesRegistrados.
def clientes_consultasYReportes_listadoDeClientesRegistrados(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarValidarMenu(ubicacion, opcion, lmenu_clientes_consultasYReportes_listadoDeClientesRegistrados)
        
        #Ordenado por clave:
        if opcion == 1:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Ordenado por nombre:
        elif opcion == 2:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Volver al menú anterior.
        else:
            break

        opcion = 0
        limpiar_consola()
        continue

#--------------------------------------------------------------------------
#SERVICIOS:
#menuPrincipal/menuServicios.
def menuServicios(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:    
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarValidarMenu(ubicacion, opcion, lmenu_servicios)

        #Agregar un servicio:
        if opcion == 1:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Consultas y reportes:
        elif opcion == 2:
            servicios_consultasYReportes(ubicacion)

        #Volver al menú anterior.
        else:
            break

        opcion = 0
        limpiar_consola()
        continue

#menuPrincipal/menuServicios/menuConsultasYReportes.
def servicios_consultasYReportes(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:    
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarValidarMenu(ubicacion, opcion, lmenu_servicios_consultasYReportes)

        #Búsqueda por clave de servicio:
        if opcion == 1:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Búsqueda por nombre de servicio:
        elif opcion == 2:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Listado de servicios:
        elif opcion == 3:
            servicios_consultasYReportes_listadoDeServicios(ubicacion)

        #Volver al menú anterior.
        else:
            break

        opcion = 0
        limpiar_consola()
        continue

#menuPrincipal/menuServicios/menuConsultasYReportes/menuListadoDeServicios.
def servicios_consultasYReportes_listadoDeServicios(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:    
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarValidarMenu(ubicacion, opcion, lmenu_servicios_consultasYReportes_listadoDeServicios)

        #Ordenado por clave:
        if opcion == 1:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Ordenado por nombre de servicio:
        elif opcion == 2:
            mostrarTitulo(ubicacion)
            input("Aquí irá su función específica")

        #Volver al menú anterior.
        else:
            break

        opcion = 0
        limpiar_consola()
        continue

#-------------------------------------------------------------------------------------------------------------------------------
#FUNCIONES ESPECÍFICAS:



#-------------------------------------------------------------------------------------------------------------------------------
#LISTAS DE MENÚS:
#--------------------------------------------------------------------------
#MENÚ PRINCIPAL:
#principal
lmenu_principal = [('Opción', 'Descripción'),
              (1, 'Notas'),
              (2, 'Clientes'),
              (3, 'Servicios'),
              (4, 'Salir')]

#--------------------------------------------------------------------------
#NOTAS:
#principal/notas
lmenu_notas = [('Opción', 'Descripción'),
              (1, 'Registrar una nota'),
              (2, 'Cancelar una nota'),
              (3, 'Recuperar una nota'),
              (4, 'Consultas y reportes'),
              (5, 'Volver al menú principal')]

#principal/notas/consultasYReportes
lmenu_notas_consultasYReportes = [('Opción', 'Descripción'),
              (1, 'Consulta por período'),
              (2, 'Consulta por folio'),
              (3, 'Volver al menú de notas')]

#--------------------------------------------------------------------------
#CLIENTES:
#principal/clientes.
lmenu_clientes = [('Opción', 'Descripción'),
                       (1, 'Agregar un cliente'),
                       (2, 'Consultas y reportes'),
                       (3, 'Volver al menú principal')]

#principal/clientes/consultasYReportes.
lmenu_clientes_consultasYReportes = [('Opción', 'Descripción'),
                       (1, 'Listado de clientes registrados'),
                       (2, 'Búsqueda por clave'),
                       (3, 'Búsqueda por nombre'),
                       (4, 'Volver al menú de clientes')]

#principal/clientes/consultasYReportes/listadoDeClientesRegistrados.
lmenu_clientes_consultasYReportes_listadoDeClientesRegistrados = [('Opción', 'Descripción'),
                       (1, 'Orden por clave'),
                       (2, 'Orden por nombre'),
                       (3, 'Volver al menú anterior')]

#--------------------------------------------------------------------------
#SERVICIOS:
#principal/servicios.
lmenu_servicios = [('Opción', 'Descripción'),
              (1, 'Agregar un servicio'),
              (2, 'Consultas y reportes'),
              (3, 'Volver al menú principal')]

#principal/servicios/consultasYReportes.
lmenu_servicios_consultasYReportes = [('Opción', 'Descripción.'),
              (1, 'Búsqueda por clave de servicio'),
              (2, 'Búsqueda por nombre de servicio'),
              (3, 'Listado de servicios'),
              (4, 'Volver al menú de servicios')]

#principal/servicios/consultasYReportes/listadoDeServicios.
lmenu_servicios_consultasYReportes_listadoDeServicios = [('Opción', 'Descripción'),
              (1, 'Orden por clave'),
              (2, 'Orden por nombre de servicio'),
              (3, 'Volver al menú anterior')]


#-------------------------------------------------------------------------------------------------------------------------------
#CREACIÓN DE TABLAS SQL:
try:
    with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
        mi_cursor = conn.cursor()
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS CLIENTES \
                        (CLAVE_CLIENTE INTEGER PRIMARY KEY NOT NULL, NOMBRE TEXT NOT NULL, \
                        RFC TEXT NULL, CORREO_ELECTRONICO TEXT NOT NULL);")

        mi_cursor.execute("CREATE TABLE IF NOT EXISTS NOTAS \
                        (FOLIO INTEGER PRIMARY KEY NOT NULL, FECHA timestamp NOT NULL, \
                        CLAVE_CLIENTE INTEGER NOT NULL, MONTO_A_PAGAR REAL NOT NULL, \
                        FOREIGN KEY (CLAVE_CLIENTE) REFERENCES CLIENTES(CLAVE_CLIENTE));")

        mi_cursor.execute("CREATE TABLE IF NOT EXISTS SERVICIOS \
                        (CLAVE_SERVICIO INTEGER PRIMARY KEY NOT NULL, NOMBRE_SERVICIO TEXT NOT NULL, \
                        COSTO_SERVICIO REAL NOT NULL);")

        mi_cursor.execute("CREATE TABLE IF NOT EXISTS DETALLE_NOTA \
                        (CLAVE_DETALLE INTEGER PRIMARY KEY NOT NULL, \
                        FOLIO INTEGER NOT NULL, \
                        CLAVE_SERVICIOS INTEGER NOT NULL,  \
                        FOREIGN KEY (FOLIO) REFERENCES NOTAS(FOLIO), \
                        FOREIGN KEY (CLAVE_SERVICIOS) REFERENCES SERVICIOS(CLAVE_SERVICIOS));")
        
        print(f'{guiones(17)}Tablas creadas o localizadas existosamente.{guiones(17)}')
except Error as e:
    print(e)
except Exception:
    print(f'Se produjo el siguiente error {sys.exc_info()[0]}')
finally:
    conn.close()


#-------------------------------------------------------------------------------------------------------------------------------
#EJECUTAR MENÚ PRINCIPAL:
menuPrincipal()
