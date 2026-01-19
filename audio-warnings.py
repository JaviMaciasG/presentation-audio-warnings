#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import time


def parse_mmss(s: str) -> int:
    mm, ss = s.split(":")
    return int(mm) * 60 + int(ss)


def fmt_mmss(seconds: int) -> str:
    m = seconds // 60
    s = seconds % 60
    return f"{m:02d}:{s:02d}"


def countdown_until(target_seconds: int, start_time: float, label: str):
    """
    Prints a countdown in the console until target_seconds (relative to start_time).
    Updates once per second.
    """
    while True:
        elapsed = time.time() - start_time
        remaining = int(round(target_seconds - elapsed))

        if remaining <= 0:
            print(f"\r[INF] {label}: 00:00   ", end="", flush=True)
            print()  # final newline
            return

        print(f"\r[INF] {label}: {fmt_mmss(remaining)}   ", end="", flush=True)
        time.sleep(1)


def pick_player():
    # Returns (base_command:list[str], uses_stdin:bool)
    # Try common audio players on Linux
    if shutil.which("ffplay"):
        # -nodisp: no window, -autoexit: quit at end, -loglevel error: quiet
        return (["ffplay", "-nodisp", "-autoexit", "-loglevel", "error"], False)
    if shutil.which("mpg123"):
        return (["mpg123", "-q"], False)
    if shutil.which("aplay"):
        return (["aplay", "-q"], False)  # usually WAV
    if shutil.which("paplay"):
        return (["paplay"], False)
    return (None, False)


def play_audio(path: str, player_cmd):
    if not player_cmd:
        raise SystemExit(
            "ERROR: No audio player found (ffplay/mpg123/aplay/paplay).\n"
            "Install one, for example: sudo apt install ffmpeg\n"
        )

    p = subprocess.Popen(player_cmd + [path])
    try:
        p.wait()
    except KeyboardInterrupt:
        print("\n[WRN] Audio interrupted by user.")
        p.terminate()
        try:
            p.wait(timeout=1)
        except subprocess.TimeoutExpired:
            p.kill()


def main():
    p = argparse.ArgumentParser(description="Plays two audio warnings at MM:SS times.")
    p.add_argument("--t1", default="9:00", help="Time for the first warning (MM:SS). Default: 9:00")
    p.add_argument("--t2", default="10:00", help="Time for the second warning (MM:SS). Default: 10:00")
    p.add_argument("--a1", default="09.mp3", help="Audio file for the first warning. Default: 09.mp3")
    p.add_argument("--a2", default="10.mp3", help="Audio file for the second warning. Default: 10.mp3")
    args = p.parse_args()

    t1 = parse_mmss(args.t1)
    t2 = parse_mmss(args.t2)
    if t2 <= t1:
        raise SystemExit("ERROR: t2 must be greater than t1")

    # Select audio player and print
    player_cmd, _ = pick_player()
    if player_cmd:
        print(f"[INF] Using audio player: {' '.join(player_cmd)}")
    else:
        print("[ERR] No audio player found (ffplay/mpg123/aplay/paplay).")

    print(f"[INF] First warning:  {args.t1} -> {args.a1}")
    print(f"[INF] Second warning: {args.t2} -> {args.a2}")

    # Check that audio files exist
    for audio_file in [args.a1, args.a2]:
        try:
            with open(audio_file, "rb"):
                pass
        except FileNotFoundError:
            raise SystemExit(f"ERROR: Audio file not found: {audio_file}")

    print("\n[INF] Starting timer...\n")

    start = time.time()

    countdown_until(t1, start, "Time until warning 1")
    print("[INF] Playing warning 1 at ", fmt_mmss(t1))
    play_audio(args.a1, player_cmd)

    countdown_until(t2, start, "Time until warning 2")
    print("[INF] Playing warning 2 at ", fmt_mmss(t2))
    play_audio(args.a2, player_cmd)


if __name__ == "__main__":
    main()

