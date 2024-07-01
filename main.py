import inicio

from compra import main_compra
from purchase import Purchase
from match import Match
import autenticar
from statistics_modulo import estadisticas_gral

from restaurantes import start_restaurante

def main(): 

    lista_equipos = inicio.setting_equipos_all()
    lista_estadios = inicio.setting_stadiums_all()
    lista_partidos = inicio.setting_matches_all(lista_equipos, lista_estadios)
    lista_purchases = [] 

    given_purchase_ids = []
    boletos_validados = [] 

    print("\t\t\t\t EUROCOPA 2024")
    print("\t\t\t M A D E by V I C T O R  A R T I S")

    while True: 
       
        print("""
        Menú: 
        1.- Comprar boleto. 
        2.- Autentificación de Boletos. 
        3.- Restaurantes. 
        4.- Estadísticas. 
        5.- Imprimir todo y guardar.
        6.- Salir
        """)

        while True:
            try: 
                accion = int(input("\nIngrese el número de su selección:    "))

                if accion not in range(1, 7):
                    raise Exception

                break

            except: 
                print("\nOpción Inválida.\n")

        
        if accion == 1: 

            main_compra(lista_estadios, lista_partidos, lista_purchases, given_purchase_ids)

            pass

        elif accion == 2: 

            receipt_id = autenticar.get_receipt_id()

            validado = autenticar.validacion(lista_purchases, receipt_id, boletos_validados)

            if validado: 

                print("\n\tAUTENTIFICACIÓN EXITOSA\n")
                for p in lista_purchases:
                    if receipt_id == Purchase.get_code(p):
                        recibo = p

                partido = Purchase.get_match(recibo)

                boletos_validados.append(receipt_id)

                Match.new_asistente(partido) 
            
            else: 
                print("\n\n El boleto no pudo ser validado por el sistema. Es falso.\n\n")

            pass
        
        elif accion == 3:
            start_restaurante(lista_purchases)
  
        elif accion == 4: 
            estadisticas_gral(lista_partidos, lista_purchases)

        elif accion == 5: 
            guardar = ""
            for purchase in lista_purchases:
                str_compra = Purchase.get_string_all(purchase)
                guardar += str_compra + "\n"
                print("------------------------") 
                Purchase.print_receipt(purchase)
                print("------------------------") 

          
            with open("COMPRAS.txt", "a") as a:
                    a.write("CLIENTES:\n")
                    a.write(guardar)
                    a.write("")
            break

        else: 
            print("\nCERRANDO")
            break
            

    
main()