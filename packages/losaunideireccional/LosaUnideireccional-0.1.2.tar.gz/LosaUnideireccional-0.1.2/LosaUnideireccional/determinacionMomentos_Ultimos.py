from LosaUnideireccional.armaduralongitudinalnegativa import armaduraNegativa

x = 0.15
def momentoUltimo(longitudTansLoza, cargaUltimaDisenio):
    momentoUltimoNegativo = ((cargaUltimaDisenio * (longitudTansLoza**2))/8) - (5/8*(cargaUltimaDisenio * longitudTansLoza)*x) + (cargaUltimaDisenio*((x**2)/2))
    momentoUltimoNegM = round(momentoUltimoNegativo) * 100

    print(f"Mu(-)= {momentoUltimoNegativo:.0f} m\nMu(-)= {momentoUltimoNegM:.0f} cm")

    momentoUltimoPositivo = (((9/128)*cargaUltimaDisenio) * (longitudTansLoza**2))
    momentoUltimoPosM = round(momentoUltimoPositivo) * 100
    print(f"Mu(+)= {momentoUltimoPositivo:.0f} m\nMu(+)= {momentoUltimoPosM:.0f} cm")

    print("Armadura Longitudinal Negativa: ", armaduraNegativa(float(momentoUltimoNegM)))

    return momentoUltimoNegM 