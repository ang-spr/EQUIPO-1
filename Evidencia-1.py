import datetime as dt
import random

nota_final = {}
tupla_servicio = {1:(600,'Cambio de nueomatico'), 2:(900,'Ajuste de vujias'),
        3:(850,'Cambio de aceite'), 4:(4500,'Reparacion de aceite'), 5:(3000,'Trasmision')}

fecha_actual=dt.date.today()

while True:
    print('----TALLER MECANICO DON HAMBLETON---')
    print('Buen dia, seleccione la opcion que desee realizar: \n1-Registrar nota \n2-Consulta y reportes')
    print('3-Cancelar una nota \n4-Recuperar una nota \n5-Salir')
    menu = int(input('Opcion: '))
    if menu == 1:
        folio = random.randint(0,9999)
        while folio in nota_final:
            folio = random.randint(0,9999)
            break
        print(f'Folio: {folio}')
        nombre_cliente = input('Ingrese el nombre del cliente: \n')
        while True:
            fecha_registro=input("Ingresar la fecha del sistema (dd/mm/aaaa): ")
            fecha_procesada = dt.datetime.strptime(fecha_registro, "%d/%m/%Y").date()
            total = 0
            if fecha_procesada < fecha_actual:       
                print("La fecha es incorrecta. La fecha no debe ser posterior a la actual")  
                continue
            else: 
                break
        
        while True:
            print('Los servicios disponibles son los siguientes: ')
            print('1-Cambio de neumaticos: $600 \n2-Ajuste de vujias: $900 \n3-Cambio de aceite: $850')
            print('4-Reparacion de motor: $4500 \n5-Trasmision: $3000')
            servicio = (input('Servicio: '))
 
            costo_servicio = float(input("Ingrese el costo del servicio: "))
            if costo_servicio <= 0:
                print("El costo debe ser mayor que cero.")
                continue

            otro_servicio = input('Desea otro servicio: (si/no) \n')
            total += costo_servicio
            if otro_servicio == 'si':
                continue
            elif otro_servicio == 'no':
                monto_pagar = print(f'El precio a pagar: ${total}')
                break
