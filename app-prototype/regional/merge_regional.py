import json, hashlib, glob, os
P = os.path.dirname(os.path.abspath(__file__)) + "/../"  # the app-prototype folder
cat = json.load(open(P+"../value-tracker/services.json"))  # read only
cat = cat["services"] if isinstance(cat, dict) else cat
taken = {v["id"] for v in cat}
for f in ["alternatives.json","explore-extra.json"]: taken |= {a["id"] for a in json.load(open(P+f))["services"]}
PAL = ["#2563eb","#0f766e","#b45309","#7c3aed","#be123c","#0369a1","#4d7c0f","#c2410c","#334155","#9d174d"]
out, seen = [], set()
# approved region files only (listed in regional/approved.txt)
for name in open(P+"regional/approved.txt").read().split():
    for a in json.load(open(P+"regional/"+name+".json")):
        if a["id"] in taken or a["id"] in seen: print("skip dup", a["id"]); continue
        if not a.get("service_states"): print("skip no states", a["id"]); continue
        seen.add(a["id"]); a.setdefault("alternative_to", []); a["region_group"] = name
        a.setdefault("color", PAL[int(hashlib.md5(a["id"].encode()).hexdigest(), 16) % len(PAL)])
        w = [x for x in a["name"].replace("+"," +").split() if (x[0].isalnum() or x=="+") and x != "The"]
        a.setdefault("mark", (w[0][0] + (w[1][0] if len(w) > 1 else w[0][1:2])) if w else "?")
        if a.get("default_plan") not in [p["id"] for p in a["plans"]]: a["default_plan"] = a["plans"][0]["id"]
        for f in a.get("features", []):
            if f.get("plans") != "all" and not isinstance(f.get("plans"), list): f["plans"] = "all"
        out.append(a)
json.dump({"generated_at":"2026-10-19","note":"Regional providers, shown only to users in service_states. verified=false means the price came from a news or review site.","services":out}, open(P+"regional.json","w"), indent=1)
from collections import Counter
print(len(out), Counter(a["category"] for a in out))
