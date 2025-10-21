import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import subprocess, platform, threading, csv, requests
from io import BytesIO
from bs4 import BeautifulSoup

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from router_database import ROUTER_DATABASE, get_all_models, get_producers, search_routers
from network_scanner import scan_network
from firmware_checker import check_firmware_updates
from speed_test import run_speed_test
from router_comparison import compare_routers

THEMES = {
    'light': {
        'bg':'#ecf0f1','fg':'#2c3e50',
        'header_bg':'#2c3e50','header_fg':'white',
        'btn_bg':'#3498db','btn_fg':'white',
        'panel_bg':'#ffffff','text_bg':'#ffffff','text_fg':'#000000'
    },
    'dark': {
        'bg':'#1e1e1e','fg':'#d4d4d4',
        'header_bg':'#252526','header_fg':'#cccccc',
        'btn_bg':'#0e639c','btn_fg':'white',
        'panel_bg':'#252526','text_bg':'#1e1e1e','text_fg':'#d4d4d4'
    }
}

TEXTS = {
    'pl': {
        'title':'Diagnostyka Routerów','ping':'📡 Ping','scan':'🌐 Skan sieci','firmware':'🔧 Sprawdź Firmware',
        'speed':'⚡ Test prędkości','compare':'⚖️ Porównaj','export':'📄 Export CSV','lang':'PL/EN',
        'theme':'Motyw:','params':'Parametry diagnostyki','ip':'Adres IP:','producer':'Producent:',
        'model':'Model:','search':'Wyszukaj:','search_btn':'🔎 Szukaj','show':'📊 Pokaż Specyfikację',
        'clear':'🗑️ Wyczyść','results':'Wyniki','images':'Zdjęcia','loading':'Ładowanie...','select':'Wybierz router',
        'enter_ip':'Wprowadź IP','select_models':'Wybierz dwa modele','ready':'Gotowy'
    },
    'en': {
        'title':'Router Diagnostic','ping':'📡 Ping','scan':'🌐 Network Scan','firmware':'🔧 Check Firmware',
        'speed':'⚡ Speed Test','compare':'⚖️ Compare','export':'📄 Export CSV','lang':'EN/PL',
        'theme':'Theme:','params':'Diagnostic Parameters','ip':'Router IP:','producer':'Producer:',
        'model':'Model:','search':'Search:','search_btn':'🔎 Search','show':'📊 Show Specs',
        'clear':'🗑️ Clear','results':'Results','images':'Images','loading':'Loading...','select':'Select router',
        'enter_ip':'Enter IP','select_models':'Select two models','ready':'Ready'
    }
}

def tr(key,lang):
    return TEXTS[lang].get(key,key)

def fetch_images(model,count=3):
    url=f"https://www.google.com/search?q={model.replace(' ','+')}+router&tbm=isch"
    try:
        html=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=5).text
        soup=BeautifulSoup(html,'html.parser')
        imgs=[img.get('src') or img.get('data-src') for img in soup.find_all('img')[1:count+1]]
        return [u for u in imgs if u and u.startswith('http')]
    except:
        return []

