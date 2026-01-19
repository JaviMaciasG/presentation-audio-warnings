#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import time


def parse_mmss(s: str) -> int:
    mm, ss = s.split(":")
    return int(mm) * 60 + int(ss)


def pick_player():
    # Devuelve (comando_base:list[str], usa_stdin:bool)
    # Probamos varios reproductores comunes en Linux
    if shutil.which("ffplay"):
        # -nodisp: sin ventana, -autoexit: sale al terminar, -loglevel error: silencioso
        return (["ffplay", "-nodisp", "-autoexit", "-loglevel", "error"], False)
    if shutil.which("mpg123"):
        return (["mpg123", "-q"], False)
    if shutil.which("aplay"):
        return (["aplay", "-q"], False)  # normalmente WAV
    if shutil.which("paplay"):
        return (["paplay"], False)
    return (None, False)


def play_audio(path: str, player_cmd):
    if not player_cmd:
        raise SystemExit(
            "ERROR: No encuentro reproductor de audio (ffplay/mpg123/aplay/paplay).\n"
            "Instala uno, por ejemplo: sudo apt install ffmpeg\n"
        )
    subprocess.run(player_cmd + [path], check=False)


def main():
    p = argparse.ArgumentParser(description="Reproduce dos avisos de audio en tiempos MM:SS.")
    p.add_argument("--t1", default="9:00", help="Tiempo del primer aviso (MM:SS). Default: 9:00")
    p.add_argument("--t2", default="10:00", help="Tiempo del segundo aviso (MM:SS). Default: 10:00")
    p.add_argument("--a1", default="09.mp3", help="Audio del primer aviso. Default: 09.mp3")
    p.add_argument("--a2", default="10.mp3", help="Audio del segundo aviso. Default: 10.mp3")
    args = p.parse_args()

    t1 = parse_mmss(args.t1)
    t2 = parse_mmss(args.t2)
    if t2 <= t1:
        raise SystemExit("ERROR: t2 debe ser mayor que t1")

    player_cmd, _ = pick_player()

    print(f"Primer aviso: {args.t1} -> {args.a1}")
    print(f"Segundo aviso: {args.t2} -> {args.a2}")

    # check that audio file exist
    for audio_file in [args.a1, args.a2]:
        try:
            with open(audio_file, "rb"):
                pass
        except FileNotFoundError:
            raise SystemExit(f"ERROR: No se encuentra el archivo de audio: {audio_file}")


    print("Iniciando...")

    start = time.time()

    time.sleep(max(0, t1 - (time.time() - start)))
    print(">>> AVISO 1")
    play_audio(args.a1, player_cmd)

    time.sleep(max(0, t2 - (time.time() - start)))
    print(">>> AVISO 2")
    play_audio(args.a2, player_cmd)


if __name__ == "__main__":
    main()
