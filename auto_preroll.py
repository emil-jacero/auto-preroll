#!/usr/bin/env python

import sys
import os
import re
import yaml
import requests
import json
from datetime import datetime
from argparse import ArgumentParser
from logging import getLogger, Formatter, DEBUG, INFO, WARNING, ERROR, StreamHandler, FileHandler

log = getLogger()
log.setLevel(DEBUG)
logger_name = 'auto_preroll'
log_levels = {'DEBUG': DEBUG, 'INFO': INFO, 'WARNING': WARNING, 'ERROR': ERROR}
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handlers = [StreamHandler()]

for handler in log_handlers:
    handler.setFormatter(fmt=formatter)  # Set Formatter
    log.addHandler(handler)  # Set Handler

log.debug(f'Loaded these handlers: {log_handlers}')

try:
    from plexapi.server import PlexServer
except:
    log.error('PlexAPI is not installed.')
    sys.exit(1)


def getArguments():
    name = 'Auto-Preroll'
    version = '0.1.0'
    parser = ArgumentParser(
        description=f'{name}: Set monthly trailers for Plex')
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version=f'{name} {version}',
                        help="Show the version number and exit")
    parser.add_argument('-c',
                        '--config',
                        dest='config',
                        type=str,
                        default='config.yaml',
                        help='Path to config')
    parser.add_argument('-l',
                        '--log-level',
                        dest='log_level',
                        type=str,
                        default='INFO',
                        help='Set log level (Default: INFO)')
    args = parser.parse_args()
    return args


def get_config(conf):
    cfg = {}
    try:
        if os.path.exists(conf):
            yaml_config = conf
            with open(yaml_config, 'r') as f:
                cfg = yaml.load(f, Loader=yaml.FullLoader)
        else:
            log.error('Cannot find config file')
            sys.exit(1)
    except ImportError as e:
        log.error('Could not load config')
        log.error(e)
    except Exception as e:
        log.error(e)
        sys.exit(1)
    log.debug(json.dumps(cfg, indent=2))
    return cfg

def generate_plex_string(files, mode="random"):
    result = str()
    if mode == 'random':
        mode = ';'
        result = f'{mode}'.join(files)
    elif mode == 'sequence':
        mode = ':'
        result = f'{mode}'.join(files)
    else:
        log.error(f'Incorrect or missing mode [{mode}]')
    return result

def get_all_videos(url, token, lib):
    files = []
    session = requests.Session()
    session.verify = False
    requests.packages.urllib3.disable_warnings()
    plex = PlexServer(url, token, session, timeout=None)
    movies = plex.library.section(lib)
    for video in movies.search():
        files.append(video.locations[0])
    
    return files


def update_plex(url, token, plex_string='empty'):
    if url is not None:
        session = requests.Session()
        session.verify = False
        requests.packages.urllib3.disable_warnings()
        plex = PlexServer(url, token, session, timeout=None)
        plex.settings.get('cinemaTrailersPrerollID').set(plex_string)
        plex.settings.save()


def validate_config(conf):
    if len(conf['schedule']) <= 1:
        sys.exit(1)


def main():
    print('###########################')
    print('#                         #')
    print('#      Auto Pre-roll!     #')
    print('#                         #')
    print('###########################' + '\n')

    # Arguments
    arguments = getArguments()
    plex_token = os.getenv('PLEX_TOKEN')
    if arguments.log_level in log_levels.keys():
        log_level = log_levels[arguments.log_level]
    else:
        log_level = INFO
    log.setLevel(log_level)
    
    conf = get_config(arguments.config)

    validate_config(conf)

    current_month = datetime.today().strftime('%b').lower()
    log.debug(f"Current Month: {current_month}")
    all_videos = get_all_videos(url=conf['plex']['url'], 
                                    token=plex_token,
                                    lib=conf['plex']['library'])

    for sched in conf['schedule']:
        if sched['module']['month']:
            if current_month in sched['module']['month']:
                filtered_videos = [video for video in all_videos if sched['search_string'] in video]
                pre_roll_string = generate_plex_string(filtered_videos, sched['mode'])
                try:
                    update_plex(conf['plex']['url'], plex_token, pre_roll_string)
                    log.info(f'Pre-roll updated to {current_month}')
                    break
                except Exception as e:
                    log.error(f'Something went wrong!')
                    log.error(e)
            else:
                try:
                    update_plex(conf['plex']['url'], plex_token)
                    log.info(f'Pre-roll empty')
                except Exception as e:
                    log.error(f'Something went wrong!')
                    log.error(e)
        else:
            log.info(f'NO ACTIVE PRE-ROLLS THIS MONTH!')


if __name__ == '__main__':
    main()