class App:
    def __init__(self,root):
        self.root=root;self.lang='pl';self.theme='light';self.widgets=[]
        self.build_ui()

    def build_ui(self):
        # Clear
        for w in self.root.winfo_children(): w.destroy()
        self.widgets.clear()

        t=lambda k:tr(k,self.lang); th=THEMES[self.theme]
        self.root.title(t('title'));self.root.configure(bg=th['bg']);self.root.geometry('1400x800')

        # Toolbar
        tb=tk.Frame(self.root,bg=th['header_bg']);tb.pack(fill=tk.X)
        for key,cmd in [('scan',self.scan_network),('firmware',self.check_firmware),
                        ('speed',self.speed_test),('compare',self.compare_routers),
                        ('export',self.export_csv)]:
            b=tk.Button(tb,text=t(key),command=cmd,bg=th['btn_bg'],fg=th['btn_fg'])
            b.pack(side=tk.LEFT,padx=2,pady=5);self.widgets.append((b,key))
        bl=tk.Button(tb,text=t('lang'),command=self.toggle_lang,bg=th['btn_bg'],fg=th['btn_fg'])
        bl.pack(side=tk.RIGHT,padx=2);self.widgets.append((bl,None))
        tk.Label(tb,text=t('theme'),bg=th['header_bg'],fg=th['header_fg']).pack(side=tk.RIGHT)
        tv=tk.StringVar(value=self.theme)
        cb=ttk.Combobox(tb,textvariable=tv,values=list(THEMES),state='readonly',width=6)
        cb.pack(side=tk.RIGHT,padx=2);tv.trace('w',lambda *a:self.apply_theme(tv.get()))

        # Main split
        main=tk.Frame(self.root,bg=th['bg']);main.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)
        left=tk.Frame(main,bg=th['bg']);left.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=(0,5))
        right=tk.Frame(main,bg=th['bg'],width=350);right.pack(side=tk.RIGHT,fill=tk.Y);right.pack_propagate(False)

        # Input & controls
        inp=tk.LabelFrame(left,text=t('params'),bg=th['panel_bg'],fg=th['fg']);inp.pack(fill=tk.X,pady=(0,5))
        # IP
        lip=tk.Label(inp,text=t('ip'),bg=th['panel_bg'],fg=th['fg']);lip.grid(row=0,column=0);self.widgets.append((lip,'ip'))
        self.ipent=tk.Entry(inp);self.ipent.grid(row=0,column=1,padx=5);self.ipent.insert(0,'192.168.1.1')
        bping=tk.Button(inp,text=t('ping'),command=self.do_ping,bg=th['btn_bg'],fg=th['btn_fg'])
        bping.grid(row=0,column=2);self.widgets.append((bping,'ping'))
        # Producer/Model
        lpr=tk.Label(inp,text=t('producer'),bg=th['panel_bg'],fg=th['fg']);lpr.grid(row=1,column=0);self.widgets.append((lpr,'producer'))
        self.prcb=ttk.Combobox(inp,values=get_producers());self.prcb.grid(row=1,column=1)
        self.prcb.bind('<<ComboboxSelected>>',lambda e:self.update_models())
        lmd=tk.Label(inp,text=t('model'),bg=th['panel_bg'],fg=th['fg']);lmd.grid(row=2,column=0);self.widgets.append((lmd,'model'))
        self.mocb=ttk.Combobox(inp,values=get_all_models());self.mocb.grid(row=2,column=1)
        self.mocb.bind('<<ComboboxSelected>>',lambda e:self.show_specs())
        # Search
        lsh=tk.Label(inp,text=t('search'),bg=th['panel_bg'],fg=th['fg']);lsh.grid(row=3,column=0);self.widgets.append((lsh,'search'))
        self.shent=tk.Entry(inp);self.shent.grid(row=3,column=1)
        bsh=tk.Button(inp,text=t('search_btn'),command=self.do_search,bg=th['btn_bg'],fg=th['btn_fg'])
        bsh.grid(row=3,column=2);self.widgets.append((bsh,'search_btn'))

        # Show/Clear
        bc=tk.Frame(left,bg=th['bg']);bc.pack(fill=tk.X,pady=5)
        bshw=tk.Button(bc,text=t('show'),command=self.show_specs,bg=th['btn_bg'],fg=th['btn_fg'])
        bshw.pack(side=tk.LEFT,expand=True,fill=tk.X,padx=5);self.widgets.append((bshw,'show'))
        bclr=tk.Button(bc,text=t('clear'),command=lambda:self.out.delete('1.0',tk.END),bg=th['btn_bg'],fg=th['btn_fg'])
        bclr.pack(side=tk.LEFT,expand=True,fill=tk.X,padx=5);self.widgets.append((bclr,'clear'))

        # Output
        of=tk.LabelFrame(left,text=t('results'),bg=th['panel_bg'],fg=th['fg']);of.pack(fill=tk.BOTH,expand=True)
        self.out=scrolledtext.ScrolledText(of,bg=th['text_bg'],fg=th['text_fg']);self.out.pack(fill=tk.BOTH,expand=True)

        # Images sidebar
        imf=tk.LabelFrame(right,text=t('images'),bg=th['panel_bg'],fg=th['fg']);imf.pack(fill=tk.BOTH,expand=True)
        self.imgs=[]
        for _ in range(3):
            lbl=tk.Label(imf,text=t('select'),bg=th['panel_bg'],fg=th['fg'],relief=tk.SUNKEN,height=6)
            lbl.pack(fill=tk.BOTH,expand=True,pady=2);self.imgs.append(lbl)

        # Status
        self.status=tk.Label(self.root,text=t('ready'),bg=th['bg'],fg=th['fg']);self.status.pack(side=tk.BOTTOM,fill=tk.X)

    def apply_theme(self,name):
        self.theme=name
        colors=THEMES[name]
        self.root.configure(bg=colors['bg'])
        def rc(w):
            cls=w.winfo_class()
            if cls in ('Frame','Labelframe'): w.configure(bg=colors['bg'])
            if cls=='Label': w.configure(bg=colors['bg'],fg=colors['fg'])
            if cls=='Button': w.configure(bg=colors['btn_bg'],fg=colors['btn_fg'])
            if cls=='LabelFrame': w.configure(bg=colors['panel_bg'],fg=colors['fg'])
            if cls=='Text': w.configure(bg=colors['text_bg'],fg=colors['text_fg'])
            for c in w.winfo_children(): rc(c)
        rc(self.root)

    def toggle_lang(self):
        self.lang='en' if self.lang=='pl' else 'pl'
        for widget,key in self.widgets:
            if key: widget.config(text=tr(key,self.lang))
        self.root.title(tr('title',self.lang))
        self.status.config(text=tr('ready',self.lang))

    def update_models(self):
        prod=self.prcb.get(); lst=[m for m,s in ROUTER_DATABASE.items() if s.get('Producent')==prod]
        self.mocb.configure(values=sorted(lst))

    def do_search(self):
        q=self.shent.get().strip()
        if q:
            lst=search_routers(q); self.mocb.configure(values=lst)
            if lst: self.mocb.set(lst[0]); self.show_specs()

    def do_ping(self):
        ip=self.ipent.get().strip()
        if not ip: return messagebox.showwarning("Error",tr('enter_ip',self.lang))
        self.out.delete('1.0',tk.END)
        try:
            cmd=['ping','-n' if platform.system().lower()=='windows' else '-c','4',ip]
            r=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
            self.out.insert(tk.END,r.stdout)
        except:
            self.out.insert(tk.END,"Ping error\n")

    def scan_network(self):
        self.out.delete('1.0',tk.END); self.out.insert(tk.END,"Network scan...\n")
        def run():
            devs=scan_network(); t=f"Found {len(devs)} devices:\n"
            for d in devs: t+=f"{d['ip']} {d['mac']} {d['hostname']}\n"
            self.out.insert(tk.END,t)
        threading.Thread(target=run,daemon=True).start()

    def check_firmware(self):
        ip=self.ipent.get().strip()
        if not ip: return messagebox.showwarning("Error",tr('enter_ip',self.lang))
        info=check_firmware_updates(ip)
        self.out.delete('1.0',tk.END)
        self.out.insert(tk.END,f"Router {ip}\nCurrent: {info['current']}\nLatest: {info['latest']}\nStatus: {info['status']}\n")

    def speed_test(self):
        self.out.delete('1.0',tk.END); self.out.insert(tk.END,"Speed test...\n")
        def run():
            r=run_speed_test();self.out.insert(tk.END,f"Download: {r['download']} Mbps\nUpload: {r['upload']} Mbps\n")
        threading.Thread(target=run,daemon=True).start()

    def show_specs(self):
        m=self.mocb.get().strip()
        if not m: return
        spec=ROUTER_DATABASE.get(m,{})
        self.out.delete('1.0',tk.END)
        self.out.insert(tk.END,"="*50+f"\nSpecs: {m}\n"+"="*50+"\n")
        for k,v in spec.items():
            if k!='Image URL': self.out.insert(tk.END,f"{k}: {v}\n")
        self.load_images(m)

    def load_images(self,m):
        for l in self.imgs: l.config(text=tr('loading',self.lang),image='')
        def run():
            urls=fetch_images(m,3)
            if not urls:
                for l in self.imgs: l.config(text="No image")
                return
            for i,u in enumerate(urls):
                try:
                    data=requests.get(u,timeout=5).content
                    img=Image.open(BytesIO(data));img.thumbnail((300,150))
                    ph=ImageTk.PhotoImage(img)
                    l=self.imgs[i];l.config(image=ph,text='');l.image=ph
                except: pass
        threading.Thread(target=run,daemon=True).start()

    def compare_routers(self):
        m1=self.mocb.get().strip();m2=self.shent.get().strip()
        if not m1 or not m2: return messagebox.showwarning("Error",tr('select_models',self.lang))
        win=tk.Toplevel(self.root);win.title("Compare")
        tbox=scrolledtext.ScrolledText(win);tbox.pack(fill=tk.BOTH,expand=True)
        tbox.insert('1.0',compare_routers([m1,m2]))

    def export_csv(self):
        fn=filedialog.asksaveasfilename(defaultextension=".csv")
        if fn:
            with open(fn,'w',newline='',encoding='utf-8') as f:
                w=csv.writer(f);w.writerow(['Model','Producer','Year'])
                for m,s in ROUTER_DATABASE.items():
                    w.writerow([m,s.get('Producent'),s.get('Data produkcji')])
            messagebox.showinfo("Export","Saved to "+fn)

if __name__=='__main__':
    root=tk.Tk()
    App(root)
    root.mainloop()
