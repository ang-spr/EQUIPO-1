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
    procesar_SI_NO = procesar_SI_NO.strip()
    procesar_SI_NO = procesar_SI_NO.upper()
    procesar_SI_NO = ''.join((c for c in unicodedata.normalize('NFD', procesar_SI_NO) if unicodedata.category(c) != 'Mn'))
    return procesar_SI_NO

def menuActual(numeroMenu, descripcionMenu):
    print(f"Usted se encuentra en la opción {numeroMenu}:\n{guiones(10)}{descripcionMenu.upper()}{guiones(10)}")

def guiones_separadores():
    return print('-' * 50)

#Listas:
lista_menu = [('Número de opción', 'Servicio'),
              (1, 'Registrar nota.'),
              (2, 'Consulta y reportes.'),
              (3, 'Cancelar una nota'),
              (4, 'Recuperar una nota'),
              (5, 'Salir')]

lista_servicios = [('Número de servicio', 'Servicio', 'Precio sugerido'),
                   (1, 'Cambio de nueomatico', 600), 
                   (2, 'Ajuste de vujias', 900),
                   (3, 'Cambio de aceite', 850),
                   (4, 'Reparación de aceite', 4500),
                   (5, 'Trasmisión', 3000)]

#Recolección de datos:
fecha_actual = dt.date.today()
nota_final = {}
notas_canceladas = []

