import pygame as pg
import sys
import modules.forms.base_form as base_form
import modules.forms.form_stage as form_stage
import modules.stage as stage_juego
import modules.particip_juego as particip_juego

from utn_fra.pygame_widgets import (
    Label, Button
)
import modules.variables as var

def create_form_wish(dict_form_data: dict) -> dict:
    form = base_form.create_base_form(dict_form_data)

    form['jugador'] = dict_form_data.get('jugador')

    form['wish_type'] = ''

    form['lbl_titulo'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=100,
        text='Seccion Bonus', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=45, color=pg.Color('blue')
    )

    form['lbl_subtitulo'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=150,
        text='Selecciona el deseo o huye', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=45, color=pg.Color('blue')
    )

    form['btn_wish'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2 - 200, y=200,
        text='', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=init_wish, on_click_param=form
    )

    form['btn_cancel'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2 + 200, y=200,
        text='CANCEL', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=click_resume, on_click_param='form_stage'
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitulo'),
        form.get('btn_wish'),
        form.get('btn_cancel')
    ]

    var.dict_forms_status[form.get('name')] = form

    return form

def update_wish_type(dict_form_data: dict, wish_type: str):
    dict_form_data['wish_type'] = wish_type
    dict_form_data.get('widgets_list')[2].update_text(text=dict_form_data.get('wish_type'), color=pg.Color('red'))

def click_resume(form_name: str):
    base_form.cambiar_pantalla(form_name)

def init_wish(form_dict_data: dict):
    wish_type = form_dict_data.get('wish_type')
    jugador = form_dict_data.get('jugador')
    
    stage_form = var.dict_forms_status.get('form_stage')
    stage = stage_form.get('stage')

    if wish_type == 'HEAL':
        wish = 'heal'
    else:
        wish = 'jackpot'
    
    stage_juego.modificar_estado_bonus(stage, wish)

    if wish_type == 'SCORE X3':
        anterior_score = particip_juego.get_score_participante(jugador)
        nuevo_score = anterior_score * 3
        print(f'Anterior SCORE: {anterior_score} | Actual SCORE: {nuevo_score}')
        particip_juego.set_score_participante(
           jugador , nuevo_score
        )
    else: # HEAL
        hp_inicial = particip_juego.get_hp_inicial_participante(jugador)
        hp_actual = particip_juego.get_hp_participante(jugador)
        hp_perdida = hp_inicial - hp_actual

        hp_bonus = int(hp_perdida * 0.75)
        nuevo_hp = hp_actual + hp_bonus

        print(f'Anterior HP: {hp_actual} | Actual HP: {nuevo_hp}')
        particip_juego.set_hp_participante(jugador, nuevo_hp)
    
    click_resume('form_stage')

def update(form_dict_data: dict):
    base_form.update(form_dict_data)

def draw(form_dict_data: dict):
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)