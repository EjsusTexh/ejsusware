#!/usr/bin/env python3
"""EJSUSWARE - UI-only novelty terminal interface.

Cross-platform (Linux / Windows / macOS), zero dependencies.
Everything shown here is simulated; no real action is ever performed.
"""
import os
import random
import re
import sys
import time

# --- terminal / color support ---------------------------------------------

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

if os.name == "nt":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass

USE_COLOR = bool(sys.stdout.isatty() or os.environ.get("FORCE_COLOR"))
if os.environ.get("NO_COLOR") or os.environ.get("TERM") == "dumb":
    USE_COLOR = False


def _c(code):
    return code if USE_COLOR else ""


RESET = _c("\x1b[0m")
BOLD = _c("\x1b[1m")
GRAY = _c("\x1b[90m")
RED = _c("\x1b[31m")
GREEN = _c("\x1b[32m")
YELLOW = _c("\x1b[33m")
CYAN = _c("\x1b[36m")
BRIGHT_RED = _c("\x1b[91m")
BRIGHT_GREEN = _c("\x1b[92m")
BRIGHT_YELLOW = _c("\x1b[93m")
BRIGHT_CYAN = _c("\x1b[96m")


def c256(n):
    return f"\x1b[38;5;{n}m" if USE_COLOR else ""


_ESC = re.compile(r"\x1b\[[0-9;]*m")


def _vis(s):
    return _ESC.sub("", s)


def _pad(s, width, align_left=True):
    pad = max(width - len(_vis(s)), 0)
    return s + " " * pad if align_left else " " * pad + s


# --- 3D block title --------------------------------------------------------

