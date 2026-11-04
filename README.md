# EJSUSWARE

**UI-only novelty terminal interface** — cross-platform (Linux / Windows / macOS), zero dependencies.

> ⚠️ **Disclaimer:** This project is a visual prop for entertainment. It contains **no real malware
> functionality** — nothing is attacked, encrypted, logged or stolen. Every output is simulated.

## Features

- **3D block-style `EJSUSWARE` title** — horizontal color gradient + drop shadow, revealed row-by-row
- **Fake boot sequence** — module checks, progress bar, operator handle, "ACCESS GRANTED"
- Classic "malware toolkit" main menu with **5 panels**, each with its own **sub-menu**
- Timestamped fake logs, animated progress bars, random **hex dumps** and stats tables
- **Interactive fake remote shell** (RAT panel) — `help`, `sysinfo`, `whoami`, `ls`, `ps`, `shot`
- **Live fake keystroke stream** (Keylogger panel) — random keys, Ctrl+C stops early
- Works on any terminal with ANSI support (Windows Terminal / CMD on Win10+, all Linux terminals)
- No third-party packages — pure Python standard library

## Requirements

- Python 3.8+

## Install & Run

### Linux

```bash
git clone https://github.com/EjsusTexh/ejsusware.git
cd ejsusware
python3 ejsusware.py
```

### Windows

```powershell
git clone https://github.com/EjsusTexh/ejsusware.git
cd ejsusware
python ejsusware.py
```

## Usage

- Select a panel with keys `1` – `5`, then pick a sub-option
- Press `0` to go back or exit
- Each simulation runs fake animations and returns with `Enter`

## Panels (UI only)

| Key | Panel               | Sub-options                                                        |
|-----|---------------------|--------------------------------------------------------------------|
| 1   | DDoS Engine         | TCP SYN Flood · UDP Flood · HTTP Layer-7 Flood · Slowloris         |
| 2   | Ransomware Builder  | Quick Build · Stealth Build · Custom Config (note + BTC amount)    |
| 3   | Keylogger           | Start Capture (live stream) · View Buffer (hex dump) · Exfiltrate  |
| 4   | Credential Stealer  | Scan Browsers · Dump Cookies · Grab Wallets                        |
| 5   | RAT Controller      | Open Listener · List Beacons · Interact (fake shell)               |

## Preview

```
  EJSUSWARE CORE BOOTLOADER v2.0.0
  ──────────────────────────────────────────────────────────

  [OK] core kernel module     v2.0.1
  [OK] crypto engine          AES-256 [SIM]
  [OK] packet forge layer     loaded
  [OK] stealth engine         hidden
  [OK] ui renderer            active
  [WRN] real payloads          none found

  initializing core modules
  [██████████████████] 100%

  operator handle [Enter = operator]:
  [*] ACCESS GRANTED — welcome back, root.

█████    ███   ████  █   █   ████  █   █   ███   ████   █████
█░░░░░    █░░ █ ░░░░ █░  █░ █ ░░░░ █░  █░ █ ░░█  █░░░█  █░░░░░
█░        █░  █░     █░  █░ █░     █░  █░ █░  █░ █░  █░ █░
████      █░   ███   █░  █░  ███   █░█ █░ █████░ ████ ░ ████
█░░░░     █░    ░░█  █░  █░   ░░█  █░█░█░ █░░░█░ █░█░░  █░░░░
█░     █  █░      █░ █░  █░     █░ █░█░█░ █░  █░ █░ █   █░
█████   ██ ░  ████ ░  ███ ░ ████ ░  █ █ ░ █░  █░ █░  █  █████

 ╔══════════════════════════════════════════════════════════╗
 ║                    EJSUSWARE MAIN MENU                     ║
 ╠══════════════════════════════════════════════════════════╣
 ║                                                            ║
 ║   [1] DDoS Engine                           FLOOD PANEL 01 ║
 ║   [2] Ransomware Builder                  CRYPTER PANEL 02 ║
 ║   [3] Keylogger                           CAPTURE PANEL 03 ║
 ║   [4] Credential Stealer                  HARVEST PANEL 04 ║
 ║   [5] RAT Controller                       REMOTE PANEL 05 ║
 ║                                                            ║
 ║   [0] Exit                                       TERMINATE ║
 ╚══════════════════════════════════════════════════════════╝

  EJSUSWARE>
```

## Environment variables

| Variable        | Effect                            |
|-----------------|-----------------------------------|
| `NO_COLOR=1`    | Disable all colors                |
| `FORCE_COLOR=1` | Force colors when output is piped |

## License

Choose a license that fits your needs (e.g. MIT) before publishing.
