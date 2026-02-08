#!/usr/bin/env python3
import os, sys, time, subprocess, readline
from datetime import datetime, timedelta

# ================= COLOR =================
RESET = "\033[0m"
def rgb(r,g,b): return f"\033[38;2;{r};{g};{b}m"

# ================= CONFIG =================
CFG = os.path.expanduser("~/.yanzzrc")
HISTORY_FILE = os.path.expanduser("~/.yanzz_history")
FILES_DB = os.path.expanduser("~/.yanzz_files")

cfg = {
    "ZONE": "WIB",
    "TYPING_SPEED": "0.01",
    "SOUND": "ON"
}

# ================= LOAD CONFIG =================
def load_cfg():
    if not os.path.exists(CFG):
        with open(CFG,"w") as f:
            for k,v in cfg.items():
                f.write(f"{k}={v}\n")
    with open(CFG) as f:
        for l in f:
            if "=" in l:
                k,v = l.strip().split("=",1)
                cfg[k]=v

# ================= HISTORY =================
readline.parse_and_bind("tab: complete")
if os.path.exists(HISTORY_FILE):
    readline.read_history_file(HISTORY_FILE)

def save_history():
    readline.write_history_file(HISTORY_FILE)

# ================= FILE TRACKER =================
def log_file(name):
    files=set()
    if os.path.exists(FILES_DB):
        files=set(open(FILES_DB).read().splitlines())
    files.add(name)
    with open(FILES_DB,"w") as f:
        f.write("\n".join(sorted(files)))

def list_files():
    if not os.path.exists(FILES_DB):
        print("belum ada file")
        return
    print("\nFILES HISTORY:")
    for f in open(FILES_DB):
        print(" -",f.strip())

# ================= UTILS =================
def beep(n=1):
    if cfg["SOUND"]=="ON":
        for _ in range(n):
            sys.stdout.write("\a")
            sys.stdout.flush()
            time.sleep(0.05)

def typing(t):
    sp=float(cfg["TYPING_SPEED"])
    for c in t:
        sys.stdout.write(c)
        sys.stdout.flush()
        beep(1)
        time.sleep(sp)
    print()

def get_time_once():
    off = 7 if cfg["ZONE"]=="WIB" else 8 if cfg["ZONE"]=="WITA" else 9
    return (datetime.utcnow()+timedelta(hours=off)).strftime("%H:%M:%S")

# ================= LOADING RGB (ADA JAM, STATIC) =================
def loading_screen():
    os.system("clear")
    jam = get_time_once()

    for i in range(1,11):
        filled="█"*i
        empty ="░"*(10-i)
        percent=i*10

        r=(i*30)%255
        g=(255-i*20)%255
        b=(100+i*15)%255

        sys.stdout.write(
            f"\r{rgb(r,g,b)}[{filled}{empty}] {percent}% | {jam}{RESET}"
        )
        sys.stdout.flush()
        beep(1)
        time.sleep(0.4)

    print("\n")

# ================= ASCII =================
ASCII = [
"██╗   ██╗ █████╗ ███╗   ██╗███████╗███████╗",
"╚██╗ ██╔╝██╔══██╗████╗  ██║╚══███╔╝╚══███╔╝",
" ╚████╔╝ ███████║██╔██╗ ██║  ███╔╝   ███╔╝ ",
"  ╚██╔╝  ██╔══██║██║╚██╗██║ ███╔╝   ███╔╝  ",
"   ██║   ██║  ██║██║ ╚████║███████╗███████╗",
"   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝",
]

# ================= ASCII ANIMATED =================
def animated_ascii():
    colors=[
        (255,0,100),(255,120,0),(255,200,0),
        (0,200,255),(0,255,150),(180,0,255)
    ]
    for shift in range(4):
        os.system("clear")
        for i,l in enumerate(ASCII):
            r,g,b = colors[(i+shift)%len(colors)]
            print(rgb(r,g,b)+l+RESET)
        time.sleep(0.25)

# ================= MENU =================
def menu():
    print("\n"+rgb(0,200,255)+"="*45+RESET)
    typing(rgb(255,100,255)+" py nama      -> run nama.py"+RESET)
    typing(rgb(100,255,150)+" js nama      -> run nama.js"+RESET)
    typing(rgb(255,255,100)+" addpy nama   -> edit nama.py"+RESET)
    typing(rgb(255,180,80)+" addjs nama   -> edit nama.js"+RESET)
    typing(rgb(0,255,255)+" github user  -> open github user"+RESET)
    typing(rgb(200,200,200)+" ls           -> list file history"+RESET)
    typing(rgb(255,80,80)+" end          -> normal terminal"+RESET)
    typing(rgb(255,0,0)+" exit         -> close"+RESET)
    print(rgb(0,200,255)+"="*45+RESET)

# ================= RUNNERS =================
def run_py(f):
    subprocess.call(["python",f])

def run_js(f):
    subprocess.call(["node",f])

def open_github(user):
    url=f"https://github.com/{user}"
    print("Opening:",url)
    subprocess.call(["xdg-open",url])

# ================= MAIN =================
def main():
    load_cfg()
    loading_screen()
    animated_ascii()
    menu()

    while True:
        try:
            cmd=input("\n>>> ").strip().split()
            if not cmd: continue

            if cmd[0]=="exit":
                save_history()
                beep(1)
                break

            if cmd[0]=="end":
                save_history()
                os.system("bash")
                break

            if cmd[0]=="ls":
                list_files()
                continue

            if cmd[0]=="github" and len(cmd)>1:
                open_github(cmd[1])
                continue

            if len(cmd)<2:
                print("nama file wajib")
                beep(2)
                continue

            name=cmd[1]

            if cmd[0]=="py":
                f=name+".py"
                open(f,"a").close()
                log_file(f)
                run_py(f)

            elif cmd[0]=="js":
                f=name+".js"
                open(f,"a").close()
                log_file(f)
                run_js(f)

            elif cmd[0]=="addpy":
                f=name+".py"
                open(f,"a").close()
                log_file(f)
                os.system("nano "+f)

            elif cmd[0]=="addjs":
                f=name+".js"
                open(f,"a").close()
                log_file(f)
                os.system("nano "+f)

            else:
                print("unknown command")
                beep(2)

        except KeyboardInterrupt:
            print("\nCTRL+C blocked")

if __name__=="__main__":
    main()
