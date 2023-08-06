"""Basically doing sound effects, graphics and music-ing.

Does paths, loading, caching, converting and such... for us.

gfx('parrot.png', convert=True) will look into the data/images/ folder, load the image,
and maybe even convert the image for you.

Next place you use gfx('parrot.png', convert=True) will give you the same cached image.

This means when using gfx, you just use it. 
Don't not worry about paths, caching, converting and such things.
"""
import os
import pygame as pg

# Our secret stashes.
_sfx_cache = {}
_gfx_cache = {}


def data_path() -> str:
    """Returns file system path for where the data at."""
    if os.path.exists("data"):
        path = "data"
    else:
        path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data",
        )
    return path


def music(
    music: str | None = None,
    load: bool = True,
    play: bool = True,
    stop: bool | None = False,
) -> None:
    """Basically music-ing. music('song.mp3')

    :param music: the music file to play. Relative to data/sounds.
    :param load: Start loading the music. If music is loaded already it's faster to play.
    :param play: Play music.
    :param stop: Stop music.

    #### Example

    ```python
    music('bla.ogg')
    music(stop=True)
    ```
    """
    # perhaps the mixer is not included or initialised.
    if pg.mixer and pg.mixer.get_init():
        if load and not stop:
            pg.mixer.music.load(music_path(music))
        if play and stop is None or stop is False:
            pg.mixer.music.play()
        elif stop:
            pg.mixer.music.stop()


def music_path(music: str) -> str:
    """Returns file system path for where the given music is at."""
    path = os.path.join(data_path(), "sounds", music)
    return path


def gfx(image: str, convert: bool = False, convert_alpha: bool = False) -> pg.Surface:
    """Basically graphics using. Loading/converting/cached. gfx('parrot.png')

    :param image: looks in data/images/ for the image to load.
    :param convert: convert to the most meow
    :param convert_alpha: convert_alpha()
    :param play: Play music.
    :param stop: Stop music.

    #### Example

    ```python
    gfx('parrot.png')
    gfx('parrot.png', convert=True)
    gfx('parrot.png', convert_alpha=True)
    ```
    """
    global _gfx_cache
    gfx_key = (image, convert, convert_alpha)
    if gfx_key in _gfx_cache:
        return _gfx_cache[gfx_key]

    path = os.path.join(data_path(), "images", image)
    asurf = pg.image.load(path)
    if convert:
        asurf = asurf.convert()
    if convert_alpha:
        asurf = asurf.convert_alpha()

    _gfx_cache[gfx_key] = asurf
    return asurf


def sfx(snd: str, play: bool = False, stop: bool = False) -> pg.mixer.Sound:
    """Basically sound using. Loading/converting/cached. sfx('parrot.mp3')

    :param snd: looks in data/sounds/ for the sound to load.
    :param play: Play sound.
    :param stop: Stop sound.

    #### Example

    ```python
    sfx('parrot.mp3')
    sfx('parrot.png', play=True)
    sfx('parrot.png', convert_alpha=True)
    ```
    """

    global _sfx_cache
    snd_key = snd
    if snd_key in _sfx_cache:
        asound = _sfx_cache[snd_key]
    else:
        path = os.path.join(data_path(), "sounds", snd)
        asound = pg.mixer.Sound(path)
        _sfx_cache[snd_key] = asound

    # print(snd_key, play, stop, time.time())
    if play:
        asound.play()
    if stop:
        asound.stop()
    return asound
