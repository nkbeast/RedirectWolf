#!/usr/bin/env python3
import os
import sys
import asyncio
import httpx
import yaml
import click
from datetime import datetime
from urllib.parse import urlparse, quote

TOOL_NAME = "RedirectWolf"
PAYLOAD_URL = "https://raw.githubusercontent.com/nkbeast/Payloads/main/openredirect/openredirect.txt"
CONFIG_PATH = os.path.expanduser("~/.config/redirectwolf/config.yaml")

HEADERS = {
    "Tool-Name": TOOL_NAME,
    "Developed-by": "NK",
    "Contact-us": "naveenbeastyt@gmail.com"
}

RED = '\x1b[31;1m'
GREEN = '\x1b[32;1m'
BLUE = '\x1b[34;1m'
MAGENTA = '\x1b[35;1m'
RESET = '\x1b[0m'

BANNER = r"""
     +--^----------,--------,-----,--------^-,       
     | |||||||||   `--------'     |          O       
     `+---------------------------^----------|       
       `\_,---------,---------,--------------'       
         / XXXXXX /'|       /'                        
        / XXXXXX /  `\    /'                         
       / XXXXXX /`-------'                          
      / XXXXXX /                                    
     / XXXXXX /                                     
    (________(                By NK             
     `------'                                       

┌──────────────────────────────────────────────┐
│  🎯 REDIRECTWOLF - OPEN REDIRECT SNIPER      │
└──────────────────────────────────────────────┘
"""

html_lines = []
html_lock = asyncio.Lock()
output_lock = asyncio.Lock()
counter_lock = asyncio.Lock()
scanned = 0
vulnerable = 0

def set_webhook(url):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        yaml.dump({"webhook": url}, f)
    print(f"{GREEN}[✓] Webhook saved!{RESET}")

def get_webhook():
    try:
        with open(CONFIG_PATH) as f:
            return yaml.safe_load(f).get("webhook", "Null")
    except:
        return "Null"

async def send_discord(webhook, poc_url):
    data = {
        "username": TOOL_NAME,
        "embeds": [{
            "title": "🐺 Open Redirect Detected!",
            "description": f"**PoC URL:** {poc_url}",
            "color": 16711680
        }]
    }
    async with httpx.AsyncClient() as client:
        try:
            await client.post(webhook, json=data, timeout=5)
        except:
            pass

async def write_html(poc_url):
    async with html_lock:
        html_lines.append(f"<tr><td>{datetime.now()}</td><td><a href='{poc_url}' target='_blank'>{poc_url}</a></td></tr>")

def generate_html():
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RedirectWolf Report</title>
    <style>
        body {{ font-family: monospace; background: #0e0e0e; color: #eee; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 8px 12px; border: 1px solid #555; }}
        a {{ color: #00f2ff; text-decoration: none; }}
        h1 {{ color: #ff4444; }}
    </style>
</head>
<body>
    <h1>🐺 RedirectWolf Report</h1>
    <p>Generated: {datetime.now()}</p>
    <table>
        <tr><th>Timestamp</th><th>PoC URL</th></tr>
        {''.join(html_lines)}
    </table>
</body>
</html>
"""
    with open("redirectwolf-report.html", "w") as f:
        f.write(html)
    print(f"{MAGENTA}[✓] HTML report saved: redirectwolf-report.html{RESET}")

async def print_stats(total):
    while scanned < total:
        async with counter_lock:
            done = scanned
            vuln = vulnerable
        sys.stdout.write(f"\r{BLUE}[🔄] Scanned: {done}/{total} | Found: {vuln}{RESET}")
        sys.stdout.flush()
        await asyncio.sleep(0.5)
    print()

async def worker(queue, client, output, verbose, webhook, html_flag, total):
    global scanned, vulnerable
    while True:
        try:
            base_url, payload = await queue.get()
        except asyncio.CancelledError:
            break  # Exit cleanly if cancelled while waiting for task

        try:
            fullurl = f"{base_url.rstrip('/')}/{quote(payload)}"
            try:
                res = await client.get(fullurl, headers=HEADERS, follow_redirects=False, timeout=5)
                status = res.status_code
                location = res.headers.get("location", "")
                domain = urlparse(location).netloc

                async with counter_lock:
                    scanned += 1

                if status in [301, 302] and "evil.com" in domain:
                    async with counter_lock:
                        vulnerable += 1

                    print(f"\n{RED}💥 [Vulnerable]{RESET} => {BLUE}{base_url}{RESET}")
                    print(f"{MAGENTA}🔗 PoC: {RESET}{fullurl}\n")

                    if output:
                        async with output_lock:
                            with open(output, "a") as f:
                                f.write(fullurl + "\n")
                    if webhook != "Null":
                        await send_discord(webhook, fullurl)
                    if html_flag:
                        await write_html(fullurl)
                elif verbose:
                    print(f"{GREEN}[Checked]{RESET} {fullurl} => {status}")
            except Exception as e:
                if verbose:
                    print(f"{RED}[x] Error:{RESET} {fullurl} [{e}]")
        finally:
            queue.task_done()
async def run_scan(targets, payloads, output, verbose, webhook, rate, html_flag):
    queue = asyncio.Queue()
    async with httpx.AsyncClient() as client:
        for target in targets:
            for payload in payloads:
                await queue.put((target, payload))

        total = queue.qsize()
        tasks = [asyncio.create_task(worker(queue, client, output, verbose, webhook, html_flag, total)) for _ in range(rate)]
        stats_task = asyncio.create_task(print_stats(total))

        await queue.join()
        for task in tasks:
            task.cancel()
        await asyncio.sleep(0.1)
        stats_task.cancel()

@click.command()
@click.option('--url', '-u', help='Scan a single URL')
@click.option('--list', '-l', help='Scan from list of URLs')
@click.option('--output', '-o', help='Save vulnerable URLs to a text file')
@click.option('--webhook', '-w', help='Set Discord webhook')
@click.option('--rate', default=20, help='Concurrency rate (default: 20)')
@click.option('--verbose', '-v', is_flag=True, help='Show all scan attempts')
@click.option('--html', is_flag=True, help='Generate HTML report')
def main(url, list, output, webhook, rate, verbose, html):
    print(BANNER)
    print(f"{GREEN}Beast mode scanning enabled — async + low RAM + HTML + Discord 🐺{RESET}\n{'-'*60}")

    if webhook:
        set_webhook(webhook)
        return

    saved_webhook = get_webhook()

    try:
        r = httpx.get(PAYLOAD_URL, timeout=10)
        payloads = r.text.strip().splitlines()
        if "<!DOCTYPE html>" in payloads[0]:
            print(f"{RED}[x] Payload file is not raw text. Fix the GitHub URL.{RESET}")
            return
    except Exception as e:
        print(f"{RED}[x] Could not fetch payloads:{RESET} {e}")
        return

    targets = []
    if url:
        targets = [url]
    elif list:
        if not os.path.exists(list):
            print(f"{RED}[x] List file not found: {list}{RESET}")
            return
        with open(list, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
    else:
        print(f"{RED}[x] Provide either --url or --list to scan.{RESET}")
        return

    asyncio.run(run_scan(targets, payloads, output, verbose, saved_webhook, rate, html))
    if html:
        generate_html()
    print(f"\n{GREEN}Scan completed. RedirectWolf has finished hunting 🐺✅{RESET}")

if __name__ == '__main__':
    main()
