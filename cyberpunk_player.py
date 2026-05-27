import re
import sys
import time
import random
import shutil

TITLE = "LÁBIA — JÃO"
LRC_FILE = "labia.lrc"

PURPLE = "\033[38;5;177m"
PURPLE_LIGHT = "\033[38;5;183m"
GRAY = "\033[90m"
RESET = "\033[0m"

LEFT_MARGIN = 6


# =============================
# terminal
# =============================

def move_cursor_top():
    sys.stdout.write("\033[H")
    sys.stdout.write("\033[J")  # limpa da posição do cursor para baixo
    sys.stdout.flush()

def hide_cursor():
    sys.stdout.write("\033[?25l")

def show_cursor():
    sys.stdout.write("\033[?25h")

def term_size():
    size = shutil.get_terminal_size((80, 24))
    return size.columns


# =============================
# align
# =============================

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def visible_length(text):
    return len(ansi_escape.sub('', text))

def left_align(text):
    return " " * LEFT_MARGIN + text


# =============================
# gradiente
# =============================

def gradient(text):

    colors = [
        "\033[38;5;177m",
        "\033[38;5;141m",
        "\033[38;5;99m",
        "\033[38;5;135m"
    ]

    result = ""

    for i, c in enumerate(text):
        result += colors[i % len(colors)] + c

    return result + RESET


# =============================
# lyrics
# =============================

def load_lyrics():

    lyrics = []

    with open(LRC_FILE, "r", encoding="utf-8") as f:

        for line in f:

            match = re.search(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)", line)

            if match:

                m = int(match.group(1))
                s = float(match.group(2))
                text = match.group(3).strip()

                lyrics.append((m*60+s, text))

    return lyrics


# =============================
# visualizer
# =============================

blocks = ["▁","▂","▃","▄","▅","▆","▇","█"]

def visualizer():

    bars = 28
    line = ""

    for _ in range(bars):
        line += random.choice(blocks) + " "

    return left_align(PURPLE + line + RESET)


# =============================
# barra de progresso
# =============================

def progress_bar(elapsed, total):

    size = 32
    progress = min(elapsed/total,1)

    filled = int(size*progress)

    bar = "█"*filled + "░"*(size-filled)

    return left_align(f"{PURPLE}[{bar}]{RESET}")


# =============================
# vinyl
# =============================

frames = [
"◜●◝",
"◠●◠",
"◝●◜",
"◡●◡",
"◞●◟",
"◠●◠"
]

def vinyl(frame):

    art = f"{GRAY}{frames[frame % len(frames)]}{RESET}"

    return left_align(art)


# =============================
# caixa de titulo
# =============================

def title_box():

    plain = TITLE
    colored = gradient(TITLE)

    padding = 4

    border = "═"*(len(plain)+padding*2)

    top = f"{PURPLE}╔{border}╗{RESET}"
    mid = f"{PURPLE}║{' '*padding}{colored}{' '*padding}║{RESET}"
    bot = f"{PURPLE}╚{border}╝{RESET}"

    return [
        left_align(top),
        left_align(mid),
        left_align(bot)
    ]


# =============================
# o player em si
# =============================

def run():

    lyrics = load_lyrics()

    total = lyrics[-1][0] + 5

    start = time.time()

    frame = 0

    hide_cursor()

    print("\n"*40)

    try:

        while True:

            move_cursor_top()

            elapsed = time.time() - start

            current = 0

            for i,(t,_) in enumerate(lyrics):
                if elapsed >= t:
                    current = i

            buffer = []

            buffer += [""] + title_box() + [""]

            buffer.append(progress_bar(elapsed,total))
            buffer.append("")

            buffer.append(vinyl(frame))
            buffer.append("")

            buffer.append(visualizer())
            buffer.append("")

            buffer.append(left_align(GRAY+"──────────── ✦ ────────────"+RESET))
            buffer.append("")


            if 0 <= current < len(lyrics):

                line = f"{PURPLE_LIGHT}\033[1m{lyrics[current][1]}{RESET}"
                buffer.append(left_align(line))


            for i in range(1,4):

                if current + i < len(lyrics):

                    next_line = f"{GRAY}{lyrics[current+i][1]}{RESET}"
                    buffer.append(left_align(next_line))

            sys.stdout.write("\n".join(buffer))
            sys.stdout.flush()

            if elapsed >= total:
                break

            frame += 1
            time.sleep(0.08)

    finally:
        show_cursor()
        print("\nEncerrado.")


if __name__ == "__main__":
    run()