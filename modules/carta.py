import modules.auxiliar as aux
import pygame as pg
"""
"id": "senkai-yami-8",
"atk": 73,
"def": 40,
"hp": 92,
"ruta_frente": "assets/img/deck_battle/senkai_yami/id_senkai-yami-8_atk_73_def_40_hp_92.png",
"ruta_reverso": "assets/img/deck_battle/senkai_yami/reverse.png"
"""
def inicializar_carta(dict_card: dict, coords: list[int]) -> dict:
    card = dict_card
    card['visible'] = False
    card['coordenadas'] = coords

    card['imagen'] = None
    card['rect'] = None

    return card

def esta_visible(dict_card: dict) -> bool:
    return dict_card.get('visible')

def cambiar_visibilidad(dict_card: dict):
    dict_card['visible'] = not dict_card.get('visible')

def get_hp_carta(dict_card: dict) -> int:
    return dict_card.get('hp')

def get_def_carta(dict_card: dict) -> int:
    return dict_card.get('def')

def get_atk_carta(dict_card: dict) -> int:
    return dict_card.get('atk')

def asignar_coordenadas_carta(dict_card: dict, coordenadas: tuple[int]):
    dict_card['coordenadas'] = coordenadas

def draw_carta(dict_card: dict, screen: pg.Surface):
    if dict_card.get('visible'):
        dict_card['imagen'] = aux.redimensionar_imagen(dict_card.get('ruta_frente'), 40)
    else:
        dict_card['imagen'] = aux.redimensionar_imagen(dict_card.get('ruta_reverso'), 40)
    
    dict_card['rect'] = dict_card.get('imagen').get_rect()
    dict_card['rect'].topleft = dict_card.get('coordenadas')

    screen.blit(dict_card.get('imagen'), dict_card.get('rect'))