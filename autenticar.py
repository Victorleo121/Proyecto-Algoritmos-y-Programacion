from purchase import Purchase

def get_receipt_id():

    while True: 
        try: 
            receipt_id = int(input("\n\nIngrese el código único de su factura:   "))
            break
        
        except: 
                print("Ingrese un ID válido")
    
    return receipt_id


def validacion(lista_purchases, receipt_id, boletos_validados):


    codes = []
    for p in lista_purchases: 
        codes.append(Purchase.get_code(p))

    if  receipt_id not in codes: 
        return False
    
    if receipt_id not in boletos_validados: 
        return True
    else: 
        return False