while True:
    #Menú principal:
    print(f'{guiones(20)}TALLER MECÁNICO DON HAMBLETON{guiones(20)}')
    print('Buen día, ingrese el número de la opción que desee realizar:')
    print(tabulate(lista_menu, headers = 'firstrow', tablefmt = 'pretty'))

    while True:
        try:
            menu = int(input('Opción: '))
            if menu >= 1 and menu <= 5:
                break
            else:
                print("\nIngrese una opción válida del 1 al 5.")
                continue
        except ValueError:
            print("\nIngrese un número válido.")
            continue

    #Registrar nota:
    total_precio_servicio = 0.00
    if menu == 1:
        numero_servicio = 0
        limpiar_consola()
        menuActual(menu, lista_menu[menu][1])
        
        #Folio:
        nueva_nota = (max(nota_final.keys(), default = 0)) + 1
        print(f'\nNúmero de folio creado: {nueva_nota}')
        guiones_separadores()

        #Fecha:
        while True:
            fecha_registro = input("Ingrese la fecha de la realización de la nota (dd/mm/aaaa): ")
            fecha_registro = fecha_registro.strip()

            try:
                fecha_procesada = dt.datetime.strptime(fecha_registro, "%d/%m/%Y").date()
                if fecha_procesada > fecha_actual:
                    print("\nLa fecha no debe ser posterior a la fecha actual. Ingrese una fecha válida.")
                    continue
                break
            except ValueError:
                print("\nIngrese una fecha válida en formato dd/mm/aaaa.")
        guiones_separadores()

        #Nombre del cliente:
        while True:
            nombre_cliente = input('Ingrese el nombre completo del cliente: ')

            if len(nombre_cliente) < 5 or len(nombre_cliente) > 50:
                print("\nEl nombre completo debe tener entre 5 y 50 caracteres.")
                continue

            if not nombre_cliente.replace(' ', '').isalpha():
                print("\nEl nombre solo debe contener letras y espacios.")
                continue
            
            nombre_cliente = nombre_cliente.strip()
            nombre_cliente = nombre_cliente.upper()
            break
        guiones_separadores()

        #Servicios realizados:        
        lista_total_productos_con_precios = [('Número de servicio', 'Descripción', 'Precio')]
        while True:
            numero_servicio += 1
            #Guardar un servicio:
            #Servicio
            print('Ingrese el número de servicio que desee: ')
            print(tabulate(lista_servicios, headers = 'firstrow', tablefmt = 'pretty'))
            while True:
                try:
                    servicio = int(input('Servicio: '))
                    if servicio >= 1 and servicio <= 5:
                        break
                    else:
                        print("\nIngrese una opción válida del 1 al 5.")
                        continue
                except ValueError:
                    print("\nIngrese un número válido.")
                    continue
            guiones_separadores()

            #Precio
            print("Ingrese el precio real del servicio (exactamente con dos decimales): ")                        
            while True:
                recibido_precio_servicio = input("Precio: ")
                recibido_precio_servicio = recibido_precio_servicio.strip()
                if re.match(r'^\d+\.\d{2}$', recibido_precio_servicio):
                    precio_servicio = float(recibido_precio_servicio)
                    break
                else:
                    print("\nIngrese un precio válido, exactamente con dos decimales.")
                    continue
            
            print(f"{guiones(50)}\nServicio agregado correctamente.")

            #Guardar todos los servicios y precios:
            tupla_servicio_actual = (numero_servicio, lista_servicios[servicio][1], precio_servicio)
            lista_total_productos_con_precios.append(tupla_servicio_actual)
            total_precio_servicio += precio_servicio

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
                continue
            else:
                limpiar_consola()
                nota_final[nueva_nota]=(fecha_procesada, nombre_cliente, total_precio_servicio)
                #Nota:
                print(f"{guiones(15)}Nota guardada correctamente{guiones(15)}")
                print(f"Información guardada de la nota: {nueva_nota}\n")
                print(tabulate([(nueva_nota, nota_final[nueva_nota][0].strftime("%d/%m/%Y"), nota_final[nueva_nota][1], nota_final[nueva_nota][2])],
                               headers=['Folio', 'Fecha', 'Cliente', 'Monto a Pagar'], tablefmt='pretty'))
                #Detalles de la nota:
                print(f"\nDetalles de la nota:\n{tabulate(lista_total_productos_con_precios, headers = 'firstrow', tablefmt = 'pretty')}")
                input(f"\n\nDe clic en Enter para continuar.")
                limpiar_consola()
                break

    #Consulta y reportes:
    elif menu == 2:
        limpiar_consola()
        menuActual(menu, lista_menu[menu][1])

        print("\n1. Consulta por periodo.\n2.Consulta por folio.")
        while True:
            try:
                opcion = int(input('Opción: '))
                if opcion >= 1 and opcion <= 2:
                    break
                else:
                    print("\nIngrese una opción válida, 1 o 2.")
                    continue
            except ValueError:
                print("\nIngrese un número válido.")
                continue

        #Consulta por periodo:
        if opcion == 1:
            print(f"\n\n{guiones(10)}Consulta por periodo{guiones(10)}".upper())

            while True:
                fecha_texto1 = input("Ingresa la fecha inicial en el formato (dd/mm/aaaa): ")
                fecha_texto2 = input("Ingresa la fecha final en el formato (dd/mm/aaaa): ")
                fecha_texto1 = fecha_texto1.strip()
                fecha_texto2 = fecha_texto2.strip()

                try:
                    fecha_inicial = dt.datetime.strptime(fecha_texto1, "%d/%m/%Y").date()
                    fecha_fin = dt.datetime.strptime(fecha_texto2, "%d/%m/%Y").date()
                    if fecha_inicial > fecha_actual:
                        print("\nLa fecha inicial no puede ser mayor que la fecha actual. Ingrese fechas válidas.")
                        continue
                    elif fecha_inicial > fecha_fin:
                        print("\nLa fecha inicial no puede ser mayor que la fecha final. Ingrese fechas válidas.")
                        continue
                    else:
                        break
                except ValueError:
                    print("\nIngrese fechas válidas en formato dd/mm/aaaa.")
                    continue     
            
            periodo=fecha_inicial.year-fecha_fin.year
            impresion_fecha_inicial = fecha_inicial.strftime("%d/%m/%Y")
            impresion_fecha_fin = fecha_fin.strftime("%d/%m/%Y")
            guiones_separadores()
            print(f"Reporte a consultar entre: {impresion_fecha_inicial} y {impresion_fecha_fin}")
            
            #Buscar notas:
            notas_periodo = []
            for folio, nota in nota_final.items():
                fecha_nota = nota[0]
                if fecha_inicial <= fecha_nota <= fecha_fin:
                    notas_periodo.append((folio, nota))

            #Imprimir notas:
            if notas_periodo:
                print("\nNotas en el período seleccionado:")
                titulos_notas = ["Folio", "Fecha", "Cliente", "Monto a pagar"]
                datos = [(folio, nota[0].strftime("%d/%m/%Y"), nota[1], nota[2]) for folio, nota in notas_periodo]
                print(tabulate(datos, headers=titulos_notas, tablefmt='pretty'))
            else:
                print("No hay notas emitidas para el período especificado")

        #Consulta por folio:
        else:
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
        input(f"\n\nDe clic en Enter para continuar.")
        limpiar_consola()
    
    #Cancelar una nota:
    elif menu == 3:
        limpiar_consola()
        menuActual(menu, lista_menu[menu][1])

        #Solicitar nota:
        print("Ingrese el folio de la nota a cancelar.")
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
            print(f"Folio: {folio_eliminar}")
            print(f"Fecha: {nota[0].strftime('%d/%m/%Y')}")
            print(f"Cliente: {nota[1]}")
            print(f"Monto a pagar: {nota[2]}")
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
                print(f"La nota con el folio {folio_eliminar} ha sido cancelada correctamente.")
            else:
                print("Entendido. La nota no ha sido cancelada.")
        else:
            print(f"El folio {folio_eliminar} que ingresó no se encuentra en el sistema o ya ha sido cancelado.")
        input("\nPresione Enter para continuar.")
        limpiar_consola()
        continue

    #Recuperar una nota
    elif menu == 4:
        limpiar_consola()
        menuActual(menu, lista_menu[menu][1])

        if notas_canceladas:
            print("Notas canceladas:")
            print(tabulate(notas_canceladas, headers=["Folio", "Detalles"], tablefmt='pretty'))
            
            #Solicitar el folio:
            print("Ingrese el folio de la nota que desea recuperar o 0 para salir: ")
            while True:
                try:
                    folio_recuperar = int(input("Folio: "))
                    if folio_recuperar == 0:
                        break
                    elif any(folio == folio_recuperar for folio, _ in notas_canceladas):
                        #Buscar en las notas canceladas
                        nota = next((nota for folio, nota in notas_canceladas if folio == folio_recuperar), None)

                        #Mostrar nota antes de recuperar:
                        print("Los elementos de la nota son:")
                        print(f"Folio: {folio_recuperar}")
                        print(f"Fecha: {nota[0].strftime('%d/%m/%Y')}")
                        print(f"Cliente: {nota[1]}")
                        print(f"Monto a pagar: {nota[2]}")
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
                            print(f"La nota con el folio {folio_recuperar} ha sido recuperada correctamente.")
                            break
                        else:
                            print("Entendido. La nota no ha sido recuperada.")
                            break
                    else:
                        print(f"El folio {folio_recuperar} que ingresó no es válido o ya ha sido recuperado.")
                        break
                except ValueError:
                    print("\nIngrese un número válido para el folio.")
        else:
            guiones_separadores()
            print("No hay notas canceladas para recuperar.")  
        input("\nPresione Enter para continuar.")
        limpiar_consola()
        continue

    #Salir:
    else:
        print('¿Está seguro que desea salir? (Sí/No)')
        salir = input("Respuesta: ")
        salir = respuesta_SI_NO(salir)

        while True:
            if salir == 'SI' or salir == 'NO':
                break
            else:
                print('\nIngrese una respuesta válida (Sí/No).')

        if salir == 'SI':
            print("Gracias por usar nuestro sistema, hasta la próxima.")
            break
        else:
            limpiar_consola()
            continue
