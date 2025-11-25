import pygame as pg
import sys
import modules.forms.base_form as base_form
import modules.auxiliar as aux
from utn_fra.pygame_widgets import (
    Label, Button
)
import modules.variables as var

def create_form_ranking(dict_form_data: dict) -> dict:
    form = base_form.create_base_form(dict_form_data)

    form['lista_ranking_file'] = []

    form['lista_ranking_GUI'] = []

    form['data_loaded'] = False

    form['lbl_titulo'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=50,
        text='DBZ Playing cards', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=70
    )

    form['lbl_subtitulo'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=130,
        text='TOP 10 Ranking', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=50
    )

    form['btn_volver'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=500,
        text='VOLVER', screen=form.get('screen'),
        font_path=var.FONT_ALAGARD, font_size=40,
        on_click=cambiar_pantalla, on_click_param=[form, 'form_menu']
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitulo'),
        form.get('btn_volver')
    ]

    var.dict_forms_status[form.get('name')] = form

    return form

def cambiar_pantalla(param_list: list):
    form_ranking = param_list[0]
    form_name = param_list[1]

    print('Saliendo del formulario ranking')
    form_ranking['data_loaded'] = False
    form_ranking['lista_ranking_GUI'] = []
    form_ranking['lista_ranking_file'] = []
    base_form.cambiar_pantalla(form_name)

def init_ranking_data(form_dict_data: dict):
    # form_dict_data['lista_ranking_GUI'] = []
    matrix = form_dict_data.get('lista_ranking_file')
    color_texto = (125,125,50)
    y_coord_inicial = 190
    for indice_fila in range(len(matrix)):
        fila = matrix[indice_fila]

        """
        POSICION        NOMBRE      SCORE
        POSICION        NOMBRE      SCORE
        POSICION        NOMBRE      SCORE
        POSICION        NOMBRE      SCORE
        POSICION        NOMBRE      SCORE
        
        """
        posicion = Label(
            x=var.DIMENSION_PANTALLA[0] // 2 - 150, y=y_coord_inicial,
            text=f'{indice_fila + 1}', screen=form_dict_data.get('screen'),
            font_size=40, font_path=var.FONT_ALAGARD, color=color_texto
        )

        nombre = Label(
            x=var.DIMENSION_PANTALLA[0] // 2, y=y_coord_inicial,
            text=fila[0], screen=form_dict_data.get('screen'),
            font_size=40, font_path=var.FONT_ALAGARD, color=color_texto
        )

        score = Label(
            x=var.DIMENSION_PANTALLA[0] // 2 + 150, y=y_coord_inicial,
            text=f'{fila[1]}', screen=form_dict_data.get('screen'),
            font_size=40, font_path=var.FONT_ALAGARD, color=color_texto
        )

        y_coord_inicial += 42

        form_dict_data['lista_ranking_GUI'].append(posicion)
        form_dict_data['lista_ranking_GUI'].append(nombre)
        form_dict_data['lista_ranking_GUI'].append(score)

        if indice_fila == 0:
            color_texto = (255, 0, 0)

def inicializar_ranking_archivo(form_dict_data: dict):
    if not form_dict_data.get('data_loaded'):
        form_dict_data['lista_ranking_file'] = aux.cargar_ranking(var.RANKING_CSV, top=7)
        init_ranking_data(form_dict_data)
        form_dict_data['data_loaded'] = True

def draw(form_dict_data: dict):
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)
    # widgets lbl ranking
    for widget in form_dict_data.get('lista_ranking_GUI'):
        widget.draw()

def update(form_dict_data: dict):

    if not form_dict_data.get('data_loaded'):
        inicializar_ranking_archivo(form_dict_data)

    base_form.update(form_dict_data)
