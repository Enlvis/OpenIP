# -------------------------------------------------------
#  EDU ONLY – tylko własne sieci
# -------------------------------------------------------
#  Name  : OPENIP
#  Author: Anonymus
# -------------------------------------------------------

import socket, subprocess, platform, sys, time, threading, errno
from concurrent.futures import ThreadPoolExecutor

# ================= WINDOWS ANSI =================
if platform.system() == "Windows":
    import ctypes
    ctypes.windll.kernel32.SetConsoleMode(
        ctypes.windll.kernel32.GetStdHandle(-11), 7
    )

# ================= COLORS =================
RESET="\033[0m"; BOLD="\033[1m"
RED="\033[31m"; GREEN="\033[32m"; YELLOW="\033[33m"
BLUE="\033[34m"; MAGENTA="\033[35m"; CYAN="\033[36m"

OK=f"{GREEN}[OPEN]{RESET}"
CLOSED=f"{RED}[CLOSED]{RESET}"
FILTERED=f"{YELLOW}[FILTERED]{RESET}"
INFO=f"{CYAN}[*]{RESET}"
WARN=f"{YELLOW}[!]{RESET}"

br="-"*60

# ================= TOP PORTS =================
TOP_PORTS=[
21,22,23,25,53,80,110,135,139,143,443,445,3389,3306,8080,
20,26,69,111,389,636,993,995,1723,5900,8000,8443,8888
]

# ================= PROGRESS BAR =================
class ProgressBar:
    def __init__(self,total,label):
        self.total=total
        self.current=0
        self.label=label
        self.last=time.time()
        self.rate=None
        self.spin=0
        self.spinner=["|","/","-","\\"]
        self.lock=threading.Lock()

    def update(self,found=0):
        with self.lock:
            now=time.time()
            dt=now-self.last
            self.last=now
            if dt>0:
                r=1/dt
                self.rate=r if self.rate is None else 0.3*r+0.7*self.rate

            self.current+=1
            pct=self.current/self.total
            eta=int((self.total-self.current)/self.rate) if self.rate else 0
            fill=int(30*pct)
            bar="█"*fill+" "*(30-fill)
            color=YELLOW if pct<0.5 else CYAN if pct<0.8 else GREEN
            sp=self.spinner[self.spin%4]; self.spin+=1

            sys.stdout.write(
                f"\r{color}[{bar}] {int(pct*100):3d}% | ETA {eta:3d}s | FOUND {found:3d} | {self.label} {sp}{RESET}"
            )
            sys.stdout.flush()
            if self.current>=self.total:
                print()

# ================= BASIC =================
def ping_ip(host, attempts):
    opt="-n" if platform.system()=="Windows" else "-c"
    bar=ProgressBar(attempts,"PING")
    alive=False
    for _ in range(attempts):
        try:
            subprocess.run(
                ["ping",opt,"1",host],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=1,
                check=True
            )
            alive=True
        except:
            pass
        finally:
            bar.update()
    return alive

def get_hostname(ip):
    try: return socket.gethostbyaddr(ip)[0]
    except: return "unknown"

def guess_os(ip):
    opt="-n" if platform.system()=="Windows" else "-c"
    try:
        out=subprocess.check_output(["ping",opt,"1",ip],timeout=1).decode().lower()
        if "ttl=64" in out: return "Linux / Unix"
        if "ttl=128" in out: return "Windows"
        if "ttl=255" in out: return "Router"
    except: pass
    return "Unknown"

# ================= AUTO TUNING =================
def auto_tune(ip):
    times=[]
    for p in (80,443,22):
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            start=time.time()
            s.settimeout(1)
            s.connect_ex((ip,p))
            times.append(time.time()-start)
            s.close()
        except:
            pass

    if not times:
        return 1.2, 80

    avg=sum(times)/len(times)
    if avg<0.05: return 0.15, 400
    if avg<0.15: return 0.3, 300
    if avg<0.4:  return 0.6, 180
    return 1.0, 120

# ================= FINGERPRINT =================
def fingerprint(port,banner):
    b=banner.lower()
    if "openssh" in b: return "SSH","OpenSSH"
    if "apache" in b: return "HTTP","Apache"
    if "nginx" in b: return "HTTP","Nginx"
    if "vsftpd" in b: return "FTP","vsFTPd"
    if "postfix" in b: return "SMTP","Postfix"
    if "exim" in b: return "SMTP","Exim"
    if "mysql" in b: return "MySQL","MySQL"
    if port==443: return "HTTPS","TLS"
    common={21:"FTP",22:"SSH",25:"SMTP",80:"HTTP",443:"HTTPS",3306:"MySQL"}
    return common.get(port,"UNKNOWN"),""

