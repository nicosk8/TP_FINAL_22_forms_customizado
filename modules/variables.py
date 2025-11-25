import pygame as pg

########## Configs Juego ##########
DIMENSION_PANTALLA = (800, 600)
TITULO_JUEGO_CAPTION = 'DBZ Playing Cards - PROG I - TP FINAL - Heck, Nicole Denise'
TITULO_JUEGO = 'DBZ Playing cards'
FPS = 30
dict_forms_status = {}
STAGE_TIMER = 500
JSON_CONFIGS = 'configs.json'
JSON_INFO_CARDS = 'info_cartas.json'

########## Configs Player ##########
CANTIDAD_VIDAS = 3

########## Configs Audio ##########
VOLUMEN_INICIAL = 10

########## Fuentes ##########
FONT_ALAGARD = 'assets/fonts/alagard.ttf'

########## Fondos de formularios ##########
FONDO_MENU = 'assets/img/background/fondo_2.png'
FONDO_RANKING = 'assets/img/background/fondo_3.png'
FONDO_OPTIONS = 'assets/img/background/fondo_6.png'
FONDO_PAUSE = 'assets/img/background/fondo_8.png'
FONDO_STAGE = 'assets/img/background/fondo_5.png'
FONDO_NAME = 'assets/img/background/fondo_7.png'
FONDO_WISH = 'assets/img/background/form_wish.jpg'

########## Archivos ##########
RANKING_CSV = 'puntajes.csv'

########## Colores ##########
colores = {
    "amarillo": pg.Color('yellow'),
    "azul": pg.Color('blue'),
    "blanco": pg.Color('white'),
    "cian": pg.Color('cyan'),
    "naranja": pg.Color('orange'),
    "negro": pg.Color('black'),
    "rojo": pg.Color('red'),
    "rosa": pg.Color('pink'),
    "verde": pg.Color('green')
}
########## Mouse Pointer ##########
MOUSE_POINTER = 'assets/img/cursor/voldemort_cursor.png'

########## RUTAS MUSICA ##########
MUSICA_RANKING = 'assets/sound/level_2.mp3'
MUSICA_MENU = 'assets/sound/music.ogg'
MUSICA_OPTIONS = 'assets/sound/level_3.mp3'
MUSICA_PAUSE = 'assets/sound/level_1.mp3'
MUSICA_STAGE = 'assets/sound/music.ogg'