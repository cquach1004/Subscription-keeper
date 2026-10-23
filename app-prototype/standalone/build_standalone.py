# Builds one self-contained HTML file of the prototype (data inlined) that testers can open without a claude.ai account.
# Run: python3 build_standalone.py  -> subscription-keeper.html beside this script.
import json, os, re
P = os.path.dirname(os.path.abspath(__file__)) + "/../"
SVC = P + "../value-tracker/services.json"  # read only; owned by the value tracker
data = {"services.json": json.load(open(SVC))}
for f in ["alternatives.json", "explore-extra.json", "location-prices.json", "regional.json"]:
    data[f] = json.load(open(P + f))
html = open(P + "index.html").read()
shim = ("<script>window.__DATA=" + json.dumps(data, separators=(",", ":")).replace("</", "<\\/") + ";"
        "(()=>{const f=window.fetch.bind(window);window.fetch=(u,o)=>u in window.__DATA?Promise.resolve(new Response(JSON.stringify(window.__DATA[u]),{headers:{'Content-Type':'application/json'}})):f(u,o);})();</script>\n")
html = html.replace("<script>", shim + "<script>", 1)
html = re.sub(r"Prototype · Version (\d+)", r"Prototype · Version \1 · Standalone copy", html, count=1)
out = "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"></head><body>\n" + html + "\n</body></html>\n"
open(os.path.dirname(os.path.abspath(__file__)) + "/subscription-keeper.html", "w").write(out)
print(len(out), "bytes")
