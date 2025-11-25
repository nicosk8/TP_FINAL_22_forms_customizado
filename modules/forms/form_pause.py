import pygame as pg
import sys
import modules.forms.base_form as base_form
import modules.forms.form_stage as form_stage
from utn_fra.pygame_widgets import (
    Label, Button
)
import modules.variables as var
import modules.sonido as sonido

def create_form_pause(dict_form_data: dict) -> dict:
    form = base_form.create_base_form(dict_form_data)
    form['last_volume'] = None
    form['lbl_titulo'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=100,
        text=var.TITULO_JUEGO, screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=45, color=pg.Color('blue')
    )

    form['lbl_subtitulo'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=160,
        text='PAUSE', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=30, color=pg.Color('blue')
    )

    form['btn_resume'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=210,
        text='RESUME', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=cambiar_pantalla, on_click_param={'form': form, 'form_name': 'form_stage'}
    )

    form['btn_restart'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=270,
        text='RESTART STAGE', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=restart_stage, on_click_param={'form': form, 'form_name': 'form_stage'}
    )

    form['btn_back'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=330,
        text='BACK TO MENU', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=base_form.cambiar_pantalla, on_click_param='form_menu'
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitulo'),
        form.get('btn_resume'),
        form.get('btn_restart'),
        form.get('btn_back')
    ]

    var.dict_forms_status[form.get('name')] = form

    return form

def cambiar_pantalla(params: dict):
    last_vol = params.get('form').get('last_volume')
    base_form.cambiar_pantalla(params.get('form_name'), change_music=False)
    set_last_vol(last_vol)

def restart_stage(params: dict):
    stage_form = var.dict_forms_status.get(params.get('form_name'))
    # base_form.cambiar_pantalla(params.get('form_name'))
    cambiar_pantalla(params)
    form_stage.iniciar_nueva_partida(stage_form)


def set_last_vol(vol: int):
    sonido.set_volume(vol)

def save_last_vol(form_dict_data: dict):
    form_dict_data['last_volume'] = sonido.get_actual_volume()
    set_last_vol(10)

def draw(form_dict_data: dict):
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)

def update(form_dict_data: dict):
    base_form.update(form_dict_data)