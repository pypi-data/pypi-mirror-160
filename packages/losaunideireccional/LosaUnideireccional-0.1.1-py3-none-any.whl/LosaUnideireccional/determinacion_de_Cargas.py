#Valores fijos de Losa Alivianada
from LosaUnideireccional.determinacionMomentos_Ultimos import momentoUltimo

espesor = 0.25
nervio = 0.10
loseta = 0.05
altoNervio = 0.20
baseViga = 0.30

pesoEspecificoHormigon = 2400
pesoEspecificoMortero = 2200
pesoEspecificoHorMor = 2000

alivianamiento =  15*12

def loseta_de_Compresion(longitudLoza):
    losetaCompresion = loseta * longitudLoza * pesoEspecificoHormigon
    pesoNerviosLongitud = 4 * nervio * altoNervio * pesoEspecificoHormigon
    pesoNerviosTansversales = nervio * altoNervio * longitudLoza * pesoEspecificoHormigon

    pesoPropio = losetaCompresion + pesoNerviosLongitud + pesoNerviosTansversales + alivianamiento

    #print(f"Peso propio = {pesoPropio:.0f}")
    #print("=================================")
    return pesoPropio


#Valores fijos de gradas
huella = 0.30
contrahuella = 0.18
hipotenusa = 0.35
areaGrada = 2.70
alturarrellenoProm = 0.09
Enlucido = 0.02
masillado = 0.02
totalEM = 0.04
espesorCamino = 0.02
valorPasamano = 50
valorNec = 500

def gradas(longitudLoza):
    
    pesoRellenoGradas = longitudLoza * 1 * alturarrellenoProm * pesoEspecificoHorMor
    enlusidoMasillado = longitudLoza * 1 * totalEM * pesoEspecificoMortero
    recubrimientoPiso = longitudLoza * 1 * espesorCamino * pesoEspecificoMortero
    pasamanos = valorPasamano

    cargaPermanente = pesoRellenoGradas + enlusidoMasillado + recubrimientoPiso + pasamanos + loseta_de_Compresion(longitudLoza)
    cargaViva = valorNec * longitudLoza 
    cargaUltimaDisenio = 1.4 * cargaPermanente + (1.7 * cargaViva)
    print(f"Carga Muerta= {cargaPermanente:.0f}\nCarga Viva= {cargaViva:.0f}\nCarga última de diseño= {cargaUltimaDisenio:.0f}")
    print("=================================")
    longitudTransLoza = float(input("Ingrese la longitud transversal: "))
    momentoUltimo(longitudTransLoza, cargaUltimaDisenio)
            
    return cargaUltimaDisenio