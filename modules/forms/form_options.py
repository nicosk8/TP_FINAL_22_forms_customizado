import pygame as pg
import sys
import modules.forms.base_form as base_form
from utn_fra.pygame_widgets import (
    Label, Button
)
import modules.variables as var
import modules.sonido as sonido

def create_form_options(dict_form_data: dict) -> dict:
    form = base_form.create_base_form(dict_form_data)
    
    form['lbl_titulo'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=100,
        text='OPTIONS', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=45, color=pg.Color('blue')
    )

    form['btn_music_on'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=200,
        text='MUSIC ON', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=activar_musica, on_click_param=form
    )
    
    form['btn_music_off'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=260,
        text='MUSIC OFF', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=desactivar_musica, on_click_param=form
    )

    form['btn_vol_down'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2 - 150, y=320,
        text='<', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=modificar_volumen, on_click_param=(-10)
    )

    form['btn_vol_up'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2 + 150, y=320,
        text='>', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=modificar_volumen, on_click_param=10
    )

    form['lbl_vol'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=320,
        text=f'{sonido.get_actual_volume()}', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=45, color=pg.Color('red')
    )

    form['btn_volver'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=500,
        text='VOLVER', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=cambiar_pantalla, on_click_param='form_menu'
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('btn_music_on'),
        form.get('btn_music_off'),
        form.get('btn_vol_up'),
        form.get('btn_vol_down'),
        form.get('lbl_vol'),
        form.get('btn_volver')
    ]

    var.dict_forms_status[form.get('name')] = form

    return form

def modificar_volumen(volumen: int):
    vol_actual = sonido.get_actual_volume()
    if vol_actual > 0 and volumen < 0 or\
        vol_actual < 100 and volumen > 0:
        vol_actual += volumen
        sonido.set_volume(vol_actual)

def activar_musica(form_dict_data: dict):
    form_dict_data['music_config']['music_on'] = True
    base_form.music_on(form_dict_data)

def desactivar_musica(form_dict_data: dict):
    form_dict_data['music_config']['music_on'] = False
    # base_form.music_off(form_dict_data)
    print("Musica Activa: {form_dict_data['music_config']['music_on']}")
    sonido.stop_music()

def cambiar_pantalla(form_name: str):
    base_form.set_active(form_name)

def draw(form_dict_data: dict):
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)

def update(form_dict_data: dict):
    lbl_vol: Label = form_dict_data.get('widgets_list')[5]
    lbl_vol.update_text(text=f'{sonido.get_actual_volume()}', color=pg.Color('red'))
    base_form.update(form_dict_data)