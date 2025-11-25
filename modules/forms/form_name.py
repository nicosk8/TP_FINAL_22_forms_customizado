import pygame as pg
import modules.forms.base_form as base_form
import modules.forms.form_stage as form_stage
import modules.particip_juego as particip_juego
import modules.auxiliar as aux

from utn_fra.pygame_widgets import (
    Label, Button, TextBox
)
import modules.variables as var

def create_form_name(dict_form_data: dict) -> dict:
    form = base_form.create_base_form(dict_form_data)
    form['jugador'] = dict_form_data.get('jugador')
    form['info_submitida'] = False

    form['lbl_titulo'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=100,
        text='Victoria!', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=45, color=pg.Color('white')
    )

    form['lbl_subtitulo'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=150,
        text='Escriba su nombre', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=45, color=pg.Color('white')
    )

    form['lbl_score'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=210,
        text=f'{particip_juego.get_score_participante(form.get('jugador'))}', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=45, color=pg.Color('white')
    )

    form['lbl_nombre_texto'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=270,
        text='', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=45, color=pg.Color('cyan')
    )

    form['text_box'] = TextBox(
        x=var.DIMENSION_PANTALLA[0] // 2, y=280,
        text=f'_________________', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=25, color=pg.Color('white')
    )

    form['btn_submit'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=370,
        text='CONFIRMAR NOMBRE', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=submit_name, on_click_param=form
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitulo'),
        form.get('lbl_score'),
        form.get('lbl_nombre_texto'),
        form.get('btn_submit')
    ]

    var.dict_forms_status[form.get('name')] = form

    return form

def update_texto_victoria(form_dict_data: dict, win_status: bool):
    if win_status:
        mensaje = 'Victoria!'
    else:
        mensaje = 'Derrota!'
    
    form_dict_data.get('widgets_list')[0].update_text(text=mensaje, color=pg.Color('white'))

def clear_text(form_data: dict):
    form_data['text_box'].writing = ''

def submit_name(form_data: dict):

    nombre_jugador = form_data.get('lbl_nombre_texto').text
    particip_juego.set_nombre_participante(form_data.get('jugador'), nombre_jugador)
    
    nombre_jugador_seteado = particip_juego.get_nombre_participante(form_data.get('jugador'))
    puntaje_jugador = particip_juego.get_score_participante(form_data.get('jugador'))
    
    print(f'NOMBRE JUGADOR: {nombre_jugador_seteado} - {puntaje_jugador}')
    data_to_csv = particip_juego.info_to_csv(form_data.get('jugador'))
    aux.guardar_info_csv(data_to_csv)

    form_data['info_submitida'] = True

    base_form.set_active('form_ranking')

def update(form_dict_data: dict, event_list: list[pg.event.Event]):
    form_dict_data['score'] = particip_juego.get_score_participante(form_dict_data.get('jugador'))

    form_dict_data.get('widgets_list')[2].update_text(text=f'SCORE: {form_dict_data.get("score")}', color=pg.Color('cyan'))
    form_dict_data.get('widgets_list')[3].update_text(text=f'{form_dict_data.get('text_box').writing.upper()}', color=pg.Color('cyan'))

    form_dict_data.get('text_box').update(event_list)
    base_form.update(form_dict_data)

def draw(form_dict_data: dict):
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)
    form_dict_data.get('text_box').draw()