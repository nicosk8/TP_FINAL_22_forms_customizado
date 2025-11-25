import pygame as pg
import sys
import modules.forms.base_form as base_form
import modules.forms.form_name as form_name
import modules.forms.form_wish as form_wish
import modules.stage as stage_juego
import modules.carta as carta_jugador
import modules.particip_juego as particip_juego

from utn_fra.pygame_widgets import (
    Label, Button
)
import modules.variables as var
import modules.forms.form_pause as form_pause

def crear_form_stage(dict_form_data: dict):
    form = base_form.create_base_form(dict_form_data)

    form['stage_restart'] = False
    form['time_finished'] = False
    form['actual_level'] = 1
    # form['stage_timer'] = var.STAGE_TIMER
    # form['last_timer'] = pg.time.get_ticks()

    form['bonus_shield_available'] = True
    form['bonus_heal_available'] = True
    form['bonus_shield_applied'] = False
    form['jugador'] = dict_form_data.get('jugador')

    # TODO
    form['stage'] = stage_juego.inicializar_stage(jugador=form.get('jugador'), pantalla=form.get('screen'), nro_stage=form.get('actual_level'))

    form['clock'] = pg.time.Clock()


    # ========== LABELS ==========
    form['lbl_timer'] = Label(
        x=50, y=15,
        text=f'{stage_juego.obtener_tiempo(form.get('stage'))}', screen=form.get('screen'),
        align='topleft', font_path=var.FONT_ALAGARD, font_size=45, color=var.colores.get('cian')
    )

    form['lbl_score'] = Label(
        x=450, y=15,
        text=f'Score: 0', screen=form.get('screen'),
        align='topleft', font_path=var.FONT_ALAGARD, font_size=45, color=var.colores.get('cian')
    )

    form['lbl_carta_e'] = Label(
        x=390, y=275,
        text=f'', screen=form.get('screen'),
        align='topleft', font_path=var.FONT_ALAGARD, font_size=20, color=var.colores.get('cian')
    )

    form['lbl_carta_p'] = Label(
        x=390, y=563,
        text=f'', screen=form.get('screen'),
        align='topleft', font_path=var.FONT_ALAGARD, font_size=20, color=var.colores.get('cian')
    )

    # Stats Enemigo

    form['lbl_enemigo_hp'] = Label(
        x=617, y=85,
        text=f'', screen=form.get('screen'),
        align='topleft', font_path=var.FONT_ALAGARD, font_size=25, color=var.colores.get('cian')
    )
    
    form['lbl_enemigo_atk'] = Label(
        x=617, y=120,
        text=f'', screen=form.get('screen'),
        align='topleft', font_path=var.FONT_ALAGARD, font_size=25, color=var.colores.get('cian')
    )
    
    form['lbl_enemigo_def'] = Label(
        x=617, y=155,
        text=f'', screen=form.get('screen'),
        align='topleft', font_path=var.FONT_ALAGARD, font_size=25, color=var.colores.get('cian')
    )

    # Stats Player

    form['lbl_jugador_hp'] = Label(
        x=617, y=365,
        text=f'', screen=form.get('screen'),
        align='topleft', font_path=var.FONT_ALAGARD, font_size=25, color=var.colores.get('cian')
    )
    
    form['lbl_jugador_atk'] = Label(
        x=617, y=395,
        text=f'', screen=form.get('screen'),
        align='topleft', font_path=var.FONT_ALAGARD, font_size=25, color=var.colores.get('cian')
    )
    
    form['lbl_jugador_def'] = Label(
        x=617, y=425,
        text=f'', screen=form.get('screen'),
        align='topleft', font_path=var.FONT_ALAGARD, font_size=25, color=var.colores.get('cian')
    )

    # ========== BUTTONS ==========

    form['btn_play'] = Button(
        x=616, y=250,
        text='JUGAR', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=20,
        on_click=jugar_mano, on_click_param=form,
        align='topleft'
    )

    form['btn_heal'] = Button(
        x=616, y=280,
        text='HEAL', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=20,
        on_click=call_wish_form, on_click_param={'form': form, 'wish': 'HEAL'},
        align='topleft'
    )

    form['btn_jackpot'] = Button(
        x=616, y=310,
        text='JACKPOT', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=20,
        on_click=call_wish_form, on_click_param={'form': form, 'wish': 'SCORE X3'},
        align='topleft'
    )

    # ========== WIDGETS LIST ==========
    form['widgets_list'] = [
        form.get('lbl_timer'),
        form.get('lbl_score'),
        form.get('lbl_carta_e'),
        form.get('lbl_carta_p'),
        form.get('lbl_enemigo_hp'),
        form.get('lbl_enemigo_atk'),
        form.get('lbl_enemigo_def'),
        form.get('lbl_jugador_hp'),
        form.get('lbl_jugador_atk'),
        form.get('lbl_jugador_def'),
        form.get('btn_play')
    ]

    form['widgets_list_bonus'] = [
        form.get('btn_heal'),
        form.get('btn_jackpot')
    ]

    var.dict_forms_status[form.get('name')] = form

    return form

def jugar_mano(form_dict_data: dict):
    
    stage = form_dict_data.get('stage')
    
    if ((not stage.get('juego_finalizado') or
        stage.get('stage_timer') > 0) and 
        (stage.get('jugador').get('hp_actual') > 0 and stage.get('enemigo').get('hp_actual') > 0)):

        critical, ganador_mano = stage_juego.jugar_mano(stage)
        print(f'El ganador de la mano es: {ganador_mano}')

