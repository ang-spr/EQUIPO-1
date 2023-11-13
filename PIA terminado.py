import os
from unidecode import unidecode
import re
import datetime as dt
from tabulate import tabulate
import sqlite3
from sqlite3 import Error
import sys
import pandas as pd

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def guiones_separadores():
    return print('-' * 50)

def guiones(longitud):
    return '-' * longitud

def aviso(mensaje, longitud):
    print(f"\n{guiones(longitud)} {mensaje} {guiones(longitud)}\n".upper()) 

def indicarEnter():
    input("\n\nDe clic en Enter para continuar.")

def fechaActual():
    fecha_actual = dt.date.today()
    return fecha_actual

def darFormatoATexto(texto, eliminarNumeros = False, eliminarCaracteresEspeciales = False):
    if eliminarNumeros:
        texto = re.sub(r'\d', '', texto)

    if eliminarCaracteresEspeciales:
        texto = re.sub(r'[^A-Za-z0-9 ]', '', texto)

    texto = unidecode(texto).strip().upper()
    texto = re.sub(r'\s+', ' ', texto)

    return texto

def validarUnicamenteTexto(texto):
    if texto.replace(' ', '').isalpha():
        return True
    return False

def solicitarSoloNumeroEntero(descripcion):
    while True:
        respuesta = input(f"{descripcion}: ")

        if respuesta.isdigit():
            return int(respuesta)
        else:
            print("\nIngrese un número válido.")

def respuestaSINO():
    while True:
        respuesta = darFormatoATexto(input('\tRespuesta: '))

        if respuesta == 'SI' or respuesta == 'NO':
            break
        else:
            print('\n\tIngrese una respuesta válida (Sí/No).')
    return respuesta

def validarContinuarOpcion():
    continuarOpcion = None
    while continuarOpcion != "0" and continuarOpcion != "":
        continuarOpcion = input(f"Pulse Enter para continuar la opción actual o ingrese 0 para volver al menú anterior. ").strip()
    if continuarOpcion == "0":
        return True
    else:
        print("\n")
    
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

def contarCantidadOpcionesDeMenu(listaActual):
    cantidad = len(listaActual) - 1
    return cantidad

def mostrarOpcionesDeMenu(listaActual):
    print('Ingrese el número de la opción que desee realizar:')
    print(tabulate(listaActual, headers = 'firstrow', tablefmt = 'pretty'))

def mostrarYValidarMenu(ubicacion, opcion, lista):
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

        if opcion == 1:
            menuNotas(ubicacion)

        elif opcion == 2:
            menuClientes(ubicacion)            

        elif opcion == 3:
            menuServicios(ubicacion)

        elif opcion == 4:
            menuEstadisticas(ubicacion)
        
        else:
            print('\n¿Está seguro que desea salir? (Sí/No)')
            respuesta = respuestaSINO()

            if respuesta == 'SI':
                aviso("Archivo cerrado correctamente.", 25)
                aviso("Gracias por usar nuestro sistema, hasta la próxima.", 15)
                break
            else:
                limpiar_consola()
                opcion = 0

        opcion = 0
        continue

