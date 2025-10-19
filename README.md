# 🔍 Router Diagnostic Tool

**Professional Router Management & Diagnostic System**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Database](https://img.shields.io/badge/Routers-829-orange.svg)

A comprehensive, multilingual (🇵🇱 Polish / 🇬🇧 English) router diagnostic and management application with an extensive database of approximately 829 router models from 2005–2025.

---

## 📸 Screenshot

![Application Screenshot](pic.jpg)

*(Place `pic.jpg` in the repository root to render this image.)*

---

## ✨ Key Features

### 🌐 Network Diagnostics
- **Ping Test** – Real-time connection testing to router
- **Network Analysis** – Advanced diagnostics with detailed output
- **Multi-router Support** – Test multiple devices simultaneously

### 📊 Extensive Router Database
- **~829 Models** – Complete router database (2005–2025)
- **0 Built-in Photos** – Images loaded dynamically; none embedded in README
- **30+ Specifications** – Detailed technical information including:
  - Wi-Fi standards (802.11g/n/ac/ax/be)
  - Ethernet speeds (100 Mbps–10 Gbps)
  - Band support (Single/Dual/Tri/Quad-band)
  - SIM card slot (4G/5G support)
  - USB ports (2.0/3.0/3.1)
  - PoE support
  - VPN Server/Client
  - Mesh networking (AiMesh, OneMesh, Velop etc.)
  - MU-MIMO & OFDMA
  - Beamforming
  - QoS & Parental Controls
  - And many more…

### 🏢 Supported Manufacturers
Linksys, ASUS, Netgear, TP-Link, D-Link, Apple, Google, Amazon, Xiaomi, Ubiquiti, Synology, MikroTik, Buffalo, Zyxel, Huawei, ZTE, Tenda, Cudy and more.

### 🌍 Multilingual Interface
- **Polish (🇵🇱)** and **English (🇬🇧)**
- Easy language switch

---

## 📦 Installation

### Prerequisites
```bash
Python 3.8 or higher
```

### Install Dependencies
```bash
pip install pillow
```

### Quick Start
```bash
# 1. Clone repository
git clone https://github.com/yourusername/router-diagnostic-tool.git
cd router-diagnostic-tool

# 2. Run application
python router_diag_gui_multilang.py
```

---

## 📁 Project Structure

```
router-diagnostic-tool/
├── router_diag_gui_multilang.py   # Main GUI application
├── router_database.py            # Database library with hardcoded image URLs
├── router_database.csv           # Router specifications database (~829 models)
├── expand_router_database.py     # Script to add extra columns (SIM, USB, PoE, etc.)
├── add_image_urls_to_database.py # Script to add image URLs to CSV
├── final_router_db.py            # Script to regenerate database (3000+ models)
├── pic.jpg                       # Screenshot displayed above
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation (this file)
```

---

## 🚀 Usage Guide

1. **Launch Application**
   ```bash
   python router_diag_gui_multilang.py
   ```
2. **Network Testing** – Enter router IP, click Ping
3. **Router Lookup** – Select manufacturer and model, click Show Specification
4. **Search** – Use search box with autocomplete
5. **Switch Language** – Click PL/EN toggle

---

## 📝 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
