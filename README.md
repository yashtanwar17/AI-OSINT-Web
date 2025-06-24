# 🔍 AI Web Scanner – OSINT & Vulnerability Assessment Tool

A modular, AI-powered web reconnaissance and vulnerability scanner that helps automate the discovery of security issues and OSINT data for a given domain. This project is designed to be free, extensible, and easy to modify, with a basic structure that can be improved further.

---

## ✅ Features

- 🧠 **AI Log Analysis**  
  Converts raw `log.txt` scan output into a human-readable report using a language model (via the SambaNova API).

- 🔍 **Recon & OSINT Modules**
  - Directory listing check
  - Employee enumeration (via search/dorking)
  - Expired domain checks
  - Email discovery using Google dorking
  - Subdomain takeover detection
  - Typosquatting scan
  - Admin panel finder
  - DNS/SPF/DKIM/DMARC validation

- 💻 **Web & CMS Vulnerability Detection**
  - Outdated CMS versions + known CVEs
  - JavaScript CDN inspection with Retire.js
  - Insecure headers detection
  - SSL misconfiguration scan
  - XSS vulnerability tester
  - Basic port scanner (non-Nmap)

- 🌐 **HTML Report UI**
  - Simple Flask app to view AI-analyzed reports in a clean format.

---

## ⚠️ Disclaimer & Notes

> This is a **basic starter framework** with several useful modules, but it is **not a fully advanced tool yet**.

- More detailed and deep scans will be added in the future.
- Several tools/modules still require enhancement or replacement with more robust alternatives.
- This project intentionally **avoids paid APIs** like Shodan, HaveIBeenPwned (HIBP), or Hunter.io — to keep it free and open.
- Using paid APIs **can significantly boost** the quality and depth of this scanner.
- Some modules (like CVE lookup) use external tools like `whatweb`, `retire.js`, and `node.js`. Please ensure they are installed and correctly configured in your environment.

---

## 🔧 Requirements

- Python 3.8+
- Node.js (for Retire.js)
- `whatweb` installed and accessible in your environment
- `pip install -r requirements.txt` (create your own with needed packages)

### External Dependencies:

- ✅ **SambaNova API**  
  Used for AI-based log interpretation. *(You can replace this with a local LLM like LLaMA or GPTQ for better security.)*

- ✅ **DNSDumpster API**  
  Used for subdomain enumeration in `sdtakeover.py`. You must supply your own valid API key.

---

## 🛠️ Configuration & Customization

- Modify `main.py` to change the scanning sequence or inputs.
- Run `flaskweb.py`
- then run `main.py` and wait, try refreshing flask web for report.
- Update or replace `sdtakeover.py` and other modules with your own keys/configs — **your API keys will not work with mine**.
- Want better accuracy or features? Integrate paid services like:
  - Shodan (host detection, ports, vulnerabilities)
  - HIBP (email breach detection)
  - Hunter.io (email discovery)

---

## 💡 Roadmap & Ideas

This is just a basic version. Planned improvements include:

- Vulnerability scoring (CVSS integration)
- Auto-patching suggestions
- Subdomain bruteforcing
- SQLi, LFI/RFI checks
- WordPress and other CMS plugins/themes scanner
- Multi-threaded or async performance boost
- Containerization (Docker support)

---

## 🙋 Troubleshooting

- **Some modules may fail or show errors** if:
  - Tools like `retire`, `whatweb`, or `node` aren't installed correctly.
  - APIs aren't set or configured for your environment.
- If something breaks, feel free to open an issue.

---

## 📜 License

This project is free and open-source for educational and research use only.

---

## 🤝 Contributing

Pull requests and suggestions are welcome! Help make this tool even more powerful.
This project was built with the help of AI tools (including ChatGPT) and various online resources, documentation, and open-source libraries. It served as a learning and experimentation platform to combine OSINT techniques, web security scanning, and AI-powered reporting into one modular system.
If you find this useful, feel free to contribute or fork it!

---

## 📷 Screenshots

<details>
<summary>Click to expand</summary>

![CLI Scan](https://via.placeholder.com/800x200?text=CLI+Scan+Output)
![AI Report UI](https://via.placeholder.com/800x200?text=AI+Generated+Flask+Report)

</details>