FONT = {
    "E": [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111],
    "J": [0b00111, 0b00010, 0b00010, 0b00010, 0b00010, 0b10010, 0b01100],
    "S": [0b01111, 0b10000, 0b10000, 0b01110, 0b00001, 0b00001, 0b11110],
    "U": [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "W": [0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b10101, 0b01010],
    "A": [0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    "R": [0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001],
}


def _seg(a, b, n):
    return [int(a + (b - a) * i / n) for i in range(n)]


def _ramp(*anchors):
    ramp = []
    for a, b in zip(anchors, anchors[1:]):
        ramp += _seg(a, b, 3)
    return ramp


GRADIENT = _ramp(21, 39, 51, 46, 82, 118, 154, 190, 226, 220, 214, 208, 202, 196)


def render_title(text):
    letters = [FONT[ch] for ch in text.upper() if ch in FONT]
    if not letters:
        return text
    w = len(letters) * 5 + (len(letters) - 1) * 2
    W, H = w + 2, 8
    face = [[" "] * W for _ in range(H)]
    shadow = [[" "] * W for _ in range(H)]
    x = 0
    for letter in letters:
        for row in range(7):
            for col in range(5):
                if letter[row] & (0b10000 >> col):
                    face[row][x + col] = "█"
                    shadow[row + 1][x + col + 1] = "░"
        x += 7
    lines = []
    for row in range(7):
        out = []
        for col in range(W):
            if face[row][col] != " ":
                idx = min(col * len(GRADIENT) // W, len(GRADIENT) - 1)
                out.append(c256(GRADIENT[idx]) + BOLD + "█")
            elif shadow[row][col] != " ":
                out.append(c256(238) + "░")
            else:
                out.append(" ")
        lines.append("".join(out).rstrip() + RESET)
    return "\n".join(lines)


# --- main menu -------------------------------------------------------------

BOX_W = 60
OPTIONS = [
    ("1", "DDoS Engine", "FLOOD PANEL 01"),
    ("2", "Ransomware Builder", "CRYPTER PANEL 02"),
    ("3", "Keylogger", "CAPTURE PANEL 03"),
    ("4", "Credential Stealer", "HARVEST PANEL 04"),
    ("5", "RAT Controller", "REMOTE PANEL 05"),
]


def _box_row(left="", right=""):
    return f" {CYAN}║{RESET} " + _pad(left, 38) + _pad(right, 20, False) + f" {CYAN}║{RESET}"


def draw_menu():
    bar = "═" * (BOX_W - 2)
    print(f" {CYAN}╔{bar}╗{RESET}")
    title = "EJSUSWARE MAIN MENU"
    pad_l = (58 - len(title)) // 2
    pad_r = 58 - len(title) - pad_l
    print(
        f" {CYAN}║{RESET} "
        + " " * pad_l + BRIGHT_RED + BOLD + title + RESET + " " * pad_r
        + f" {CYAN}║{RESET}"
    )
    print(f" {CYAN}╠{bar}╣{RESET}")
    print(_box_row())
    for num, name, tag in OPTIONS:
        print(_box_row(f"  [{BRIGHT_CYAN}{num}{RESET}] {name}", f"{GRAY}{tag}{RESET}"))
    print(_box_row())
    print(_box_row(f"  [{GRAY}0{RESET}] Exit", f"{GRAY}TERMINATE{RESET}"))
    print(f" {CYAN}╚{bar}╝{RESET}")


# --- fake panels -----------------------------------------------------------

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def fake_bar(label, total=22, delay=0.04):
    print(f"  {label}")
    for i in range(total + 1):
        pct = i * 100 // total
        print(
            f"\r  [{GREEN}{'█' * i}{RESET}{GRAY}{'░' * (total - i)}{RESET}] {pct:3d}%",
            end="", flush=True,
        )
        time.sleep(delay)
    print()


def panel_box(title, rows):
    bar = "═" * (BOX_W - 2)
    print(f" {CYAN}╔{bar}╗{RESET}")
    print(f" {CYAN}║{RESET} " + _pad(BRIGHT_RED + BOLD + title + RESET, 58) + f" {CYAN}║{RESET}")
    print(f" {CYAN}╠{bar}╣{RESET}")
    for row in rows:
        print(f" {CYAN}║{RESET} " + _pad(row, 58) + f" {CYAN}║{RESET}")
    print(f" {CYAN}╚{bar}╝{RESET}")


def fake_ip():
    return f"{random.randint(11, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def fake_key():
    return "".join(random.choice("0123456789ABCDEF") for _ in range(32))


def run_panel(num, title, modules, stages, stats):
    clear()
    print(render_title("EJSUSWARE"))
    print()
    print(f"  {GRAY}v1.0.0 · UI-ONLY · SIMULATED PANEL{RESET}")
    print()
    panel_box(f"{title} — PANEL 0{num}", [f"  [*] {m}" for m in modules])
    print()
    for stage in stages:
        fake_bar(stage)
    print()
    for line in stats:
        print(f"  {GREEN}[+] {line}{RESET}")
        time.sleep(0.25)
    print()
    print(f"  {BRIGHT_YELLOW}[!] SIMULATION ONLY — no real action was performed.{RESET}")
    try:
        input(f"\n  {GRAY}Press Enter to return to the main menu...{RESET}")
    except EOFError:
        print()


def panel_ddos():
    run_panel(
        1, "DDoS ATTACK ENGINE",
        ["target-resolver   state: armed",
         "botnet-link       state: linked [SIM]",
         "flood-socket      state: ready",
         "ip-spoofer        state: engaged"],
        ["resolving target host", "linking bot nodes [SIM]", "launching flood loop"],
        [f"target      : {fake_ip()} [SIM]",
         f"nodes       : {random.randint(800, 20000):,}",
         f"requests/s  : {random.randint(5000, 60000):,}",
         "status      : loop terminated (simulated)"],
    )


def panel_ransom():
    run_panel(
        2, "RANSOMWARE BUILDER",
        ["locker-core       state: loaded",
         "key-gen           state: ready",
         "packer            state: packed [SIM]",
         "ransom-note       state: generated"],
        ["generating session key", "packing locker payload", "compiling dropper"],
        [f"session key : {fake_key()}",
         f"payload size: {random.randint(2, 9)}.{random.randint(0, 9)} MB",
         "note        : read_me.txt [SIM]",
         "status      : build complete (simulated)"],
    )


def panel_keylogger():
    run_panel(
        3, "KEYLOGGER",
        ["hook-engine       state: injected [SIM]",
         "capture-buffer    state: active",
         "uploader          state: standby"],
        ["installing input hooks", "starting silent capture"],
        [f"keystrokes  : {random.randint(1200, 90000):,} [SIM]",
         "log file    : /tmp/.sys/cap.log",
         "upload      : every 60s (simulated)",
         "status      : capture stopped (simulated)"],
    )


def panel_stealer():
    run_panel(
        4, "CREDENTIAL STEALER",
        ["browser-scanner   state: scanning [SIM]",
         "cookie-dumper     state: active",
         "wallet-grab       state: idle",
         "uploader          state: standby"],
        ["scanning browser profiles", "dumping stored credentials"],
        [f"credentials : {random.randint(20, 500):,} [SIM]",
         f"cookies     : {random.randint(300, 5000):,}",
         f"target host : {fake_ip()}",
         "status      : dump complete (simulated)"],
    )


def panel_rat():
    run_panel(
        5, "RAT CONTROLLER",
        ["listener          state: bound [SIM]",
         "beacon-handler    state: active",
         "shell-bridge      state: linked",
         "persistence       state: waiting"],
        ["binding listener socket", "awaiting beacon [SIM]", "opening remote shell"],
        [f"session     : {fake_ip()}:{random.randint(1024, 65535)} [SIM]",
         f"beacons     : {random.randint(1, 40)}",
         "shell       : interactive (simulated)",
         "status      : session closed (simulated)"],
    )


# --- main loop -------------------------------------------------------------

def main():
    try:
        while True:
            clear()
            print(render_title("EJSUSWARE"))
            print()
            print(f"  {GRAY}v1.0.0 · UI-ONLY TERMINAL · LINUX / WINDOWS / macOS{RESET}")
            print()
            draw_menu()
            try:
                choice = input(f"\n  {BRIGHT_CYAN}EJSUSWARE{RESET}{GRAY}>{RESET} ").strip().lower()
            except EOFError:
                choice = "0"
            if choice in ("0", "q", "exit", "quit"):
                break
            if choice == "1":
                panel_ddos()
            elif choice == "2":
                panel_ransom()
            elif choice == "3":
                panel_keylogger()
            elif choice == "4":
                panel_stealer()
            elif choice == "5":
                panel_rat()
            else:
                print(f"\n  {RED}[!] Invalid option — choose 0-5.{RESET}")
                time.sleep(0.9)
    except KeyboardInterrupt:
        print()
    print(f"\n  {BRIGHT_GREEN}[*] EJSUSWARE terminated.{RESET}\n")


if __name__ == "__main__":
    main()
