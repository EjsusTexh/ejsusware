#!/usr/bin/env python3
"""EJSUSWARE v2.0 - UI-only novelty terminal interface.

Cross-platform (Linux / Windows / macOS), zero dependencies.
Everything shown here is simulated; no real action is ever performed.
"""
import os
import random
import re
import sys
import time

VERSION = "2.0.0"

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

IS_TTY = bool(sys.stdout.isatty())


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


# --- shared helpers --------------------------------------------------------

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def fake_bar(label, total=22, delay=0.04):
    print(f"  {label}")
    if not IS_TTY:
        print(f"  [{GREEN}{'█' * total}{RESET}] 100%")
        return
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


def stats_box(rows):
    bar = "═" * (BOX_W - 2)
    print(f" {CYAN}╔{bar}╗{RESET}")
    for key, val in rows:
        print(f" {CYAN}║{RESET} " + _pad(f"  {key}: {val}", 58) + f" {CYAN}║{RESET}")
    print(f" {CYAN}╚{bar}╝{RESET}")


def fake_ip():
    return f"{random.randint(11, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def fake_key():
    return "".join(random.choice("0123456789ABCDEF") for _ in range(32))


def wait_enter(msg="Press Enter to continue..."):
    try:
        input(f"\n  {GRAY}{msg}{RESET}")
    except EOFError:
        print()


def get_input(prompt, default):
    try:
        val = input(prompt).strip()
    except EOFError:
        return default
    return val or default


def sim_header(label):
    clear()
    print(render_title("EJSUSWARE"))
    print()
    print(f"  {GRAY}v{VERSION} · UI-ONLY · {label}{RESET}")
    print()


# --- simulation engine -----------------------------------------------------

def ts():
    return time.strftime("%H:%M:%S")


def log_line(level, msg, color=GREEN):
    print(f"  {GRAY}[{ts()}]{RESET} {color}{level:<5}{RESET} {color}{msg}{RESET}")
    time.sleep(0.12)


def hexdump(n=64, title="hex dump [SIM]:"):
    print(f"  {GRAY}{title}{RESET}")
    data = bytes(random.getrandbits(8) for _ in range(n))
    for off in range(0, len(data), 16):
        chunk = data[off:off + 16]
        hexs = " ".join(f"{b:02x}" for b in chunk)
        asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        print(f"  {GRAY}{off:08x}{RESET}  {hexs:<47}  {GREEN}{asc}{RESET}")
    print()


def simulate_attack(name, target, phases, stats):
    sim_header(f"SIMULATED ATTACK — {name}")
    print(f"  {RED}{BOLD}[ TARGET ACQUIRED ]{RESET} {BRIGHT_RED}{target}{RESET} {GRAY}[SIM]{RESET}")
    print()
    for label, logs in phases:
        fake_bar(label)
        for level, msg in logs:
            log_line(level, msg)
        print()
    hexdump(48, "captured payload sample [SIM]:")
    stats_box([(k, str(v)) for k, v in stats])
    print()
    print(f"  {BRIGHT_YELLOW}[!] SIMULATION ONLY — no real action was performed.{RESET}")
    wait_enter()


def run_submenu(title, items):
    while True:
        clear()
        print(render_title("EJSUSWARE"))
        print()
        print(f"  {GRAY}v{VERSION} · UI-ONLY · {title}{RESET}")
        print()
        rows = [f"  [{BRIGHT_CYAN}{num}{RESET}] {label}" for num, label, _ in items]
        rows += ["", f"  [{GRAY}0{RESET}] Back to main menu"]
        panel_box(title, rows)
        try:
            choice = input(f"\n  {BRIGHT_CYAN}panel{RESET}{GRAY}>{RESET} ").strip()
        except EOFError:
            return
        if choice in ("0", ""):
            return
        for num, label, handler in items:
            if choice == num:
                handler()
                break
        else:
            print(f"\n  {RED}[!] Invalid option — choose 0-{len(items)}.{RESET}")
            time.sleep(0.9)


# --- boot sequence ---------------------------------------------------------

OPERATOR = "operator"


