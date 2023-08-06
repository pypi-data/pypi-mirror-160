def lozasMacizas(num):
    if num == 1:
        longitud_libre_apoyo = float(input("Ingrese longitud LIBRE APOYO\n"))
        valor = longitud_libre_apoyo/20
        
    elif num == 2:
        longitud_extremo_continuo = float(input("Ingrese valor del EXTREMO CONTINUO\n"))
        valor = longitud_extremo_continuo/24

    elif num == 3:
        long_extremos_continuo = float(input("Ingrese valor del AMBOS EXTREMOS CONTINUOS\n"))
        valor = long_extremos_continuo/28

    elif num == 4:
        longitud_en_voladizo = float(input("Ingrese valor de EN VOLADIZO\n"))
        valor = longitud_en_voladizo/10

    print(f"El valor es: {valor:.2f}")
    return valor
def lozasNervadas(num):
    if num == 1:
        longitud_libre_apoyo = float(input("Ingrese valor del LIBRE APOYO\n"))
        valor = longitud_libre_apoyo/16

    elif num == 2:
        longitud_extremo_continuo = float(input("Ingrese valor del EXTREMO CONTINUO\n"))
        valor = longitud_extremo_continuo/18.5

    elif num == 3:
        long_extremos_continuo = float(input("Ingrese valor del AMBOS EXTREMOS CONTINUOS\n"))
        valor = long_extremos_continuo/21

    elif num == 4:
        longitud_en_voladizo = float(input("Ingrese valor de EN VOLADIZO\n"))
        valor = longitud_en_voladizo/8

    print(f"El valor es: {valor:.2f}")
    return valor