def menuNotas(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:    
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarYValidarMenu(ubicacion, opcion, lmenu_notas)

        if opcion == 1:
            mostrarTitulo(ubicacion)
            registrarNota()

        elif opcion == 2:
            mostrarTitulo(ubicacion)
            cancelarNota()

        elif opcion == 3:
            mostrarTitulo(ubicacion)
            recuperarNota()
            
        elif opcion == 4:
            notas_consultasYReportes(ubicacion)

        else:
            break

        opcion = 0
        limpiar_consola()
        continue

def notas_consultasYReportes(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarYValidarMenu(ubicacion, opcion, lmenu_notas_consultasYReportes)
        
        if opcion == 1:
            mostrarTitulo(ubicacion)
            notas_consultaPorPeriodo()

        elif opcion == 2:
            mostrarTitulo(ubicacion)
            notas_consultaPorFolio()

        else:
            break

        opcion = 0
        limpiar_consola()
        continue

def registrarNota():
    if validarContinuarOpcion():
        return

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT CLAVE_CLIENTE, NOMBRE, RFC, CORREO_ELECTRONICO FROM CLIENTES WHERE ESTADO_CLIENTE = 1;")
            clientes = mi_cursor.fetchall()
            mi_cursor.execute("SELECT CLAVE_SERVICIO, NOMBRE_SERVICIO, COSTO_SERVICIO FROM SERVICIOS WHERE ESTADO_SERVICIO = 1;")
            servicios = mi_cursor.fetchall()

            if not clientes:
                aviso("Es necesario tener al menos un cliente registrado y activo para generar una nota.", 15)
                indicarEnter()
                return
            
            if not servicios:
                aviso("Es necesario tener al menos un servicio registrado y activo para generar una nota.", 15)
                indicarEnter()
                return 
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}.')
    finally:
        conn.close()

    print("Ingrese la fecha de la realización de la nota (dd/mm/aaaa).")
    while True:
        fecha_registro = input("Fecha: ").strip()
        try:
            fecha_procesada = dt.datetime.strptime(fecha_registro, "%d/%m/%Y").date()
            if fecha_procesada > fechaActual():
                print("\nLa fecha ingresada no debe ser posterior a la fecha actual.\nIngrese una fecha válida.")
                continue
            break
        except ValueError:
            print("\nIngrese una fecha válida en formato (dd/mm/aaaa).")
    guiones_separadores()

    print('Ingrese la clave del cliente: ')
    print(tabulate(clientes, headers = ['Clave del cliente', 'Nombre', 'RFC', 'Correo electrónico'], tablefmt = 'pretty'))
    while True:
        id_cliente = solicitarSoloNumeroEntero('Clave')
        try:
            with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT CLAVE_CLIENTE FROM CLIENTES WHERE CLAVE_CLIENTE = ? AND ESTADO_CLIENTE = 1", (id_cliente,))
                existencia = mi_cursor.fetchall()

                if existencia:
                    break
                else:
                    print("\nEl cliente con la clave proporcionada no existe, ingrese una clave válida.")
        except Error as e:
            print(e)
        except Exception:
            print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
        finally:
            conn.close()
    guiones_separadores()

    servicios_seleccionados = []
    cantidadServicios = 0
    costos_servicios = []
    print('Ingrese la clave del servicio:') 
    print(tabulate(servicios, headers = ['Clave del servicio', 'Nombre', 'Precio'], tablefmt = 'pretty'))
    
    while True:
        id_servicio = solicitarSoloNumeroEntero('Clave')
        try:
            with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT CLAVE_SERVICIO FROM SERVICIOS WHERE CLAVE_SERVICIO = ? AND ESTADO_SERVICIO = 1", (id_servicio,))
                existencia = mi_cursor.fetchall()

                if existencia:
                    mi_cursor.execute("SELECT COSTO_SERVICIO FROM SERVICIOS WHERE CLAVE_SERVICIO = ? AND ESTADO_SERVICIO = 1", (id_servicio,))
                    servicios_seleccionados.append(id_servicio)
                    costo_servicio = mi_cursor.fetchone()[0]
                    costos_servicios.append(costo_servicio)
                    cantidadServicios += 1
                    guiones_separadores()
                    aviso(f"Servicio agregado correctamente.", 0)
                    print('\t¿Desea agregar otro servicio? (Sí/No)')
                    otro_servicio = respuestaSINO()
                    
                    if otro_servicio == 'SI':
                        limpiar_consola()
                        aviso(f"{cantidadServicios} servicio(s) guardado(s) correctamente.", 15)
                        print(f"Ingrese el servicio número {cantidadServicios + 1}.")
                        print(tabulate(servicios, headers = ['Clave del servicio', 'Nombre', 'Precio'], tablefmt = 'pretty'))
                        continue
                    break
                else:
                    print("\nEl servicio con la clave proporcionada no existe, ingrese una clave válida.")
        except Error as e:
            print(e)
        except Exception:
            print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
        finally:
            conn.close()
    guiones_separadores()

    monto_a_pagar = sum(costos_servicios)
    estado_nota = 1

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            datos_notas = (fecha_procesada, id_cliente, monto_a_pagar, estado_nota)
            mi_cursor.execute("INSERT INTO NOTAS(FECHA, CLAVE_CLIENTE, MONTO_A_PAGAR, ESTADO_NOTA) \
                                VALUES (?, ?, ?, ?)", datos_notas)
            folio = mi_cursor.lastrowid
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            for id_servicio in servicios_seleccionados:
                mi_cursor.execute("INSERT INTO DETALLE_NOTA(FOLIO, CLAVE_SERVICIO) VALUES (?, ?)",
                                  (folio, id_servicio))
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()

    limpiar_consola()
    aviso("Nota guardada correctamente.", 20)

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db',
                             detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("""
            SELECT 
                N.FOLIO, 
                strftime('%d/%m/%Y', N.FECHA) AS 'FECHA',
                C.NOMBRE AS 'Cliente', 
                C.RFC, 
                C.CORREO_ELECTRONICO AS 'Correo Electrónico', 
                N.MONTO_A_PAGAR
                FROM NOTAS N
                INNER JOIN CLIENTES C ON N.CLAVE_CLIENTE = C.CLAVE_CLIENTE
                WHERE N.FOLIO = ?;
            """, (folio,))
            nota_generada = mi_cursor.fetchall()

            if nota_generada:
                print("Datos de la nota guardada:")
                print(tabulate(nota_generada, headers=["Folio", "Fecha", "Cliente", "RFC", "Correo Electrónico", "Monto a Pagar"], tablefmt='pretty'))
            else:
                print("No se encontró la nota guardada.")
    except sqlite3.Error as e:
        print(e)

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("""
                SELECT 
                    S.NOMBRE_SERVICIO AS 'Servicio', 
                    S.COSTO_SERVICIO AS 'Precio'
                FROM DETALLE_NOTA DN
                INNER JOIN SERVICIOS S ON DN.CLAVE_SERVICIO = S.CLAVE_SERVICIO
                WHERE DN.FOLIO = ?;
            """, (folio,))
            detalle_nota = mi_cursor.fetchall()

            if detalle_nota:
                print("\nDetalle de la nota generada:")
                print(tabulate(detalle_nota, headers = ["Servicio", "Precio"], tablefmt = 'pretty'))
            else:
                print("No se encontraron los detalles de la nota guardada.")
    except sqlite3.Error as e:
        print(e)

    indicarEnter()
    limpiar_consola()

def cancelarNota():
    
    if validarContinuarOpcion():
        return

    print('Ingrese el folio de la nota a cancelar: ')
    folio = solicitarSoloNumeroEntero('Folio')

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT FOLIO FROM NOTAS WHERE (FOLIO = ?) AND (ESTADO_NOTA = 1)", (folio,))
            existencia = mi_cursor.fetchall()

            if not existencia:
                aviso("La nota con el folio proporcionado no existe o ya fue eliminada.", 15)
                indicarEnter()
                return
            
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()
    guiones_separadores()
    
    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db',
                             detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("""
                SELECT 
                    N.FOLIO, 
                    strftime('%d/%m/%Y', N.FECHA) AS 'FECHA',
                    C.NOMBRE AS 'Cliente', 
                    C.RFC, 
                    C.CORREO_ELECTRONICO AS 'Correo Electrónico', 
                    N.MONTO_A_PAGAR
                FROM NOTAS N
                INNER JOIN CLIENTES C ON N.CLAVE_CLIENTE = C.CLAVE_CLIENTE
                WHERE N.FOLIO = ?;
            """, (folio,))
            nota_generada = mi_cursor.fetchall()

            if nota_generada:
                print("Datos de la nota:")
                print(tabulate(nota_generada, headers = ["Folio", "Fecha", "Cliente", "RFC", "Correo Electrónico", "Monto a Pagar"], tablefmt = 'pretty'))
            else:
                print("No se encontró la nota guardada.")
                indicarEnter()
                return
    except sqlite3.Error as e:
        print(e)

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("""
                SELECT 
                    S.NOMBRE_SERVICIO AS 'Servicio', 
                    S.COSTO_SERVICIO AS 'Precio'
                FROM DETALLE_NOTA DN
                INNER JOIN SERVICIOS S ON DN.CLAVE_SERVICIO = S.CLAVE_SERVICIO
                WHERE DN.FOLIO = ?;
            """, (folio,))
            detalle_nota = mi_cursor.fetchall()

            if detalle_nota:
                print("\nDetalle de la nota generada:")
                print(tabulate(detalle_nota, headers = ["Servicio", "Precio"], tablefmt = 'pretty'))
            else:
                print("No se encontraron los detalles de la nota guardada.")
                indicarEnter()
                
                return
    except sqlite3.Error as e:
        print(e)
        indicarEnter()
        return
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
        indicarEnter()
        return

    guiones_separadores()
    print('¿Desea eliminar la nota? Confirme su respuesta (Sí/No).')
    confirmarEliminar = respuestaSINO()

    if confirmarEliminar == 'SI':
        try:
            with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("UPDATE NOTAS SET ESTADO_NOTA = 0 WHERE FOLIO = ?", (folio,))
                aviso("La nota ha sido eliminada.", 20)
        except sqlite3.Error as e:
            print(e)
            indicarEnter()
            return 
        except Exception:
            print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
            indicarEnter()
            return
        finally:
            conn.close()
    else:
        aviso("La nota no fue eliminada.", 20)

    indicarEnter()
    limpiar_consola()

def recuperarNota():
    if validarContinuarOpcion():
        return

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db',
                            detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT FOLIO FROM NOTAS WHERE ESTADO_NOTA = 0")
            notas_canceladas = mi_cursor.fetchall()

            if not notas_canceladas:
                aviso("No existen notas canceladas para recuperar.", 15)
                indicarEnter()
                return
            
            print("Lista de notas canceladas:")
            mi_cursor.execute("""
                SELECT 
                    N.FOLIO, 
                    strftime('%d/%m/%Y', N.FECHA) AS 'FECHA',
                    C.NOMBRE AS 'Cliente', 
                    C.RFC, 
                    C.CORREO_ELECTRONICO AS 'Correo Electrónico', 
                    N.MONTO_A_PAGAR
                FROM NOTAS N
                INNER JOIN CLIENTES C ON N.CLAVE_CLIENTE = C.CLAVE_CLIENTE
                WHERE N.ESTADO_NOTA = 0;
            """)
            notasCanceladas = mi_cursor.fetchall()
            print(tabulate(notasCanceladas, headers = ["Folio", "Fecha", "Cliente", "RFC", "Correo Electrónico", "Monto a Pagar"], tablefmt = 'pretty'))                
    except Error as e:
        print(e)
        indicarEnter()
        return
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
        indicarEnter()
        return
    finally:
        conn.close()
    guiones_separadores()

    print("Ingrese el folio de la nota o ingrese 0 para regresar al menu.")
    while True:
        folio = solicitarSoloNumeroEntero('Folio')
        if folio == 0:
            return

        try:
            with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT FOLIO FROM NOTAS WHERE (FOLIO = ?) AND (ESTADO_NOTA = 0)", (folio,))
                existencia = mi_cursor.fetchall()

                if not existencia:
                    print("\nIngrese un folio válido.")
                    continue

                mi_cursor.execute("""
                    SELECT 
                        S.NOMBRE_SERVICIO AS 'Servicio', 
                        S.COSTO_SERVICIO AS 'Precio'
                    FROM DETALLE_NOTA DN
                    INNER JOIN SERVICIOS S ON DN.CLAVE_SERVICIO = S.CLAVE_SERVICIO
                    WHERE DN.FOLIO = ?;
                """, (folio,))
                detalle_nota = mi_cursor.fetchall()
                guiones_separadores()
                print("Detalles de la nota:")
                print(tabulate(detalle_nota, headers = ["Servicio", "Precio"], tablefmt = 'pretty'))
                break
        except Error as e:
            print(e)
            indicarEnter()
            return
        except Exception:
            print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
            indicarEnter()
            return
        finally:
            conn.close()
    guiones_separadores()

    print("¿Desea recuperar la nota? Confirme su respuesta (Sí/No).")
    confirmar = respuestaSINO()

    if confirmar == 'SI':
        try:
            with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("UPDATE NOTAS SET ESTADO_NOTA = 1 WHERE FOLIO = ?", (folio,))
                aviso("La nota ha sido recuperada exitosamente.", 20)
                indicarEnter()
        except sqlite3.Error as e:
            print(e)
            indicarEnter()
            return 
        except Exception:
            print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
            indicarEnter()
            return
        finally:
            conn.close()
    else:
        aviso("La nota no fue recuperada.", 20)
        indicarEnter()
        return

def notas_consultaPorPeriodo():
    if validarContinuarOpcion():
        return

    print("Ingrese la fecha inicial en el formato (dd/mm/aaaa).")
    while True:
        fecha_texto1 = input("Fecha inicial: ").strip()

        if fecha_texto1 == "":
            fecha_texto1 = "01/01/2000"
            aviso("La fecha inicial se asumió como 01/01/2000.", 0)

        try:
            fecha_inicial = dt.datetime.strptime(fecha_texto1, "%d/%m/%Y").date()
            break
        except ValueError:
            print("\nIngrese una fecha inicial válida en formato dd/mm/aaaa.")
            continue

    print("\nIngresa la fecha final en el formato (dd/mm/aaaa).")
    while True:
        fecha_texto2 = input("Fecha final: ").strip()

        if fecha_texto2 == "":
            fecha_fin = fechaActual()
            aviso(f"La fecha final se asumió como la actual: {fecha_fin.strftime('%d/%m/%Y')}.", 0)
            break

        try:
            fecha_fin = dt.datetime.strptime(fecha_texto2, "%d/%m/%Y").date()
            if fecha_inicial <= fecha_fin:
                break
            else:
                print("\nLa fecha inicial no puede ser mayor que la fecha final. Ingrese fechas válidas.")
        except ValueError:
            print("\nIngrese una fecha final válida en formato dd/mm/aaaa.")
            continue

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("""
                SELECT N.FOLIO, strftime('%d/%m/%Y', N.FECHA) AS 'FECHA', C.NOMBRE, N.MONTO_A_PAGAR
                FROM NOTAS N
                JOIN CLIENTES C ON N.CLAVE_CLIENTE = C.CLAVE_CLIENTE
                WHERE (N.FECHA BETWEEN ? AND ?) AND N.ESTADO_NOTA = 1 
                ORDER BY N.FECHA
            """, (fecha_inicial, fecha_fin))
            registros = mi_cursor.fetchall()

            if registros:
                guiones_separadores()
                aviso("Registros encontrados:", 0)
                print(tabulate(registros, headers = ['Folio', 'Fecha', 'Cliente', 'Monto a Pagar'], tablefmt = 'pretty'))
            else:
                aviso('No se encontraron registros de notas en el rango de fechas proporcionado.', 20)
                indicarEnter()
                return
            mi_cursor.execute("""
                SELECT AVG(N.MONTO_A_PAGAR) AS "MONTO PROMEDIO"
                FROM NOTAS N
                WHERE (N.FECHA BETWEEN ? AND ?) AND ESTADO_NOTA = 1 """,(fecha_inicial,fecha_fin))
            monto_promedio = mi_cursor.fetchone()[0]
            print(guiones(80))
            print(f'El monto promedio de las notas en ese periodo es: {monto_promedio:.2f}')
            print(guiones(80))
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()

    print('¿Desea exportar los registros encontrados? (Sí/No).')
    respuesta = respuestaSINO()

    if respuesta == 'SI':
        guiones_separadores()
        print("Ingrese el número de la opción que desee realizar.")
        print("1. Exportar a Excel.\n2. Exportar a CSV.\n3. Regresar al menú de reportes.")
        respuesta = validarOpcionesNumericas(1, 3)

        if respuesta in (1, 2):
            guiones_separadores()
            nombre_archivo = f'ReportePorPeriodo_{fecha_inicial.strftime("%d%m%Y")}_{fecha_fin.strftime("%d%m%Y")}'
            df = pd.DataFrame(registros, columns = ['Clave', 'Nombre', 'RFC', 'Correo electronico'])

            if respuesta == 1:
                nombre_archivo += '.xlsx'
                df.to_excel(nombre_archivo, index = False)

            else:
                nombre_archivo += '.csv'
                df.to_csv(nombre_archivo, index = False)
            
            aviso(f'Información exportada en {nombre_archivo} exitosamente', 15)
            indicarEnter()
    else:
        aviso('Información no exportada', 20)
        indicarEnter()

def notas_consultaPorFolio():
    if validarContinuarOpcion():
        return
    
    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db',
                             detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("""
                SELECT FOLIO, strftime('%d/%m/%Y', FECHA) AS 'FECHA', C.NOMBRE
                FROM NOTAS N
                JOIN CLIENTES C ON N.CLAVE_CLIENTE = C.CLAVE_CLIENTE
                WHERE ESTADO_NOTA = 1
                ORDER BY FOLIO;
            """)
            notas_ordenadas = mi_cursor.fetchall()

            if notas_ordenadas:
                print('Ingrese el folio de la nota a buscar:')
                print(tabulate(notas_ordenadas, headers=["Folio", "Fecha", "Nombre del Cliente"], tablefmt='pretty'))
            else:
                aviso("No hay notas disponibles en el sistema.", 15)
                indicarEnter()
                return

            folio = solicitarSoloNumeroEntero('Folio')

            mi_cursor.execute("SELECT FOLIO FROM NOTAS WHERE (FOLIO = ?) AND (ESTADO_NOTA = 1)", (folio,))
            existencia = mi_cursor.fetchall()

            if not existencia:
                aviso("La nota con el folio proporcionado no se encuentra en el sistema.", 15)
                indicarEnter()
                return
            
            mi_cursor.execute("""
                SELECT FOLIO, strftime('%d/%m/%Y', FECHA) AS 'FECHA', C.NOMBRE, MONTO_A_PAGAR
                FROM NOTAS N
                JOIN CLIENTES C ON N.CLAVE_CLIENTE = C.CLAVE_CLIENTE
                WHERE (FOLIO = ?) AND (ESTADO_NOTA = 1);
            """, (folio,))
            nota_consulta = mi_cursor.fetchone()
            print('\nInformación de la nota seleccionada:')
            print(tabulate([nota_consulta], headers=["Folio", "Fecha", "Nombre del Cliente", "Monto a Pagar"], tablefmt='pretty'))
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()
        guiones_separadores()

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db',
                             detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("""
                SELECT 
                    N.FOLIO, 
                    strftime('%d/%m/%Y', N.FECHA) AS 'FECHA',
                    C.NOMBRE AS 'Cliente', 
                    C.RFC, 
                    C.CORREO_ELECTRONICO AS 'Correo Electrónico', 
                    N.MONTO_A_PAGAR
                FROM NOTAS N
                INNER JOIN CLIENTES C ON N.CLAVE_CLIENTE = C.CLAVE_CLIENTE
                WHERE N.FOLIO = ?;
            """, (folio,))
            nota_generada = mi_cursor.fetchall()

            if nota_generada:
                print("Datos de la nota:")
                print(tabulate(nota_generada, headers = ["Folio", "Fecha", "Cliente", "RFC", "Correo Electrónico", "Monto a Pagar"], tablefmt = 'pretty'))
            else:
                print("No se encontró la nota guardada.")
                indicarEnter()
                return
    except sqlite3.Error as e:
        print(e)

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("""
                SELECT 
                    S.NOMBRE_SERVICIO AS 'Servicio', 
                    S.COSTO_SERVICIO AS 'Precio'
                FROM DETALLE_NOTA DN
                INNER JOIN SERVICIOS S ON DN.CLAVE_SERVICIO = S.CLAVE_SERVICIO
                WHERE DN.FOLIO = ?;
            """, (folio,))
            detalle_nota = mi_cursor.fetchall()

            if detalle_nota:
                print("\nDetalle de la nota:")
                print(tabulate(detalle_nota, headers = ["Servicio", "Precio"], tablefmt = 'pretty'))
                indicarEnter()
            else:
                print("No se encontraron los detalles de la nota guardada.")
                indicarEnter()    
                return
    except sqlite3.Error as e:
        print(e)
        indicarEnter()
        return
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
        indicarEnter()
        return

def menuClientes(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:    
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarYValidarMenu(ubicacion, opcion, lmenu_clientes)

        if opcion == 1:
            mostrarTitulo(ubicacion)
            registrarCliente()

        elif opcion == 2:
            mostrarTitulo(ubicacion)
            suspenderCliente()

        elif opcion == 3:
            mostrarTitulo(ubicacion)
            recuperarCliente()

        elif opcion == 4:
            clientes_consultasYReportes(ubicacion)

        else:
            break

        opcion = 0
        limpiar_consola()
        continue

def registrarCliente():
    if validarContinuarOpcion():
        return

    print('Ingrese el nombre(s) del cliente.')
    while True:
        nombre = darFormatoATexto(input('Nombre: '))
        if len(nombre) < 3 or len(nombre) > 50:
            print("\nEl nombre no puede omitirse. Ingrese de nuevo.")
            continue
        if not validarUnicamenteTexto(nombre):
            print("\nEl nombre solo debe contener letras y espacios.")
            continue
        break
    guiones_separadores()

    print('Ingrese los apellido(s) del cliente.')
    while True:
        apellido = darFormatoATexto(input('Apellido(s): '))
        if len(apellido) < 3 or len(apellido) > 50:
            print("\nLos apellidos no puede omitirse. Ingrese de nuevo.")
            continue
        if not validarUnicamenteTexto(apellido):
            print("\nEl nombre solo debe contener letras y espacios.")
            continue
        break

    nombre_cliente = nombre + ' ' +  apellido
    guiones_separadores()

    print('Ingrese el número del tipo de RFC:\n1. Físico.\n2. Moral.')
    tipo = validarOpcionesNumericas(1, 2)
    guiones_separadores()

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

    print('Ingrese el correo electrónico.')
    while True:
        mail = darFormatoATexto(input('Correo electronico: '))
        if not re.match(r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$', mail):
            print('\nEl correo no es valido, ingrese un correo válido.')
            continue
        break
    guiones_separadores()

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            estadoCliente = 1
            datos_clientes = (nombre_cliente, rfc, mail, estadoCliente)
            mi_cursor.execute("INSERT INTO CLIENTES(NOMBRE, RFC, CORREO_ELECTRONICO, ESTADO_CLIENTE)\
            VALUES (?, ?, ?, ?)", datos_clientes)

            aviso('Cliente registado correctamente', 15)
            indicarEnter()
    except Error as e:
        print(e)
        indicarEnter()
        return
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
        indicarEnter()
        return
    finally:
        conn.close() 

def suspenderCliente():
    if validarContinuarOpcion():
        return
    
    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT CLAVE_CLIENTE, NOMBRE FROM CLIENTES WHERE ESTADO_CLIENTE = 1")
            clientes_activos = mi_cursor.fetchall()

            if not clientes_activos:
                aviso("No hay clientes activos para suspender.", 15)
                indicarEnter()
                return
            
            print("Lista de clientes activos:")
            print(tabulate(clientes_activos, headers = ["Clave", "Nombre"], tablefmt = 'pretty'))

            print('\nIngrese la clave del cliente a suspender o 0 para volver al menú anterior.')

            while True:
                clave_cliente_suspender = solicitarSoloNumeroEntero('Clave')
                if clave_cliente_suspender == 0:
                    return
        
                mi_cursor.execute("""SELECT CLAVE_CLIENTE, NOMBRE, RFC, CORREO_ELECTRONICO \
                                FROM CLIENTES WHERE CLAVE_CLIENTE = ? AND ESTADO_CLIENTE = 1;
                                """, (clave_cliente_suspender,))

                cliente_a_suspender = mi_cursor.fetchall()

                if not cliente_a_suspender:
                    print("\nIngrese una clave válida de los clientes presentados o 0 para regresar al menú anterior.")
                    continue
                guiones_separadores()

                print("Datos del cliente:")
                print(tabulate(cliente_a_suspender, headers = ["Clave del cliente", "Nombre cliente", "RFC", "Correo Electrónico"], tablefmt = 'pretty'))
                break
            guiones_separadores()

            print('¿Desea suspender al cliente? Confirme su respuesta (Sí/No).')
            confirmarSuspender = respuestaSINO()

            if confirmarSuspender == 'SI':
                mi_cursor.execute("UPDATE CLIENTES SET ESTADO_CLIENTE = 0 WHERE CLAVE_CLIENTE = ?", (clave_cliente_suspender,))
                aviso("El cliente ha sido suspendido correctamente.", 20)
            else:
                aviso("El cliente no fue suspendido.", 20)

    except sqlite3.Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()
    indicarEnter()

def recuperarCliente():
    if validarContinuarOpcion():
        return

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT CLAVE_CLIENTE, NOMBRE FROM CLIENTES WHERE ESTADO_CLIENTE = 0")
            clientes_suspendidos = mi_cursor.fetchall()

            if not clientes_suspendidos:
                aviso("No hay clientes suspendidos que recuperar.", 20)
                indicarEnter()
                return
            else:
                print("Lista de clientes suspendidos:")
                print(tabulate(clientes_suspendidos, headers = ["Clave", "Nombre"], tablefmt = 'pretty'))

                print('\nIngrese la clave del cliente a recuperar o 0 para volver al menú anterior.')

            while True:
                clave_cliente_recuperar = solicitarSoloNumeroEntero('Clave')
                if clave_cliente_recuperar == 0:
                    return

                mi_cursor.execute("""SELECT CLAVE_CLIENTE, NOMBRE, RFC, CORREO_ELECTRONICO \
                                FROM CLIENTES WHERE CLAVE_CLIENTE = ? AND ESTADO_CLIENTE = 0;
                                """, (clave_cliente_recuperar,))
                cliente_a_recuperar = mi_cursor.fetchall()

                if not cliente_a_recuperar:
                    print("\nIngrese una clave válida de los clientes presentados o 0 para regresar al menú anterior.")
                    continue
                guiones_separadores()

                print("Datos del cliente:")
                print(tabulate(cliente_a_recuperar, headers = ["Clave del cliente", "Nombre cliente", "RFC", "Correo Electrónico"], tablefmt = 'pretty'))
                break
            guiones_separadores()

            print('¿Desea recuperar al cliente? Confirme su respuesta (Sí/No).')
            confirmarRecuperar = respuestaSINO()

            if confirmarRecuperar == 'SI':
                mi_cursor.execute("UPDATE CLIENTES SET ESTADO_CLIENTE = 1 WHERE CLAVE_CLIENTE = ?", (clave_cliente_recuperar,))
                aviso("El cliente ha sido recuperado correctamente.", 20)
            else:
                aviso("El cliente no fue recuperado.", 20)
    except sqlite3.Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()
    indicarEnter()

def clientes_consultasYReportes(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarYValidarMenu(ubicacion, opcion, lmenu_clientes_consultasYReportes)

        if opcion == 1:
            clientes_consultasYReportes_listadoDeClientesRegistrados(ubicacion)

        elif opcion == 2:
            mostrarTitulo(ubicacion)
            clientes_busquedaClave()

        elif opcion == 3:
            mostrarTitulo(ubicacion)
            clientes_busquedaNombre()

        else:
            break

        opcion = 0
        limpiar_consola()
        continue

def clientes_consultasYReportes_listadoDeClientesRegistrados(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarYValidarMenu(ubicacion, opcion, lmenu_clientes_consultasYReportes_listadoDeClientesRegistrados)

        if opcion == 1:
            mostrarTitulo(ubicacion)
            clientes_ordenadoClave()

        elif opcion == 2:
            mostrarTitulo(ubicacion)
            clientes_ordenadoNombre()

        else:
            break

        opcion = 0
        limpiar_consola()
        continue

def clientes_ordenadoClave():
    if validarContinuarOpcion():
        return
    
    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT CLAVE_CLIENTE, NOMBRE, RFC, CORREO_ELECTRONICO FROM CLIENTES WHERE ESTADO_CLIENTE = 1 ORDER BY CLAVE_CLIENTE")
            registros = mi_cursor.fetchall()

            if registros:
                aviso("Registros encontrados:", 0)
                print(tabulate(registros, headers = ['Clave', 'Nombre', 'RFC', 'Correo electrónico'], tablefmt = 'pretty'))
            else:
                aviso('No se encontraron registros de clientes registrados.', 20)
                indicarEnter()
                return
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()

    print('¿Desea exportar los registros encontrados? (Sí/No).')
    respuesta = respuestaSINO()

    if respuesta == 'SI':
        guiones_separadores()
        print("Ingrese el número de la opción que desee realizar.")
        print("1. Exportar a Excel.\n2. Exportar a CSV.\n3. Regresar al menú de reportes.")
        respuesta = validarOpcionesNumericas(1, 3)

        if respuesta in (1, 2):
            guiones_separadores()
            fechaReporte = fechaActual().strftime("%d%m%Y")
            nombre_archivo = f'ReporteClientesActivosPorClave_{fechaReporte}'
            df = pd.DataFrame(registros, columns = ['Clave', 'Nombre', 'RFC', 'Correo electrónico'])

            if respuesta == 1:
                nombre_archivo += '.xlsx'
                df.to_excel(nombre_archivo, index = False)

            else:
                nombre_archivo += '.csv'
                df.to_csv(nombre_archivo, index = False)
            
            aviso(f'Información exportada en {nombre_archivo} exitosamente', 15)
            indicarEnter()
    else:
        aviso('Información no exportada', 20)
        indicarEnter()

def clientes_ordenadoNombre():
    if validarContinuarOpcion():
        return
    
    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT CLAVE_CLIENTE, NOMBRE, RFC, CORREO_ELECTRONICO FROM CLIENTES WHERE ESTADO_CLIENTE = 1 ORDER BY NOMBRE")
            registros = mi_cursor.fetchall()

            if registros:
                aviso("Registros encontrados:", 0)
                print(tabulate(registros, headers = ['Clave', 'Nombre', 'RFC', 'Correo electronico'], tablefmt = 'pretty'))
            else:
                aviso('No se encontraron registros de clientes registrados.', 20)
                indicarEnter()
                return
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()

    print('¿Desea exportar los registros encontrados? (Sí/No).')
    respuesta = respuestaSINO()

    if respuesta == 'SI':
        guiones_separadores()
        print("Ingrese el número de la opción que desee realizar.")
        print("1. Exportar a Excel.\n2. Exportar a CSV.\n3. Regresar al menú de reportes.")
        respuesta = validarOpcionesNumericas(1, 3)

        if respuesta in (1, 2):
            guiones_separadores()
            fechaReporte = fechaActual().strftime("%d%m%Y")
            nombre_archivo = f'ReporteClientesActivosPorNombre_{fechaReporte}'
            df = pd.DataFrame(registros, columns=['Clave', 'Nombre', 'RFC', 'Correo electronico'])

            if respuesta == 1:
                nombre_archivo += '.xlsx'
                df.to_excel(nombre_archivo, index = False)
        
            else:
                nombre_archivo += '.csv'
                df.to_csv(nombre_archivo, index = False)
            
            aviso(f'Información exportada en {nombre_archivo} exitosamente', 15)
            indicarEnter()
    else:
        aviso('Información no exportada', 20)
        indicarEnter()

def clientes_busquedaClave():
    if validarContinuarOpcion():
        return

    print("Ingrese la clave a buscar.")
    clave_a_buscar = solicitarSoloNumeroEntero('Clave')

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            valores = {"CLAVE_CLIENTE":clave_a_buscar}
            mi_cursor.execute("SELECT CLAVE_CLIENTE, NOMBRE, RFC, CORREO_ELECTRONICO FROM CLIENTES WHERE (CLAVE_CLIENTE = :CLAVE_CLIENTE) AND ESTADO_CLIENTE = 1", valores)
            registros = mi_cursor.fetchall()

            if registros:
                guiones_separadores()
                aviso("Registro encontrado:", 0)
                print(tabulate(registros, headers = ['Clave', 'Nombre', 'RFC', 'Correo electrónico'], tablefmt = 'pretty'))
            else:
                aviso('No se encontró el cliente con la clave ingresada.', 20)
            indicarEnter()
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()  

def clientes_busquedaNombre():
    if validarContinuarOpcion():
        return

    print("Ingrese el nombre completo a buscar.")
    nombre_a_buscar = darFormatoATexto(input('Nombre completo: '))
    guiones_separadores()

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            valores = {"NOMBRE":nombre_a_buscar}
            mi_cursor.execute("SELECT CLAVE_CLIENTE, NOMBRE, RFC, CORREO_ELECTRONICO FROM CLIENTES WHERE (NOMBRE = :NOMBRE) AND ESTADO_CLIENTE = 1", valores)
            registros = mi_cursor.fetchall()

            if registros:
                aviso("Registro encontrado:", 0)
                print(tabulate(registros, headers = ['Clave', 'Nombre', 'RFC', 'Correo electrónico'], tablefmt = 'pretty'))
            else:
                aviso('No se encontró el cliente con la clave ingresada.', 20)
            indicarEnter()
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()

def menuServicios(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:    
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarYValidarMenu(ubicacion, opcion, lmenu_servicios)

        if opcion == 1:
            mostrarTitulo(ubicacion)
            agregarServicio()
            
        elif opcion == 2:
            mostrarTitulo(ubicacion)
            suspenderServicio()
            
        elif opcion == 3:
            mostrarTitulo(ubicacion)
            recuperarServicio()

        elif opcion ==4:
            servicios_consultasYReportes(ubicacion)
            
        else:
            break

        opcion = 0
        limpiar_consola()
        continue

def servicios_consultasYReportes(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:    
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarYValidarMenu(ubicacion, opcion, lmenu_servicios_consultasYReportes)

        if opcion == 1:
            mostrarTitulo(ubicacion)
            servicios_busquedaClave()

        elif opcion == 2:
            mostrarTitulo(ubicacion)
            servicio_busquedaNombre()

        elif opcion == 3:
            servicios_consultasYReportes_listadoDeServicios(ubicacion)

        else:
            break

        opcion = 0
        limpiar_consola()
        continue

def servicios_consultasYReportes_listadoDeServicios(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:    
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarYValidarMenu(ubicacion, opcion, lmenu_servicios_consultasYReportes_listadoDeServicios)

        if opcion == 1:
            mostrarTitulo(ubicacion)

            regresarMenuReportes = servicio_ordenadoClave(respuesta = False)
            if regresarMenuReportes:
                return

        elif opcion == 2:
            mostrarTitulo(ubicacion)

            regresarMenuReportes = servicio_ordenadoNombre(respuesta = False)
            if regresarMenuReportes:
                return
        else:
            break

        opcion = 0
        limpiar_consola()

def agregarServicio():
    if validarContinuarOpcion():
        return

    print('Ingrese el nombre del servicio. ')
    while True:
        servicio = darFormatoATexto(input('Servicio: '))
        if servicio == '' or len(servicio) < 3:
            print('\nIngrese una descripción válida.')
            continue
        break
    guiones_separadores()

    print(f"Ingrese el precio del servicio. (Máximo dos decimales).")
    while True:
        precio_servicio_recibido = input("Precio: ").strip()
        if re.match(r'^\d+(\.\d{1,2})?$', precio_servicio_recibido):
            precio = float(precio_servicio_recibido)
            break
        else:
            print("\nIngrese un precio válido (Máximo dos decimales).")
            continue

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            estadoServicio = 1
            datos_servicios = (servicio, precio, estadoServicio)
            mi_cursor.execute("INSERT INTO SERVICIOS(NOMBRE_SERVICIO, COSTO_SERVICIO, ESTADO_SERVICIO)\
            VALUES (?, ?, ?)", datos_servicios)

            aviso('Servicio registado correctamente', 20)
            indicarEnter()
    except Error as e:
        input(e)
    except Exception:
        input(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()

def suspenderServicio():
    if validarContinuarOpcion():
        return
    
    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT CLAVE_SERVICIO, NOMBRE_SERVICIO FROM SERVICIOS WHERE ESTADO_SERVICIO = 1")
            servicios_activos = mi_cursor.fetchall()

            if not servicios_activos:
                aviso("No hay servicios activos para suspender.", 15)
                indicarEnter()
                return
            
            print("Lista de servicios activos:")
            print(tabulate(servicios_activos, headers = ["Clave", "Servicio"], tablefmt = 'pretty'))

            print('\nIngrese la clave del servicio a suspender o 0 para volver al menú anterior.')

            while True:
                clave_servicio_suspender = solicitarSoloNumeroEntero('Clave')
                if clave_servicio_suspender == 0:
                    return
        
                mi_cursor.execute("""SELECT CLAVE_SERVICIO, NOMBRE_SERVICIO, COSTO_SERVICIO \
                                FROM SERVICIOS WHERE CLAVE_SERVICIO = ? AND ESTADO_SERVICIO = 1;
                                """, (clave_servicio_suspender,))

                servicio_a_suspender = mi_cursor.fetchall()

                if not servicio_a_suspender:
                    print("\nIngrese una clave válida de los servicios presentados o 0 para regresar al menú anterior.")
                    continue
                guiones_separadores()

                print("Datos del servicio:")
                print(tabulate(servicio_a_suspender, headers = ["Clave del servicio", "Nombre servicio", "Costo servicio"], tablefmt = 'pretty'))
                break
            guiones_separadores()

            print('¿Desea suspender el servicio? Confirme su respuesta (Sí/No).')
            confirmarSuspender = respuestaSINO()

            if confirmarSuspender == 'SI':
                mi_cursor.execute("UPDATE SERVICIOS SET ESTADO_SERVICIO = 0 WHERE CLAVE_SERVICIO = ?", (clave_servicio_suspender,))
                aviso("El servicio ha sido suspendido correctamente.", 20)
            else:
                aviso("El servicio no fue suspendido.", 20)

    except sqlite3.Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()
    indicarEnter()

def recuperarServicio():
    if validarContinuarOpcion():
        return
    
    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT CLAVE_SERVICIO, NOMBRE_SERVICIO FROM SERVICIOS WHERE ESTADO_SERVICIO = 0")
            servicios_suspendidos = mi_cursor.fetchall()

            if not servicios_suspendidos:
                aviso("No hay servicios activos para recuperar.", 15)
                indicarEnter()
                return
            
            print("Lista de servicios suspendidos:")
            print(tabulate(servicios_suspendidos, headers = ["Clave", "Servicio"], tablefmt = 'pretty'))

            print('\nIngrese la clave del servicio a suspender o 0 para volver al menú anterior.')

            while True:
                clave_servicio_recuperar = solicitarSoloNumeroEntero('Clave')
                if clave_servicio_recuperar == 0:
                    return
        
                mi_cursor.execute("""SELECT CLAVE_SERVICIO, NOMBRE_SERVICIO, COSTO_SERVICIO \
                                FROM SERVICIOS WHERE CLAVE_SERVICIO = ? AND ESTADO_SERVICIO = 0;
                                """, (clave_servicio_recuperar,))

                servicio_a_recuperar = mi_cursor.fetchall()

                if not servicio_a_recuperar:
                    print("\nIngrese una clave válida de los servicios presentados o 0 para regresar al menú anterior.")
                    continue
                guiones_separadores()

                print("Datos del servicio:")
                print(tabulate(servicio_a_recuperar, headers = ["Clave del servicio", "Nombre servicio", "Costo servicio"], tablefmt = 'pretty'))
                break
            guiones_separadores()

            print('¿Desea recuperar el servicio? Confirme su respuesta (Sí/No).')
            confirmarRecuperar = respuestaSINO()

            if confirmarRecuperar == 'SI':
                mi_cursor.execute("UPDATE SERVICIOS SET ESTADO_SERVICIO = 1 WHERE CLAVE_SERVICIO = ?", (clave_servicio_recuperar,))
                aviso("El servicio ha sido recuperado correctamente.", 20)
            else:
                aviso("El servicio no fue recuperado.", 20)

    except sqlite3.Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()
    indicarEnter()

def servicios_busquedaClave():
    if validarContinuarOpcion():
        return
    
    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT CLAVE_SERVICIO, NOMBRE_SERVICIO FROM SERVICIOS WHERE ESTADO_SERVICIO = 1")
            servicio = mi_cursor.fetchall()

            if not servicio:
                aviso("No hay notas disponibles en el sistema.", 15)
                indicarEnter()
                return
            
            print("Ingrese la clave a buscar.")
            print(tabulate(servicio, headers = ["Clave", "Servicio"], tablefmt = 'pretty'))
            clave_a_buscar = solicitarSoloNumeroEntero('Clave')

            valores = {"CLAVE_SERVICIO":clave_a_buscar}
            mi_cursor.execute("SELECT CLAVE_SERVICIO, NOMBRE_SERVICIO, COSTO_SERVICIO FROM SERVICIOS WHERE (CLAVE_SERVICIO = :CLAVE_SERVICIO) AND ESTADO_SERVICIO = 1", valores)
            registros = mi_cursor.fetchall()

            if registros:
                guiones_separadores()
                aviso("Servicio encontrado:", 0)
                print(tabulate(registros, headers = ['Clave servicio', 'Nombre servicio', 'Precio'], tablefmt = 'pretty'))
            else:
                aviso('No se encontró el servicio con la clave ingresada.', 20)
            indicarEnter()
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()    

def servicio_busquedaNombre():
    if validarContinuarOpcion():
        return

    print("Ingrese el nombre del servicio a buscar.")
    nombre_a_buscar = darFormatoATexto(input('Servicio: '))
    guiones_separadores()

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            valores = {"NOMBRE_SERVICIO":nombre_a_buscar}
            mi_cursor.execute("SELECT CLAVE_SERVICIO, NOMBRE_SERVICIO, COSTO_SERVICIO FROM SERVICIOS WHERE (NOMBRE_SERVICIO = :NOMBRE_SERVICIO) AND ESTADO_SERVICIO = 1", valores)
            registros = mi_cursor.fetchall()

            if registros:
                aviso("Servicio encontrado:", 0)
                print(tabulate(registros, headers = ['Clave servicio', 'Nombre servicio', 'Precio'], tablefmt = 'pretty'))
            else:
                aviso('No se encontró el servicio con el nombre ingresado.', 20)
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()   
        indicarEnter()            

def servicio_ordenadoClave(respuesta):
    if validarContinuarOpcion():
        return
    
    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT CLAVE_SERVICIO,  NOMBRE_SERVICIO, COSTO_SERVICIO FROM SERVICIOS WHERE ESTADO_SERVICIO = 1 ORDER BY CLAVE_SERVICIO")
            registros = mi_cursor.fetchall()

            if registros:
                aviso("Registros encontrados:", 0)
                print(tabulate(registros, headers = ['Clave servicio', 'Nombre servicio', 'Precio'], tablefmt = 'pretty'))
            else:
                aviso('No se encontraron registros de clientes registrados.', 20)
                indicarEnter()
                return
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()

    try:
        print('¿Desea exportar los registros encontrados? (Sí/No).')
        respuesta = respuestaSINO()

        if respuesta == 'SI':
            guiones_separadores()
            print("Ingrese el número de la opción que desee realizar.")
            print("1. Exportar a Excel.\n2. Exportar a CSV.\n3. Regresar al menú de reportes.")
            respuesta = validarOpcionesNumericas(1, 3)

            if respuesta in (1, 2):
                guiones_separadores()
                fechaReporte = fechaActual().strftime("%d%m%Y")
                nombre_archivo = f'ReporteServicioPorClave_{fechaReporte}'

                df = pd.DataFrame(registros, columns=['Clave servicio', 'Nombre servicio', 'Precio'])

                if respuesta == 1:
                    nombre_archivo += '.xlsx'
                    df.to_excel(nombre_archivo, index = False)
                else:
                    nombre_archivo += '.csv'
                    df.to_csv(nombre_archivo, index = False)

                aviso(f'Información exportada en {nombre_archivo} exitosamente', 15)
                indicarEnter()
            else:
                return True
        else:
            aviso('Información no exportada', 20)
            indicarEnter()

        return False
    except Exception:
        input(f'Se produjo el siguiente error: {sys.exc_info()[0]}')

def servicio_ordenadoNombre(respuesta):
    if validarContinuarOpcion():
        return
    
    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT CLAVE_SERVICIO,  NOMBRE_SERVICIO, COSTO_SERVICIO FROM SERVICIOS WHERE ESTADO_SERVICIO = 1 ORDER BY NOMBRE_SERVICIO")
            registros = mi_cursor.fetchall()

            if registros:
                aviso("Registros encontrados:", 0)
                print(tabulate(registros, headers = ['Clave servicio', 'Nombre servicio', 'Precio'], tablefmt = 'pretty'))
            else:
                aviso('No se encontraron registros de clientes registrados.', 20)
                indicarEnter()
                return
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()
    
    try:
        print('¿Desea exportar los registros encontrados? (Sí/No).')
        respuesta = respuestaSINO()

        if respuesta == 'SI':
            guiones_separadores()
            print("Ingrese el número de la opción que desee realizar.")
            print("1. Exportar a Excel.\n2. Exportar a CSV.\n3. Regresar al menú de reportes.")
            respuesta = validarOpcionesNumericas(1, 3)

            if respuesta in (1, 2):
                guiones_separadores()
                fechaReporte = fechaActual().strftime("%d%m%Y")
                nombre_archivo = f'ReporteServicioPorNombre_{fechaReporte}'

                df = pd.DataFrame(registros, columns=['Clave servicio', 'Nombre servicio', 'Precio'])

                if respuesta == 1:
                    nombre_archivo += '.xlsx'
                    df.to_excel(nombre_archivo, index = False)
            
                else:
                    nombre_archivo += '.csv'
                    df.to_csv(nombre_archivo, index = False)
                
                aviso(f'Información exportada en {nombre_archivo} exitosamente', 15)
                indicarEnter()
            else:
                return True
        else:
            aviso('Información no exportada', 20)
            indicarEnter()
        return False
    except Exception:
        input(f'Se produjo el siguiente error: {sys.exc_info()[0]}')

def menuEstadisticas(ubicacion):
    ubicacionOriginal = ubicacion.copy()
    opcion = 0

    while True:    
        ubicacion = ubicacionOriginal.copy()
        if opcion == 0:
            opcion, ubicacion = mostrarYValidarMenu(ubicacion, opcion, lmenu_estadisticas)

        if opcion == 1:
            mostrarTitulo(ubicacion)
            serviciosMasPrestados()

        elif opcion == 2:
            mostrarTitulo(ubicacion)
            clientesMasNotas()

        elif opcion == 3:
            mostrarTitulo(ubicacion)
            promedioMontoDeNotas()

        else:
            break

        opcion = 0
        limpiar_consola()
        continue

def serviciosMasPrestados():
    if validarContinuarOpcion():
        return
    
    print("Ingrese la cantidad de servicios que desea conocer.")    
    while True:
        cantidad_servicios = solicitarSoloNumeroEntero("Cantidad")
        if cantidad_servicios < 1:
            print("\nIngrese una cantidad válida.")
        break
    guiones_separadores()

    print("Ingrese la fecha inicial en el formato (dd/mm/aaaa).")
    while True:
        fecha_str = input('Fecha inicial: ').strip()
        try:
            fecha_inicial2 = dt.datetime.strptime(fecha_str, "%d/%m/%Y").date()
            break
        except ValueError:
            print("\nIngrese una fecha inicial válida en formato (dd/mm/aaaa).")
            continue
    guiones_separadores()

    print("Ingrese la fecha final en el formato (dd/mm/aaaa).")
    while True:
        fecha_str2 = input("Fecha final: ").strip()
        try:
            fecha_final2 = dt.datetime.strptime(fecha_str2, "%d/%m/%Y").date()
            if fecha_inicial2 <= fecha_final2:
                break
            else:
                print("\nLa fecha inicial no puede ser mayor que la fecha final. Ingrese fechas válidas.")
        except ValueError:
                print("\nIngrese una fecha final válida en formato (dd/mm/aaaa).")
                continue
    guiones_separadores()

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("""
                        SELECT S.NOMBRE_SERVICIO, COUNT(D.CLAVE_SERVICIO) AS "CANTIDAD"
                        FROM DETALLE_NOTA D INNER JOIN SERVICIOS S ON D.CLAVE_SERVICIO = S.CLAVE_SERVICIO
                        INNER JOIN NOTAS N ON N.FOLIO = D.FOLIO
                        WHERE N.FECHA BETWEEN ? AND ? 
                        GROUP BY S.CLAVE_SERVICIO
                        ORDER BY CANTIDAD DESC
                        LIMIT ?""", (fecha_inicial2, fecha_final2, cantidad_servicios))
            resultados = mi_cursor.fetchall()

            if not resultados:
                aviso('No se encontraron servicios', 20)
                indicarEnter()
                return
            
            aviso("Servicios más presentados:", 0)
            print(tabulate(resultados, headers = ["Nombre del Servicio", "Cantidad"], tablefmt = 'pretty'))
            guiones_separadores()
    except sqlite3.Error as e:
        input(e)
    except Exception:
        input(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close() 

    print('¿Desea exportar el reporte a Excel o CSV? (Sí/No).')
    respuesta = respuestaSINO()
    guiones_separadores()

    if respuesta == 'NO':
        return
    
    print("Ingrese el número de la opción que desee realizar.")
    print("1. Exportar a Excel.\n2. Exportar a CSV.")
    respuesta = validarOpcionesNumericas(1, 2)
    guiones_separadores()

    df = pd.DataFrame(resultados, columns = ['Servicio', 'Cantidad prestada'])
    fecha_inicial_str = fecha_inicial2.strftime("%d%m%Y")
    fecha_final_str = fecha_final2.strftime("%d%m%Y")
    nombre_archivo = f'ReporteServiciosMasPrestados_{fecha_inicial_str}_{fecha_final_str}'

    if respuesta == 1:
        nombre_archivo += '.xlsx'
        df.to_excel(nombre_archivo, index = False)
    else:
        nombre_archivo += '.csv'
        df.to_csv(nombre_archivo, index = False)
            
    aviso(f'Información exportada en {nombre_archivo} exitosamente', 15)
    indicarEnter()

def clientesMasNotas():
    if validarContinuarOpcion():
        return

    print('Ingrese la cantidad de clientes con más notas a identificar. ')
    while True:
        cantidad = solicitarSoloNumeroEntero('Cantidad')
        if cantidad < 1:
            print('\nIngrese una cantidad válida.')
            continue
        break
    guiones_separadores()

    print("Ingrese la fecha inicial del periodo a reportar en el formato (dd/mm/aaaa).")
    while True:
        fecha_texto1 = input("Fecha inicial: ").strip()
        try:
            fecha_inicial = dt.datetime.strptime(fecha_texto1, "%d/%m/%Y").date()
            break 
        except ValueError:
            print("\nIngrese una fecha inicial válida en formato dd/mm/aaaa.")
            continue
    guiones_separadores

    print("\nIngresa la fecha final en el formato (dd/mm/aaaa).")
    while True:
        fecha_texto2 = input("Fecha final: ").strip()
        try:
            fecha_fin = dt.datetime.strptime(fecha_texto2, "%d/%m/%Y").date()
            
            if fecha_inicial <= fecha_fin:
                break
            else:
                print("\nLa fecha inicial no puede ser mayor que la fecha final. Ingrese fechas válidas.")
        except ValueError:
            print("\nIngrese una fecha final válida en formato dd/mm/aaaa.")
            continue
    guiones_separadores()

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db', detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()            
            mi_cursor.execute("""
                        SELECT C.NOMBRE, COUNT(N.FOLIO) AS "CANTIDAD"      
                        FROM CLIENTES C INNER JOIN NOTAS N
                        ON C.CLAVE_CLIENTE = N.CLAVE_CLIENTE
                        WHERE N.FECHA BETWEEN ? AND ? 
                        GROUP BY C.CLAVE_CLIENTE
                        ORDER BY CANTIDAD DESC
                        LIMIT ?""", (fecha_inicial, fecha_fin, cantidad))
            
            datos_obtenidos = mi_cursor.fetchall() 
            
            if not datos_obtenidos:
                aviso('No se encontraron registros de clientes en el rango de fechas proporcionado.', 20)
                indicarEnter()
                return
            
            aviso("Clientes con más notas:", 0)
            print(tabulate(datos_obtenidos, headers = ['Cliente', 'Número de notas'], tablefmt = "pretty"))
    except Error as e:
        input(e)
    except Exception:
        input(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()

    print('¿Desea exportar el reporte a Excel o CSV? (Sí/No).')
    respuesta = respuestaSINO()
    guiones_separadores()

    if respuesta == 'NO':
        return
    
    print("Ingrese el número de la opción que desee realizar.")
    print("1. Exportar a Excel.\n2. Exportar a CSV.")
    respuesta = validarOpcionesNumericas(1, 2)
    guiones_separadores()

    df = pd.DataFrame(datos_obtenidos, columns = ['Servicio', 'Cantidad prestada'])
    fecha_inicial_str = fecha_inicial.strftime("%d%m%Y")
    fecha_final_str = fecha_fin.strftime("%d%m%Y")
    nombre_archivo = f'ReporteClientesConMasNotas_{fecha_inicial_str}_{fecha_final_str}'

    if respuesta == 1:
        nombre_archivo += '.xlsx'
        df.to_excel(nombre_archivo, index = False)
    else:
        nombre_archivo += '.csv'
        df.to_csv(nombre_archivo, index = False)
            
    aviso(f'Información exportada en {nombre_archivo} exitosamente', 15)
    indicarEnter()


def promedioMontoDeNotas():
    if validarContinuarOpcion():
        return
    
    print("Ingrese la fecha inicial en el formato (dd/mm/aaaa).")
    while True:
        fecha_texto1 = input("Fecha inicial: ").strip()

        try:
            fecha_inicial = dt.datetime.strptime(fecha_texto1, "%d/%m/%Y").date()
            break
        except ValueError:
            print("\nIngrese una fecha inicial válida en formato dd/mm/aaaa.")
            continue
    guiones_separadores()

    print("\nIngresa la fecha final en el formato (dd/mm/aaaa).")
    while True:
        fecha_texto2 = input("Fecha final: ").strip()

        try:
            fecha_fin = dt.datetime.strptime(fecha_texto2, "%d/%m/%Y").date()
            if fecha_inicial <= fecha_fin:
                break
            else:
                print("\nLa fecha inicial no puede ser mayor que la fecha final. Ingrese fechas válidas.")
        except ValueError:
            print("\nIngrese una fecha final válida en formato dd/mm/aaaa.")
            continue
    guiones_separadores()

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("""
                SELECT MONTO_A_PAGAR
                FROM NOTAS 
                WHERE (FECHA BETWEEN ? AND ?) AND ESTADO_NOTA = 1 
                ORDER BY FECHA
            """, (fecha_inicial, fecha_fin))
            registros = mi_cursor.fetchall()

            if registros:
                aviso("Información encontrada:", 0)
                mi_cursor.execute("""
                    SELECT AVG(MONTO_A_PAGAR) AS "MONTO PROMEDIO"
                    FROM NOTAS 
                    WHERE (FECHA BETWEEN ? AND ?) AND ESTADO_NOTA = 1  """,(fecha_inicial, fecha_fin))
                monto_promedio = mi_cursor.fetchone()[0]
                aviso(f'El monto promedio de las notas en el periodo indicado es: {monto_promedio:.2f}', 0)

            else:
                aviso('No se encontraron registros de notas en el rango de fechas proporcionado.', 0)
                indicarEnter()
                return
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()
    indicarEnter()

lmenu_principal = [('Opción', 'Descripción'),
              (1, 'Notas'),
              (2, 'Clientes'),
              (3, 'Servicios'),
              (4, 'Estadísticas'),
              (5, 'Salir')]

lmenu_notas = [('Opción', 'Descripción'),
              (1, 'Registrar una nota'),
              (2, 'Cancelar una nota'),
              (3, 'Recuperar una nota'),
              (4, 'Consultas y reportes'),
              (5, 'Volver al menú principal')]

lmenu_notas_consultasYReportes = [('Opción', 'Descripción'),
              (1, 'Consulta por período'),
              (2, 'Consulta por folio'),
              (3, 'Volver al menú de notas')]

lmenu_clientes = [('Opción', 'Descripción'),
                       (1, 'Agregar un cliente'),
                       (2, 'Suspender un cliente'),
                       (3, 'Recuperar un cliente'),
                       (4, 'Consultas y reportes'),
                       (5, 'Volver al menú principal')]

lmenu_clientes_consultasYReportes = [('Opción', 'Descripción'),
                       (1, 'Listado de clientes registrados'),
                       (2, 'Búsqueda por clave'),
                       (3, 'Búsqueda por nombre'),
                       (4, 'Volver al menú de clientes')]

lmenu_clientes_consultasYReportes_listadoDeClientesRegistrados = [('Opción', 'Descripción'),
                       (1, 'Orden por clave'),
                       (2, 'Orden por nombre'),
                       (3, 'Volver al menú anterior')]

lmenu_servicios = [('Opción', 'Descripción'),
              (1, 'Agregar un servicio'),
              (2, 'Suspender un servicio'),
              (3, 'Recuperar un servicio'),
              (4, 'Consultas y reportes'),
              (5, 'Volver al menú principal')]

lmenu_servicios_consultasYReportes = [('Opción', 'Descripción.'),
              (1, 'Búsqueda por clave de servicio'),
              (2, 'Búsqueda por nombre de servicio'),
              (3, 'Listado de servicios'),
              (4, 'Volver al menú de servicios')]

lmenu_servicios_consultasYReportes_listadoDeServicios = [('Opción', 'Descripción'),
              (1, 'Orden por clave'),
              (2, 'Orden por nombre de servicio'),
              (3, 'Volver al menú anterior')]

lmenu_estadisticas = [('Opción', 'Descripción'),
                (1, 'Servicios más prestados'),
                (2, 'Clientes con más notas'),
                (3, 'Promedio de los montos de las notas'),
                (4, 'Volver al menú principal')]

try:
    with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
        mi_cursor = conn.cursor()
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS CLIENTES \
                        (CLAVE_CLIENTE INTEGER PRIMARY KEY NOT NULL, NOMBRE TEXT NOT NULL, \
                        RFC TEXT NULL, ESTADO_CLIENTE INTEGER NOT NULL, \
                        CORREO_ELECTRONICO TEXT NOT NULL);")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS NOTAS \
                        (FOLIO INTEGER PRIMARY KEY NOT NULL, FECHA timestamp NOT NULL, \
                        CLAVE_CLIENTE INTEGER NOT NULL, MONTO_A_PAGAR REAL NOT NULL, ESTADO_NOTA INTEGER NOT NULL, \
                        FOREIGN KEY (CLAVE_CLIENTE) REFERENCES CLIENTES(CLAVE_CLIENTE));")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS SERVICIOS \
                        (CLAVE_SERVICIO INTEGER PRIMARY KEY NOT NULL, NOMBRE_SERVICIO TEXT NOT NULL, \
                        ESTADO_SERVICIO INTEGER NOT NULL, \
                        COSTO_SERVICIO REAL NOT NULL);")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS DETALLE_NOTA \
                        (CLAVE_DETALLE INTEGER PRIMARY KEY NOT NULL, \
                        FOLIO INTEGER NOT NULL, \
                        CLAVE_SERVICIO INTEGER NOT NULL,  \
                        FOREIGN KEY (FOLIO) REFERENCES NOTAS(FOLIO), \
                        FOREIGN KEY (CLAVE_SERVICIO) REFERENCES SERVICIOS(CLAVE_SERVICIO));")
                
        print(f'{guiones(17)}Tablas creadas o cargadas exitosamente.{guiones(17)}')
except Error as e:
    print(e)
except Exception:
    print(f'Se produjo el siguiente error {sys.exc_info()[0]}')
finally:
    conn.close()

menuPrincipal()