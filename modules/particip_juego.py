import pygame as pg
import modules.carta as carta
import modules.variables as var
import modules.auxiliar as aux
from functools import reduce

def inicializar_participante(pantalla: pg.Surface, nombre: str = 'PC'):
    player = {}
    player['nombre'] = nombre
    player['hp_inicial'] = 1
    player['hp_actual'] = 1
    player['attack'] = 1
    player['defense'] = 1
    player['score'] = 0

    player['mazo_asignado'] = []
    player['cartas_mazo'] = []
    player['cartas_mazo_usadas'] = []

    player['screen'] = pantalla
    player['pos_deck_inicial'] = (0,0)
    player['pos_deck_jugado'] = (0,0)

    return player

def get_hp_participante(participante: dict) -> int:
    return participante.get('hp_actual')

def get_hp_inicial_participante(participante: dict) -> int:
    return participante.get('hp_inicial')

def get_attack_participante(participante: dict) -> int:
    return participante.get('attack')

def get_defense_participante(participante: dict) -> int:
    return participante.get('defense')

def get_nombre_participante(participante: dict) -> str:
    return participante.get('nombre')

def get_cartas_iniciales_participante(participante: dict) -> list[dict]:
    return participante.get('mazo_asignado')

def get_cartas_restantes_participante(participante: dict) -> list[dict]:
    return participante.get('cartas_mazo')

def get_cartas_jugadas_participante(participante: dict) -> list[dict]:
    return participante.get('cartas_mazo_usadas')

def get_coordenadas_mazo_inicial(participante: dict):
    return participante.get('pos_deck_inicial')

def get_coordenadas_mazo_jugada(participante: dict):
    return participante.get('pos_deck_jugado')

def get_carta_actual_participante(participante: dict):
    return participante.get('cartas_mazo_usadas')[-1]

def setear_stat_participante(participante: dict, stat: str, valor: int):
    participante[stat] = valor

def set_cartas_participante(participante: dict, lista_cartas: list[dict]):

    for carta_b in lista_cartas:
        coordenada = get_coordenadas_mazo_inicial(participante)
        carta_b['coordenadas'] = coordenada
    
    participante['mazo_asignado'] = lista_cartas
    participante['cartas_mazo'] = lista_cartas.copy()

def set_score_participante(participante: dict, score: int):
    participante['score'] = score

def get_score_participante(participante: dict) -> int:
    return participante.get('score')

def set_nombre_participante(participante: dict, nuevo_nombre: str):
    participante['nombre'] = nuevo_nombre

def set_hp_participante(participante: dict, hp_actual: int):
    participante['hp_actual'] = hp_actual

def add_score_participante(participante: dict, score: int):
    participante['score'] += score

def asignar_stats_iniciales_participante(participante: dict):
    participante['hp_inicial'] = aux.reducir(
        carta.get_hp_carta,
        participante.get('mazo_asignado')
    )

    participante['hp_actual'] = participante['hp_inicial']

    participante['attack'] = aux.reducir(
        carta.get_atk_carta,
        participante.get('mazo_asignado')
    )

    participante['defense'] = aux.reducir(
        carta.get_def_carta,
        participante.get('mazo_asignado')
    )

def chequear_valor_negativo(stat: int):
    if stat < 0:
        return 0
    return stat

def restar_stats_participante(participante: dict, carta_g: dict, is_critic: bool):

    """
    Comparar ataque carta con la defensa de la carta del jugador,
    la resta es la que vamos a restarle al jugador
    """
    damage_mul = 1
    if is_critic:
        damage_mul = 3

    carta_jugador = participante.get('cartas_mazo_usadas')[-1]
    damage = carta.get_atk_carta(carta_g) - carta.get_def_carta(carta_jugador)
    damage *= damage_mul

    participante['hp_actual'] = chequear_valor_negativo(participante.get('hp_actual') - damage)
    participante['attack'] -= carta.get_atk_carta(carta_jugador)
    participante['defense'] -= carta.get_def_carta(carta_jugador)

def jugar_carta(participante: dict):
    if participante.get('cartas_mazo'):
        print(f'El jugador {participante.get("nombre")} tiene {len(participante.get('cartas_mazo'))} cartas')
        carta_actual = participante.get('cartas_mazo').pop()
        carta.cambiar_visibilidad(carta_actual)
        carta.asignar_coordenadas_carta(carta_actual, get_coordenadas_mazo_jugada(participante))
        participante.get('cartas_mazo_usadas').append(carta_actual)
    else:
        print(f'El jugador {participante.get("nombre")} no tiene cartas')
        

def info_to_csv(participante: dict):
    return f'{get_nombre_participante(participante)},{participante.get('score')}\n'

def reiniciar_datos_participante(player: dict):
    set_nombre_participante(player, 'PLAYER')
    set_score_participante(player, 0)
    set_cartas_participante(player, list())
    player['cartas_mazo_usadas'].clear()
    setear_stat_participante(player, 'hp_inicial', 0)
    setear_stat_participante(player, 'hp_actual', 0)
    setear_stat_participante(player, 'ataque', 0)
    setear_stat_participante(player, 'defensa', 0)

def draw_participante(participante: dict, screen: pg.Surface):

    # Solo dibujamos la ultima de cada mazo
    # El mazo que aun no se dio vuelta y el mazo de cartas jugadas
    if participante.get('cartas_mazo'):
        # print(f'Se dibuja carta restante de {participante.get("nombre")}')
        carta.draw_carta(participante.get('cartas_mazo')[-1], screen)
    
    if participante.get('cartas_mazo_usadas'):
        # print(f'Se dibuja carta usada de {participante.get("nombre")}')
        carta.draw_carta(participante.get('cartas_mazo_usadas')[-1], screen)

