# Untitled Re-Namer

A Python script to automatically clean up, rename, and deduplicate track titles on Untitled Stream. This tool capitalizes titles, removes unwanted prefixes/suffixes, and deletes duplicate tracks based on title. It works using your browser cookies for authentication.

## Why I Made This

Bro... I got *so* tired of renaming the same songs over and over. Every time someone uploaded something to our Untitled project, it was like:

- "final_final_MASTER.mp3"
- "Copy of copy - V2 real this time"
- or just... "untitled 15"

It's actually insane. I couldn’t take it anymore. So I wrote this script to automate everything because my sanity was genuinely at risk. Now, every track gets cleaned up, named properly, and any duplicates are *gone*. Life’s too short to manually rename tracks.

## What It Fixes

This script is a lifesaver if:
- You’re tired of clicking into 20 versions of the same file.
- You hate lowercase, janky, or repetitive track names.
- You want to look like you got your sh*t together in front of collaborators.

## Features

- Renames tracks with clean title-case formatting.
- Skips already processed tracks using a log file.
- Skips titles with blacklisted prefixes/suffixes.
- Detects and deletes duplicates automatically.
- Requires no browser automation.
- Fully configurable through `settings.yaml`.

## Setup

### 1. Clone the repo or download the files

### 2. Install required packages:
```bash
pip install requests pyyaml
```

### 3. Export your cookies
- Install this Chrome Extension: [Cookie Editor](https://chromewebstore.google.com/detail/cookie-editor/ookdjilphngeeeghgngjabigmpepanpl?hl=en-US&utm_source=ext_sidebar)
- Go to [https://untitled.stream](https://untitled.stream)
- Open the Cookie Editor and click "Export"
- Paste the result into a file called `cookies.txt` in the script folder

### 4. Edit your `settings.yaml`
```yaml
get_url: https://untitled.stream/library/project/PASTE_YOUR_PROJECT_ID_HERE

blacklist:
  prefixes:
    - new_
    - final_
    - test_
    - copy_
    - old_
    - temp_
    - v1
    - v2
    - untitled
  suffixes:
    - _new
    - _final
    - _copy
    - _old
    - _temp
    - v1
    - v2
    - demo
    - master
```
> To find your `get_url`, open your Untitled Stream project and copy the link from the browser’s address bar.

### 5. Run the script
```bash
python script_name.py
```

## Notes
- If `cookies.txt` or `used.txt` are missing, the script creates them.
- If `used.txt` is empty, it’ll notify you and exit.
- Processed track IDs are logged in `used.txt` so you’re not renaming the same thing twice.
- If there are duplicates (same title), it keeps one and deletes the rest.

## License
MIT

---
Coded out of frustration. Shared for your sanity. 😤
