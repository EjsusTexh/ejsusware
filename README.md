# EJSUSWARE

**UI-only novelty terminal interface** — cross-platform (Linux / Windows / macOS), zero dependencies.

> ⚠️ **Disclaimer:** This project is a visual prop for entertainment. It contains **no real malware
> functionality** — nothing is attacked, encrypted, logged or stolen. Every output is simulated.

## Features

- **3D block-style `EJSUSWARE` title** — rendered with a horizontal color gradient and a drop shadow
- Classic "malware toolkit" style main menu with **5 panels** (1-5)
- Animated fake progress bars and randomized fake stats for every panel
- Works on any terminal with ANSI support (Windows Terminal / CMD on Win10+, all Linux terminals)
- No third-party packages — pure Python standard library

## Requirements

- Python 3.8+

## Install & Run

### Linux

```bash
git clone https://github.com/<your-username>/ejsusware.git
cd ejsusware
python3 ejsusware.py
```

### Windows

```powershell
git clone https://github.com/<your-username>/ejsusware.git
cd ejsusware
python ejsusware.py
```

## Usage

- Select a panel with keys `1` – `5`
- Press `0` (or `q`) to exit
- Each panel runs a simulated animation and returns to the menu with `Enter`

## Panels (UI only)

| Key | Panel               | Simulated content                     |
|-----|---------------------|---------------------------------------|
| 1   | DDoS Engine         | flood loop, bot nodes, requests/s     |
| 2   | Ransomware Builder  | session key, payload packing          |
| 3   | Keylogger           | input hooks, silent capture           |
| 4   | Credential Stealer  | browser scan, credential dump         |
| 5   | RAT Controller      | listener, beacon, remote shell        |

## Preview

```
█████    ███   ████  █   █   ████  █   █   ███   ████   █████
█░░░░░    █░░ █ ░░░░ █░  █░ █ ░░░░ █░  █░ █ ░░█  █░░░█  █░░░░░
█░        █░  █░     █░  █░ █░     █░  █░ █░  █░ █░  █░ █░
████      █░   ███   █░  █░  ███   █░█ █░ █████░ ████ ░ ████
█░░░░     █░    ░░█  █░  █░   ░░█  █░█░█░ █░░░█░ █░█░░  █░░░░
█░     █  █░      █░ █░  █░     █░ █░█░█░ █░  █░ █░ █   █░
█████   ██ ░  ████ ░  ███ ░ ████ ░  █ █ ░ █░  █░ █░  █  █████

  v1.0.0 · UI-ONLY TERMINAL · LINUX / WINDOWS / macOS

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

| Variable      | Effect                            |
|---------------|-----------------------------------|
| `NO_COLOR=1`  | Disable all colors                |
| `FORCE_COLOR=1` | Force colors when output is piped |

## License

Choose a license that fits your needs (e.g. MIT) before publishing.
