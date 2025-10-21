Router Diagnostic Tool
A comprehensive, multilingual (Polish/English) router diagnostic application with an extended database of 829 models from 2005–2025—including live preview of router appearance from Google Images.

🚀 Features
Database of 829 routers (2005–2025)

Live Google Images preview (no browser required!)

Search and filter by producer, model, or features

Ping/network diagnostics

Detailed spec view for each router

Multilingual interface: 🇵🇱 Polish / 🇬🇧 English

No Selenium, no Chrome required

💻 Technologies
Python 3.8+

Tkinter (GUI)

Pillow (image handling)

Requests, BeautifulSoup (Google image scraping)

CSV (database)

subprocess (network tests)

🛠 Installation
1. Clone
bash
git clone https://github.com/yourusername/router-diagnostic-tool.git
cd router-diagnostic-tool
2. Install dependencies
bash
pip install pillow requests beautifulsoup4
3. Run
bash
python router_diag_gui_multilang.py
⏱ Quick Start
Run program

Select router manufacturer and model

View specs and instant photos from Google Images in the right panel

Use search/autocomplete for quick filtering

📋 Project Structure
text
router-diagnostic-tool/
├── router_diag_gui_multilang.py    # Main application
├── router_database.py              # Database helper, loads .csv
├── router_database.csv             # Router data (829 models)
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation (this file)
📊 Example Specifications
Field	Example
Model	TP-Link Archer C7
Producer	TP-Link
Production Year	2016
WiFi Power	20 dBm
Ethernet Speed	1 Gbps
WiFi Standard	802.11ac Dual Band
5GHz Support	Yes
Firmware Version	3.15.3 Build 18020
Max WiFi Throughput	1750 Mbps
Max Ethernet Speed	1 Gbps
Features	MU-MIMO, Beamforming, WPS, USB
🖼 Router Image Live Preview
Whenever you choose a model, the app automatically:

Queries Google Images for your router

Shows up to 3 images directly in the app panel (no browser needed)

Falls back to a custom placeholder if no images found

All images are loaded live from the internet and are not included in the repository.

🌍 Multilingual Support
Polish and English UI

Convenient language switch button

📝 License
MIT License. See LICENSE for full text.

🤝 Contributing
Pull requests and issues are welcome! Please update documentation and add tests when relevant.

📞 Support
Issues: https://github.com/yourusername/router-diagnostic-tool/issues

Email: youremail@example.com

📣 Credits
BeautifulSoup

Pillow

Google Images

Community contributors

🧑‍💻 Status
Stable: Version 1.0 (October 2025)

Database: 829 router models

Live image preview (Google Images) without browser or third-party API
