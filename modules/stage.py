import pygame as pg
import modules.variables as var
import modules.auxiliar as aux
import random as rd
import modules.carta as carta
import modules.particip_juego as particip_juego

def inicializar_stage(jugador: dict, pantalla: pg.Surface, nro_stage: int):
    stage_data = {}
    stage_data['nro_stage'] = nro_stage
    stage_data['configs'] = {}
    stage_data['data_cargada'] = False

    stage_data['cartas_mazo_inicial_e'] = []
    stage_data['cartas_mazo_inicial_p'] = []
    stage_data['cartas_mazo_preparadas_e'] = []
    stage_data['cartas_mazo_preparadas_p'] = []
    
    stage_data['ruta_mazos'] = ''
    stage_data['screen'] = pantalla
    stage_data['jugador'] = jugador
    stage_data['coords_inicial_mazo_enemigo'] = (20,70)
    stage_data['coords_final_mazo_enemigo'] = (390,70)

    stage_data['coords_inicial_mazo_player'] = (20,360)
    stage_data['coords_final_mazo_player'] = (390,360)

    stage_data['heal_available'] = True
    stage_data['jackpot_available'] = True

    stage_data['enemigo'] = particip_juego.inicializar_participante(stage_data.get('screen'), nombre='Enemigo')
    
    particip_juego.setear_stat_participante(stage_data.get('enemigo'), 'pos_deck_inicial', stage_data.get('coords_inicial_mazo_enemigo'))
    particip_juego.setear_stat_participante(stage_data.get('enemigo'), 'pos_deck_jugado', stage_data.get('coords_final_mazo_enemigo'))
    
    particip_juego.setear_stat_participante(stage_data.get('jugador'), 'pos_deck_inicial', stage_data.get('coords_inicial_mazo_player'))
    particip_juego.setear_stat_participante(stage_data.get('jugador'), 'pos_deck_jugado', stage_data.get('coords_final_mazo_player'))
    
    
    stage_data['cantidad_cartas_jugadores'] = 0


    stage_data['juego_finalizado'] = False
    stage_data['puntaje_guardado'] = False
    stage_data['stage_timer'] = var.STAGE_TIMER
    stage_data['last_timer'] = pg.time.get_ticks()
    stage_data['ganador'] = None

    stage_data['data_cargada'] = False
    
    return stage_data

def modificar_estado_bonus(stage_data: dict, bonus: str):
    stage_data[f'{bonus}_available'] = False

def timer_update(stage_data: dict):
    if stage_data.get('stage_timer') > 0:
        tiempo_actual = pg.time.get_ticks() # 21:04:22 -> MS

        if tiempo_actual - stage_data.get('last_timer') > 1000:
            stage_data['stage_timer'] -= 1
            stage_data['last_timer'] = tiempo_actual

def obtener_tiempo(stage_data: dict):
    return stage_data.get('stage_timer')

def asignar_cartas_stage(stage_data: dict, participante: dict):
    cant_cartas = stage_data.get('cantidad_cartas_jugadores')
    if particip_juego.get_nombre_participante(participante) != 'Enemigo':
        rd.shuffle(stage_data.get('cartas_mazo_preparadas_p'))
        cartas_participante = stage_data.get('cartas_mazo_preparadas_p')[:cant_cartas]
    else:
        rd.shuffle(stage_data.get('cartas_mazo_preparadas_e'))
        cartas_participante = stage_data.get('cartas_mazo_preparadas_e')[:cant_cartas]

    # TODO ASIGNAR CARTAS AL PARTICIPANTE
    particip_juego.set_cartas_participante(participante, cartas_participante)


def generar_mazo(stage_data: dict):
    for carta_inicial_e, carta_inicial_p in zip(
        stage_data.get('cartas_mazo_inicial_e'),
        stage_data.get('cartas_mazo_inicial_p')
    ):
        carta_power_e = carta.inicializar_carta(carta_inicial_e, (0,0))
        carta_power_p = carta.inicializar_carta(carta_inicial_p, (0,0))
        stage_data.get('cartas_mazo_preparadas_e').append(carta_power_e)
        stage_data.get('cartas_mazo_preparadas_p').append(carta_power_p)

def barajar_mazos_stage(stage_data: dict):
    if not stage_data.get('stage_finalizado'):
        asignar_cartas_stage(stage_data, stage_data.get('jugador'))
        asignar_cartas_stage(stage_data, stage_data.get('enemigo'))

        particip_juego.asignar_stats_iniciales_participante(stage_data.get('jugador'))
        particip_juego.asignar_stats_iniciales_participante(stage_data.get('enemigo'))

        stage_data['data_cargada'] = True

