from modules.auxiliar import generar_bd_cartas, guardar_info_cartas

cartas = generar_bd_cartas("21_forms/assets/img/deck_battle")
guardar_info_cartas('21_forms/info_cartas.json', cartas)
print(cartas.get('cartas'))