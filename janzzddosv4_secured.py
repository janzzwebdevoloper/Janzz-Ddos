import os
import csv
import time
import random
import shutil
import platform
import re
import json
import ipaddress
from pathlib import Path
from datetime import datetime

# JANZZ NET-STRIKE v5.0 - ELITE CYBER OPERATIONS
VERSION = "5.0"
AUTHOR = "JANZZ"

REPORT_DIR = Path("janzz_lab_reports")
HISTORY_FILE = Path("janzz_history.json")
MAX_EVENTS = 1000
MAX_HISTORY = 20
COLORS_ENABLED = True

COLORS = {
    "RED": "\033[91m", "GREEN": "\033[92m", "BLUE": "\033[94m",
    "YELLOW": "\033[93m", "CYAN": "\033[96m", "PURPLE": "\033[95m",
    "WHITE": "\033[97m", "RESET": "\033[0m", "BOLD": "\033[1m",
}
SETTINGS = {"delay": 0.03, "show_events": True, "animation": True}
SESSION_HISTORY = []
LATEST_SESSION = None
TOTAL_SESSIONS = 0


def paint(text, color="WHITE"):
    return COLORS.get(color, "") + str(text) + COLORS["RESET"] if COLORS_ENABLED else str(text)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def terminal_width():
    return min(shutil.get_terminal_size((70, 20)).columns, 70)


def box_header(title):
    width = terminal_width()
    print(paint("╔" + "═" * (width - 2) + "╗", "CYAN"))
    print(paint("║ " + title.center(width - 4) + " ║", "WHITE"))
    print(paint("╚" + "═" * (width - 2) + "╝", "CYAN"))

def box_footer():
    width = terminal_width()
    print(paint("╚" + "═" * (width - 2) + "╝", "CYAN"))

def box_line():
    width = terminal_width()
    print(paint("╟" + "─" * (width - 2) + "╢", "CYAN"))

def box_text(text, color="WHITE", align="left"):
    width = terminal_width()
    if align == "center":
        print(paint("║ " + str(text).center(width - 4) + " ║", color))
    else:
        print(paint("║ " + str(text).ljust(width - 4) + " ║", color))


def pause():
    print()
    input(paint("  [ Tekan Enter untuk melanjutkan... ]", "YELLOW"))


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def type_text(text, delay=0.04, color="WHITE"):
    if not SETTINGS["animation"]:
        print(paint(text, color))
        return
    for char in text:
        print(paint(char, color), end="", flush=True)
        if char in ".!?":
            time.sleep(delay * 5)
        else:
            time.sleep(delay)
    print()


def animate_matrix():
    clear()
    chars = "01"
    for _ in range(15):
        line_str = "".join(random.choice(chars) if random.random() > 0.5 else " " for _ in range(terminal_width()))
        print(paint(line_str, "GREEN"))
        time.sleep(0.05)
    clear()


def animate_radar():
    if not SETTINGS["animation"]:
        return
    spinners = ['|', '/', '-', '\\']
    print(paint("\n  [*] Memindai jaringan lokal...", "CYAN"))
    for i in range(15):
        print(paint(f"\r      {spinners[i % 4]} Scanning...", "YELLOW"), end="", flush=True)
        time.sleep(0.1)
    print(paint("\r      [✓] Scan selesai. Sistem siap.       ", "GREEN"))


def save_history():
    try:
        with HISTORY_FILE.open("w", encoding="utf-8") as f:
            json.dump(SESSION_HISTORY, f, indent=4)
    except Exception:
        pass


def load_history():
    global SESSION_HISTORY, TOTAL_SESSIONS
    if HISTORY_FILE.exists():
        try:
            with HISTORY_FILE.open("r", encoding="utf-8") as f:
                SESSION_HISTORY = json.load(f)
                TOTAL_SESSIONS = len(SESSION_HISTORY)
        except Exception:
            SESSION_HISTORY = []
            TOTAL_SESSIONS = 0


