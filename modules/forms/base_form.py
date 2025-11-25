import pygame as pg
import modules.variables as var
import modules.sonido as sonido


def create_base_form(dict_form_data: dict) -> dict:
    form = {}
    form['name'] = dict_form_data.get('name')
    form['screen'] = dict_form_data.get('screen')
    form['active'] = dict_form_data.get('active')
    form['x_coord'] = dict_form_data.get('coord')[0]
    form['y_coord'] = dict_form_data.get('coord')[1]

    form['music_path'] = dict_form_data.get('music_path')
    form['surface'] = pg.image.load(dict_form_data.get('background')).convert_alpha()
    form['surface'] = pg.transform.scale(form.get('surface'), dict_form_data.get('screen_dimentions'))

    form['rect'] = form.get('surface').get_rect()
    form['rect'].x = dict_form_data.get('coord')[0]
    form['rect'].y = dict_form_data.get('coord')[1]
    form['music_config'] = dict_form_data.get('music_config')
    return form

def draw_widgets(form_data: dict):
    for widget in form_data.get('widgets_list'):
        widget.draw()

def update_widgets(form_data: dict):

    for widget in form_data.get('widgets_list'):
        widget.update()

def set_active(form_name: str, change_music: bool = True):
    for form in var.dict_forms_status.values():
        form['active'] = False
    form_activo = var.dict_forms_status[form_name]
    form_activo['active'] = True

    if change_music:
        music_off(form_activo)
        music_on(form_activo)

    # for form_n in var.dict_forms_status.keys():
    #     if form_n != form_name:
    #         var.dict_forms_status[form_n]['active'] = False
    #     else:
    #         var.dict_forms_status[form_n]['active'] = True

def music_on(form_dict_data: dict):
    print(f"Musica activa: {form_dict_data.get('music_config').get('music_on')}")
    if form_dict_data.get('music_config').get('music_on'):
        ruta_musica = form_dict_data.get('music_path')
        print(f'Ruta musica: {ruta_musica}')
        sonido.set_music_path(ruta_musica)
        sonido.play_music()

def music_off(form_dict_data: dict):
    if form_dict_data.get('music_config').get('music_on'):
        sonido.stop_music()

def cambiar_pantalla(form_name: str, change_music: bool = True):
    set_active(form_name, change_music)


def update(form_data: dict):
    update_widgets(form_data)

def draw(form_data: dict):
    form_data['screen'].blit(form_data.get('surface'), form_data.get('rect'))