def verificar_terminado(form_dict_data: dict):
    stage = form_dict_data.get('stage')
    if stage_juego.esta_finalizado(stage):
        
        print('EL JUEGO ESTA TERMINADO')
       
        if particip_juego.get_nombre_participante(
            stage_juego.obtener_ganador(stage)
        ) == 'Enemigo':
            win_status = False
        else:
            win_status = True
        # activar el form enter name
        name_form = var.dict_forms_status.get('form_name')
        form_name.update_texto_victoria(name_form, win_status)
        base_form.set_active('form_name')

def call_wish_form(params: dict):
    """'form': form, 'wish': 'SCORE X3'"""
    print('DENTRO DE LA FUNCION CALL_WISH')

    form_dict_data = params.get('form')
    wish_type= params.get('wish')
    wish_form = var.dict_forms_status.get('form_wish')
    form_wish.update_wish_type(wish_form, wish_type)

    print(f'Estado de activacion: {wish_form.get("active")}')
    base_form.cambiar_pantalla('form_wish')
    print(f'Estado de activacion: {wish_form.get("active")}')

def iniciar_nueva_partida(form_dict_data: dict):
    stage = form_dict_data.get('stage')
    jugador = form_dict_data.get('jugador')
    pantalla = form_dict_data.get('screen')
    form_dict_data['stage'] = stage_juego.restart_stage(stage_data=stage, jugador=jugador, pantalla=pantalla, nro_stage=stage.get('nro_stage'))

def events_handler(events: list[pg.event.Event]):
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                base_form.set_active('form_pause', change_music=False)
                pause_form = var.dict_forms_status.get('form_pause')
                form_pause.save_last_vol(pause_form)
        if event.type == pg.MOUSEBUTTONDOWN:
            print(event.pos)
                
def update_lbls_card_info(form_dict_data: dict):
    mazo_enemigo = form_dict_data.get('stage').get('enemigo').get('cartas_mazo_usadas')
    mazo_player = form_dict_data.get('stage').get('jugador').get('cartas_mazo_usadas')

    if mazo_enemigo and mazo_player:
        ultima_carta_e = particip_juego.get_carta_actual_participante(form_dict_data.get('stage').get('enemigo'))
        ultima_carta_p = particip_juego.get_carta_actual_participante(form_dict_data.get('stage').get('jugador'))

        form_dict_data['lbl_carta_e'].update_text(
            f"HP: {carta_jugador.get_hp_carta(ultima_carta_e)} ATK: {carta_jugador.get_atk_carta(ultima_carta_e)} DEF: {carta_jugador.get_def_carta(ultima_carta_e)}",
            var.colores.get('cian')
        )

        form_dict_data['lbl_carta_p'].update_text(
            f"HP: {carta_jugador.get_hp_carta(ultima_carta_p)} ATK: {carta_jugador.get_atk_carta(ultima_carta_p)} DEF: {carta_jugador.get_def_carta(ultima_carta_p)}",
            var.colores.get('cian')
        )

def update_lbls_participante(form_dict_data: dict, tipo_participante: str):
    participante = form_dict_data.get('stage').get(tipo_participante)

    form_dict_data[f'lbl_{tipo_participante}_hp'].update_text(text=f'HP: {particip_juego.get_hp_participante(participante)}', color=var.colores.get('cian'))
    form_dict_data[f'lbl_{tipo_participante}_atk'].update_text(text=f'ATK: {particip_juego.get_attack_participante(participante)}', color=var.colores.get('cian'))
    form_dict_data[f'lbl_{tipo_participante}_def'].update_text(text=f'DEF: {particip_juego.get_defense_participante(participante)}', color=var.colores.get('cian'))

def update_score(form_dict_data: dict):
    participante = form_dict_data.get('stage').get('jugador')
    score = participante.get('score')
    form_dict_data.get('lbl_score').update_text(text=f'Score: {score}', color=var.colores.get('cian'))

def draw_bonus_widgets(form_dict_data: dict):
    # for widget in form_dict_data.get('widgets_list_bonus'):
    #     widget.draw()

    widgets_bonus = form_dict_data.get('widgets_list_bonus')
    stage = form_dict_data.get('stage')
    if stage.get('heal_available'):
        widgets_bonus[0].draw()
    if stage.get('jackpot_available'):
        widgets_bonus[1].draw()
    
def update_bonus_widgets(form_dict_data: dict):
    widgets_bonus = form_dict_data.get('widgets_list_bonus')
    stage = form_dict_data.get('stage')
    if stage.get('heal_available'):
        widgets_bonus[0].update()
    if stage.get('jackpot_available'):
        widgets_bonus[1].update()

def draw(form_dict_data: dict):
    base_form.draw(form_dict_data)
    stage_juego.draw_jugadores(form_dict_data.get('stage'))
    base_form.draw_widgets(form_dict_data)
    draw_bonus_widgets(form_dict_data)


def update(form_dict_data: dict, eventos: list[pg.event.Event]):
    form_dict_data['lbl_timer'].update_text(f'{stage_juego.obtener_tiempo(form_dict_data.get('stage'))}', var.colores.get('cian'))
    base_form.update(form_dict_data)
    stage_juego.update(form_dict_data.get('stage'))
    update_lbls_card_info(form_dict_data)
    update_lbls_participante(form_dict_data, tipo_participante='jugador')
    update_score(form_dict_data)
    update_lbls_participante(form_dict_data, tipo_participante='enemigo')
    update_bonus_widgets(form_dict_data)
    
    events_handler(eventos)
    verificar_terminado(form_dict_data)
