<h1 align="center">🐺 RedirectWolf</h1>

<p align="center">
  <b>Async Open Redirect Scanner</b><br>
  Ultra-fast bulk scanner to identify open redirect vulnerabilities.<br>
  Developed with <code>httpx</code>, <code>asyncio</code>, and built for performance.<br>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Made%20by-NK-blue?style=flat-square&logo=python" />
  <img src="https://img.shields.io/github/license/nkbeast/RedirectWolf?style=flat-square" />
  <img src="https://img.shields.io/github/stars/nkbeast/RedirectWolf?style=flat-square" />
  <img src="https://img.shields.io/badge/status-async%20turbo-green?style=flat-square" />
</p>

---

![RedirectWolf Banner](https://raw.githubusercontent.com/nkbeast/RedirectWolf/main/assets/banner.gif)

---

## 🧠 What is RedirectWolf?

**RedirectWolf** is a fully asynchronous, low-RAM, high-speed open redirect vulnerability scanner — perfect for mass scanning and bug bounty automation. It supports:

- ✅ Async-powered scanning with `httpx` + `asyncio`
- ✅ Bulk mode for huge URL lists
- ✅ Discord webhook alerts
- ✅ HTML & TXT report generation
- ✅ Custom rate control
- ✅ Verbose logging and zone-sniper-style UX

---

## 🚀 Features

| Feature         | Description |
|----------------|-------------|
| 🧠 Async Core   | Built with `asyncio.Queue` for max speed and low memory usage |
| ⚡ Turbo Mode   | Scan thousands of URLs with controlled concurrency |
| 📄 HTML Report  | Generate clean, clickable HTML reports with `--html` |
| 💾 Output File  | Save vulnerable results to `.txt` |
| 🔔 Webhook      | Discord alert support (`--webhook`) |
| 📢 Verbose Logs | Optional `-v` flag for detailed scanning logs |
| 🧪 PoC Friendly | Designed for `evil.com` redirection validation |

---

## 📦 Installation

```bash
pip install 
