# Builds one self-contained HTML file of the prototype (data inlined) that testers can open without a claude.ai account.
# Run: python3 build_standalone.py  -> subscription-keeper.html beside this script.
import json, os, re
P = os.path.dirname(os.path.abspath(__file__)) + "/../"
SVC = "/mnt/project-files/value-tracker/services.json"  # read only; owned by the value tracker thread
data = {"services.json": json.load(open(SVC))}
for f in ["alternatives.json", "explore-extra.json", "location-prices.json", "regional.json"]:
    data[f] = json.load(open(P + f))
html = open(P + "index.html").read()
shim = ("<script>window.__DATA=" + json.dumps(data, separators=(",", ":")).replace("</", "<\\/") + ";"
        "(()=>{const f=window.fetch.bind(window);window.fetch=(u,o)=>u in window.__DATA?Promise.resolve(new Response(JSON.stringify(window.__DATA[u]),{headers:{'Content-Type':'application/json'}})):f(u,o);})();</script>\n")
html = html.replace("<script>", shim + "<script>", 1)
html = re.sub(r"Prototype · Version (\d+)", r"Prototype · Version \1 · Standalone copy", html, count=1)
# Home-screen app (v112, Cuong): icon files and manifest sit beside the public site's index.html in the repo root.
HOME = ('<link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">'
        '<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#081634">'
        '<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">'
        '<meta name="apple-mobile-web-app-status-bar-style" content="black"><meta name="apple-mobile-web-app-title" content="MoSuBi">')
out = "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">" + HOME + "</head><body>\n" + html + "\n</body></html>\n"
open(os.path.dirname(os.path.abspath(__file__)) + "/subscription-keeper.html", "w").write(out)
print(len(out), "bytes")
