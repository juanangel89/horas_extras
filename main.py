from clases.turnos import Funciones
horas_totales=0
print('-'*20)
print('Bienvenido a su gestionador de turnos')
print('-'*20)
print('D-Turno Diurno')
print('N-Turno Nocturno')
print('X-Descasa o no trabaja')
print('-'*20)

dias=['lunes','martes','miercoles','jueves','viernes','sabado','domingo']
for dia in dias:
    turno=input(f'Digite el inicial del turno para el dia {dia}: ')
    conceptos,horas_totales=Funciones.calcular_turnos (dia,turno,horas_totales)
    print('-'*20)
# print(conceptos)
print('-'*95)

print(f"{'Turno':<20} | {'Día':<12} | {'Inicio':<7} | {'Fin':<7} | {'Concepto':<25} | {'Horas':>5}")
print('-'*95)

for concepto in conceptos:
    for con in concepto:
        turno = con['turno']
        dia = con['dia']
        horas_ini = f"{con['hora_ini']}:00"
        horas_fin = f"{con['hora_fin']}:00"
        # horario= f"{horas_ini}:00 - {horas_fin}:00 "
        concep = con['concepto']
        horas = con['horas_trabajadas']
        print(f"{turno:<20} | {dia:<12} | {horas_ini:<7} | {horas_fin:<7} | {concep:<25} | {horas:<5} ")


