#!/usr/bin/env python3

'''
    YT-DL-MP3 -- v. 2020.08.09.0
    A small command-line tool with a simple set of options for downloading MP3s using youtube-dl
    Copyright (c) 2020 atouchofclass

    Portions use youtube-dl <github.com/ytdl-org/youtube-dl> under license
'''

from __future__ import unicode_literals
import sys
import json
import youtube_dl

class Logger(object):
    '''
        Enable logging to stdout from YoutubeDL object
    '''
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

# download options
ydl_opts = {
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'updatetime': False,
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'
        },
        {
            'key': 'EmbedThumbnail'
        }
    ],
    'progress_hooks': []
}

'''
    Read options from JSON file; if a problem occurs, use defaults
'''
def read_options(file='options.json'):
    print('[INFO] Reading options')
    opts = {}
    try:
        with open(file, 'r') as f:
            opts = json.load(f)
    except (TypeError, FileNotFoundError):
        print('[ERROR] There was a problem reading the options file; using default options\n')
        opts = ydl_opts
    finally:
        # enable logging
        opts['logger'] = Logger()
    return opts

'''
    Toogle the runtime option for embedding thumbnails when downloading files
'''
def toggle_embed_thumb(cur_opts):
    cur_opts_temp = cur_opts
    if cur_opts_temp['writethumbnail']:
        try:
            cur_opts_temp['writethumbnail'] = False
            cur_opts_temp['postprocessors'].remove({ 'key': 'EmbedThumbnail' })
        except KeyError: # TODO return status code, show message on error
            return cur_opts
    else:
        try:
            cur_opts_temp['writethumbnail'] = True
            cur_opts_temp['postprocessors'].append({ 'key': 'EmbedThumbnail' })
        except KeyError: # TODO return status code, show message on error
            return cur_opts
    return cur_opts_temp

'''
    Toggle the runtime option for preferred quality when downloading files
'''
def toggle_quality(cur_opts):
    cur_setting = cur_opts['postprocessors'][0]['preferredquality']
    if cur_setting == '320':
        cur_setting = '192'
    elif cur_setting == '192':
        cur_setting = '256'
    else:
        cur_setting = '320'
    cur_opts['postprocessors'][0]['preferredquality'] = cur_setting
    return cur_opts

'''
    Given a link and options object, download and convert to MP3 according to the provided options
'''
def downloadMp3(link, options):
    with youtube_dl.YoutubeDL(options) as ydl:
        # TODO check if it works with list of links
        try:
            ydl.download([link])
        except youtube_dl.DownloadError as err:
            # clear cache on 403 error
            if str(err).endswith("HTTP Error 403: Forbidden"):
                print('[INFO] Detected 403 error. Attempting to automatically clear the cache...')
                ydl.cache.remove()
                print('[IMFO] YoutubeDL cache was cleared. Try downloading again.')
        except youtube_dl.SameFileError as err:
            pass

if __name__ == '__main__':
    print('+----------------------------------------------------------+')
    print('|          Welcome to YT-DL-MP3 by atouchofclass           |')
    print('| Portions use youtube-dl <github.com/ytdl-org/youtube-dl> |')
    print('|                     v. 2020.08.09.0                      |')
    print('+----------------------------------------------------------+')
    print('')

    opts = read_options()
    print('[INFO] Download quality setting = {}kbps'.format(opts['postprocessors'][0]['preferredquality']))
    print('[INFO] Embed thumbnail option = {}'.format(opts['writethumbnail']))
    d_links = []

    if len(sys.argv) > 1:
        # got an arg
        if sys.argv[1].endswith('.txt'):
            print("\n[INFO] Found argument for batch download = <{}>".format(sys.argv[1]))
            # TODO batch download
            print('Not yet available')
        else:
            d_links += [sys.argv[1]]
            print("\n[INFO] Found argument for download = <{}>".format(d_links[0]))
            downloadMp3(d_links[0], opts)
    else:
        # options menu
        print('\nOptions:')
        print(' [q] Toggle 192/256/320 quality setting')
        print(' [t] Toggle embed thumbnail option')
        print(' [d] Download link')
        print(' [b] Batch download')
        print(' [x] Exit')
        while True:
            op = input('\nWhat would you like to do? ')
            if op == 'q':
                # toggle quality
                opts = toggle_quality(opts)
                print('[INFO] Download quality setting = {}kbps'.format(opts['postprocessors'][0]['preferredquality']))
            elif op == 't':
                # toggle embed thumbnail
                opts = toggle_embed_thumb(opts)
                print('[INFO] Embed thumbnail option = {}'.format(opts['writethumbnail']))
            elif op == 'd':
                # download 1 link
                lnk = input('Enter link: ')
                if lnk.strip() != '':
                    downloadMp3(lnk, opts)
            elif op == 'b':
                # download many links
                # TODO batch d
                print('Not yet available')
            elif op in ['x', 'exit']:
                print('Ok, goodbye!')
                sys.exit(0)
            else:
                print('Unrecognized option')
