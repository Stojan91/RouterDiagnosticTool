# RouterDiagnosticTool[README.md](https://github.com/user-attachments/files/22987282/README.md)
# 🔍 Router Diagnostic Tool

**Professional router diagnostic application with a database of 1000+ router models (2015-2025)**

![Router Diagnostic Tool](pic.jpg)

## 📋 Description

Router Diagnostic Tool is a multilingual (Polish/English) desktop application for browsing specifications of router models from various manufacturers. The application features an intuitive graphical interface, autocomplete search functionality, and a comprehensive database of modern routers including WiFi 6, WiFi 6E, and WiFi 7 models.

## ✨ Features

### 🌍 **Multilingual Interface**
- **Polish** and **English** language support
- Easy switching between languages with one click
- Complete translations of all interface elements

### 🔎 **Smart Search**
- **Autocomplete** functionality (Google-style suggestions)
- Real-time search results as you type
- Search by router model name
- Filter by manufacturer
- Browse by production year

### 📊 **Comprehensive Database**
- **1000+ router models** from 2015-2025
- **25+ manufacturers**: TP-Link, ASUS, Netgear, D-Link, Xiaomi, Linksys, MikroTik, Huawei, Fritz!Box, Cisco, and more
- Complete technical specifications for each model
- Support for latest WiFi standards (WiFi 6, WiFi 6E, WiFi 7)

### 🛠️ **Diagnostic Tools**
- **Ping test** - test connectivity to your router
- **Detailed specifications** - view complete router parameters
- **Export capabilities** - copy specifications for documentation

### 📱 **User-Friendly Interface**
- Modern, clean design
- Intuitive navigation
- Keyboard shortcuts support (Arrow keys, Enter)
- Status bar with helpful information
- Clear output window with formatted results

## 🚀 Installation

### Requirements
- **Python 3.7+**
- **tkinter** (usually included with Python)
- Standard Python libraries: `csv`, `subprocess`, `platform`

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/router-diagnostic-tool.git
cd router-diagnostic-tool
```

2. **Ensure all files are present:**
```
router-diagnostic-tool/
├── router_diag_gui_multilang.py    # Main application
├── router_database.py              # Database library
├── router_database.csv             # Router database (1000+ models)
├── README.md                       # Documentation
└── pic.jpg                         # Screenshot
```

3. **Run the application:**
```bash
python router_diag_gui_multilang.py
```

## 📦 Creating Standalone Executable (.exe)

### Using PyInstaller

1. **Install PyInstaller:**
```bash
pip install pyinstaller
```

2. **Build the executable:**
```bash
pyinstaller --onefile --windowed --add-data "router_database.csv;." --name="RouterDiagnostic" router_diag_gui_multilang.py
```

3. **Find your executable:**
```
dist/RouterDiagnostic.exe
```

### Using auto-py-to-exe (GUI Method)

1. **Install auto-py-to-exe:**
```bash
pip install auto-py-to-exe
```

2. **Launch the GUI:**
```bash
auto-py-to-exe
```

3. **Configure:**
   - Script Location: `router_diag_gui_multilang.py`
   - One File: ✓ Enabled
   - Console Window: **Window Based**
   - Additional Files: Add `router_database.csv` and `router_database.py`

4. **Click "Convert .py to .exe"**

## 💻 Usage

### Basic Workflow

1. **Start the application**
2. **Select language** (PL/EN) using the button in top-right corner
3. **Search for router:**
   - Type in search box (autocomplete will show suggestions)
   - OR select manufacturer from dropdown
   - OR choose model directly from the list
4. **View specifications** by clicking "Show Specification" button
5. **Test connectivity** by entering router IP and clicking "Ping"

### Keyboard Shortcuts

- **↑/↓ Arrow Keys** - Navigate autocomplete suggestions
- **Enter** - Select highlighted suggestion
- **Tab** - Move between fields
- **Esc** - Close autocomplete

## 📊 Database Structure

The database includes the following information for each router:

| Field | Description |
|-------|-------------|
| Model | Router model name |
| Producent | Manufacturer |
| Data produkcji | Production year (2015-2025) |
| Moc WiFi | WiFi power (dBm) |
| Moc Ethernetu | Ethernet speed |
| Liczba gniazd Ethernet | Number of Ethernet ports |
| Rodzaj sygnału WiFi | WiFi standard and frequency bands |
| Obsługa 5G | 5GHz support (Yes/No) |
| Wersja firmware | Firmware version |
| Maksymalna przepustowość WiFi | Maximum WiFi throughput |
| Maksymalna przepustowość Ethernet | Maximum Ethernet throughput |
| Lista funkcji | Features list (Mesh, QoS, VPN, etc.) |

### Supported WiFi Standards

- 802.11n (WiFi 4)
- 802.11ac (WiFi 5)
- 802.11ac Wave 2 (WiFi 5)
- 802.11ax (WiFi 6)
- 802.11ax (WiFi 6E)
- 802.11be (WiFi 7)

## 🏢 Supported Manufacturers

- TP-Link
- ASUS
- Netgear
- D-Link
- Linksys
- Xiaomi
- MikroTik
- Huawei
- Fritz!Box (AVM)
- Cisco
- Tenda
- Mercusys
- Totolink
- ZTE
- Cudy
- Acer
- Ubiquiti
- Synology
- Google
- Amazon (eero)
- Aruba
- EnGenius
- Zyxel
- And more...

## 🔧 Extending the Database

To add more router models:

1. **Edit `router_database.csv`** using any text editor or Excel
2. **Follow the format:**
```csv
Model,Producent,Data produkcji,Moc WiFi,Moc Ethernetu,...
TP-Link Archer AX11000,TP-Link,2024,30 dBm,10 Gbps,...
```
3. **Save the file** with UTF-8 encoding
4. **Restart the application**

Or use the provided generator script:
```bash
python generate_router_db.py
```

## 🐛 Troubleshooting

### Application won't start
- Ensure Python 3.7+ is installed
- Verify all files are in the same directory
- Check that `router_database.csv` exists

### Database not loading
- Verify CSV file encoding is UTF-8
- Check CSV format matches the structure
- Ensure no empty lines at the end of the file

### Autocomplete not working
- Check if model names are correctly formatted
- Ensure CSV file loads without errors

## 📝 License

This project is released under the **MIT License**.

```
MIT License

Copyright (c) 2025 Router Diagnostic Tool

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

## 🙏 Acknowledgments

- Router manufacturers for publicly available specifications
- Python tkinter community for GUI development resources
- Contributors to the router database

## 📈 Roadmap

- [ ] Add firmware update checking
- [ ] Implement router comparison feature
- [ ] Add more manufacturers and models
- [ ] Export specifications to PDF/Excel
- [ ] Add router performance benchmarks
- [ ] Integrate with online router databases
- [ ] Add dark mode theme
- [ ] Create mobile version

---

**⭐ If you find this tool useful, please consider giving it a star on GitHub!**

---

*Last updated: October 2025*
*Version: 1.0.0*
