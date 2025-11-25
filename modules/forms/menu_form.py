import pygame as pg
import sys
import modules.forms.base_form as base_form
import modules.forms.form_stage as form_stage
from utn_fra.pygame_widgets import (
    Label, Button
)
import modules.variables as var

def create_form_menu(dict_form_data: dict) -> dict:
    form = base_form.create_base_form(dict_form_data)

    form['lbl_titulo'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=100,
        text='Menu principal', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=45, color=pg.Color('blue')
    )

    form['btn_play'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=150,
        text='JUGAR', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=iniciar_stage, on_click_param='form_stage'
    )

    form['btn_ranking'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=210,
        text='RANKING', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=base_form.cambiar_pantalla, on_click_param='form_ranking'
    )

    form['btn_options'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=280,
        text='OPCIONES', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=base_form.cambiar_pantalla, on_click_param='form_options'
    )

    form['btn_exit'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=370,
        text='Salir', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=salir_juego, on_click_param=None
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('btn_play'),
        form.get('btn_ranking'),
        form.get('btn_options'),
        form.get('btn_exit')
    ]

    var.dict_forms_status[form.get('name')] = form

    return form

def iniciar_stage(form_name: str):
    base_form.cambiar_pantalla(form_name)
    stage_form = var.dict_forms_status.get(form_name)
    form_stage.iniciar_nueva_partida(stage_form)

def salir_juego(_):
    print('Saliendo del juego desde el boton')
    pg.quit()
    sys.exit()

def draw(dict_form_data: dict):
    base_form.draw(dict_form_data)
    base_form.draw_widgets(dict_form_data)


def events_handler():
    events = pg.event.get()

    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = event.pos
            print(f'Coordenada mouse: X={x} | Y={y}')
        if event.type == pg.QUIT:
            salir_juego()
        # if event.type == pg.KEYDOWN:
        #     if event.key == pg.K_ESCAPE:
        #         base_form.set_active('form_pause')


def update(dict_form_data: dict):
    events_handler()
    base_form.update(dict_form_data)
    if not dict_form_data.get('music_config').get('music_init'):
        base_form.music_on(dict_form_data)
        dict_form_data['music_config']['music_init'] = True
