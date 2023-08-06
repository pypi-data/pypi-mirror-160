from math import sqrt
#from LosaUnideireccional.determinacionMomentos_Ultimos import momentoUltimo



fy = 42000
fc = 210
phi = 0.9
b = 40
r = 0.03
d = 22
beta1 = 0.85 
nervios = 4

def armaduraNegativa (momentoUltimoNeg):
    #seleccion de diametro de acero
    As1n = (((beta1*fc*b*d)/fy)*(1 - (sqrt(1-((2*momentoUltimoNeg)/(beta1*phi*fc*b*(d**2))))))*10)/4
    
    print(f'Area de una barra = {As1n}')

    print(f'Area total de acero = {As1n*4}')
  

    if As1n<=0.503:
        varilla = 8
    elif As1n>0.503 and As1n<=0.786:
        varilla = 10
    elif As1n>0.786 and As1n<=1.131:
        varilla = 12
    elif As1n>1.131 and As1n<=1.539:
        varilla = 14
    elif As1n>1.539 and As1n<=2.011:
        varilla = 16
    elif As1n>2.011 and As1n<=2.545:
        varilla = 18
    elif As1n>2.545 and As1n<=3.142:
        varilla = 20
    elif As1n>3.142 and As1n<=3.801:
        varilla = 22
    elif As1n>3.801 and As1n<=4.909:
        varilla = 25
    elif As1n>4.909 and As1n<=6.158:
        varilla = 28
    elif As1n>6.158 and As1n<=8.043:
        varilla = 32
    else:
        print("armadura Negativa Incorrecta")

    return varilla

