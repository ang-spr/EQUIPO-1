#Módulos:
import datetime as dt           # Módulo para utilizar formato fechas.
import os                       # Módulo para limpiar pantalla
from tabulate import tabulate   # Módulo para dar formato tabular.
                                # Si marca error es necesario ejecutar en el símbolo de sistema la siguiente línea: pip install tabulate
import re                       # Módulo para expresiones regulares.
                                # Lo utilizamos para saber si el texto ingresado tenía decimales
import unicodedata              # Módulo para eliminar acentos y caracteres especiales.

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

#Listas:
lista_menu = [('Número de opción', 'Servicio'),
              (1, 'Registrar nota.'),
              (2, 'Consulta y reportes.'),
              (3, 'Cancelar una nota.'),
              (4, 'Recuperar una nota.'),
              (5, 'Salir')]

#Recolección de datos:
fecha_actual = dt.date.today()
nota_final = {}
notas_canceladas = []
lista_servicios = []
opcion = 0

while True:    
    if opcion == 0:
        #Menú principal:
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
                print("\nIngrese una fecha válida en formato dd/mm/aaaa.")
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

    #Consulta y reportes:
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

                while True:
                    fecha_texto1 = input("Ingresa la fecha inicial en el formato (dd/mm/aaaa): ").strip()
                    fecha_texto2 = input("Ingresa la fecha final en el formato (dd/mm/aaaa): ").strip()

                    try:
                        fecha_inicial = dt.datetime.strptime(fecha_texto1, "%d/%m/%Y").date()
                        fecha_fin = dt.datetime.strptime(fecha_texto2, "%d/%m/%Y").date()
                        if fecha_inicial > fecha_actual:
                            print("\nLa fecha inicial no puede ser mayor que la fecha actual. Ingrese fechas válidas.")
                        elif fecha_inicial > fecha_fin:
                            print("\nLa fecha inicial no puede ser mayor que la fecha final. Ingrese fechas válidas.")
                        else:
                            break
                    except ValueError:
                        print("\nIngrese fechas válidas en formato dd/mm/aaaa.")
                        continue     
                
                periodo = fecha_inicial.year-fecha_fin.year
                impresion_fecha_inicial = fecha_inicial.strftime("%d/%m/%Y")
                impresion_fecha_fin = fecha_fin.strftime("%d/%m/%Y")
                guiones_separadores()
                print(f"Reporte a consultar entre: {impresion_fecha_inicial} y {impresion_fecha_fin}.")
                
                #Buscar notas:
                notas_periodo = []
                for folio, nota in nota_final.items():
                    fecha_nota = nota[0]
                    if fecha_inicial <= fecha_nota <= fecha_fin:
                        notas_periodo.append((folio, nota))

                #Imprimir notas:
                if notas_periodo:
                    print("\nNotas en el período seleccionado:")
                    print(tabulate([(folio, nota[0].strftime("%d/%m/%Y"), nota[1], nota[2], nota[3], nota[5]) for folio, nota in notas_periodo],
                                   headers= ['Folio', 'Fecha', 'Cliente','RFC', 'Correo Electronico', 'Monto a Pagar'],
                                   tablefmt='pretty'))
                else:
                    print("No hay notas emitidas para el período especificado.")
                
                input(f"\n\nDe clic en Enter para continuar.")
                limpiar_consola()
                break

            #Consulta por folio:
            elif tipo == 2:
                print(f"\n\n{guiones(10)}Consulta por folio{guiones(10)}".upper())

                while True:
                    try:
                        folio = int(input("Ingrese el folio del cual desea consultar información: "))
                        if folio in nota_final:
                            nota = nota_final[folio]
                            titulos_notas = ["Folio", "Fecha", "Cliente", "Monto a pagar"]
                            datos = [(folio, nota[0].strftime('%d/%m/%Y'), nota[1], nota[2])]
                            print(tabulate(datos, headers=titulos_notas, tablefmt='pretty'))
                            break
                        else:
                            print(f"\nEl folio {folio} no se encuentra en el sistema.")
                            break
                    except ValueError:
                        print("\nIngrese un número de folio válido.")
                        continue
                break
            
            #Consulta por cliente:
            else:
                print(f"\n\n{guiones(10)}Consulta por cliente{guiones(10)}".upper())
                
                lista_rfc=set([nota[2] for nota in nota_final.values()])

                #Mostrar rfc al usuario
                print("Lista de RFC disponibles")
                for i, rfc in enumerate(lista_rfc,start=1):
                    print(f"{i}. {rfc}")

                while True:
                    try:
                        elegir_folio_rfc=int(input("Ingrese el folio que se generó del RFC que deseas consultar: "))
                        if 1>= elegir_folio_rfc<=len(lista_rfc):
                            consulta_rfc=list(lista_rfc)[elegir_folio_rfc-1]

                            #filtrar los folios asociados a los RFC
                            folios_rfc=[folio for folio, nota in nota_final.items() if nota[2]==consulta_rfc]
                            nuevo_folio=max(folios_rfc,default=0) + 1   #asegurar que los folios sean únicos
                            
                            print(f"\nNotas para el RFC {consulta_rfc}: ") #mostrar notas para RFC seleccionado
                            notas_promedio=[]
                            
                            for folio in folios_rfc:
                                nota=nota_final[folio]
                                notas_promedio.append(nota[5]) #para calcular el monto promedio
                                print(f"Folio: {folio}\nFecha: {nota[0].strftime ('%d/%m/%Y')}\nCliente: {nota[1]}\nMonto a pagar: {nota[5]}")
                                print(f"\nDetalles de la nota:\n{tabulate(nota[4], headers = ['Detalle', 'Precio'], tablefmt = 'pretty')}")
                                
                            promedio=sum(notas_promedio)/len (notas_promedio) #calcular monto promedio
                            print(f"Monto promedio de las notas para el RFC {consulta_rfc}: {promedio:.2f}")


                            while True:
                                try:
                                    exportar_excel=int(input("¿Desea exportar esta información a un archivo Excel? (1: Sí, 2: No): "))
                                    if exportar_excel==1:
                                        print("Exportando a Excel...")
                                        break
                                    elif exportar_excel== 2:
                                            break
                                    else:
                                        print("Ingrese una opción válida (1 o 2).")
                                except ValueError:
                                    print("Ingrese una opción válida (1 o 2).")
                                else:
                                    print(f"No hay notas para el RFC {rfc}.")
                                    
                        else:
                            print(f"EL FOLIO {folio} NO SE ENCUENTRA EN EL SISTEMA.")
                            break
                        
                    except ValueError:
                        print("Ingrese un número de folio válido.")
                        continue
                break        

        #input(f"\n\nDe clic en Enter para continuar.")
        #limpiar_consola()

    elif opcion == 3:
        print("")

    elif opcion == 4:
        print("")

    else:
        print("")