def boot_sequence():
    global OPERATOR
    clear()
    print(f"  {BRIGHT_RED}{BOLD}EJSUSWARE CORE BOOTLOADER{RESET} {GRAY}v{VERSION}{RESET}")
    print(f"  {GRAY}{'─' * 58}{RESET}")
    print()
    checks = [
        ("core kernel module", "v2.0.1", "OK", GREEN),
        ("crypto engine", "AES-256 [SIM]", "OK", GREEN),
        ("packet forge layer", "loaded", "OK", GREEN),
        ("stealth engine", "hidden", "OK", GREEN),
        ("ui renderer", "active", "OK", GREEN),
        ("real payloads", "none found", "WRN", BRIGHT_YELLOW),
    ]
    for name, detail, status, color in checks:
        print(f"  {GRAY}[{color}{status}{GRAY}]{RESET} {name:<22} {GRAY}{detail}{RESET}")
        time.sleep(0.3)
    print()
    fake_bar("initializing core modules", total=18, delay=0.05)
    print()
    OPERATOR = get_input(f"  {GRAY}operator handle [Enter = operator]{RESET}: ", "operator")
    print()
    print(f"  {BRIGHT_GREEN}[*] ACCESS GRANTED — welcome back, {OPERATOR}.{RESET}")
    time.sleep(0.9)
    print()
    for row in render_title("EJSUSWARE").splitlines():
        print(row)
        time.sleep(0.1)
    wait_enter()


# --- panel 1: DDoS engine --------------------------------------------------

def ddos_tcp():
    target = get_input(f"  {GRAY}target IP [Enter = random]{RESET}: ", "") or fake_ip()
    simulate_attack(
        "TCP SYN FLOOD", target,
        [("spoofing source addresses",
          [("INF", "interface eth0 → promiscuous mode"),
           ("INF", "raw socket layer bound"),
           ("OK", f"source pool: {random.randint(50, 500)} addresses generated")]),
         ("filling target syn queue",
          [("INF", f"handshake storm → {target}:{random.randint(1, 65535)}"),
           ("OK", "syn packets in flight"),
           ("INF", "half-open queue rising")]),
         ("launching flood loop",
          [("INF", f"rate: {random.randint(5000, 80000):,} pkt/s"),
           ("OK", "flood loop stable [SIM]"),
           ("WRN", "loop terminated by operator (simulated)")])],
        [("target", f"{target} [SIM]"),
         ("method", "TCP SYN"),
         ("duration", f"{random.randint(10, 300)}s"),
         ("packets", f"{random.randint(100000, 9000000):,}")],
    )


def ddos_udp():
    target = get_input(f"  {GRAY}target IP [Enter = random]{RESET}: ", "") or fake_ip()
    simulate_attack(
        "UDP FLOOD", target,
        [("resolving reflectors",
          [("INF", f"reflector pool: {random.randint(20, 200)} nodes [SIM]"),
           ("OK", "amplification candidates selected")]),
         ("sending amplification queries",
          [("INF", f"queries → {target}:{random.randint(1, 65535)}"),
           ("INF", "spoofed source: target address"),
           ("OK", "reflection in progress")]),
         ("launching flood loop",
          [("INF", f"rate: {random.randint(20000, 120000):,} pkt/s"),
           ("OK", "flood loop stable [SIM]"),
           ("WRN", "loop terminated by operator (simulated)")])],
        [("target", f"{target} [SIM]"),
         ("method", "UDP amplification"),
         ("duration", f"{random.randint(10, 300)}s"),
         ("bandwidth", f"{random.randint(50, 900)} Mb/s")],
    )


def ddos_http():
    target = get_input(f"  {GRAY}target URL [Enter = random]{RESET}: ", "") or f"http://{fake_ip()}"
    simulate_attack(
        "HTTP LAYER-7 FLOOD", target,
        [("rotating bot nodes",
          [("INF", f"bot nodes online: {random.randint(500, 8000):,} [SIM]"),
           ("INF", "user-agent pool rotating"),
           ("OK", "nodes synchronized")]),
         ("flooding endpoints",
          [("INF", f"GET {target}/index.php?..."),
           ("INF", "request rate climbing"),
           ("OK", "layer-7 pressure applied")]),
         ("launching flood loop",
          [("INF", f"rate: {random.randint(5000, 60000):,} req/s"),
           ("OK", "flood loop stable [SIM]"),
           ("WRN", "loop terminated by operator (simulated)")])],
        [("target", f"{target} [SIM]"),
         ("method", "HTTP GET flood"),
         ("duration", f"{random.randint(10, 300)}s"),
         ("requests", f"{random.randint(100000, 9000000):,}")],
    )


