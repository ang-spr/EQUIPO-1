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
            #Nombre Cliente
            print('Ingrese el nombre completo del cliente.')
            while True:
                nombre_cliente = darFormatoATexto(input('Nombre: '))
                if len(nombre_cliente) < 0 or len(nombre_cliente) > 50:
                    print("\nEl nombre del Cliente no puede omitirse. Ingrese de nuevo.")
                    continue
                if not validarUnicamenteTexto(nombre_cliente):
                    print("\nEl nombre solo debe contener letras y espacios.")
                    continue
                break
            guiones_separadores()

            #RFC:
            #Tipo de RFC:
            print('Ingrese el número del tipo de RFC:\n1. Físico.\n2. Moral.')
            tipo = validarOpcionesNumericas(1, 2)
            guiones_separadores()

            #Homoclave:
            print(f"Ingrese el RFC {'Físico' if tipo == 1 else 'Moral'}.")
            while True:
                rfc = darFormatoATexto(input("RFC: "))
                darFormatoATexto(rfc)            
                if (tipo == 1 and not len(rfc) == 13) or (tipo == 2 and not len(rfc) == 12):
                    print("\nIngrese la longitud correcta del RFC.")
                    continue

                if not re.match(r'^[A-Z]{3,4}[0-9]{4}[0-9]{2}[A-Z0-9]{3}$', rfc):
                    print("\nEl formato del RFC es incorrecto, ingrese un RFC válido.")
                    continue
                break
            guiones_separadores()

            #Correo electrónico:
            print('Ingrese el correo electrónico.')
            while True:
                mail = darFormatoATexto(input('Correo electronico: '))
                if not re.match(r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$', mail):
                    print('\nEl correo no es valido, ingrese un correo válido.')
                    continue
                break
            guiones_separadores()

            #Se insertan los datos en la BD (Tabla Clientes)
            try:
                with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
                    mi_cursor = conn.cursor()
                    datos_clientes = (nombre_cliente, rfc, mail)
                    mi_cursor.execute("INSERT INTO CLIENTES(NOMBRE, RFC, CORREO_ELECTRONICO)\
                    VALUES (?, ?, ?)", datos_clientes)
            except Error as e:
                print(e)
            except Exception:
                print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
            finally:
                conn.close()

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
            #Agragar un Servicio
            print('Ingrese el nuevo servicio. ')
            while True:
                nombre_servicio = darFormatoATexto(input('Nombre servicio: '))
                if nombre_servicio == '':
                    print('\nIngrese una descripción válida.')
                    continue
                break
            guiones_separadores()

            #Precio
            print('Ingrese el precio del servicio:')
            while True:
                precio = float(input('Precio: '))
                if precio <= 0.00:
                    print('El precio no es valido. Ingrese un valor superior a 0.00')
                    continue
                break
            guiones_separadores()

            #Se insertan los datos en la BD (Tabla Servicios)
            try:
                with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
                    mi_cursor = conn.cursor()
                    datos_servicios = (nombre_servicio,precio)
                    mi_cursor.execute("INSERT INTO SERVICIOS(NOMBRE_SERVICIO, PRECIO)\
                    VALUES (?, ?)", datos_servicios)
            except Error as e:
                print(e)
            except Exception:
                print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
            finally:
                conn.close()

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

##AQUI EMPECE A MODIFICAR (FATIMA LOPEZ)(como quiera modifiq arriba)
def servicios_consultasYReportes(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:    
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarValidarMenu(ubicacion, opcion, lmenu_servicios_consultasYReportes)

        
        #Listado de servicios registrados
        if opcion==1:
            servicios_consultasYReportes_listadoDeServicios(ubicacion)

        #Búsqueda por clave de servicio:
        elif opcion == 2:
            mostrarTitulo(ubicacion)
            buscarServicioPorClave()

        #Búsqueda por nombre del servicio:
        elif opcion == 3:
            mostrarTitulo(ubicacion)
            buscarServicioPorNombre()

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
                
                #Ordenado por clave
                if opcion == 1:
                    mostrarTitulo(ubicacion)
                    listarServiciosOrdenadosPorClave() #input("Aquí irá su función específica")

                #Ordenado por nombre de servicio
                elif opcion == 2:
                    mostrarTitulo(ubicacion)
                    listarServiciosOrdenadosPorNombre()

                #Volver al menú anterior.
                else:
                    break

                opcion = 0
                limpiar_consola()
                continue

#funciones para las operaciones con base da datos
def listarServiciosOrdenadosPorClave(): #listado servicio por clave
    while True:
        try:
            with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute("SELECT * FROM SERVICIOS ORDER BY CLAVE_SERVICIO")
                registros = mi_cursor.fetchall()

                guiones_separadores()
                if registros:
                    print("*" * 50)
                    print(tabulate(registros, headers = ['Clave servicio', 'Nombre servicio'], tablefmt = 'pretty'))
                    guiones_separadores()
                    while True:
                        print("1. Exportar a CSV")
                        print("2. Exportar a Excel")
                        print("3. Regresar al menú de reportes")
                        opcion = input("Seleccione una opción: ")

                        if opcion == '1':
                            exportar_a_csv(registros)
                            break
                        elif opcion == '2':
                            exportar_a_excel(registros)
                            break
                        elif opcion == '3':
                            break
                        else:
                            print("Opción no válida. Por favor, seleccione una opción válida.")
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    print("No se encontraron registros en la respuesta")

        except Error as e:
            print(e)
        except Exception:
            print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
        finally:
            conn.close()

#Exportar a EXCEL/CSV            
def exportar_a_csv(datos):
    nombre_archivo = f"ReporteServiciosPorClave_{dt.now().strftime('%m_%d_%Y')}.csv"
    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        grabador = csv.writer(archivo_csv)
        grabador.writerow(['Clave servicio', 'Nombre servicio', 'Precio'])
        grabador.writerows(datos)
    print(f"El reporte ha sido exportado a {nombre_archivo}")


def exportar_a_excel(datos):
    nombre_archivo = f"ReporteServiciosPorClave_{dt.now().strftime('%m_%d_%Y')}.xlsx"
    libro_excel = openpyxl.Workbook()
    hoja_excel = libro_excel.active
    hoja_excel.append(['Clave servicio', 'Nombre', 'Precio'])
    for fila in datos:
        hoja_excel.append(fila)
    libro_excel.save(nombre_archivo)
    print(f"El reporte ha sido exportado a {nombre_archivo}")

#******************************************************************************
#LISTADO DE SERVICIOS REGISTRADOS/ORDENADO POR NOMBRE
def listarServiciosOrdenadosPorNombre():
    while True:
        try:
            with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT * FROM SERVICIOS ORDER BY NOMBRE")
                registros = mi_cursor.fetchall()
                guiones_separadores()

                if registros:
                    print("*" * 50)
                    print(tabulate(registros, headers = ['Clave servicio', 'Nombre servicio', 'Precio'], tablefmt = 'pretty'))
                    while True:
                        print("1. Exportar a CSV")
                        print("2. Exportar a Excel")
                        print("3. Regresar al menú de reportes")
                        selecciona = input("Seleccione una opción: ")
                        if selecciona == '1':
                            exportar_a_csv(registros)
                            break
                        elif selecciona == '2':
                            exportar_a_excel(registros)
                            break
                        elif selecciona == '3':
                            break
                        else:
                            print("Opción no válida. Por favor, seleccione una opción válida.")
                        os.system('cls' if os.name == 'nt' else 'clear')    

                else:
                    print("No se encontraron registros en la respuesta")
        except Error as e:
            print(e)
        except Exception:
            print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
        finally:
            conn.close()


#Exportar datos por el nombre
def exportar_a_csv(datos):
    archivo_csv_nombre = f"ReporteServiciosPorNombre_{dt.now().strftime('%m_%d_%Y')}.csv"
    with open(archivo_csv_nombre, 'w', newline='') as csvfile:
        grabador = csv.writer(csvfile)
        grabador.writerow(['Clave servicio', 'Nombre servicio', 'Precio'])
        grabador.writerows(datos)
    print(f"El reporte ha sido exportado a {archivo_csv_nombre}")

def exportar_a_excel(datos):
    Archivo_EXCEL_Nombre = f"ReporteServiciosPorNombre_{dt.now().strftime('%m_%d_%Y')}.xlsx"
    libro_Excel = openpyxl.Workbook()
    hoja_excel = libro_Excel.active
    hoja_excel.append(['Clave servicio', 'Nombre servicio', 'Precio'])
    for fila in datos:
        hoja_excel.append(fila)
    libro_Excel.save(Archivo_EXCEL_Nombre)
    print(f"El reporte ha sido exportado a {Archivo_EXCEL_Nombre}")

def buscarServicioPorClave():
    clave_a_buscar2 = int(input('Ingrese la clave a buscar: '))
    while True:
            try:
                with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
                    mi_cursor = conn.cursor()
                    valores = {"CLAVE_SERVICIO":clave_a_buscar2}
                    mi_cursor.execute("SELECT * FROM SERVICIOS WHERE CLAVE_SERVICIO = :CLAVE_SERVICIO", valores)
                    registros = mi_cursor.fetchall()
                    if registros:
                        os.system('cls' if os.name =='nt' else 'clear')
                        print("*" * 50)
                        print(tabulate(registros, headers = ['Clave servicio', 'Nombre servicio', 'Precio'], tablefmt = 'pretty'))
                        input("Presione Enter para continuar. ")
                        break
                        os.system('cls' if os.name =='nt' else 'clear')
                    else:
                        print(f"No se encontró un registro asociado a la clave ingresada: {clave_a_buscar2}")
                        input("Presione Enter para continuar. ")
                        break
                        os.system('cls' if os.name =='nt' else 'clear')
            except Error as e:
                print(e)
            except Exception:
                print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
            finally:
                conn.close()    

#******************************************************************************
#BUSQUEDA POR NOMBRE SERVICIO
def buscarServicioPorNombre():
    nombre_a_buscar2 = darFormatoATexto(input('Ingrese el nombre a buscar: '))
    while True:
            try:
                with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
                    mi_cursor = conn.cursor()
                    valores = {"NOMBRE":nombre_a_buscar2}
                    mi_cursor.execute("SELECT * FROM SERVICIOS WHERE NOMBRE = :NOMBRE", valores)
                    registros = mi_cursor.fetchall()
                    if registros:
                        os.system('cls' if os.name =='nt' else 'clear')
                        print("*" * 50)
                        print(tabulate(registros, headers = ['Clave servicio', 'Nombre servicio', 'Precio'], tablefmt = 'pretty'))
                        input("Presione Enter para continuar. ")
                        break
                        os.system('cls' if os.name =='nt' else 'clear')
                    else:
                        print(f"No se encontró un registro asociado al nombre ingresado: {nombre_a_buscar2}")
                        input("Presione Enter para continuar. ")
                        break
                        os.system('cls' if os.name =='nt' else 'clear')
            except Error as e:
                print(e)
            except Exception:
                print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
            finally:
                conn.close()               

##### HASTA AQUIII MODIFIQUE FATIMA LOPEZ




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
        
        print(guiones(25))
        print('Tablas creadas existosamente')
        print(guiones(25))
except Error as e:
    print(e)
except Exception:
    print(f'Se produjo el siguiente error {sys.exc_info()[0]}')
finally:
    conn.close()

#-------------------------------------------------------------------------------------------------------------------------------
#EJECUTAR MENÚ PRINCIPAL:
menuPrincipal()


#prueba commit
