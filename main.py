import requests
import json
import os
import yaml
import sys
from collections import defaultdict

def load_config(path='settings.yaml'):
    if not os.path.exists(path):
        print(f"[ERROR] Missing settings file: {path}. Please create it using the template or re-download it.")
        sys.exit(1)
    with open(path, 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"[ERROR] Failed to parse settings file: {e}")
            sys.exit(1)
    if 'get_url' not in config or 'blacklist' not in config or 'prefixes' not in config['blacklist'] or 'suffixes' not in config['blacklist']:
        print(f"[ERROR] settings.yaml must contain get_url and blacklist with prefixes and suffixes.")
        sys.exit(1)
    return config

def read_cookies_from_file(file_path='cookies.txt'):
    if not os.path.exists(file_path):
        print(f"[ERROR] Cookies file '{file_path}' not found. Please export cookies to this file.")
        sys.exit(1)
    with open(file_path, 'r') as f:
        cookie_str = f.read().strip()
    cookies = {}
    for pair in cookie_str.split(';'):
        if '=' in pair:
            key, value = pair.strip().split('=', 1)
            cookies[key] = value
    return cookies

def capitalize_title(title):
    words = title.split()
    return ' '.join(word.capitalize() for word in words)

def is_blacklisted(title, prefixes, suffixes):
    title_lower = title.lower()
    for pre in prefixes:
        if title_lower.startswith(pre.lower()):
            return True
    for suf in suffixes:
        if title_lower.endswith(suf.lower()):
            return True
    return False

def get_songs(cookies, get_url):
    headers = {
        'accept': '*/*',
        'referer': get_url,
        'user-agent': 'Mozilla/5.0',
    }
    params = {
        '_data': 'routes/library.project.$projectSlug',
    }
    response = requests.get(get_url, headers=headers, cookies=cookies, params=params)
    try:
        data = response.json()
    except:
        print("Invalid JSON response from server.")
        return []

    songs = []
    def recurse(item):
        if isinstance(item, dict):
            if item.get('id', '').startswith('trck_') and item.get('title'):
                songs.append({'id': item['id'], 'title': item['title']})
            for v in item.values():
                recurse(v)
        elif isinstance(item, list):
            for v in item:
                recurse(v)
    recurse(data)
    return songs

def update_song_title(song_id, new_title, cookies, referer):
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'origin': 'https://untitled.stream',
        'referer': referer,
        'user-agent': 'Mozilla/5.0',
    }
    params = {
        '_data': 'routes/track',
    }
    json_data = {
        'id': song_id,
        'title': new_title
    }
    response = requests.patch('https://untitled.stream/track', headers=headers, cookies=cookies, params=params, json=json_data)
    return response.status_code == 200

def delete_song(song_id, cookies, referer):
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'origin': 'https://untitled.stream',
        'referer': referer,
        'user-agent': 'Mozilla/5.0',
    }
    params = {
        '_data': 'routes/track',
    }
    json_data = {
        'id': song_id
    }
    response = requests.delete('https://untitled.stream/track', headers=headers, cookies=cookies, params=params, json=json_data)
    return response.status_code == 200

def main():
    config = load_config()
    get_url = config['get_url']
    referer = get_url
    processed_file = 'used.txt'
    blacklist = config['blacklist']
    prefixes = blacklist['prefixes']
    suffixes = blacklist['suffixes']

    if not os.path.exists(processed_file):
        with open(processed_file, 'w') as f:
            f.write('')
    if os.path.getsize(processed_file) == 0:
        print("used.txt is empty. Add previously processed IDs or it will start fresh. Aborting to prevent mistakes.")
        return

    cookies = read_cookies_from_file()

    with open(processed_file, 'r') as f:
        processed = set(line.strip() for line in f if line.strip())

    songs = get_songs(cookies, get_url)
    title_map = defaultdict(list)
    for song in songs:
        title_map[song['title'].strip().lower()].append(song)

    for title, tracks in title_map.items():
        if len(tracks) > 1:
            print(f"Duplicate Found: '{title}' -> deleting {len(tracks)-1} duplicates")
            for song in tracks[1:]:
                if delete_song(song['id'], cookies, referer):
                    print(f"Deleted duplicate track: {song['id']}")
                    processed.add(song['id'])

    for song in songs:
        song_id = song['id']
        original_title = song['title']
        fixed_title = capitalize_title(original_title)

        if song_id in processed:
            print(f"{fixed_title} Already Processed.")
            continue

        if fixed_title == original_title or is_blacklisted(original_title, prefixes, suffixes):
            print(f"{original_title} Skipped.")
            with open(processed_file, 'a') as f:
                f.write(song_id + '\n')
            continue

        try:
            success = update_song_title(song_id, fixed_title, cookies, referer)
            if success:
                print(f"Song Name Changed: {original_title} -> {fixed_title}")
                with open(processed_file, 'a') as f:
                    f.write(song_id + '\n')
            else:
                print(f"Failed to update {original_title}")
        except Exception as e:
            print(f"Error updating {original_title}: {e}")

if __name__ == '__main__':
    main()