def ddos_slow():
    target = get_input(f"  {GRAY}target URL [Enter = random]{RESET}: ", "") or f"http://{fake_ip()}"
    simulate_attack(
        "SLOWLORIS", target,
        [("opening sockets slowly",
          [("INF", f"opening connections → {target}"),
           ("INF", "partial headers trickling out [SIM]"),
           ("OK", "connections held open")]),
         ("holding connections",
          [("INF", f"active sockets: {random.randint(500, 3000):,}"),
           ("INF", "keep-alive pings every 10s"),
           ("OK", "target max-connections approaching")]),
         ("maintaining siege",
          [("INF", "siege stable [SIM]"),
           ("WRN", "siege lifted by operator (simulated)")])],
        [("target", f"{target} [SIM]"),
         ("method", "Slowloris"),
         ("duration", f"{random.randint(30, 600)}s"),
         ("sockets", f"{random.randint(500, 3000):,}")],
    )


def panel_ddos():
    run_submenu("DDoS ATTACK ENGINE", [
        ("1", "TCP SYN Flood", ddos_tcp),
        ("2", "UDP Flood", ddos_udp),
        ("3", "HTTP Layer-7 Flood", ddos_http),
        ("4", "Slowloris", ddos_slow),
    ])


# --- panel 2: ransomware builder -------------------------------------------

FILES = [
    "documents/tax_2025.pdf", "photos/vacation.jpg", "work/project_secrets.zip",
    "documents/passwords.txt", "music/playlist.m3u", "videos/family.mp4",
    "work/salary_2025.xlsx", "documents/contract.pdf",
]


def ransom_build(mode, note, amount):
    sim_header(f"RANSOMWARE BUILDER — {mode} MODE")
    print(f"  {GRAY}note: “{note[:36]}” · amount: {amount} BTC{RESET}")
    print()
    fake_bar("generating session key")
    key = fake_key()
    log_line("INF", "key-gen: RSA-2048 [SIM]")
    log_line("OK", f"session key: {key}")
    print()
    fake_bar("packing locker payload")
    log_line("INF", "packer: stub compression [SIM]")
    log_line("INF", "obfuscator: control flow flattening")
    log_line("OK", "payload packed")
    print()
    fake_bar("encrypting files")
    for f in FILES:
        log_line("INF", f"C:/Users/victim/{f} → C:/Users/victim/{f}.ejsus")
    print()
    stats_box([
        ("mode", mode),
        ("session key", key),
        ("files encrypted", f"{len(FILES)} [SIM]"),
        ("ransom amount", f"{amount} BTC"),
        ("note", "read_me.txt"),
    ])
    print()
    print(f"  {BRIGHT_YELLOW}[!] SIMULATION ONLY — no real action was performed.{RESET}")
    wait_enter()


def panel_ransom():
    def quick():
        ransom_build("QUICK", "YOUR FILES ARE ENCRYPTED. PAY TO DECRYPT.", "0.5")

    def stealth():
        ransom_build("STEALTH", "WE HAVE YOUR DATA. DO NOT CONTACT ANYONE.", "1.0")

    def custom():
        note = get_input(f"  {GRAY}ransom note [Enter = default]{RESET}: ",
                         "YOUR FILES ARE ENCRYPTED.")
        amount = get_input(f"  {GRAY}amount (BTC) [Enter = 0.5]{RESET}: ", "0.5")
        ransom_build("CUSTOM", note, amount)

    run_submenu("RANSOMWARE BUILDER", [
        ("1", "Quick Build", quick),
        ("2", "Stealth Build", stealth),
        ("3", "Custom Config", custom),
    ])


# --- panel 3: keylogger ----------------------------------------------------

LOWER = list("abcdefghijklmnopqrstuvwxyz")
UPPER = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
DIGIT = list("0123456789")
SYM = list(" .,!?")
POOL = LOWER + UPPER + DIGIT + SYM
WEIGHTS = [4] * 26 + [1] * 26 + [3] * 10 + [8, 8, 4, 4, 2]


def keylog_capture():
    sim_header("KEYLOGGER — LIVE CAPTURE")
    print(f"  {GRAY}[*] live capture stream [SIM] — Ctrl+C stops early{RESET}")
    print()
    count = 0
    try:
        while count < 150:
            print(random.choices(POOL, weights=WEIGHTS, k=1)[0], end="", flush=True)
            time.sleep(random.uniform(0.02, 0.08))
            count += 1
            if count % 40 == 0:
                print()
    except KeyboardInterrupt:
        print()
    print()
    print(f"  {BRIGHT_GREEN}[*] capture flushed → /tmp/.sys/cap.log [SIM]{RESET}")
    print()
    stats_box([
        ("keystrokes", str(count)),
        ("buffer", "/tmp/.sys/cap.log"),
        ("clipboard", "off"),
        ("screenshots", "off [SIM]"),
    ])
    print()
    print(f"  {BRIGHT_YELLOW}[!] SIMULATION ONLY — keys shown are random.{RESET}")
    wait_enter()


