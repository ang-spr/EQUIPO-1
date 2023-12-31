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
            notas_ordenadoPeriodo()
            limpiar_consola()
            break

        elif opcion == 2:
            mostrarTitulo(ubicacion)
            notas_ordenadoFolio()
            opcion = 0

        else:
            break

        limpiar_consola()

def registrarNota():
    
    if validarContinuarOpcion():
        return

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT * FROM CLIENTES;")
            clientes = mi_cursor.fetchall()
            mi_cursor.execute("SELECT * FROM SERVICIOS;")
            servicios = mi_cursor.fetchall()

            if not clientes:
                aviso("Es necesario tener al menos un cliente registrado para generar una nota.", 15)
                indicarEnter()
                return
            
            if not servicios:
                aviso("Es necesario tener al menos un servicio registrado para generar una nota.", 15)
                indicarEnter()
                return 
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}.')
    finally:
        conn.close()

    #Fecha.
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
                mi_cursor.execute("SELECT COUNT(*) FROM CLIENTES WHERE CLAVE_CLIENTE = ?", (id_cliente,))
                if mi_cursor.fetchone()[0] > 0:
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
                mi_cursor.execute("SELECT COUNT(*) FROM SERVICIOS WHERE CLAVE_SERVICIO = ?", (id_servicio,))

                if mi_cursor.fetchone()[0] > 0:
                    mi_cursor.execute("SELECT COSTO_SERVICIO FROM SERVICIOS WHERE CLAVE_SERVICIO = ?", (id_servicio,))
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
            mi_cursor.execute("SELECT COUNT(*) FROM NOTAS WHERE (FOLIO = ?) AND (ESTADO_NOTA = 1)", (folio,))

            if not mi_cursor.fetchone()[0] > 0:
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
            mi_cursor.execute("SELECT COUNT(*) FROM NOTAS WHERE ESTADO_NOTA = 0")

            if not mi_cursor.fetchone()[0] > 0:
                aviso("No existen notas canceladas para recuperar.", 15)
                indicarEnter()
                return
            else:
                print("Notas canceladas:")
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

    print("Ingrese el folio de la nota a recuperar.")
    while True:
        folio = solicitarSoloNumeroEntero('Folio')

        try:
            with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT COUNT(*) FROM NOTAS WHERE (FOLIO = ?) AND (ESTADO_NOTA = 0)", (folio,))

                if not mi_cursor.fetchone()[0] > 0:
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

def notas_ordenadoPeriodo():
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
                WHERE N.FECHA BETWEEN ? AND ?
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
            nombre_archivo = f'ReportePorPeriodo_{fecha_inicial.strftime("%m_%d_%Y")}_{fecha_fin.strftime("%m_%d_%Y")}'
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

def notas_ordenadoFolio():
    if validarContinuarOpcion():
        return

    print('Ingrese el folio de la nota a buscar: ')
    folio = solicitarSoloNumeroEntero('Folio')

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT COUNT(*) FROM NOTAS WHERE (FOLIO = ?) AND (ESTADO_NOTA = 1)", (folio,))

            if not mi_cursor.fetchone()[0] > 0:
                aviso("La nota con el folio proporcionado no se encuentra en el sistema.", 15)
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
            clientes_consultasYReportes(ubicacion)

        else:
            break

        opcion = 0
        limpiar_consola()
        continue

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

        limpiar_consola()
        break

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
            datos_clientes = (nombre_cliente, rfc, mail)
            mi_cursor.execute("INSERT INTO CLIENTES(NOMBRE, RFC, CORREO_ELECTRONICO)\
            VALUES (?, ?, ?)", datos_clientes)

            aviso('Cliente registado correctamente', 20)
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

def clientes_ordenadoClave():
    if validarContinuarOpcion():
        return
    
    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT * FROM CLIENTES ORDER BY CLAVE_CLIENTE")
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
            fechaReporte = fechaActual().strftime("%m%d%Y")
            nombre_archivo = f'ReporteClientesActivosPorClave_{fechaReporte}'
            df = pd.DataFrame(registros, columns=['Clave', 'Nombre', 'RFC', 'Correo electrónico'])

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
            mi_cursor.execute("SELECT * FROM CLIENTES ORDER BY NOMBRE")
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
            fechaReporte = fechaActual().strftime("%m%d%Y")
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
            mi_cursor.execute("SELECT * FROM CLIENTES WHERE CLAVE_CLIENTE = :CLAVE_CLIENTE", valores)
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
            mi_cursor.execute("SELECT * FROM CLIENTES WHERE NOMBRE = :NOMBRE", valores)
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
            servicio_ordenadoClave()

        elif opcion == 2:
            mostrarTitulo(ubicacion)
            servicio_ordenadoNombre()

        else:
            break

        limpiar_consola()
        break

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
            datos_servicios = (servicio, precio)
            mi_cursor.execute("INSERT INTO SERVICIOS(NOMBRE_SERVICIO, COSTO_SERVICIO)\
            VALUES (?, ?)", datos_servicios)

            aviso('Servicio registado correctamente', 20)
            indicarEnter()
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()

