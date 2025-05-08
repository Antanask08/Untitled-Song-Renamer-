# Untitled Re-Namer

A professional-grade Python script designed to automate the cleanup, renaming, and deduplication of track titles on Untitled Stream. It standardizes titles, removes noisy naming patterns, and ensures your tracklist stays organized. It uses your browser cookies to authenticate requests and interact directly with the Untitled API.

## Why This Exists

Keeping track titles clean shouldn't be a chore. Musicians and producers constantly upload files named things like:

- "mix_FINAL_for_real_this_time.mp3"
- "v2_demo_untitled_09"
- or just "track15"

Manually fixing this is inefficient, repetitive, and unnecessary. Untitled Re-Namer eliminates the burden by intelligently renaming, deduplicating, and skipping unnecessary rework—so you can focus on the music.

## What It Solves

If you:
- Constantly rename tracks after uploading them
- Struggle with inconsistent or messy naming
- End up with several near-identical versions of a song

Then this tool will:
- Clean up your titles into neat, readable formats
- Prevent duplicate naming issues
- Automatically remove repeated uploads

## Features

- 🔤 Capitalizes and formats track titles consistently
- ⏭ Skips already processed tracks via log tracking
- 🚫 Filters blacklisted prefixes and suffixes from names
- 🗑 Detects and deletes duplicate songs (based on title match)
- ⚙️ Easy YAML configuration
- 🔒 No need for browser automation (API only)

## Setup Instructions

### 1. Download or Clone the Repository

### 2. Install Required Python Packages
```bash
pip install requests pyyaml
```

### 3. Export Your Cookies
- Install this Chrome Extension: [Cookie Editor](https://chromewebstore.google.com/detail/cookie-editor/ookdjilphngeeeghgngjabigmpepanpl?hl=en-US&utm_source=ext_sidebar)
- Navigate to [https://untitled.stream](https://untitled.stream)
- Open the Cookie Editor and click **Export**
- Paste the result into a file called `cookies.txt` in your script directory

### 4. Configure `settings.yaml`
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
> To find your `get_url`, go to your Untitled Stream project and copy the URL from your browser address bar.

### 5. Run the Script
```bash
python script_name.py
```

## Behavior
- If `cookies.txt` or `used.txt` are missing, the script will auto-generate them.
- If `used.txt` is empty, you’ll be notified and the script will exit.
- Tracks already processed (renamed or skipped) are logged in `used.txt`.
- Duplicate tracks (same original title) will be deleted automatically, keeping only the first occurrence.

## License
MIT

---
Created for efficient workflows and cleaner libraries. Feel free to contribute or adapt to your needs.
