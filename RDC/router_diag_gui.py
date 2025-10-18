"""
Router Diagnostic Tool - router_diag_gui_multilang.py
Multilingual GUI Application (Polish/English)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from router_database import ROUTER_DATABASE, get_all_models, get_producers, search_routers
import subprocess
import platform

# Language dictionaries
TRANSLATIONS = {
    'en': {
        'title': 'Router Diagnostic Tool - 500+ Models Database',
        'db_info': 'Database: {} router models (2015-2025)',
        'params': 'Diagnostic Parameters',
        'ip_label': 'Router IP Address:',
        'ping_btn': '📡 Ping',
        'producer_label': 'Select Producer:',
        'model_label': 'Select Router Model:',
        'search_label': 'Search Model:',
        'search_btn': '🔎 Search',
        'show_btn': '📊 Show Specification',
        'clear_btn': '🗑️ Clear',
        'results': 'Diagnostic Results',
        'status_ready': 'Ready',
        'status_found': 'Found {} models from {}',
        'status_search': 'Found {} models matching \'{}\'',
        'status_ping': 'Pinging {}...',
        'status_completed': 'Ping completed',
        'status_timeout': 'Error: Timeout',
        'status_error': 'Ping execution error',
        'status_cleared': 'Results cleared',
        'status_displayed': 'Displayed specification: {}',
        'error_no_data': 'Error: No data',
        'warn_no_keyword': 'No Keyword',
        'warn_enter_keyword': 'Enter a search keyword',
        'warn_no_ip': 'No IP',
        'warn_enter_ip': 'Enter router IP address',
        'warn_no_selection': 'No Selection',
        'warn_select_model': 'Select a router model from the list',
        'no_spec': 'No specification found for selected model.',
        'connection_test': '=== Connection Test to Router {} ===\n\n',
        'spec_header': '  ROUTER SPECIFICATION: {}\n',
        'error_timeout_msg': 'ERROR: Connection timeout\n',
        'language': 'Language:',
    },
    'pl': {
        'title': 'Diagnostyka Routerów - Baza 500+ Modeli',
        'db_info': 'Baza danych: {} modeli routerów (2015-2025)',
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
    }
}

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
        # Delay to allow click on listbox
        self.after(200, self.destroy_listbox)
    
    def get(self):
        return self.var.get()
    
    def set(self, value):
        self.var.set(value)

class RouterDiagnosticApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'pl'  # Default language: Polish
        self.root.title(TRANSLATIONS[self.current_lang]['title'])
        self.root.geometry("950x800")
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        
    def _(self, key):
        """Get translation for current language"""
        return TRANSLATIONS[self.current_lang].get(key, key)
        
    def switch_language(self):
        """Switch between Polish and English"""
        self.current_lang = 'en' if self.current_lang == 'pl' else 'pl'
        self.refresh_ui()
        
    def refresh_ui(self):
        """Refresh UI with new language"""
        # Update window title
        self.root.title(self._('title'))
        
        # Update all labels and buttons
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
        
    def create_widgets(self):
        # Top frame - info and language selector
        info_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        info_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # Language selector in top right
        lang_frame = tk.Frame(info_frame, bg='#2c3e50')
        lang_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        
        self.lang_label = tk.Label(lang_frame, text=self._('language'), 
                                   font=('Arial', 9), bg='#2c3e50', fg='white')
        self.lang_label.pack(side=tk.LEFT, padx=5)
        
        lang_btn = tk.Button(lang_frame, text="🇵🇱 PL / 🇬🇧 EN", 
                            command=self.switch_language,
                            bg='#34495e', fg='white', font=('Arial', 9, 'bold'),
                            relief=tk.RAISED, bd=2)
        lang_btn.pack(side=tk.LEFT)
        
        title_label = tk.Label(info_frame, text="🔍 Router Diagnostic Tool", 
                              font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=10)
        
        self.db_info_label = tk.Label(info_frame, 
                          text=self._('db_info').format(len(ROUTER_DATABASE)),
                          font=('Arial', 9), bg='#2c3e50', fg='#ecf0f1')
        self.db_info_label.pack()
        
        # Input frame
        self.input_frame = tk.LabelFrame(self.root, text=self._('params'), 
                                   font=('Arial', 10, 'bold'), padx=10, pady=10)
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Router IP
        self.ip_label = tk.Label(self.input_frame, text=self._('ip_label'), font=('Arial', 9))
        self.ip_label.grid(row=0, column=0, sticky='w', pady=5)
        self.ip_entry = tk.Entry(self.input_frame, width=30, font=('Arial', 9))
        self.ip_entry.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        self.ip_entry.insert(0, "192.168.1.1")
        
        # Ping button
        self.ping_btn = tk.Button(self.input_frame, text=self._('ping_btn'), command=self.ping_router, 
                           bg='#3498db', fg='white', font=('Arial', 9))
        self.ping_btn.grid(row=0, column=2, padx=5)
        
        # Producer
        self.producer_label = tk.Label(self.input_frame, text=self._('producer_label'), font=('Arial', 9))
        self.producer_label.grid(row=1, column=0, sticky='w', pady=5)
        self.producer_var = tk.StringVar()
        self.producer_combo = ttk.Combobox(self.input_frame, textvariable=self.producer_var, 
                                          values=get_producers(), width=27, font=('Arial', 9))
        self.producer_combo.grid(row=1, column=1, sticky='w', pady=5, padx=5)
        self.producer_combo.bind("<<ComboboxSelected>>", self.update_models)
        
        # Router model
        self.model_label = tk.Label(self.input_frame, text=self._('model_label'), font=('Arial', 9))
        self.model_label.grid(row=2, column=0, sticky='w', pady=5)
        self.router_var = tk.StringVar()
        self.router_combo = ttk.Combobox(self.input_frame, textvariable=self.router_var, 
                                        values=get_all_models(), width=27, font=('Arial', 9))
        self.router_combo.grid(row=2, column=1, sticky='w', pady=5, padx=5)
        self.router_combo.bind("<<ComboboxSelected>>", self.show_spec)
        
        # Search with autocomplete
        self.search_label = tk.Label(self.input_frame, text=self._('search_label'), font=('Arial', 9))
        self.search_label.grid(row=3, column=0, sticky='w', pady=5)
        
        self.search_entry = AutocompleteEntry(
            self.input_frame,
            autocomplete_list=get_all_models(),
            font=('Arial', 9),
            width=28
        )
        self.search_entry.grid(row=3, column=1, sticky='w', pady=5, padx=5)
        
        self.search_btn = tk.Button(self.input_frame, text=self._('search_btn'), command=self.search_models,
                             bg='#27ae60', fg='white', font=('Arial', 9))
        self.search_btn.grid(row=3, column=2, padx=5)
        
        # Action buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.show_btn = tk.Button(btn_frame, text=self._('show_btn'), command=self.show_spec,
                           bg='#e67e22', fg='white', font=('Arial', 10, 'bold'), height=2)
        self.show_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.clear_btn = tk.Button(btn_frame, text=self._('clear_btn'), command=self.clear_output,
                            bg='#95a5a6', fg='white', font=('Arial', 10, 'bold'), height=2)
        self.clear_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Output frame
        self.output_frame = tk.LabelFrame(self.root, text=self._('results'), 
                                    font=('Arial', 10, 'bold'), padx=10, pady=10)
        self.output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.output_text = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, 
                                                     font=('Courier New', 9), height=20)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text=self._('status_ready'), 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W, font=('Arial', 8))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def update_models(self, event=None):
        """Update model list after selecting producer"""
        producer = self.producer_var.get()
        if producer:
            models = [model for model, spec in ROUTER_DATABASE.items() 
                     if spec.get('Producent') == producer]
            self.router_combo['values'] = sorted(models)
            self.status_bar.config(text=self._('status_found').format(len(models), producer))
    
    def search_models(self):
        """Search router models"""
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
        """Execute ping to router"""
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
        """Display selected router specification"""
        selected = self.router_var.get()
        if not selected:
            messagebox.showwarning(self._('warn_no_selection'), self._('warn_select_model'))
            return
        
        spec = ROUTER_DATABASE.get(selected, {})
        if not spec:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, self._('no_spec'))
            self.status_bar.config(text=self._('error_no_data'))
            return
        
        # Format output
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, "=" * 80 + "\n")
        self.output_text.insert(tk.END, self._('spec_header').format(selected))
        self.output_text.insert(tk.END, "=" * 80 + "\n\n")
        
        # Display all parameters
        for key, value in spec.items():
            self.output_text.insert(tk.END, f"{key:.<35} {value}\n")
        
        self.output_text.insert(tk.END, "\n" + "=" * 80 + "\n")
        self.status_bar.config(text=self._('status_displayed').format(selected))
    
    def clear_output(self):
        """Clear output field"""
        self.output_text.delete('1.0', tk.END)
        self.status_bar.config(text=self._('status_cleared'))

def main():
    root = tk.Tk()
    app = RouterDiagnosticApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