def inicializar_data_stage(stage_data: dict):
    print('Estoy cargando los datos del stage')
    aux.cargar_configs_stage(stage_data) # leer la configuracion del juego desde un archivo
    aux.cargar_bd_cartas(stage_data)
    generar_mazo(stage_data)
    barajar_mazos_stage(stage_data)

def hay_jugadores_con_cartas(stage_data: dict) -> bool:
    jugador_con_cartas = particip_juego.get_cartas_restantes_participante(stage_data.get('jugador'))
    enemigo_con_cartas = particip_juego.get_cartas_restantes_participante(stage_data.get('enemigo'))
    return jugador_con_cartas or enemigo_con_cartas

def restart_stage(stage_data: dict, jugador: dict, pantalla: pg.Surface, nro_stage: int):
    stage_data = inicializar_stage(jugador, pantalla, nro_stage)
    particip_juego.reiniciar_datos_participante(jugador)
    inicializar_data_stage(stage_data)
    return stage_data

def jugar_mano_stage(stage_data: dict):
    particip_juego.jugar_carta(stage_data.get('jugador'))
    particip_juego.jugar_carta(stage_data.get('enemigo'))

def es_golpe_gritico() -> bool:
    critical = rd.choice([False, False, False, True])
    # critical = True if rd.randint(0, 1) == 0.5 else False
    return critical

def comparar_damage(stage_data: dict):
    ganador_mano = None
    jugador = stage_data.get('jugador')
    enemigo = stage_data.get('enemigo')
    critical = False
    carta_jugador = particip_juego.get_carta_actual_participante(jugador)
    carta_enemigo = particip_juego.get_carta_actual_participante(enemigo)

    if carta_enemigo and carta_jugador:
        critical = es_golpe_gritico()
        atk_jugador = carta.get_atk_carta(carta_jugador)
        atk_enemigo = carta.get_atk_carta(carta_enemigo)

        if atk_enemigo > atk_jugador:
            ganador_mano = 'PC'
            particip_juego.restar_stats_participante(jugador, carta_enemigo, critical)
        else:
            score = atk_jugador - carta.get_def_carta(carta_enemigo)
            ganador_mano = 'PLAYER'
            particip_juego.restar_stats_participante(enemigo, carta_jugador, critical)
            particip_juego.add_score_participante(jugador, score)
    
    print(f'Datos de la ronda actual:')
    print(f'{stage_data.get('jugador').get('nombre')} -> Carta -> HP: {carta.get_hp_carta(carta_jugador)} - ATK: {atk_jugador} - DEF: {carta.get_def_carta(carta_jugador)} - Critical: {critical} - Vida total jugador: {stage_data.get('jugador').get('hp_actual')}')
    print(f'{stage_data.get('enemigo').get('nombre')} -> Carta -> HP: {carta.get_hp_carta(carta_jugador)} - ATK: {atk_enemigo} - DEF: {carta.get_def_carta(carta_enemigo)} - Critical: {critical} - Vida total enemigo: {stage_data.get('enemigo').get('hp_actual')}')
    
    return critical, ganador_mano

def setear_ganador(stage_data: dict, participante: dict):
    stage_data['ganador'] = participante
    stage_data['juego_finalizado'] = True

def chequear_ganador(stage_data: dict):
    jugador = stage_data.get('jugador')
    enemigo = stage_data.get('enemigo')

    if (particip_juego.get_hp_participante(jugador) <= 0 or\
        (particip_juego.get_hp_participante(jugador) < particip_juego.get_hp_participante(enemigo)) and\
            (len(particip_juego.get_cartas_restantes_participante(enemigo)) == 0)):
        
        setear_ganador(stage_data, enemigo)

        puntaje_jug_actual = particip_juego.get_score_participante(jugador) // 2
        particip_juego.set_score_participante(jugador, puntaje_jug_actual)

    elif (particip_juego.get_hp_participante(enemigo) <= 0 or\
        (particip_juego.get_hp_participante(enemigo) < particip_juego.get_hp_participante(jugador)) and\
            (len(particip_juego.get_cartas_restantes_participante(jugador)) == 0)):
        
        setear_ganador(stage_data, jugador)

def esta_finalizado(stage_data: dict) -> bool:
    return stage_data.get('juego_finalizado')

def obtener_ganador(stage_data: dict) -> bool:
    return stage_data.get('ganador')

def jugar_mano(stage_data: dict):
#    if not stage_data.get('juego_finalizado'):
        jugar_mano_stage(stage_data)

        critical, ganador_mano = comparar_damage(stage_data)

        return critical, ganador_mano
#    return None

def draw_jugadores(stage_data: dict):
    particip_juego.draw_participante(stage_data.get('jugador'), stage_data.get('screen'))
    particip_juego.draw_participante(stage_data.get('enemigo'), stage_data.get('screen'))

def update(stage_data: dict):
    timer_update(stage_data)
    chequear_ganador(stage_data)