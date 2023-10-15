#Módulos: 
import datetime as dt           # Módulo para utilizar formato fechas.
import os                       # Módulo para limpiar pantalla
from tabulate import tabulate   # Módulo para dar formato tabular.
                                # Si marca error es necesario ejecutar en el símbolo de sistema la siguiente línea: pip install tabulate
import re                       # Módulo para expresiones regulares.
                                # Lo utilizamos para saber si el texto ingresado tenía decimales
import unicodedata              # Módulo para eliminar acentos y caracteres especiales.
import numpy as np              # pip install numpy
import pandas as pd

#Funciones:
def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def guiones(longitud):
    return '-' * longitud

def respuesta_SI_NO(procesar_SI_NO):
    procesar_SI_NO = procesar_SI_NO.strip().upper()
    procesar_SI_NO = ''.join((c for c in unicodedata.normalize('NFD', procesar_SI_NO) if unicodedata.category(c) != 'Mn'))
    return procesar_SI_NO

def menuActual(numeroMenu, descripcionMenu):
    print(f"Usted se encuentra en la opción {numeroMenu}:\n{guiones(20)}{descripcionMenu.upper()}{guiones(20)}")

def guiones_separadores():
    return print('-' * 50)

def validadorOpcionesNumericas(opcionMin, opcionMax):
    while True:
        try:
            opcionValida = int(input(f"Opción: "))
            if opcionValida >= opcionMin and opcionValida <= opcionMax:
                return opcionValida
            else:
                print(f"\nIngrese un número válido ({opcionMin}-{opcionMax}).")
        except ValueError:
            print(f"\nIngrese un número válido ({opcionMin}-{opcionMax}).")

def validarContinuarOpcion(continuarOpcion):
    continuarOpcion = None
    while continuarOpcion != "0" and continuarOpcion != "":
        continuarOpcion = input(f"Pulse Enter para continuar la opción actual o ingrese 0 para volver al menú principal. ").strip()
    if continuarOpcion == "0":
        return True

def guardarCSV():
    data = []
    for folio, nota in nota_final.items():
        detalles = nota[4]  # Detalles es una lista de tuplas
        for detalle in detalles:
            data.append([folio, nota[0].strftime("%d/%m/%Y"), nota[1], nota[2], nota[3], detalle[0], detalle[1], nota[5]])

    df = pd.DataFrame(data, columns=['Folio', 'Fecha', 'Cliente', 'RFC', 'Correo Electrónico', 'Detalle', 'Precio', 'Monto a Pagar'])
    df.to_csv('programa.csv', index=False)

nota_final = {} 

def cargarCSV(nota_final):
    try:
        df = pd.read_csv('programa.csv')
        for index, row in df.iterrows():
            folio = int(row['Folio'])
            fecha = dt.datetime.strptime(row['Fecha'], "%d/%m/%Y").date()
            cliente = row['Cliente']
            rfc = row['RFC']
            correo = row['Correo Electrónico']
            monto = float(row['Monto a Pagar'])
            detalle_desc = row['Detalle']
            detalle_precio = float(row['Precio'])

            # Verificar si el folio existe en nota_final
            if folio in nota_final:
                detalles = nota_final[folio][4]
                detalles.append((detalle_desc, detalle_precio))
                nota_final[folio] = (fecha, cliente, rfc, correo, detalles, monto)
            else:
                nota_final[folio] = (fecha, cliente, rfc, correo, [(detalle_desc, detalle_precio)], monto)

        print(f"\n{guiones(17)} Datos cargados exitosamente {guiones(17)}".upper())
    except FileNotFoundError:
        print(f"\n{guiones(17)} El archivo CSV no existe. Se creará uno nuevo al salir {guiones(17)}".upper())

#Listas:
lista_menu = [('Número de opción', 'Servicio'),
              (1, 'Registrar nota.'),
              (2, 'Consulta y reportes.'),
              (3, 'Cancelar una nota.'),
              (4, 'Recuperar una nota.'),
              (5, 'Salir')]

cargarCSV(nota_final) 

#Recolección de datos:
fecha_actual = dt.date.today()
notas_canceladas = []
lista_servicios = []
opcion = 0

