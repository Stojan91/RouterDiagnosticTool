"""
Router Diagnostic Tool - FIXED VERSION
Naprawiona wersja z obsługą błędów i offline fallback
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from router_database import ROUTER_DATABASE, get_all_models, get_producers, search_routers, get_router_image_url
import subprocess
import platform
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠ Pillow nie zainstalowane - zdjęcia nie będą się wyświetlać")
import urllib.request
from io import BytesIO
import threading

# Language dictionaries
TRANSLATIONS = {
    'pl': {
        'title': 'Diagnostyka Routerów - Baza 3000+ Modeli',
        'db_info': 'Baza danych: {} modeli routerów (2005-2025)',
        'params': 'Parametry diagnostyki',
        'ip_label': 'Adres IP routera:',
        'ping_btn': '📡 Ping',
        'producer_label': 'Wybierz producenta:',
        'model_label': 'Wybierz model routera:',
        'search_label': 'Wyszukaj model:',
        'search_btn': '🔎 Szukaj',
        'show_btn': '📊 Pokaż specyfikację',
        'clear_btn': '🗑️ Wyczyść',
        'results': 'Wyniki diagnostyki',
        'status_ready': 'Gotowy do pracy',
        'status_found': 'Znaleziono {} modeli producenta {}',
        'status_search': 'Znaleziono {} modeli pasujących do \'{}\'',
        'status_ping': 'Wykonywanie ping do {}...',
        'status_completed': 'Ping zakończony',
        'status_timeout': 'Błąd: Timeout',
        'status_error': 'Błąd wykonania ping',
        'status_cleared': 'Wyczyszczono wyniki',
        'status_displayed': 'Wyświetlono specyfikację: {}',
        'error_no_data': 'Błąd: Brak danych',
        'warn_no_keyword': 'Brak słowa kluczowego',
        'warn_enter_keyword': 'Wprowadź słowo do wyszukania',
        'warn_no_ip': 'Brak IP',
        'warn_enter_ip': 'Wprowadź adres IP routera',
        'warn_no_selection': 'Brak wyboru',
        'warn_select_model': 'Wybierz model routera z listy',
        'no_spec': 'Nie znaleziono specyfikacji dla wybranego modelu.',
        'connection_test': '=== Test połączenia z routerem {} ===\n\n',
        'spec_header': '  SPECYFIKACJA ROUTERA: {}\n',
        'error_timeout_msg': 'BŁĄD: Przekroczono limit czasu połączenia\n',
        'language': 'Język:',
        'router_image': 'Zdjęcie Routera',
        'loading_image': 'Ładowanie zdjęcia...',
        'select_router': 'Wybierz router\naby zobaczyć zdjęcie',
        'no_image': 'Brak zdjęcia',
        'offline_mode': 'Tryb offline\nBrak połączenia\nz internetem',
    },
    'en': {
        'title': 'Router Diagnostic Tool - 3000+ Models Database',
        'db_info': 'Database: {} router models (2005-2025)',
        'params': 'Diagnostic Parameters',
        'router_image': 'Router Image',
        'loading_image': 'Loading image...',
        'select_router': 'Select a router\nto view image',
        'no_image': 'No image available',
        'offline_mode': 'Offline mode\nNo internet\nconnection',
    }
}

def create_offline_placeholder(model, producent, width=400, height=300):
    """Tworzy piękny placeholder lokalnie (bez internetu)"""
    if not PIL_AVAILABLE:
        return None
    
    # Kolory
    bg_color = '#2c3e50'
    primary_color = '#3498db'
    secondary_color = '#2ecc71'
    text_color = '#ecf0f1'
    
    # Utwórz obraz z gradientem
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Gradient
    for y in range(height):
        shade = int(44 + (y / height) * 20)
        color = f'#{shade:02x}{62 + int(y/height*10):02x}{80:02x}'
        draw.line([(0, y), (width, y)], fill=color)
    
    # Ramki
    draw.rectangle([15, 15, width-15, height-15], outline=primary_color, width=4)
    draw.rectangle([25, 25, width-25, height-25], outline=secondary_color, width=2)
    
    # Router grafika
    router_x = width // 2
    router_y = height // 2 - 20
    router_w = 120
    router_h = 60
    
    # Korpus
    draw.rectangle([router_x - router_w//2, router_y - router_h//2, 
                   router_x + router_w//2, router_y + router_h//2], 
                   fill='#34495e', outline=primary_color, width=3)
    
    # LEDy
    for i in range(5):
        led_x = router_x - 40 + i * 20
        led_y = router_y - 10
        draw.ellipse([led_x-3, led_y-3, led_x+3, led_y+3], fill=secondary_color)
    
    # Anteny
    antenna_h = 40
    # Lewa
    draw.line([router_x - 50, router_y - router_h//2, 
              router_x - 60, router_y - router_h//2 - antenna_h], 
              fill=primary_color, width=4)
    draw.ellipse([router_x - 65, router_y - router_h//2 - antenna_h - 5,
                 router_x - 55, router_y - router_h//2 - antenna_h + 5], 
                 fill=secondary_color, outline=primary_color)
    # Prawa
    draw.line([router_x + 50, router_y - router_h//2, 
              router_x + 60, router_y - router_h//2 - antenna_h], 
              fill=primary_color, width=4)
    draw.ellipse([router_x + 55, router_y - router_h//2 - antenna_h - 5,
                 router_x + 65, router_y - router_h//2 - antenna_h + 5], 
                 fill=secondary_color, outline=primary_color)
    
    # Porty
    for i in range(4):
        port_x = router_x - 40 + i * 27
        port_y = router_y + 15
        draw.rectangle([port_x-8, port_y-5, port_x+8, port_y+5], 
                      fill='#2c3e50', outline=secondary_color, width=1)
    
    # Czcionka - używamy default jeśli nie ma systemowej
    try:
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_model = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        try:
            font_title = ImageFont.truetype("Arial.ttf", 24)
            font_model = ImageFont.truetype("Arial.ttf", 18)
            font_small = ImageFont.truetype("Arial.ttf", 14)
        except:
            # Default font
            from PIL import ImageFont
            font_title = ImageFont.load_default()
            font_model = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # Tekst producenta
    producer_text = f"● {producent} ●"
    try:
        bbox = draw.textbbox((0, 0), producer_text, font=font_title)
        text_w = bbox[2] - bbox[0]
        draw.text(((width - text_w) / 2, 40), producer_text, fill=primary_color, font=font_title)
    except:
        # Fallback dla starej wersji PIL
        draw.text((width//2 - 50, 40), producer_text, fill=primary_color, font=font_title)
    
    # Model
    model_short = model.replace(producent, "").strip()
    if len(model_short) > 25:
        words = model_short.split()
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        
        try:
            bbox1 = draw.textbbox((0, 0), line1, font=font_model)
            w1 = bbox1[2] - bbox1[0]
            draw.text(((width - w1) / 2, router_y + router_h//2 + 50), line1, fill=text_color, font=font_model)
            
            bbox2 = draw.textbbox((0, 0), line2, font=font_model)
            w2 = bbox2[2] - bbox2[0]
            draw.text(((width - w2) / 2, router_y + router_h//2 + 75), line2, fill=text_color, font=font_model)
        except:
            draw.text((width//2 - 100, router_y + router_h//2 + 50), line1, fill=text_color, font=font_model)
            draw.text((width//2 - 100, router_y + router_h//2 + 75), line2, fill=text_color, font=font_model)
    else:
        try:
            bbox = draw.textbbox((0, 0), model_short, font=font_model)
            text_w = bbox[2] - bbox[0]
            draw.text(((width - text_w) / 2, router_y + router_h//2 + 50), model_short, fill=text_color, font=font_model)
        except:
            draw.text((width//2 - 100, router_y + router_h//2 + 50), model_short, fill=text_color, font=font_model)
    
    # Footer
    footer = "ROUTER DATABASE"
    try:
        bbox = draw.textbbox((0, 0), footer, font=font_small)
        text_w = bbox[2] - bbox[0]
        draw.text(((width - text_w) / 2, height - 35), footer, fill=secondary_color, font=font_small)
    except:
        draw.text((width//2 - 60, height - 35), footer, fill=secondary_color, font=font_small)
    
    return img

class AutocompleteEntry(tk.Frame):
    def __init__(self, parent, autocomplete_list, **kwargs):
        tk.Frame.__init__(self, parent)
        self.autocomplete_list = autocomplete_list
        self.var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.var, **kwargs)
        self.entry.pack(fill=tk.BOTH, expand=True)
        self.listbox = None
        self.listbox_frame = None
        self.var.trace('w', self.on_change)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.bind("<Up>", self.move_up)
        self.entry.bind("<Down>", self.move_down)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        
    def on_change(self, *args):
        if self.var.get() == '':
            self.destroy_listbox()
        else:
            words = self.autocomplete()
            if words:
                self.show_listbox(words)
            else:
                self.destroy_listbox()
                    
    def autocomplete(self):
        text = self.var.get().lower()
        matches = [item for item in self.autocomplete_list if text in item.lower()]
        return sorted(matches)[:8]
    
    def show_listbox(self, words):
        if not self.listbox_frame:
            self.listbox_frame = tk.Frame(self)
            self.listbox_frame.pack(fill=tk.BOTH, expand=True)
            self.listbox = tk.Listbox(self.listbox_frame, height=min(8, len(words)))
            self.listbox.pack(fill=tk.BOTH, expand=True)
            self.listbox.bind("<Button-1>", self.on_select)
            self.listbox.bind("<Return>", self.on_select)
        self.listbox.delete(0, tk.END)
        for w in words:
            self.listbox.insert(tk.END, w)
    
    def destroy_listbox(self):
        if self.listbox_frame:
            self.listbox_frame.destroy()
            self.listbox_frame = None
            self.listbox = None
    
    def on_select(self, event=None):
        if self.listbox:
            selection = self.listbox.get(tk.ACTIVE)
            self.var.set(selection)
            self.destroy_listbox()
            self.entry.icursor(tk.END)
            
    def on_enter(self, event=None):
        if self.listbox:
            self.on_select()
        return 'break'
    
    def move_up(self, event):
        if self.listbox:
            if self.listbox.curselection():
                index = self.listbox.curselection()[0]
                if index > 0:
                    self.listbox.selection_clear(0, tk.END)
                    self.listbox.selection_set(index - 1)
                    self.listbox.activate(index - 1)
            return 'break'
    
    def move_down(self, event):
        if self.listbox:
            if self.listbox.curselection():
                index = self.listbox.curselection()[0]
                if index < self.listbox.size() - 1:
                    self.listbox.selection_clear(0, tk.END)
                    self.listbox.selection_set(index + 1)
                    self.listbox.activate(index + 1)
            else:
                self.listbox.selection_set(0)
                self.listbox.activate(0)
            return 'break'
    
    def on_focus_out(self, event):
        self.after(200, self.destroy_listbox)
    
    def get(self):
        return self.var.get()
    
    def set(self, value):
        self.var.set(value)

class RouterDiagnosticApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'pl'
        self.root.title(TRANSLATIONS[self.current_lang]['title'])
        self.root.geometry("1200x800")
        self.current_image = None
        self.photo_image = None
        style = ttk.Style()
        style.theme_use('clam')
        self.create_widgets()
        
    def _(self, key):
        return TRANSLATIONS[self.current_lang].get(key, key)
        
    def switch_language(self):
        self.current_lang = 'en' if self.current_lang == 'pl' else 'pl'
        self.refresh_ui()
        
    def refresh_ui(self):
        self.root.title(self._('title'))
        self.db_info_label.config(text=self._('db_info').format(len(ROUTER_DATABASE)))
        self.input_frame.config(text=self._('params'))
        self.ip_label.config(text=self._('ip_label'))
        self.ping_btn.config(text=self._('ping_btn'))
        self.producer_label.config(text=self._('producer_label'))
        self.model_label.config(text=self._('model_label'))
        self.search_label.config(text=self._('search_label'))
        self.search_btn.config(text=self._('search_btn'))
        self.show_btn.config(text=self._('show_btn'))
        self.clear_btn.config(text=self._('clear_btn'))
        self.output_frame.config(text=self._('results'))
        self.status_bar.config(text=self._('status_ready'))
        self.lang_label.config(text=self._('language'))
        self.image_frame.config(text=self._('router_image'))
        
    def create_widgets(self):
        # [KOD GUI - bez zmian, kopiuj z poprzedniej wersji]
        info_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        info_frame.pack(fill=tk.X)
        
        lang_frame = tk.Frame(info_frame, bg='#2c3e50')
        lang_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        
        self.lang_label = tk.Label(lang_frame, text=self._('language'), 
                                   font=('Arial', 9), bg='#2c3e50', fg='white')
        self.lang_label.pack(side=tk.LEFT, padx=5)
        
        lang_btn = tk.Button(lang_frame, text="🇵🇱 PL / 🇬🇧 EN", 
                            command=self.switch_language,
                            bg='#34495e', fg='white', font=('Arial', 9, 'bold'))
        lang_btn.pack(side=tk.LEFT)
        
        title_label = tk.Label(info_frame, text="🔍 Router Diagnostic Tool", 
                              font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=10)
        
        self.db_info_label = tk.Label(info_frame, 
                          text=self._('db_info').format(len(ROUTER_DATABASE)),
                          font=('Arial', 9), bg='#2c3e50', fg='#ecf0f1')
        self.db_info_label.pack()
        
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_panel = tk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.input_frame = tk.LabelFrame(left_panel, text=self._('params'), 
                                   font=('Arial', 10, 'bold'), padx=10, pady=10)
        self.input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.ip_label = tk.Label(self.input_frame, text=self._('ip_label'), font=('Arial', 9))
        self.ip_label.grid(row=0, column=0, sticky='w', pady=5)
        self.ip_entry = tk.Entry(self.input_frame, width=30, font=('Arial', 9))
        self.ip_entry.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        self.ip_entry.insert(0, "192.168.1.1")
        
        self.ping_btn = tk.Button(self.input_frame, text=self._('ping_btn'), command=self.ping_router, 
                           bg='#3498db', fg='white', font=('Arial', 9))
        self.ping_btn.grid(row=0, column=2, padx=5)
        
        self.producer_label = tk.Label(self.input_frame, text=self._('producer_label'), font=('Arial', 9))
        self.producer_label.grid(row=1, column=0, sticky='w', pady=5)
        self.producer_var = tk.StringVar()
        self.producer_combo = ttk.Combobox(self.input_frame, textvariable=self.producer_var, 
                                          values=get_producers(), width=27, font=('Arial', 9))
        self.producer_combo.grid(row=1, column=1, sticky='w', pady=5, padx=5)
        self.producer_combo.bind("<<ComboboxSelected>>", self.update_models)
        
        self.model_label = tk.Label(self.input_frame, text=self._('model_label'), font=('Arial', 9))
        self.model_label.grid(row=2, column=0, sticky='w', pady=5)
        self.router_var = tk.StringVar()
        self.router_combo = ttk.Combobox(self.input_frame, textvariable=self.router_var, 
                                        values=get_all_models(), width=27, font=('Arial', 9))
        self.router_combo.grid(row=2, column=1, sticky='w', pady=5, padx=5)
        self.router_combo.bind("<<ComboboxSelected>>", self.show_spec)
        
        self.search_label = tk.Label(self.input_frame, text=self._('search_label'), font=('Arial', 9))
        self.search_label.grid(row=3, column=0, sticky='w', pady=5)
        
        self.search_entry = AutocompleteEntry(self.input_frame, autocomplete_list=get_all_models(), font=('Arial', 9), width=28)
        self.search_entry.grid(row=3, column=1, sticky='w', pady=5, padx=5)
        
        self.search_btn = tk.Button(self.input_frame, text=self._('search_btn'), command=self.search_models,
                             bg='#27ae60', fg='white', font=('Arial', 9))
        self.search_btn.grid(row=3, column=2, padx=5)
        
        btn_frame = tk.Frame(left_panel)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.show_btn = tk.Button(btn_frame, text=self._('show_btn'), command=self.show_spec,
                           bg='#e67e22', fg='white', font=('Arial', 10, 'bold'), height=2)
        self.show_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.clear_btn = tk.Button(btn_frame, text=self._('clear_btn'), command=self.clear_output,
                            bg='#95a5a6', fg='white', font=('Arial', 10, 'bold'), height=2)
        self.clear_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.output_frame = tk.LabelFrame(left_panel, text=self._('results'), 
                                    font=('Arial', 10, 'bold'), padx=10, pady=10)
        self.output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, 
                                                     font=('Courier New', 9), height=20)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        right_panel = tk.Frame(main_container, width=420)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_panel.pack_propagate(False)
        
        self.image_frame = tk.LabelFrame(right_panel, text=self._('router_image'), 
                                        font=('Arial', 10, 'bold'), padx=10, pady=10)
        self.image_frame.pack(fill=tk.BOTH, expand=True)
        
        self.image_label = tk.Label(self.image_frame, text=self._('select_router'), 
                                    font=('Arial', 12), fg='gray',
                                    bg='#ecf0f1', relief=tk.SUNKEN, bd=2)
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.status_bar = tk.Label(self.root, text=self._('status_ready'), 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W, font=('Arial', 8))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def load_router_image(self, model, producent):
        """Ładuje zdjęcie routera - prawdziwe z netu lub lokalne"""
        self.image_label.config(text=self._('loading_image'), image='')
        
        def download_or_create():
            image_url = get_router_image_url(model)
            error_msg = None
            
            try:
                if not image_url or 'placeholder.com' in image_url:
                    # Brak prawdziwego URL - wygeneruj lokalnie
                    raise Exception("No real image URL - using local placeholder")
                
                print(f"📥 Pobieranie: {image_url}")
                req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                
                with urllib.request.urlopen(req, timeout=10) as url:
                    image_data = url.read()
                
                if not PIL_AVAILABLE:
                    raise Exception("Pillow not installed")
                
                image = Image.open(BytesIO(image_data))
                image.thumbnail((400, 300), Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(image)
                self.root.after(0, lambda p=photo: self.display_image(p))
                print("✓ Zdjęcie załadowane!")
                return
                
            except Exception as e:
                print(f"✗ Błąd pobierania: {e}")
                error_msg = str(e)
            
            # FALLBACK - wygeneruj lokalny placeholder
            try:
                print(f"🎨 Generuję lokalny placeholder...")
                image = create_offline_placeholder(model, producent)
                
                if image:
                    photo = ImageTk.PhotoImage(image)
                    self.root.after(0, lambda p=photo: self.display_image(p))
                    print("✓ Placeholder wygenerowany!")
                else:
                    raise Exception("Cannot create placeholder")
                    
            except Exception as e2:
                print(f"✗ Błąd generowania: {e2}")
                # OSTATECZNY FALLBACK - tekst
                final_msg = f"{self._('offline_mode')}\n\n{model}"
                self.root.after(0, lambda msg=final_msg: self.image_label.config(
                    image="",
                    text=msg,
                    font=('Arial', 10),
                    fg='#e74c3c'
                ))
        
        threading.Thread(target=download_or_create, daemon=True).start()
    
    def display_image(self, photo):
        self.photo_image = photo
        self.image_label.config(image=self.photo_image, text="")
        
    def update_models(self, event=None):
        producer = self.producer_var.get()
        if producer:
            models = [model for model, spec in ROUTER_DATABASE.items() 
                     if spec.get('Producent') == producer]
            self.router_combo['values'] = sorted(models)
            self.router_var.set('')
            self.output_text.delete('1.0', tk.END)
            self.image_label.config(image="", text=self._('select_router'))
            self.photo_image = None
            self.status_bar.config(text=self._('status_found').format(len(models), producer))
    
    def search_models(self):
        keyword = self.search_entry.get()
        if keyword:
            results = search_routers(keyword)
            self.router_combo['values'] = results
            self.status_bar.config(text=self._('status_search').format(len(results), keyword))
            if results:
                self.router_var.set(results[0])
                self.show_spec()
        else:
            messagebox.showwarning(self._('warn_no_keyword'), self._('warn_enter_keyword'))
    
    def ping_router(self):
        ip = self.ip_entry.get()
        if not ip:
            messagebox.showwarning(self._('warn_no_ip'), self._('warn_enter_ip'))
            return
        self.status_bar.config(text=self._('status_ping').format(ip))
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, self._('connection_test').format(ip))
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '4', ip]
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.output_text.insert(tk.END, result.stdout)
            self.status_bar.config(text=self._('status_completed'))
        except subprocess.TimeoutExpired:
            self.output_text.insert(tk.END, self._('error_timeout_msg'))
            self.status_bar.config(text=self._('status_timeout'))
        except Exception as e:
            self.output_text.insert(tk.END, f"ERROR: {str(e)}\n")
            self.status_bar.config(text=self._('status_error'))
    
    def show_spec(self, event=None):
        selected = self.router_var.get()
        if not selected:
            messagebox.showwarning(self._('warn_no_selection'), self._('warn_select_model'))
            return
        spec = ROUTER_DATABASE.get(selected, {})
        if not spec:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, self._('no_spec'))
            return
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, "=" * 80 + "\n")
        self.output_text.insert(tk.END, self._('spec_header').format(selected))
        self.output_text.insert(tk.END, "=" * 80 + "\n\n")
        for key, value in spec.items():
            if key != 'Image URL':
                self.output_text.insert(tk.END, f"{key:.<35} {value}\n")
        self.output_text.insert(tk.END, "\n" + "=" * 80 + "\n")
        self.status_bar.config(text=self._('status_displayed').format(selected))
        
        producent = spec.get('Producent', 'Unknown')
        self.load_router_image(selected, producent)
    
    def clear_output(self):
        self.output_text.delete('1.0', tk.END)
        self.image_label.config(image="", text=self._('select_router'))
        self.photo_image = None
        self.status_bar.config(text=self._('status_cleared'))

def main():
    root = tk.Tk()
    app = RouterDiagnosticApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