def banner():
    colors = ["PURPLE", "CYAN", "GREEN", "YELLOW", "RED"]
    random_color = random.choice(colors)
    clear()
    print(paint(r"""
     ██╗ █████╗ ███╗   ██╗███████╗███████╗
     ██║██╔══██╗████╗  ██║╚══███╔╝╚══███╔╝
     ██║███████║██╔██╗ ██║  ███╔╝   ███╔╝
██   ██║██╔══██║██║╚██╗██║ ███╔╝   ███╔╝
╚█████╔╝██║  ██║██║╚████║███████╗███████╗
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
""", random_color))
    width = terminal_width()
    print(paint(" JANZZ NET-STRIKE ".center(width, " "), "WHITE"))
    print(paint(f" v{VERSION} - ELITE CYBER OPERATIONS ".center(width, " "), "YELLOW"))
    print(paint("═" * width, "CYAN"))
    print(paint("[ NETWORK: DISABLED ]".ljust(width//2) + "[ MODE: SIMULATION ]".rjust(width//2), "GREEN"))
    print(paint("═" * width, "CYAN"))


def login():
    """Offline demo: no hard-coded credentials or fake security gate."""
    print(paint("[i] Offline simulation mode. No login credentials are embedded.", "CYAN"))
    return True


def loading():
    if not SETTINGS["animation"]:
        print(paint("[+] Sistem siap.", "GREEN"))
        return
    banner()
    box_header(" SYSTEM BOOT ")
    box_text("[*] Menginisialisasi sistem...", "CYAN")
    time.sleep(0.3)
    box_text("[*] Memuat modul jaringan...", "CYAN")
    time.sleep(0.3)
    box_text("[*] Menyiapkan enkripsi lokal...", "CYAN")
    time.sleep(0.3)
    box_footer()
    
    print()
    for i in range(31):
        percent = int(i / 30 * 100)
        bar = "█" * i + "░" * (30 - i)
        print(paint(f"\r  [{bar}] {percent:3d}%", "GREEN"), end="", flush=True)
        time.sleep(0.02)
    print("\n\n" + paint("  [+] SYSTEM READY", "GREEN"))
    
    animate_radar()
    time.sleep(0.5)


def dashboard():
    banner()
    total_events = sum(item["total_events"] for item in SESSION_HISTORY)
    box_header(" SYSTEM DASHBOARD ")
    box_text(f"  Author          : {AUTHOR}")
    box_text(f"  Version         : {VERSION}")
    box_text(f"  Login           : {USER}")
    box_text("  Network         : DISABLED")
    box_text(f"  Runtime         : Python {platform.python_version()}")
    box_text(f"  Operating System: {platform.system()}")
    box_text(f"  Current Time    : {timestamp()}")
    box_line()
    box_text("             SESSION STATISTICS", "CYAN")
    box_text(f"  Total sessions  : {TOTAL_SESSIONS}")
    box_text(f"  Saved history   : {len(SESSION_HISTORY)}")
    box_text(f"  Recorded events : {total_events}")
    if LATEST_SESSION:
        box_text(f"  Last session    : {LATEST_SESSION['started_at']}")
        box_text(f"  Last label      : {LATEST_SESSION['target']}")
        box_text(f"  Last events     : {LATEST_SESSION['total_events']}")
    else:
        box_text("  Last session    : Belum ada")
    box_footer()
    pause()


def get_integer(prompt, default, minimum, maximum):
    while True:
        value = input(paint(f"  {prompt} [{default}]: ", "WHITE")).strip()
        if not value:
            return default
        try:
            number = int(value)
            if minimum <= number <= maximum:
                return number
        except ValueError:
            pass
        print(paint(f"  [!] Masukkan angka {minimum} sampai {maximum}.", "RED"))


def validate_target(target):
    try:
        ipaddress.ip_address(target)
        return True, "IPv4 Valid"
    except ValueError:
        if re.match(r"^[a-zA-Z0-9.-]+$", target):
            return True, "Domain Lokal Valid"
        return False, "Format tidak valid"


def configure_simulation():
    banner()
    box_header(" STRIKE CONFIGURATION ")
    box_text("Semua input hanya menjadi label lokal.", "WHITE")
    box_text("Format: IP (192.168.1.1) / Domain (test.local)", "YELLOW")
    box_footer()
    
    while True:
        print()
        target = input(paint("  Label target [LOCAL-LAB]: ", "CYAN")).strip() or "LOCAL-LAB"
        target = re.sub(r"[\x00-\x1f\x7f]", "", target)[:40]
        
        is_valid, msg = validate_target(target)
        if is_valid:
            print(paint(f"  [✓] {msg}", "GREEN"))
            break
        else:
            print(paint(f"  [!] {msg}. Coba lagi.", "RED"))

    print()
    port = get_integer("Label port", 80, 1, 65535)
    total = get_integer("Jumlah packet", 1000, 1, MAX_EVENTS)

    print()
    box_header(" SPEED SETTINGS ")
    box_text(" [1] Slow (0.10s)")
    box_text(" [2] Normal (0.03s)")
    box_text(" [3] Fast (0.005s)")
    box_text(" [4] Insane (0.00s)")
    box_footer()
    speed_choice = input(paint("  Pilihan [2]: ", "CYAN")).strip() or "2"
    speed_map = {"1": 0.10, "2": 0.03, "3": 0.005, "4": 0.0}
    if speed_choice not in speed_map:
        speed_choice = "2"
    delay = speed_map[speed_choice]

    print()
    box_header(" CONFIGURATION SUMMARY ")
    box_text(f"  Label      : {target}")
    box_text(f"  Port label : {port}")
    box_text(f"  Packets    : {total}")
    box_text(f"  Delay      : {delay} seconds")
    box_text("  Network    : DISABLED (OFFLINE SIMULATION)")
    box_footer()

    print()
    if input(paint("  Mulai eksekusi? (y/n): ", "YELLOW")).strip().lower() != "y":
        print(paint("  Dibatalkan.", "YELLOW"))
        time.sleep(0.7)
        return None
    return {"target": target, "port": port, "total": total, "delay": delay}


def generate_event(event_number, elapsed, config):
    event_types = ["TCP-SYN", "UDP-FLOOD", "HTTP-GET", "PING-OF-DEATH", "SSH-BRUTE"]
    status = random.choices(["NORMAL", "WARNING", "TEST"], weights=[75, 15, 10], k=1)[0]
    event_id = "".join(random.choices("0123456789ABCDEF", k=8))
    return {
        "time": timestamp(), "number": event_number,
        "event": random.choice(event_types), "status": status,
        "id": event_id, "elapsed_seconds": round(elapsed, 3),
        "target": config["target"], "port": config["port"],
    }


def draw_bar_chart(counts, total):
    print(paint("  [ GRAFIK STATISTIK ]", "CYAN"))
    max_width = terminal_width() - 20
    for status, count in counts.items():
        if total > 0:
            bar_len = int((count / total) * max_width)
        else:
            bar_len = 0
        bar = "█" * bar_len
        color = {"NORMAL": "GREEN", "WARNING": "YELLOW", "TEST": "PURPLE"}[status]
        print(paint(f"  {status:<7} | {bar} {count}", color))

def auto_export(report):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    file_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = REPORT_DIR / f"janzz_report_{file_stamp}.csv"
    txt_path = REPORT_DIR / f"janzz_report_{file_stamp}.txt"
    fields = ["time", "number", "event", "status", "id", "elapsed_seconds", "target", "port"]

    try:
        with csv_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(report["events"])

        with txt_path.open("w", encoding="utf-8") as file:
            file.write("JANZZ NET-STRIKE - OFFLINE REPORT\n")
            file.write("=" * 45 + "\n")
            file.write(f"Version      : {report['version']}\n")
            file.write(f"Target label : {report['target']}\n")
            file.write(f"Port label   : {report['port']}\n")
            file.write(f"Started      : {report['started_at']}\n")
            file.write(f"Finished     : {report['ended_at']}\n")
            file.write(f"Duration     : {report['duration']} seconds\n")
            file.write(f"Total packets: {report['total_events']}\n")
            file.write(f"Normal       : {report['counts']['NORMAL']}\n")
            file.write(f"Warning      : {report['counts']['WARNING']}\n")
            file.write(f"Test         : {report['counts']['TEST']}\n")
            file.write(f"Network      : {report['network']}\n")
            file.write("\nAll entries are locally generated simulation events.\n")
        return True
    except OSError:
        return False


def simulate():
    global LATEST_SESSION, TOTAL_SESSIONS
    config = configure_simulation()
    if config is None:
        pause()
        return

    banner()
    box_header(" [+] ATTACK INITIATED ")
    box_text(f"  Label       : {config['target']}")
    box_text(f"  Port label  : {config['port']}")
    box_text(f"  Total pkts  : {config['total']}")
    box_text(f"  Network     : DISABLED (OFFLINE SIMULATION)")
    box_footer()
    
    print()
    print(paint("  Simulasi dimulai dalam...", "YELLOW"))
    for i in range(3, 0, -1):
        print(paint(f"  >> {i} <<", "RED"))
        time.sleep(0.8)
    print(paint("  >> SIMULATION STARTED <<\n", "GREEN"))
    time.sleep(0.5)

    start_time = time.time()
    started_at = timestamp()
    events = []
    counts = {"NORMAL": 0, "WARNING": 0, "TEST": 0}
    spinners = ['|', '/', '-', '\\']

    try:
        for number in range(1, config["total"] + 1):
            elapsed = time.time() - start_time
            event = generate_event(number, elapsed, config)
            events.append(event)
            counts[event["status"]] += 1

            if SETTINGS["show_events"]:
                color = {"NORMAL": "GREEN", "WARNING": "YELLOW", "TEST": "PURPLE"}[event["status"]]
                status_line = paint(f"  [LIVE] N: {counts['NORMAL']} | W: {counts['WARNING']} | T: {counts['TEST']}", "CYAN")
                print(f"\r{status_line.ljust(terminal_width())}", end="", flush=True)
                
                print(paint(
                    f"\n  [PKT {number:05d}] [{event['status']}] {event['event']} "
                    f"| ID={event['id']} | {elapsed:.2f}s", color
                ), end="")
            else:
                percent = int(number / config["total"] * 100)
                width = 25
                filled = int(width * percent / 100)
                bar = "█" * filled + "░" * (width - filled)
                spin = spinners[number % len(spinners)]
                print(paint(f"\r  {spin} [{bar}] {percent:3d}% | Packets: {number}", "CYAN"), end="", flush=True)
            
            if config["delay"] > 0:
                time.sleep(config["delay"])
    except KeyboardInterrupt:
        print(paint("\n\n  [!] Dihentikan pengguna.", "YELLOW"))

    duration = time.time() - start_time
    report = {
        "version": VERSION, "target": config["target"], "port": config["port"],
        "started_at": started_at, "ended_at": timestamp(),
        "duration": round(duration, 3), "total_events": len(events),
        "counts": counts, "events": events,
        "network": "DISABLED - OFFLINE ONLY",
    }
    LATEST_SESSION = report
    TOTAL_SESSIONS += 1
    SESSION_HISTORY.append({
        "started_at": started_at, "target": config["target"], "port": config["port"],
        "total_events": len(events), "duration": round(duration, 3), "counts": counts.copy(),
    })
    if len(SESSION_HISTORY) > MAX_HISTORY:
        SESSION_HISTORY.pop(0)
        
    save_history()
    auto_export(report)
    
    print("\n")
    banner()
    box_header("          STRIKE REPORT ")
    box_text(f"  Label         : {report['target']}")
    box_text(f"  Port label    : {report['port']}")
    box_text(f"  Started       : {report['started_at']}")
    box_text(f"  Finished      : {report['ended_at']}")
    box_text(f"  Duration      : {report['duration']} seconds")
    box_text(f"  Total pkts    : {report['total_events']}")
    box_line()
    draw_bar_chart(report["counts"], report["total_events"])
    box_line()
    box_text("  [✓] OPERATION COMPLETE", "GREEN")
    box_text("  Network packets sent: 0")
    box_text("  Auto-Save Report    : YES", "CYAN")
    box_footer()
    pause()


def event_logs():
    banner()
    box_header("             PACKET LOG ")
    if not LATEST_SESSION:
        box_text("  Belum ada packet yang direkam.")
    else:
        events = LATEST_SESSION["events"]
        box_text(f"  Label: {LATEST_SESSION['target']}")
        box_text(f"  Total: {len(events)} packet")
        box_line()
        box_text("  20 packet terakhir:", "CYAN")
        for event in events[-20:]:
            box_text(f"  [{event['number']:05d}] {event['status']:<7} {event['event']:<14} ID={event['id']}")
    box_footer()
    pause()


def history_menu():
    banner()
    box_header("             SESSION HISTORY ")
    if not SESSION_HISTORY:
        box_text("  Riwayat masih kosong.")
    else:
        for index, item in enumerate(reversed(SESSION_HISTORY), start=1):
            box_text(
                f"  [{index:02d}] {item['started_at']} | {item['target']} "
                f"| {item['total_events']} pkt | {item['duration']}s"
            )
    box_footer()
    pause()


def settings_menu():
    global COLORS_ENABLED
    while True:
        banner()
        box_header("             SETTINGS ")
        box_text(f"  [1] Warna terminal : {'ON' if COLORS_ENABLED else 'OFF'}")
        box_text(f"  [2] Detail packet  : {'ON' if SETTINGS['show_events'] else 'OFF'}")
        box_text(f"  [3] Animasi        : {'ON' if SETTINGS['animation'] else 'OFF'}")
        box_text(f"  [4] Kecepatan      : {SETTINGS['delay']}s")
        box_text("  [5] Kembali")
        box_footer()
        choice = input(paint("  janzz@settings > ", "CYAN")).strip()

        if choice == "1":
            COLORS_ENABLED = not COLORS_ENABLED
        elif choice == "2":
            SETTINGS["show_events"] = not SETTINGS["show_events"]
        elif choice == "3":
            SETTINGS["animation"] = not SETTINGS["animation"]
        elif choice == "4":
            print()
            box_header(" SPEED SETTINGS ")
            box_text(" [1] Slow   = 0.10s")
            box_text(" [2] Normal = 0.03s")
            box_text(" [3] Fast   = 0.005s")
            box_text(" [4] Insane = 0.0s")
            box_footer()
            speed = input(paint("  Kecepatan: ", "CYAN")).strip()
            speed_map = {"1": 0.10, "2": 0.03, "3": 0.005, "4": 0.0}
            if speed in speed_map:
                SETTINGS["delay"] = speed_map[speed]
        elif choice == "5":
            break
        else:
            print(paint("  Pilihan tidak valid.", "RED"))
            time.sleep(0.7)


def about():
    banner()
    box_header("             ABOUT JANZZ LAB ")
    box_text("  Application : JANZZ NET-STRIKE")
    box_text(f"  Version     : {VERSION} - ELITE EDITION")
    box_text(f"  Author      : {AUTHOR}")
    box_text(f"  Python      : {platform.python_version()}")
    box_text(f"  Platform    : {platform.platform()}")
    box_text("  Network     : Disabled")
    box_text("  Events      : Locally generated")
    box_text(f"  Max packets : {MAX_EVENTS}")
    box_text(f"  Max history : {MAX_HISTORY}")
    box_line()
    box_text("  FITUR v5.0:", "YELLOW")
    box_text("  - UI Kotak Pro (ASCII Box)")
    box_text("  - Validasi IP / Domain Lokal")
    box_text("  - Grafik Bar Statistik")
    box_text("  - Animasi Matrix & Radar")
    box_text("  - Auto-Save report per eksekusi")
    box_text("  - History permanen (JSON)")
    box_footer()
    pause()


def main():
    load_history()
    animate_matrix()
    
    if not login():
        return
    loading()
    while True:
        banner()
        box_header("             MAIN MENU ")
        box_text("  [1] Dashboard")
        box_text("  [2] Jalankan Strike")
        box_text("  [3] Lihat packet log")
        box_text("  [4] Riwayat sesi")
        box_text("  [5] Export report manual")
        box_text("  [6] Settings")
        box_text("  [7] About")
        box_text("  [8] Keluar")
        box_footer()
        choice = input(paint("  janzz@lab > ", "CYAN")).strip()

        if choice == "1":
            dashboard()
        elif choice == "2":
            simulate()
        elif choice == "3":
            event_logs()
        elif choice == "4":
            history_menu()
        elif choice == "5":
            if not LATEST_SESSION:
                print(paint("  Belum ada laporan untuk diekspor.", "YELLOW"))
                pause()
            else:
                if auto_export(LATEST_SESSION):
                    print(paint("  [+] EXPORT MANUAL BERHASIL", "GREEN"))
                else:
                    print(paint("  [!] Gagal export manual.", "RED"))
                pause()
        elif choice == "6":
            settings_menu()
        elif choice == "7":
            about()
        elif choice == "8":
            clear()
            print(paint("\n  JANZZ LAB SESSION CLOSED.", "GREEN"))
            print(paint("  Terima kasih telah menggunakan JANZZ LAB.\n", "WHITE"))
            break
        else:
            print(paint("  Pilihan tidak valid.", "RED"))
            time.sleep(0.8)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(paint("\n  [!] Program ditutup.", "YELLOW"))
    except EOFError:
        print(paint("\n  [!] Input berakhir. Program ditutup.", "YELLOW"))