while True:    
    #Menú principal:
    if opcion == 0:
        print(f'{guiones(20)}TALLER MECÁNICO DON HAMBLETON{guiones(20)}')
        print('Buen día, ingrese el número de la opción que desee realizar:')
        print(tabulate(lista_menu, headers = 'firstrow', tablefmt = 'pretty'))

        while opcion == 0:
            opcion = validadorOpcionesNumericas(1, 5)

    #Registrar nota:
    if opcion == 1:
        numero_servicio = 0
        total_precio_servicio = 0.00
        limpiar_consola()
        menuActual(opcion, lista_menu[opcion][1])

        if validarContinuarOpcion(opcion):
            opcion = 0
            limpiar_consola()
            continue

        #Folio:
        nueva_nota = (max(nota_final.keys(), default = 0)) + 1
        print(f'\nNúmero de folio creado: {nueva_nota}')
        guiones_separadores()

        #Fecha:
        print("Ingrese la fecha de la realización de la nota (dd/mm/aaaa).")
        while True:
            fecha_registro = input("Fecha: ").strip()
            try:
                fecha_procesada = dt.datetime.strptime(fecha_registro, "%d/%m/%Y").date()
                if fecha_procesada > fecha_actual:
                    print("\nLa fecha ingresada no debe ser posterior a la fecha actual.\nIngrese una fecha válida.")
                    continue
                break
            except ValueError:
                print("\nIngrese una fecha válida en formato (dd/mm/aaaa).")
        guiones_separadores()

        #Nombre del cliente:
        print('Ingrese el nombre completo del cliente.')
        while True:
            nombre_cliente = input('Nombre: ').strip().upper()
            if len(nombre_cliente) < 5 or len(nombre_cliente) > 50:
                print("\nEl nombre completo debe tener entre 5 y 50 caracteres.")
                continue
            if not nombre_cliente.replace(' ', '').isalpha():
                print("\nEl nombre solo debe contener letras y espacios.")
                continue
            break
        guiones_separadores()

        #RFC:
        #Tipo de RFC:
        print('Ingrese el número del tipo de RFC:\n1. Físico.\n2. Moral.')
        tipo = validadorOpcionesNumericas(1, 2)
        guiones_separadores()

        #Homoclave:
        print(f"Ingrese el RFC {'Físico' if tipo == 1 else 'Moral'}.")
        while True:
            rfc = input("RFC: ").strip().upper()
            if (tipo == 1 and not len(rfc) == 13) or (tipo == 2 and not len(rfc) == 12):
                print("\nIngrese la longitud correcta del RFC.")
                continue

            if not re.match(r'^[A-Z]{3,4}[0-9]{2}[0-9]{2}[0-9]{2}[A-Z0-9]{3}$', rfc):
                print("\nEl formato del RFC es incorrecto, ingrese un RFC válido.")
                continue
            break
        guiones_separadores()

        #Correo electrónico:
        print('Ingrese el correo electrónico.')
        while True:
            mail = input('Correo electronico: ').strip().upper()
            if not re.match(r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$', mail):
                print('\nEl correo no es valido, ingrese un correo válido.')
                continue
            break
        guiones_separadores()

        #Servicios realizados:      
        while True:
            numero_servicio += 1
            #Guardar un servicio:
            #Servicio:
            print('Ingrese la descripción del servicio.')
            while True:
                servicio = input('Servicio: ').strip().upper()
                if servicio == '':
                    print('\nIngrese una descripción válida.')
                    continue
                break
            guiones_separadores()

            #Precio:
            print("Ingrese el precio del servicio (Máximo dos decimales).")
            while True:
                precio_servicio_recibido = input("Precio: ").strip()
                if re.match(r'^\d+(\.\d{1,2})?$', precio_servicio_recibido):
                    precio_servicio = float(precio_servicio_recibido)
                    break
                else:
                    print("\nIngrese un precio válido (Máximo dos decimales).")
                    continue
            print(f"{guiones(50)}\nServicio agregado correctamente.")

            #Guardar todos los servicios y precios:
            tupla_servicio_actual = (servicio, precio_servicio)
            lista_servicios.append(tupla_servicio_actual)
            total_precio_servicio += precio_servicio
            total_precio_servicio = round(total_precio_servicio, 2)

            #Conocer si desea agregar más servicios y llevarlo a su elección:
            print('\t¿Desea agregar otro servicio? (Sí/No)')
            while True:
                otro_servicio = input('\tRespuesta: ')
                otro_servicio = respuesta_SI_NO(otro_servicio)

                if otro_servicio == 'SI' or otro_servicio == 'NO':
                    break
                else:
                    print('\n\tIngrese una respuesta válida (Sí/No).')
            
            if otro_servicio == 'SI':
                limpiar_consola()
                print(f"{numero_servicio} servicio guardado correctamente.\n\n")
                guiones_separadores()
                continue
            else:
                limpiar_consola()
                nota_final[nueva_nota]=(fecha_procesada, nombre_cliente, rfc, mail, lista_servicios, total_precio_servicio)
                #Nota:
                print(f"{guiones(15)}Nota guardada correctamente{guiones(15)}")
                print(f"Información guardada de la nota: {nueva_nota}\n")
                print(tabulate([(nueva_nota, nota_final[nueva_nota][0].strftime("%d/%m/%Y"), nota_final[nueva_nota][1], nota_final[nueva_nota][2],
                                nota_final[nueva_nota][3], nota_final[nueva_nota][5])],
                               headers=['Folio', 'Fecha', 'Cliente','RFC', 'Correo Electronico', 'Monto a Pagar'], tablefmt='pretty'))
                #Detalles de la nota:
                print(f"\nDetalles de la nota:\n{tabulate(lista_servicios, headers = ['Detalle', 'Precio'], tablefmt = 'pretty')}")
                input(f"\n\nDe clic en Enter para continuar.")
                limpiar_consola()
                lista_servicios = []
                tupla_servicio_actual = ()
                break

    #Consultar notas:
    elif opcion == 2:
        limpiar_consola()
        menuActual(opcion, lista_menu[opcion][1])

        if validarContinuarOpcion(opcion):
            opcion = 0
            limpiar_consola()
            continue

        print('\nIngrese el número del tipo de consulta:\n1. Consulta por periodo.\n2. Consulta por folio.\n3. Consulta por cliente.')
        tipo = validadorOpcionesNumericas(1, 3)

        while True:
            #Consulta por periodo:
            if tipo == 1:
                print(f"\n\n{guiones(10)}Consulta por periodo{guiones(10)}".upper())

                #Fecha inicial
                print("Ingrese la fecha inicial en el formato (dd/mm/aaaa).")
                while True:
                    fecha_texto1 = input("Fecha inicial: ").strip()

                    if fecha_texto1 == "":
                        fecha_texto1 = "01/01/2000"
                        print("La fecha inicial se asumió como 01/01/2000.")
                    try:
                        fecha_inicial = dt.datetime.strptime(fecha_texto1, "%d/%m/%Y").date()
                        break
                    except ValueError:
                        print("\nIngrese una fecha inicial válida en formato dd/mm/aaaa.")
                        continue

                #Fecha final
                print("\nIngresa la fecha final en el formato (dd/mm/aaaa).")
                while True:
                    fecha_texto2 = input("Fecha final: ").strip()

                    if fecha_texto2 == "":
                        fecha_fin = fecha_actual
                        print(f"La fecha final se asumió como la actual: {fecha_fin.strftime('%d/%m/%Y')}.")
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

                periodo = fecha_inicial.year-fecha_fin.year
                impresion_fecha_inicial = fecha_inicial.strftime("%d/%m/%Y")
                impresion_fecha_fin = fecha_fin.strftime("%d/%m/%Y")
                guiones_separadores()
                print(f"Reporte a consultar entre: {impresion_fecha_inicial} a {impresion_fecha_fin}:")
                
                #Buscar notas:
                notas_periodo = []
                for folio, nota in nota_final.items():
                    fecha_nota = nota[0]
                    if fecha_inicial <= fecha_nota <= fecha_fin:
                        notas_periodo.append((folio, nota))

                #Imprimir notas:
                if notas_periodo:
                    print("\nNotas en el período seleccionado:".upper())
                    print(tabulate([(folio, nota[0].strftime("%d/%m/%Y"), nota[1], nota[2], nota[3], nota[5]) for folio, nota in notas_periodo],
                                   headers= ['Folio', 'Fecha', 'Cliente','RFC', 'Correo Electronico', 'Monto a Pagar'],
                                   tablefmt='pretty'))
                    
                    promedio_montos = np.mean((sum(nota[5] for _, nota in notas_periodo)) / len(notas_periodo))
                    print(f"\nEl promedio de las notas en el período es de: ${promedio_montos:.2f}.")

                else:
                    print(f"\n\n\t{guiones(10)}No hay notas emitidas para el período especificado.{guiones(10)}".upper())
                
                input(f"\n\nDe clic en Enter para continuar.")
                limpiar_consola()
                break

            #Consulta por folio:
            elif tipo == 2:
                print(f"\n\n{guiones(10)}Consulta por folio{guiones(10)}".upper())

                print("Ingrese el folio del cual desea consultar la nota.")
                while True:
                    try:
                        folio = int(input("Folio: "))
                        guiones_separadores()
                        if folio in nota_final:
                            nota = nota_final[folio]
                            print(tabulate([(folio, nota[0].strftime("%d/%m/%Y"), nota[1], nota[2], nota[3], nota[5])],
                                        headers= ['Folio', 'Fecha', 'Cliente','RFC', 'Correo Electronico', 'Monto a Pagar'],
                                        tablefmt='pretty'))
                            break
                        else:
                            print(f"\n\n\t{guiones(10)}El folio {folio} no se encuentra en el sistema.{guiones(10)}".upper())
                            break
                    except ValueError:
                        print("\nIngrese un número válido.")
                        continue
                input(f"\n\nDe clic en Enter para continuar.")
                limpiar_consola()

            #Consulta por cliente:
            else:
                print(f"\n\n{guiones(10)}Consulta por cliente{guiones(10)}".upper())
                
                lista_rfc = sorted(set([nota[2] for nota in nota_final.values()]))

                #Mostrar RFC al usuario.
                if lista_rfc:
                    print("\nLista de RFC disponibles:")
                    tabla_rfc = [(i, rfc) for i, rfc in enumerate(lista_rfc, start=1)]
                    print(tabulate(tabla_rfc, headers = ['Folio', 'RFC'], tablefmt = 'pretty'))
                else:
                    print(f"\n\n\t{guiones(10)}Actualmente no hay notas guardadas{guiones(10)}".upper())
                    input(f"\n\nDe clic en Enter para continuar.")
                    limpiar_consola()
                    break
                guiones_separadores()

                print("Ingrese el folio del RFC que desea consultar.")
                while True:
                    try:
                        elegir_folio_rfc = int(input("Folio: "))
                        guiones_separadores()
                        
                        if 1 >= elegir_folio_rfc <= len(lista_rfc):
                            consulta_rfc = list(lista_rfc)[elegir_folio_rfc-1]

                            folios_rfc = [folio for folio, nota in nota_final.items() if nota[2]==consulta_rfc]
                            monto_promedio = sum(nota_final[folio][5] for folio in folios_rfc) / len(folios_rfc)

                            #En la siguiente evidencia validaremos que si ya había ingresado un RFC tome el mismo nombre y correo, en caso de que agrege más notas con dicho RFC.
                            #No pudimos hacer esta validación por cuestiones de tiempo
                            limpiar_consola()
                            print(f"\nNotas con detalles del cliente: {consulta_rfc}.".upper()) 
                            for folio in folios_rfc:
                                nota = nota_final[folio]

                                print(f"{guiones(20)}Nota: {folio}{guiones(20)}".upper())
                                print(tabulate([(folio, nota[0].strftime("%d/%m/%Y"), nota[1], nota[2], nota[3], nota[5])],
                                        headers= ['Folio', 'Fecha', 'Cliente','RFC', 'Correo Electronico', 'Monto a Pagar'],
                                        tablefmt='pretty'))
                                print(f"\nDetalles de la nota:\n{tabulate(nota[4], headers = ['Detalle', 'Precio'], tablefmt = 'pretty')}\n\n\n")
                            guiones_separadores()
                            
                            #Promedio
                            print(f"El monto promedio de las notas para el RFC {consulta_rfc} es: ${monto_promedio:.2f}")
                            guiones_separadores()
                            
                            #Exportar a Excel
                            print("¿Desea exportar esta información a un archivo Excel? (Sí/No)")
                            while True:
                                exportar_excel = input("Respuesta: ")
                                if respuesta_SI_NO(exportar_excel) == "SI":
                                    #DataFrame con los elementos de la nota:
                                    notas_cliente = [(folio, nota[0].strftime("%d/%m/%Y"), nota[1], nota[2], nota[3], nota[5]) for folio, nota in nota_final.items() if nota[2] == consulta_rfc]
                                    df_notas = pd.DataFrame(notas_cliente, columns=['Folio', 'Fecha', 'Cliente', 'RFC', 'Correo Electrónico', 'Monto a pagar'])

                                    #DataFrame con los detalles:
                                    detalles_cliente = []
                                    for folio, nota in nota_final.items():
                                        if nota[2] == consulta_rfc:
                                            for detalle in nota[4]:
                                                detalles_cliente.append([folio, detalle[0], detalle[1]])
                                    df_detalles = pd.DataFrame(detalles_cliente, columns=['Folio', 'Detalle', 'Precio'])

                                    #Combinar DataFrames:
                                    df_completo = pd.merge(df_notas, df_detalles, on='Folio')

                                    #Nombre de archivo:
                                    rfc_cliente = consulta_rfc
                                    fecha_emision = fecha_actual.strftime("%d%m%Y")
                                    nombre_archivo = f'{rfc_cliente}_{fecha_emision}.xlsx'

                                    #Ubicación:
                                    ubicacion_documento = os.path.abspath(nombre_archivo)

                                    #Guardar:
                                    df_completo.to_excel(nombre_archivo, index=False)
                                    print(f"\n\n\t{guiones(10)}Documento generado y guardado exitosamente en {ubicacion_documento}.{guiones(10)}".upper())
                                    break

                                elif respuesta_SI_NO(exportar_excel) == "NO":
                                    print(f"\n\n\t{guiones(10)}Documento no generado.{guiones(10)}".upper())
                                    break
                                else:
                                    print("\nIngrese una respuesta válida.")
                                    continue
                            input(f"\n\nDe clic en Enter para continuar.")
                            limpiar_consola()
                            break
                        else:
                            print(f"\n\n\t{guiones(10)}El folio del RFC ingresado no existe.{guiones(10)}".upper())
                            input(f"\n\nDe clic en Enter para continuar.")
                            limpiar_consola()
                            break 
                    except ValueError:
                        print("\nIngrese un número válido.")
                        continue
            break

    #Cancelar notas:
    elif opcion == 3:
        limpiar_consola()
        menuActual(opcion, lista_menu[opcion][1])

        if validarContinuarOpcion(opcion):
            opcion = 0
            limpiar_consola()
            continue

        #Solicitar nota:
        print("\nIngrese el folio de la nota a cancelar.")
        while True:
            try:
                folio_eliminar = int(input("Respuesta: "))
                break
            except ValueError:
                print("\nIngrese un número válido para el folio.")
        guiones_separadores()

        #Buscar nota:
        if folio_eliminar in nota_final:
            nota = nota_final[folio_eliminar]

            #Mostrar datos antes de eliminar:
            print("Los elementos de la nota son:")
            print(tabulate([(folio_eliminar, nota[0].strftime("%d/%m/%Y"), nota[1], nota[2], nota[3], nota[5])],
                    headers= ['Folio', 'Fecha', 'Cliente','RFC', 'Correo Electronico', 'Monto a Pagar'],
                    tablefmt='pretty'))
            print(f"\nDetalles de la nota:\n{tabulate(nota[4], headers = ['Detalle', 'Precio'], tablefmt = 'pretty')}")
            guiones_separadores()

            #Confirmación de eliminar nota:
            print("¿Está seguro que desea cancelar la nota? (Sí/No): ")
            while True:
                respuesta = input('Respuesta: ')
                respuesta = respuesta_SI_NO(respuesta)
                if respuesta == 'SI' or respuesta == 'NO':
                    break
                else:
                    print('\n\tIngrese una respuesta válida (Sí/No).')
            guiones_separadores()

            if respuesta == "SI":
                #Eliminar la nota
                notas_canceladas.append((folio_eliminar, nota_final[folio_eliminar]))
                del nota_final[folio_eliminar]
                print(f"\n\n\t{guiones(10)}La nota con el folio {folio_eliminar} ha sido cancelada correctamente{guiones(10)}".upper())
            else:
                print(f"\n\n\t{guiones(10)}La nota no ha sido cancelada{guiones(10)}".upper())
        else:
            print(f"\n\n\t{guiones(10)}El folio {folio_eliminar} no existe o ha sido cancelado{guiones(10)}".upper())
        input(f"\n\nDe clic en Enter para continuar.")
        limpiar_consola()

    #Recuperar una nota.    
    elif opcion == 4:
        limpiar_consola()
        menuActual(opcion, lista_menu[opcion][1])

        if notas_canceladas:             
            if validarContinuarOpcion(opcion):
                opcion = 0
                limpiar_consola()
                continue

            print("\nNotas canceladas:")
            print(tabulate([(folio, nota[0].strftime("%d/%m/%Y"), nota[1], nota[2], nota[3], nota[5]) for folio, nota in notas_canceladas],
                           headers = ['Folio', 'Fecha', 'Cliente', 'RFC', 'Correo Electrónico', 'Monto a pagar'],
                           tablefmt='pretty'))

            #Solicitar el folio:
            guiones_separadores()
            print("Ingrese el folio de la nota que desea recuperar o 0 para regresar al menú principal: ")
            while True:
                try:
                    folio_recuperar = int(input("Folio: "))
                    if folio_recuperar == 0:
                        opcion = 0
                        break
                    elif any(folio == folio_recuperar for folio, _ in notas_canceladas):
                        nota = next((nota for folio, nota in notas_canceladas if folio == folio_recuperar), None)

                        guiones_separadores()
                        print("Los elementos de la nota son:")
                        print(tabulate([(folio_recuperar, nota[0].strftime("%d/%m/%Y"), nota[1], nota[2], nota[3], nota[5])],
                                headers= ['Folio', 'Fecha', 'Cliente','RFC', 'Correo Electronico', 'Monto a Pagar'],
                                tablefmt='pretty'))
                        print(f"\nDetalles de la nota:\n{tabulate(nota[4], headers = ['Detalle', 'Precio'], tablefmt = 'pretty')}")
                        guiones_separadores()
                        
                        #Confirmar de recuperar nota:
                        print("¿Está seguro que desea recuperar la nota? (Sí/No): ")
                        while True:
                            respuesta = input('Respuesta: ')
                            respuesta = respuesta_SI_NO(respuesta)
                            if respuesta == 'SI' or respuesta == 'NO':
                                break
                            else:
                                print('\n\tIngrese una respuesta válida (Sí/No).')
                        guiones_separadores()

                        if respuesta == "SI":
                            #Recuperar la nota
                            nota_final[folio_recuperar] = nota
                            notas_canceladas.remove((folio_recuperar, nota))
                            print(f"\n\n\t{guiones(10)}La nota con el folio {folio_recuperar} ha sido recuperada correctamente.{guiones(10)}".upper()) 
                            break
                        else:
                            print(f"\n\n\t{guiones(10)}La nota no ha sido recuperada{guiones(10)}".upper()) 
                            break
                    else:
                        print(f"\n\n\t{guiones(10)}El folio {folio_recuperar} que ingresó no es válido o ya ha sido recuperado.{guiones(10)}".upper()) 
                        break
                except ValueError:
                    print("\nIngrese un número válido.")
        else:
            print(f"\n\n\t{guiones(10)}No hay notas canceladas para recuperar{guiones(10)}".upper()) 
            opcion = 0       
        input("\nPresione Enter para continuar.")
        limpiar_consola()
        continue

    #Salir.
    else:
        print('¿Está seguro que desea salir? (Sí/No)')

        while True:
            salir = input("Respuesta: ")
            salir = respuesta_SI_NO(salir)
            if salir == 'SI' or salir == 'NO':
                break
            else:
                print('\nIngrese una respuesta válida (Sí/No).')
                continue

        if salir == 'SI':
            guardarCSV()  
            print(f"\nLas notas han sido guardadas correctamente.")
            print(f"\n{guiones(15)}Gracias por usar nuestro sistema, hasta la próxima.{guiones(15)}\n".upper())
            break
        elif salir == 'NO':
            limpiar_consola()
            opcion = 0
        else:
            limpiar_consola()
            continue
