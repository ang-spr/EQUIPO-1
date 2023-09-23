#librerías:
import datetime as dt
import os
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

#Recolección de datos:
fecha_actual = dt.date.today()

#Juntar datos:
nota_final = {}

while True:
    #Menú principal:
    print('----TALLER MECÁNICO DON HAMBLETON----')
    print('Buen día, seleccione la opción que desee realizar:')
    print('\n1. Registrar nota.\n2. Consulta y reportes.\n3. Cancelar una nota.\n4. Recuperar una nota.\n5. Salir.')
    #VALIDAR QUE INGRESE UNA OPCIÓN VÁLIDA.
    menu = int(input('Opción: '))

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

      #RFC
        while True:
            print('Tipo de RFC: \n1-Física \n2-Moral ')
            while True:
                try:
                    tipo = int(input('Tipo: '))
                    if tipo >= 1 and tipo <= 2:
                        break
                    else:
                        print("\nIngrese una opción válida del 1 al 2.")
                        continue
                except ValueError:
                    print("\nIngrese un número válido.")
                    continue  
            guiones_separadores()
            while True:
                if tipo == 1:
                    rfc = input('RFC: ')
                    if rfc.strip() == '':
                        print('El dato no puede omitirse, intente de nuevo.')
                        continue
                    if not re.match(r'^[A-Z]{4}[0-9]{2}[0-9]{2}[0-9]{2}[A-Z0-9]{3}$', rfc):
                        print('El RFC no cumple con el formato esperado.\nNombre(4 iniciales) \nFecha de nacimiento(YYMMDD) \nHomoclave unica')
                        continue
                    break
                elif tipo == 2:
                    rfc = input('RFC: ')
                    if rfc.strip() == '':
                        print('El dato no puede omitirse, intente de nuevo.')
                        continue
                    if not re.match(r'^[A-Z]{3}[0-9]{2}[0-9]{2}[0-9]{2}[A-Z0-9]{3}$', rfc):
                        print('El RFC no cumple con el formato esperado.\nNombre(3 iniciales) \nFecha de nacimiento(YYMMDD) \nHomoclave unica')
                        continue
                    break
            break
        guiones_separadores()

        #Servicio(s) realizado(s):
        total_costo_servicio = 0
        while True:
            print('Los servicios disponibles son los siguientes: ')
            print('1. Cambio de neumáticos: $600\n2. Ajuste de vujias: $900\n3. Cambio de aceite: $850\n4. Reparación de motor: $4500\n5. Transmisión: $3000')
            servicio = int(input('Servicio: '))
            #VALIDAR QUE INGRESE UN NÚMERO VÁLIDO.

            costo_servicio = float(input("Ingrese el costo real del servicio: "))
            #VALIDAR QUE INGRESE UN COSTO VÁLIDO.

            #CAMBIAR LA VALICACIÓN DEL COSTO:
            if costo_servicio <= 0:
                print("El costo debe ser mayor que cero.")
                continue

            print("----------------------------------------\nServicio agregado correctamente.")
            otro_servicio = input('\tDesea ingresar otro servicio (Sí/No): ')

            #CONVERTIR RESPUESTA:
            #CONVERTIRLO A MAYÚSCULAS
            #QUITAR ESPACIOS VACÍOS AL PRINCIPIO Y FINAL DEL TEXTO.
            #QUITAR ACENTOS.

            #VALIDAR QUE INGRESE UNA RESPUESTA CORRECTA.

            if otro_servicio == 'SI':             
                #GUARDAR SERVICIO Y PRECIO ACTUAL A TUPLA QUE TENGA TODOS LOS SERVICIOS REALIZADOS.
                
                total_costo_servicio += costo_servicio
                limpiar_consola()
                continue
            
            elif otro_servicio == 'NO':
                monto_pagar = print(f'El precio a pagar es: ${total_costo_servicio}')

                #AQUÍ CREO QUE GUARDAREMOS DICCIONARIO.
                #IMPRIMIR FECHA SIN EL TIPO DE DATO QUE ES.
                nota_final[nueva_nota]=(nombre_cliente, fecha_procesada, servicio, monto_pagar)

                #FALTA ENCONTRAR MANERA PARA DAR ENTER Y SALIR.
                print(f"Nota guardada correctamente:\n{nota_final}\nDe clic en Enter para continuar.")
                #limpiar_consola()
                break

    #Consulta y reportes:
    elif menu == 2:
        print("\n1.Consulta por periodo.\n2.Consulta por folio ")
        op=int(input("Seleccione el número de la consulta que desea realizar: "))
        if op==1:
            print("*** Consulta por periodo ***")
            
            #import datatime
            fecha_texto1=input("Ingresa la fecha inicial en el formato 'dd/mm/aaaa': \n")
            fecha_texto2=input("Ingresa la fecha final en el formato 'dd/mm/aaaa': \n")
    
            fecha_inicial=datetime.datetime.strptime(fecha_texto1,"%d/%m/%Y").date()
            fecha_fin=datetime.datetime.strptime(fecha_texto2,"%d/%m/%Y").date()

            periodo=fecha_inicial.year-fecha_fin.year
            #print(f"Periodo a consultar: {periodo}")
            print(f"Reporte a consultar entre: {fecha_inicial} y {fecha_fin}")
            
            notas_periodo=[]
            for nueva_nota,nota in nota_final.items():
                fecha_nota=nota[1]
                if fecha_inicial <= fecha_nota <= fecha_fin:
                    notas_periodo.append((nota_final, nota))

            if notas_periodo:
                print("\nNotas en el período seleccionado:")
                print("{:<10} {:<12} {:<20} {:<15}".format("Folio", "Fecha", "Cliente", "Monto a pagar"))

                for nueva_nota, nota in notas_periodo:
                    print("{:<10} {:<12} {:<20} {:<15}".format(nueva_nota, nota[1], nota[0], nota[3]))
                    #otra posible solucion: print(f"Folio: {nueva_nota}, Fecha: {nota[1]}, Cliente: {nota[0]}, Monto a pagar: {nota[3]}")

            else:
                print("No hay notas emitidas para el período especificado")

        
        else:
            print("*** Consulta por folio ***")
            folio=int(input("Ingresa el folio del cual desea consultar información: "))
            if folio in nota_final: #o folio in nueva_nota,,,
                nota=nota_final[folio]
                print(f"Folio: {nueva_nota}, Fecha: {nota[1]}, Cliente: {nota[0]}, Monto a pagar: {nota[3]}")
    
            else:
                print(f"El folio {nueva_nota} no se encuentra en el sistema")    

        break
    
    #Cancelar una nota:
    elif menu == 3:
        folio_eliminar = int(input("Ingrese el folio de la nota a cancelar: "))

        #Datos de la nota cancelada
        if folio_eliminar in nota_final:
            nota = nota_final[folio_eliminar]
            print("Los elementos de la nota son:")
            print(f"Folio: {folio_eliminar}")
            print(f"Fecha: {nota[1]}")
            print(f"Cliente: {nota[0]}")
            print(f"Monto a pagar: {nota[3]}")

            print("¿Está seguro que desea cancelar la nota? (Sí/No): ")
            while True:
                respuesta = input('Respuesta: ')
                respuesta = respuesta_SI_NO(respuesta)
                if respuesta == 'SI' or respuesta == 'NO':
                    break
                else:
                    print('\n\tIngrese una respuesta válida (Sí/No).')

           if respuesta == "SI":
                #Eliminar la nota
                notas_canceladas.append((folio_eliminar, nota_final[folio_eliminar]))
                del nota_final[folio_eliminar]
                print(f"La nota con el folio {folio_eliminar} ha sido cancelada correctamente.")
            else:
                print("Entendido. La nota no ha sido cancelada.")

            elif respuesta == "NO":
              print ("Entendido. Puede continuar")
              break

        else:
            print(f"El folio {folio_eliminar} que ingresó no se encuentra en el sistema o ya ha sido cancelado.")
        input("\nPresione Enter para continuar.")
        continue

    #Recuperar una nota
    elif menu == 4:
        break

    #Salir:
    elif menu==5:
        print("Confirma (1) si deseas salir del sistema o (2) si deseas continuar en el sistema")
        salir=int(input("¿Desea salir del sistema? "))
        if salir==1:
            break 
        else:
            print("Saliste del sistema")