def keylog_view():
    sim_header("KEYLOGGER — BUFFER VIEW")
    print(f"  {GRAY}[*] buffer: /tmp/.sys/cap.log [SIM]{RESET}")
    print()
    hexdump(96, "buffer contents [SIM]:")
    wait_enter()


def keylog_exfil():
    sim_header("KEYLOGGER — EXFILTRATION")
    print(f"  {GRAY}[*] drop zone: {fake_ip()}:443 [SIM]{RESET}")
    print()
    fake_bar("establishing upload channel")
    log_line("INF", "tls handshake → drop zone")
    log_line("OK", "channel established")
    print()
    fake_bar("compressing buffer")
    log_line("INF", f"buffer size: {random.randint(4, 90)} KB")
    log_line("OK", "compression complete")
    print()
    fake_bar("uploading")
    log_line("INF", "chunked upload in progress [SIM]")
    log_line("OK", "buffer delivered to drop zone")
    print()
    stats_box([
        ("drop zone", f"{fake_ip()}:443 [SIM]"),
        ("bytes sent", f"{random.randint(4000, 90000):,}"),
        ("interval", "60s"),
    ])
    print()
    print(f"  {BRIGHT_YELLOW}[!] SIMULATION ONLY — no real action was performed.{RESET}")
    wait_enter()


def panel_keylogger():
    run_submenu("KEYLOGGER", [
        ("1", "Start Capture", keylog_capture),
        ("2", "View Buffer", keylog_view),
        ("3", "Exfiltrate", keylog_exfil),
    ])


# --- panel 4: credential stealer -------------------------------------------

BROWSERS = ["Chrome", "Firefox", "Edge", "Opera", "Brave"]


def steal_scan():
    sim_header("CREDENTIAL STEALER — BROWSER SCAN")
    print(f"  {GRAY}[*] scanning installed browsers [SIM]{RESET}")
    print()
    total = 0
    for b in BROWSERS:
        log_line("INF", f"scanning {b} profile")
        time.sleep(0.15)
        n = random.randint(5, 120)
        total += n
        log_line("OK", f"{b}: {n} credentials found")
    print()
    stats_box([
        ("browsers scanned", str(len(BROWSERS))),
        ("credentials", f"{total} [SIM]"),
        ("master key", "decrypted [SIM]"),
    ])
    print()
    print(f"  {BRIGHT_YELLOW}[!] SIMULATION ONLY — no real action was performed.{RESET}")
    wait_enter()


def steal_cookies():
    sim_header("CREDENTIAL STEALER — COOKIE DUMP")
    print(f"  {GRAY}[*] dumping session cookies [SIM]{RESET}")
    print()
    for b in BROWSERS:
        log_line("INF", f"{b}: sqlite decryption")
        time.sleep(0.15)
        log_line("OK", f"{b}: {random.randint(50, 900)} cookies dumped")
    print()
    hexdump(64, "cookie jar sample [SIM]:")
    stats_box([
        ("cookies", f"{random.randint(500, 4000):,} [SIM]"),
        ("sessions", f"{random.randint(10, 80)} active"),
        ("output", "/tmp/.sys/cookies.json"),
    ])
    print()
    print(f"  {BRIGHT_YELLOW}[!] SIMULATION ONLY — no real action was performed.{RESET}")
    wait_enter()


def steal_wallets():
    sim_header("CREDENTIAL STEALER — WALLET GRAB")
    print(f"  {GRAY}[*] locating crypto wallets [SIM]{RESET}")
    print()
    wallets = ["wallet.dat", "metamask vault", "electrum wallet", "exodus wallet"]
    for w in wallets:
        log_line("INF", f"locating {w}")
        time.sleep(0.15)
        log_line("OK", f"{w}: 0.00000000 BTC (empty) [SIM]")
    print()
    stats_box([
        ("wallets found", f"{len(wallets)} [SIM]"),
        ("balance", "0.00000000 BTC"),
        ("seed phrases", "0"),
    ])
    print()
    print(f"  {BRIGHT_YELLOW}[!] SIMULATION ONLY — no real action was performed.{RESET}")
    wait_enter()


def panel_stealer():
    run_submenu("CREDENTIAL STEALER", [
        ("1", "Scan Browsers", steal_scan),
        ("2", "Dump Cookies", steal_cookies),
        ("3", "Grab Wallets", steal_wallets),
    ])


# --- panel 5: RAT controller -----------------------------------------------

