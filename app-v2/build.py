# MoSuBi v2 build (2026-11-11, Cuong's pivot): one self-contained HTML file with the verified data inlined.
# Run: python3 /mnt/project-files/app-v2/build.py  ->  app-v2/mosubi.html
# Source of truth stays where it was: value-tracker/services.json and the app-prototype/*.json data files are read, never written.
# Brand logos, category names, popular services and sourced price news are lifted from the v1 app (app-prototype/index.html).
import json, os, subprocess, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
V1 = os.path.join(ROOT, "app-prototype", "index.html")


def const_block(src, name):
    """Return the JS literal assigned to `const NAME = ...` (balanced brackets)."""
    i = src.index("const %s = " % name) + len("const %s = " % name)
    open_ch = src[i]
    close_ch = {"{": "}", "[": "]"}[open_ch]
    depth, j, q = 0, i, None
    while True:
        c = src[j]
        if q:
            if c == "\\":
                j += 2
                continue
            if c == q:
                q = None
        elif c in "\"'`":
            q = c
        elif c in "{[":
            depth += 1
        elif c in "}]":
            depth -= 1
            if depth == 0:
                return src[i:j + 1]
        j += 1


v1 = open(V1).read()
names = ["LOGOS", "COLORS", "CATEGORY_LABEL", "POPULAR", "TRENDS", "US_STATES", "COUNTRIES", "US_ONLY", "PROTECTION_CATS", "PROVIDER_LABEL"]
js = "const o={};" + "".join("o.%s=%s;" % (n, const_block(v1, n)) for n in names) + "process.stdout.write(JSON.stringify(o));"
legacy = json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout)

data = {"services": json.load(open(os.path.join(ROOT, "value-tracker", "services.json")))}
for f in ["alternatives", "explore-extra", "regional", "location-prices"]:
    data[f] = json.load(open(os.path.join(ROOT, "app-prototype", f + ".json")))
data["legacy"] = legacy
data["additions"] = json.load(open(os.path.join(HERE, "data", "additions.json")))
data["scout"] = json.load(open(os.path.join(HERE, "data", "scout.json")))

src = open(os.path.join(HERE, "src", "app.html")).read()
blob = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
out = src.replace("/*__DATA__*/null", blob, 1)
assert out != src, "data placeholder missing"
# Home-screen icon (Subi, 2026-11-11): files sit beside v2/index.html on the public site.
HOME = ('<link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">'
        '<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png"><link rel="manifest" href="manifest.webmanifest">'
        '<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">'
        '<meta name="apple-mobile-web-app-status-bar-style" content="black"><meta name="apple-mobile-web-app-title" content="MoSuBi">')
site = out.replace('<meta name="theme-color" content="#142f73">', '<meta name="theme-color" content="#142f73">\n' + HOME, 1)
open(os.path.join(HERE, "mosubi.html"), "w").write(site)
print(len(out), "bytes ->", os.path.join(HERE, "mosubi.html"))
# Artifact copy: the Artifact host adds its own document shell, so drop ours.
art = re.sub(r"<!doctype html>\s*<html[^>]*>\s*<head>|</head>\s*<body>|</body>\s*</html>\s*$", "", out, flags=re.I)
art = art.replace('<meta charset="utf-8">', "").replace('<meta name="viewport" content="width=device-width, initial-scale=1">', "")
open(os.path.join(HERE, "mosubi-artifact.html"), "w").write(art)
