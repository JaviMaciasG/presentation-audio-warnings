# Meeting Audio Warnings (Python)

A tiny command-line Python tool that plays **two audio warnings** at configurable times during a session (e.g., a 10-minute presentation).

It also shows a **live countdown** in the terminal so presenters can see how much time is left.



## Features

- Two configurable warning times (`--t1`, `--t2`) in **MM:SS** format
- Two configurable audio files (`--a1`, `--a2`)
- Terminal **countdown timer** (updates every second)
- No Python audio dependencies required  
  (it uses an external player available on Linux)
- Graceful interruption: press **Ctrl+C** while audio is playing to stop it



## Requirements

- Python **3.8+**
- One of these audio players installed (Linux):
  - `ffplay` *(recommended)* — from **FFmpeg**
  - `mpg123`
  - `aplay` *(typically for WAV)*
  - `paplay`

### Install recommended player (ffplay)

On Ubuntu / Debian:

```bash
sudo apt update
sudo apt install ffmpeg
```

This provides the `ffplay` command.



## Usage

```bash
python3 audio-warnings.py
```

Default configuration:

- First warning at **09:00** → `09.mp3`
- Second warning at **10:00** → `10.mp3`



## Custom times and audio files

Example (8:30 and 10:00):

```bash
python3 audio-warnings.py --t1 8:30 --a1 warning1.mp3 --t2 10:00 --a2 warning2.mp3
```



## Notes

### Audio formats
- If you use **ffplay**, it supports most formats: MP3, WAV, OGG, etc.
- If the selected player is `aplay`, it usually expects **WAV** files.

### Stopping playback from the keyboard
- During audio playback, press **Ctrl+C** to interrupt the player.
- The program will terminate the audio process safely.

### Time constraints
- `--t2` must be greater than `--t1`.  
  Otherwise the script exits with an error.



## Example output

```text
[INF] Using audio player: ffplay -nodisp -autoexit -loglevel error
[INF] First warning:  9:00 -> 09.mp3
[INF] Second warning: 10:00 -> 10.mp3

[INF] Starting timer...

[INF] Time until warning 1: 00:10
...
[INF] Playing warning 1 at  09:00
```

### IA usage

The `audio-warnings.py` script and associated `README.md` have been generated using an original version by ChatGPT 5.2.


## License

Use it freely for your presentations and teaching sessions.
