import pygame.mixer as mixer
import pygame as pg

music_configs = {
    "actual_music_path": ''
}

def set_music_path(music_path: str):
    music_configs['actual_music_path'] = music_path

def play_music():
    if music_configs.get('actual_music_path'):
        # stop_music()
        mixer.music.load(music_configs.get('actual_music_path'))
        # mixer.music.set_volume(0.3)
        mixer.music.play(-1, 0, 2500)

def get_actual_volume() -> int:
    actual_vol = mixer.music.get_volume() * 100
    return int(actual_vol)

def set_volume(volume: int):
    actual_vol = volume / 100
    actual_vol = round(actual_vol, 1)
    mixer.music.set_volume(actual_vol)

def stop_music():
    if music_configs.get('actual_music_path'):
        mixer.music.fadeout(500)
        pg.time.wait(500)
        mixer.music.stop()
