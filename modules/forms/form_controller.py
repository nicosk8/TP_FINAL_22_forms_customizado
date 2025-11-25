import pygame as pg
import modules.variables as var
import modules.forms.menu_form as menu_form
import modules.forms.ranking_form as ranking_form
import modules.forms.form_options as options_form
import modules.forms.form_pause as pause_form
import modules.forms.form_stage as stage_form
import modules.forms.form_name as form_name
import modules.forms.form_wish as wish_form

from utn_fra.pygame_widgets import MousePointer, Particle


def create_form_controller(screen: pg.Surface, datos_juego: dict):
    controller = {}

    controller['main_screen'] = screen
    controller['current_stage'] = 1
    controller['game_started'] = False
    controller['player'] = datos_juego.get('player')
    controller['music_config'] = datos_juego.get('music_config')

    controller['particle_manager'] = Particle(controller.get('main_screen'), circle_radius=10, particle_color=var.colores.get('verde'))
    controller['particle_event'] = pg.USEREVENT + 1

    pg.time.set_timer(controller.get('particle_event'), 500)


    cursor_img = pg.image.load(var.MOUSE_POINTER)
    size = cursor_img.get_size()
    half_size = (size[0] // 2, size[1] // 2)
    cursor_img = pg.transform.scale(cursor_img, half_size)


    controller['mouse_cursor'] = MousePointer(controller.get('main_screen'), cursor_img)
    controller['mouse_c'] = pg.sprite.Group(controller.get('mouse_cursor'))
    
    controller['forms_list'] = [
        menu_form.create_form_menu(
            {
                "name": 'form_menu',
                "screen": controller.get('main_screen'),
                "active": True,
                "coord": (0, 0),
                "music_path": var.MUSICA_MENU,
                "background": var.FONDO_MENU,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get('music_config')
            }
        ),
        ranking_form.create_form_ranking(
            {
                "name": 'form_ranking',
                "screen": controller.get('main_screen'),
                "active": False,
                "coord": (0, 0),
                "music_path": var.MUSICA_RANKING,
                "background": var.FONDO_RANKING,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get('music_config')
            }
        ),
        options_form.create_form_options(
            {
                "name": 'form_options',
                "screen": controller.get('main_screen'),
                "active": False,
                "coord": (0, 0),
                "music_path": var.MUSICA_OPTIONS,
                "background": var.FONDO_OPTIONS,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get('music_config')
            }
        ),
        pause_form.create_form_pause(
            {
                "name": 'form_pause',
                "screen": controller.get('main_screen'),
                "active": False,
                "coord": (0, 0),
                "music_path": var.MUSICA_PAUSE,
                "background": var.FONDO_PAUSE,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get('music_config')
            }
        ),
        stage_form.crear_form_stage(
            {
                "name": 'form_stage',
                "screen": controller.get('main_screen'),
                "active": False,
                "coord": (0, 0),
                "music_path": var.MUSICA_STAGE,
                "background": var.FONDO_STAGE,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get('music_config'),
                'jugador': controller.get('player')
            }
        ),
        form_name.create_form_name(
            {
                "name": 'form_name',
                "screen": controller.get('main_screen'),
                "active": False,
                "coord": (0, 0),
                "music_path": var.MUSICA_OPTIONS,
                "background": var.FONDO_NAME,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get('music_config'),
                'jugador': controller.get('player')
            }
        ),
        wish_form.create_form_wish(
            {
                "name": 'form_wish',
                "screen": controller.get('main_screen'),
                "active": False,
                "coord": (0, 0),
                "music_path": var.MUSICA_MENU,
                "background": var.FONDO_WISH,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get('music_config'),
                'jugador': controller.get('player')
            }
        )
    ]

    return controller

def forms_update(form_controller: dict, eventos: list[pg.event.Event]):

    lista_formularios = form_controller.get('forms_list')
    
    for form in lista_formularios:
        if form.get('active'):
            match form.get('name'):
                case 'form_menu':
                    form_menu = lista_formularios[0]
                    menu_form.update(form_menu)
                    menu_form.draw(form_menu)
                case 'form_ranking':
                    form_ranking = lista_formularios[1]
                    ranking_form.update(form_ranking)
                    ranking_form.draw(form_ranking)
                case 'form_options':
                    form_options = lista_formularios[2]
                    options_form.update(form_options)
                    options_form.draw(form_options)
                case 'form_pause':
                    form_pause = lista_formularios[3]
                    pause_form.update(form_pause)
                    pause_form.draw(form_pause)
                case 'form_stage':
                    form_stage = lista_formularios[4]
                    stage_form.update(form_stage, eventos)
                    stage_form.draw(form_stage)
                case 'form_name':
                    name_form = lista_formularios[5]
                    form_name.update(name_form, eventos)
                    form_name.draw(name_form)
                case 'form_wish':
                    form_wish = lista_formularios[6]
                    wish_form.update(form_wish)
                    wish_form.draw(form_wish)

def handle_events(eventos: list[pg.event.Event], form_controller: dict):

    for evento in eventos:
        if evento.type == form_controller.get('particle_event'):
            for _ in range(10):
                form_controller['particle_manager'].add_particles()

def update(form_controller: dict, eventos: list[pg.event.Event]):
    forms_update(form_controller, eventos)
    handle_events(eventos, form_controller)
    # form_controller.get('mouse_c').update()
    # form_controller.get('mouse_c').draw(form_controller.get('main_screen'))
    # form_controller.get('particle_manager').draw()
    
    