def grab_banner(sock,port):
    try:
        sock.settimeout(0.4)
        if port in (80,8080,8000,443):
            sock.send(b"HEAD / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        return sock.recv(1024).decode(errors="ignore").strip()
    except:
        return ""

# ================= PORT SCAN =================
def port_scan(ip, ports, label):
    timeout, threads = auto_tune(ip)

    print(f"""
{INFO} Target   : {ip}
{INFO} Hostname : {get_hostname(ip)}
{INFO} OS Guess : {guess_os(ip)}
{INFO} Timeout  : {timeout}s
{INFO} Threads  : {threads}
{br}
""")

    results={}
    stats={"OPEN":0,"CLOSED":0,"FILTERED":0}
    lock=threading.Lock()
    bar=ProgressBar(len(ports),label)

    def worker(p):
        state=None; banner=""; svc=""; soft=""
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(timeout)
            res=s.connect_ex((ip,p))

            if res==0:
                state="OPEN"
                banner=grab_banner(s,p)
                svc,soft=fingerprint(p,banner)
            elif res in (errno.ECONNREFUSED,10061):
                state="CLOSED"
            else:
                state="FILTERED"

            s.close()
        except socket.timeout:
            state="FILTERED"
        except:
            state="FILTERED"
        finally:
            with lock:
                stats[state]+=1
                if state=="OPEN":
                    results[p]=(svc,soft,banner.split("\n")[0])
            bar.update(stats["OPEN"])

    with ThreadPoolExecutor(max_workers=threads) as ex:
        ex.map(worker, ports)

    print(f"""
{GREEN}OPEN     : {stats['OPEN']}
{RED}CLOSED   : {stats['CLOSED']}
{YELLOW}FILTERED : {stats['FILTERED']}
{RESET}
""")

    for p,(svc,soft,b) in sorted(results.items()):
        print(f"{OK} {p:<6} {CYAN}{svc:<8}{RESET} {soft} {b}")

# ================= NETWORK SCAN =================
def scan_network(prefix):
    print(f"\n{INFO} Skanowanie sieci {prefix}.0/24\n")
    alive=[]
    bar=ProgressBar(254,"NET SCAN")
    opt="-n" if platform.system()=="Windows" else "-c"

    def worker(i):
        ip=f"{prefix}.{i}"
        try:
            subprocess.run(
                ["ping",opt,"1",ip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=0.7,
                check=True
            )
            alive.append(ip)
        except:
            pass
        finally:
            bar.update(len(alive))

    with ThreadPoolExecutor(max_workers=80) as ex:
        ex.map(worker, range(1,255))

    print(f"\n{GREEN}AKTYWNE HOSTY:{RESET}")
    for ip in alive:
        print(f"{GREEN}[+]{RESET} {ip:<15} {get_hostname(ip)}")

# ================= NETWORK INFO =================
def network_info():
    info={"ip":"unknown","gateway":"unknown"}
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        info["ip"]=s.getsockname()[0]
        s.close()
    except:
        pass
    return info

# ================= BANNER =================
print(f"""
{GREEN} 
 ███████╗ ██████╗ ███████╗███╗   ██╗  ██╗██████╗
 ██╔══██║ ██╔══██╗██╔════╝████╗  ██║  ██║██╔══██╗
 ██║  ██║ ██████╔╝█████╗  ██╔██╗ ██║  ██║██████╔╝
 ██║  ██║ ██╔═══╝ ██╔══╝  ██║╚██╗██║  ██║██╔═══╝
 ███████║ ██║     ███████╗██║ ╚████║  ██║██║
 ╚══════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝  ╚═╝╚═╝
{RESET}
""")

# ================= MAIN LOOP =================
while True:
    try:
        cmd=input("> ").lower().strip()

        if cmd=="help":
            print(br)
            print("                   Podstawowe polecenia")
            print(br)
            print("help - Polecenia na wywołanie tłumaczenia poleceń")
            print("info - Pokazuje dane sieci")
            print("exit - Wyjście z programu")
            print(" ")
            print(" ")
            print(br)
            print("                       Narzędzia IP")
            print(br)
            print("scan - zakres portów")
            print("scan fast - Skanuje topowe porty")
            print("scan full - Skanuje porty: 1-65535")
            print("net - Skan sieć ip.1-24")
            print(" ")
            print(" ")

        elif cmd=="ping":
            ip=input("IP > ")
            n=int(input("Ile razy > "))
            print(f"\n{OK} HOST AKTYWNY" if ping_ip(ip,n) else f"\n{ERR} BRAK ODPOWIEDZI")

        elif cmd=="net":
            prefix=input("Prefix (np. 192.168.1) > ")
            scan_network(prefix)

        elif cmd=="scan":
            ip=input("IP > ")
            s=int(input("Port start > "))
            e=int(input("Port end   > "))
            port_scan(ip, range(s,e+1), "CUSTOM SCAN")

        elif cmd=="scan fast":
            ip=input("IP > ")
            port_scan(ip, TOP_PORTS, "FAST SCAN")

        elif cmd=="scan full":
            ip=input("IP > ")
            port_scan(ip, range(1,65536), "FULL SCAN")

        elif cmd=="info":
            i=network_info()
            print(f"{INFO} IP: {i['ip']}  GATEWAY: {i['gateway']}")

        elif cmd=="exit":
            sys.exit()

        else:
            print(f"{WARN} Nieznana komenda")

    except KeyboardInterrupt:
        print("\nPrzerwano"); sys.exit()