def rat_listener():
    port = get_input(f"  {GRAY}listen port [Enter = random]{RESET}: ", "") or str(random.randint(1024, 65535))
    simulate_attack(
        "RAT LISTENER", f"0.0.0.0:{port}",
        [("binding listener socket",
          [("INF", f"0.0.0.0:{port} → bound"),
           ("OK", "listener active")]),
         ("awaiting beacon",
          [("INF", "listening for incoming beacons [SIM]"),
           ("OK", f"beacon received from {fake_ip()}")])],
        [("bind", f"0.0.0.0:{port}"),
         ("protocol", "TCP"),
         ("beacons", str(random.randint(1, 40)))],
    )


def rat_beacons():
    sim_header("RAT CONTROLLER — BEACON LIST")
    print(f"  {GRAY}[*] live beacons [SIM]:{RESET}")
    print()
    beacons = random.randint(4, 9)
    for i in range(beacons):
        log_line("INF", f"#{i + 1:03d}  {fake_ip():<15}  win10  x64  latency {random.randint(20, 300)}ms")
    print()
    stats_box([
        ("active beacons", str(beacons)),
        ("c2 channel", "encrypted [SIM]"),
        ("heartbeat", "10s"),
    ])
    print()
    print(f"  {BRIGHT_YELLOW}[!] SIMULATION ONLY — no real action was performed.{RESET}")
    wait_enter()


def rat_shell():
    host = fake_ip()
    sim_header("RAT CONTROLLER — REMOTE SHELL")
    print(f"  {BRIGHT_GREEN}[+] session established → {host} [SIM]{RESET}")
    print(f"  {GRAY}type 'help' for commands · 'exit' to disconnect{RESET}")
    print()
    while True:
        try:
            cmd = input(f"  {GREEN}shell@{host}{RESET} {GRAY}#{RESET} ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if cmd in ("exit", "quit", "back"):
            print(f"  {GRAY}[*] session closed [SIM]{RESET}")
            break
        elif cmd == "help":
            print(f"  {GRAY}  help · sysinfo · whoami · ls · ps · shot · exit{RESET}")
        elif cmd == "sysinfo":
            print()
            stats_box([
                ("hostname", "VICTIM-PC [SIM]"),
                ("os", "Windows 10 Pro x64"),
                ("cpu", "Intel Core i7-9700K"),
                ("ram", "16 GB"),
                ("user", "victim-admin"),
                ("ip", host),
            ])
            print()
        elif cmd == "whoami":
            print(f"  victim-admin [SIM]")
        elif cmd == "ls":
            for f in ["Documents", "Desktop", "Downloads", "bank_details.txt",
                      "passwords.xlsx", "vacation.jpg"]:
                print(f"  {GREEN}{f}{RESET}")
        elif cmd == "ps":
            for p in ["explorer.exe", "chrome.exe", "svchost.exe",
                      "ejsus-core.exe [SIM]", "taskmgr.exe"]:
                print(f"  {GREEN}{p}{RESET}")
        elif cmd in ("shot", "screenshot"):
            print(f"  {BRIGHT_GREEN}[+] screenshot saved → /tmp/shot_{random.randint(1000, 9999)}.png [SIM]{RESET}")
        elif cmd == "":
            continue
        else:
            print(f"  {RED}[!] '{cmd}': command not found — type 'help'{RESET}")
    wait_enter()


def panel_rat():
    run_submenu("RAT CONTROLLER", [
        ("1", "Open Listener", rat_listener),
        ("2", "List Beacons", rat_beacons),
        ("3", "Interact (Fake Shell)", rat_shell),
    ])


# --- main loop -------------------------------------------------------------

def main():
    boot_sequence()
    try:
        while True:
            clear()
            print(render_title("EJSUSWARE"))
            print()
            print(f"  {GRAY}v{VERSION} · UI-ONLY TERMINAL · operator: {OPERATOR}{RESET}")
            print()
            draw_menu()
            try:
                choice = input(f"\n  {BRIGHT_CYAN}EJSUSWARE{RESET}{GRAY}>{RESET} ").strip().lower()
            except EOFError:
                choice = "0"
            if choice in ("0", "q", "exit", "quit"):
                break
            panels = {
                "1": panel_ddos,
                "2": panel_ransom,
                "3": panel_keylogger,
                "4": panel_stealer,
                "5": panel_rat,
            }
            if choice in panels:
                panels[choice]()
            else:
                print(f"\n  {RED}[!] Invalid option — choose 0-5.{RESET}")
                time.sleep(0.9)
    except KeyboardInterrupt:
        print()
    print(f"\n  {BRIGHT_GREEN}[*] EJSUSWARE terminated.{RESET}\n")


if __name__ == "__main__":
    main()
