"""
Play a sequence of commands concurrently via yaml specification
"""
import copy
from pathos.multiprocessing import ProcessingPool as Pool

import yaml
import click

from saysynth.cli.commands import chord, midi, note, arp


TRACK_FUNCS = {
    "chord": chord.run,
    "midi": midi.run,
    "note": note.run,
    "arp": arp.run,
}

def _run_track_func(item):
    name, kwargs = item
    type = kwargs.get('type', None)
    options = kwargs.get('options', {})
    options['exec'] = True
    if type not in TRACK_FUNCS:
        raise ValueError(f'Invalid track type: {type}. Choose from: {",".join(TRACK_FUNCS.keys())}')
    print(f'Starting track {name} with  options: {kwargs}')
    return TRACK_FUNCS.get(type)(**options)

def run(**kwargs):
    base_config = yaml.safe_load(kwargs['base_config'])
    config_overrides = kwargs['config_overrides']
    globals = base_config.pop('globals', {})
    tracks = kwargs.get('tracks') or []
    items = []
    for track_name, track_config in base_config.get('tracks', {}).items():

        # optionally skip tracks
        if len(tracks):
            if track_name not in tracks:
                continue

        # allow for track-specific overrides
        track_overrides = config_overrides.pop(track_name, {})
        config_overrides.update(track_overrides)

        # create track config
        track_options = copy.copy(globals) # start with globals
        track_options.update(track_config.get('options', {})) # override with base track configs
        track_options.update(config_overrides)
        track_config['options'] = track_options

        # add to run items
        items.append((track_name, track_config))
    return Pool(len(items)).map(_run_track_func, items)


@click.command()
@click.argument("base_config", type=click.File(), required=True)
@click.option("-t", "--tracks", type=lambda x: [track for track in x.split(',')])
@click.option("-c", "--config-overrides", type=lambda x: yaml.safe_load(x), default='{}', help="Override global and track configurations at runtime")
def cli(**kwargs):
    try:
        return run(**kwargs)
    except KeyboardInterrupt as e:
        pass