def servicios_busquedaClave():
    if validarContinuarOpcion():
        return

    print("Ingrese la clave a buscar.")
    clave_a_buscar = solicitarSoloNumeroEntero('Clave')

    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            valores = {"CLAVE_SERVICIO":clave_a_buscar}
            mi_cursor.execute("SELECT * FROM SERVICIOS WHERE CLAVE_SERVICIO = :CLAVE_SERVICIO", valores)
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
            mi_cursor.execute("SELECT * FROM SERVICIOS WHERE NOMBRE_SERVICIO = :NOMBRE_SERVICIO", valores)
            registros = mi_cursor.fetchall()

            if registros:
                aviso("Servicio encontrado:", 0)
                print(tabulate(registros, headers = ['Clave', 'Nombre', 'RFC', 'Correo electrónico'], tablefmt = 'pretty'))
            else:
                aviso('No se encontró el servicio con la clave ingresada.', 20)
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    finally:
        conn.close()   
        indicarEnter()            

def servicio_ordenadoClave():
    if validarContinuarOpcion():
        return
    
    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT * FROM SERVICIOS ORDER BY CLAVE_SERVICIO")
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

    print('¿Desea exportar los registros encontrados? (Sí/No).')
    respuesta = respuestaSINO()

    if respuesta == 'SI':
        guiones_separadores()
        print("Ingrese el número de la opción que desee realizar.")
        print("1. Exportar a Excel.\n2. Exportar a CSV.\n3. Regresar al menú de reportes.")
        respuesta = validarOpcionesNumericas(1, 3)

        if respuesta in (1, 2):
            guiones_separadores()
            fechaReporte = fechaActual().strftime("%m%d%Y")
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
        aviso('Información no exportada', 20)
        indicarEnter()

def servicio_ordenadoNombre():
    if validarContinuarOpcion():
        return
    
    try:
        with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT * FROM SERVICIOS ORDER BY NOMBRE_SERVICIO")
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

    print('¿Desea exportar los registros encontrados? (Sí/No).')
    respuesta = respuestaSINO()

    if respuesta == 'SI':
        guiones_separadores()
        print("Ingrese el número de la opción que desee realizar.")
        print("1. Exportar a Excel.\n2. Exportar a CSV.\n3. Regresar al menú de reportes.")
        respuesta = validarOpcionesNumericas(1, 3)

        if respuesta in (1, 2):
            guiones_separadores()
            fechaReporte = fechaActual().strftime("%m%d%Y")
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
        aviso('Información no exportada', 20)
        indicarEnter()

lmenu_principal = [('Opción', 'Descripción'),
              (1, 'Notas'),
              (2, 'Clientes'),
              (3, 'Servicios'),
              (4, 'Salir')]

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
                       (2, 'Consultas y reportes'),
                       (3, 'Volver al menú principal')]

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
              (2, 'Consultas y reportes'),
              (3, 'Volver al menú principal')]

lmenu_servicios_consultasYReportes = [('Opción', 'Descripción.'),
              (1, 'Búsqueda por clave de servicio'),
              (2, 'Búsqueda por nombre de servicio'),
              (3, 'Listado de servicios'),
              (4, 'Volver al menú de servicios')]

lmenu_servicios_consultasYReportes_listadoDeServicios = [('Opción', 'Descripción'),
              (1, 'Orden por clave'),
              (2, 'Orden por nombre de servicio'),
              (3, 'Volver al menú anterior')]

try:
    with sqlite3.connect('EVIDENCIA_3_TALLER_MECANICO.db') as conn:
        mi_cursor = conn.cursor()
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS CLIENTES \
                        (CLAVE_CLIENTE INTEGER PRIMARY KEY NOT NULL, NOMBRE TEXT NOT NULL, \
                        RFC TEXT NULL, CORREO_ELECTRONICO TEXT NOT NULL);")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS NOTAS \
                        (FOLIO INTEGER PRIMARY KEY NOT NULL, FECHA timestamp NOT NULL, \
                        CLAVE_CLIENTE INTEGER NOT NULL, MONTO_A_PAGAR REAL NOT NULL, ESTADO_NOTA INTEGER NOT NULL, \
                        FOREIGN KEY (CLAVE_CLIENTE) REFERENCES CLIENTES(CLAVE_CLIENTE));")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS SERVICIOS \
                        (CLAVE_SERVICIO INTEGER PRIMARY KEY NOT NULL, NOMBRE_SERVICIO TEXT NOT NULL, \
                        COSTO_SERVICIO REAL NOT NULL);")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS DETALLE_NOTA \
                        (CLAVE_DETALLE INTEGER PRIMARY KEY NOT NULL, \
                        FOLIO INTEGER NOT NULL, \
                        CLAVE_SERVICIO INTEGER NOT NULL,  \
                        FOREIGN KEY (FOLIO) REFERENCES NOTAS(FOLIO), \
                        FOREIGN KEY (CLAVE_SERVICIO) REFERENCES SERVICIOS(CLAVE_SERVICIO));")
        
        print(f'{guiones(22)}Tablas creadas existosamente{guiones(22)}')
except Error as e:
    print(e)
except Exception:
    print(f'Se produjo el siguiente error {sys.exc_info()[0]}')
finally:
    conn.close()

menuPrincipal()
