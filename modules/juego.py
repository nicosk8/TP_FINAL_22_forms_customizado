import pygame as pg
import modules.variables as var
import sys
import modules.forms.form_controller as form_controller
import modules.particip_juego as participante
import modules.sonido as sonido

def dbz_playing_cards_game():

    pg.init()

    pg.display.set_caption(var.TITULO_JUEGO_CAPTION)
    pantalla_juego = pg.display.set_mode(var.DIMENSION_PANTALLA)
    # pg.mouse.set_visible(False)

    sonido.set_volume(var.VOLUMEN_INICIAL)
    # cargar icono
    corriendo = True
    reloj = pg.time.Clock()
    datos_juego = {
        "puntaje": 0,
        "cantidad_vidas": var.CANTIDAD_VIDAS,
        "player": participante.inicializar_participante(pantalla=pantalla_juego, nombre='PLAYER'),
        "music_config": {
            "music_volume": var.VOLUMEN_INICIAL,
            "music_on": True,
            'music_init': False
        }
    }


    form_control = form_controller.create_form_controller(pantalla_juego, datos_juego)

    while corriendo:
        
        eventos = pg.event.get()
        reloj.tick(var.FPS)

        for evento in eventos:
            if evento.type == pg.QUIT:
                corriendo = False
            # if evento.type == pg.MOUSEBUTTONDOWN:
            #     particle_manager.add_particles()
        
        # particle_manager.draw()
        form_controller.update(form_control, eventos)


        pg.display.flip()
    
    pg.quit()
    sys.exit()
