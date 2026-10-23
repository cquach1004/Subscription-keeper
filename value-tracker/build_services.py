"""Builds value-tracker/services.json (schema v1)."""
import json, sys

def plan(id, name, monthly=None, annual=None, verified=True, note=None, intro=None):
    p = {"id": id, "name": name, "price_monthly": monthly, "price_annual": annual,
         "effective_monthly": round(monthly if monthly is not None else annual / 12, 2),
         "verified": verified}
    if note: p["note"] = note
    if intro: p["intro_offer"] = intro
    return p

def feat(id, name, plans="all", overlap=None):
    f = {"id": id, "name": name, "plans": plans}
    if overlap: f["overlap_tag"] = overlap
    return f

S = []
def svc(**k): S.append(k)

svc(id="spotify", name="Spotify Premium", category="music", user_listed=True,
    value_model="usage", use_unit="day you listened", use_period="month",
    benchmark={"good_at_or_below": 0.5, "poor_at_or_above": 1.5},
    plans=[plan("individual", "Individual", 12.99), plan("student", "Student", 6.99),
           plan("duo", "Duo (2 accounts)", 18.99), plan("family", "Family (up to 6)", 21.99)],
    default_plan="individual",
    features=[feat("ad_free", "Ad-free listening"), feat("offline", "Offline downloads"),
              feat("audiobooks", "15 hrs/month of audiobooks", ["individual", "duo", "family"]),
              feat("lossless", "Lossless audio"), feat("dj", "AI DJ and AI playlists"),
              feat("podcasts", "Video podcasts")],
    recent_changes=[{"date": "2026-02", "summary": "US prices rose $1-2 on every plan (Individual $11.99 to $12.99)."}],
    tips=["Duo or Family split with others cuts per-person cost to about $9.50 or $3.67.",
          "If you have Apple One or YouTube Premium you already pay for a music service."],
    sources=["https://www.soundguys.com/spotify-confirms-us-subscription-price-hike-151412/"])

svc(id="netflix", name="Netflix", category="video", user_listed=True,
    value_model="usage", use_unit="evening/title watched", use_period="month",
    benchmark={"good_at_or_below": 1.0, "poor_at_or_above": 4.0},
    plans=[plan("ads", "Standard with Ads", 8.99), plan("standard", "Standard", 19.99),
           plan("premium", "Premium (4K, 4 screens)", 26.99)],
    default_plan="standard",
    features=[feat("ad_free", "No ads", ["standard", "premium"]), feat("hd", "1080p HD"),
              feat("uhd", "4K + HDR, spatial audio", ["premium"]),
              feat("screens", "Watch on 2 screens (4 on Premium)"),
              feat("downloads", "Downloads", ["standard", "premium"]),
              feat("extra_member", "Extra member slot (+$7.99 / $9.99)", ["standard", "premium"]),
              feat("games", "Netflix Games"), feat("live", "Live events (sports, specials)")],
    recent_changes=[{"date": "2026-03", "summary": "Price increase on all plans: Standard now $19.99, Premium $26.99."}],
    tips=["Most people don't need Premium; 4K only matters on a 4K TV.",
          "Rotate: cancel between shows you want and resubscribe for a month at a time."],
    sources=["https://www.fox5ny.com/news/netflix-raising-prices-again-all-plans-how-much-more-youll-be-paying",
             "https://stream-wiser.com/prices"])

svc(id="evernote", name="Evernote", category="productivity", user_listed=True,
    value_model="usage", use_unit="day you used it", use_period="month",
    benchmark={"good_at_or_below": 0.5, "poor_at_or_above": 2.0},
    plans=[plan("starter", "Starter", None, 99.00,
                note="Monthly-equivalent of $99/yr; monthly billing is higher."),
           plan("advanced", "Advanced", None, 249.99)],
    default_plan="starter",
    features=[feat("sync", "Sync across devices", overlap="notes"), feat("offline", "Offline notebooks"),
              feat("doc_search", "Search inside PDFs and images"), feat("clipper", "Web clipper"),
              feat("ai", "AI Assistant / AI search"), feat("tasks", "Tasks and calendar"),
              feat("unlimited", "Unlimited notes and notebooks", ["advanced"])],
    recent_changes=[{"date": "2025-2026", "summary": "Plans renamed to Starter/Advanced; Starter caps at 1,000 notes and 20 notebooks."}],
    tips=["OneNote (in Microsoft 365) and Apple Notes cover most note-taking for no extra cost.",
          "Check your note count: Starter's 1,000-note cap may push you to Advanced."],
    sources=["https://www.eesel.ai/blog/evernote-pricing"])

svc(id="wsj", name="The Wall Street Journal", category="news", user_listed=True,
    value_model="usage", use_unit="article read", use_period="month",
    benchmark={"good_at_or_below": 0.5, "poor_at_or_above": 2.0},
    plans=[plan("digital", "Digital", 38.99, intro="$4/mo for the first 12 months"),
           plan("print_digital", "Print + Digital", 56.99)],
    default_plan="digital",
    features=[feat("articles", "Unlimited articles and app", overlap="business_news"),
              feat("enewspaper", "Digital print edition"), feat("audio", "Audio articles and podcasts"),
              feat("newsletters", "Subscriber newsletters"), feat("puzzles", "Puzzles"),
              feat("print", "Home delivery", ["print_digital"])],
    recent_changes=[],
    tips=["The intro rate ends after 12 months and the price jumps about 10x; set a reminder.",
          "Calling to cancel often triggers a retention offer near the intro price.",
          "Apple News+ (in Apple One Premier) includes a selection of WSJ stories."],
    sources=["https://subger.com/en/ke/service/wall-street-journal"])

svc(id="cnbc", name="CNBC+ / CNBC Pro", category="news", user_listed=True,
    value_model="usage", use_unit="hour watched", use_period="month",
    benchmark={"good_at_or_below": 1.0, "poor_at_or_above": 3.0},
    plans=[plan("plus", "CNBC+", 14.99), plan("pro", "CNBC Pro", 34.99, 299.99)],
    default_plan="plus",
    features=[feat("live", "Live CNBC and CNBC World stream", overlap="business_news"),
              feat("intl", "Asia and Europe live feeds"),
              feat("pro_articles", "Exclusive Pro stories and articles", ["pro"]),
              feat("pro_insight", "Analyst calls, Pro Playbook and real-time alerts", ["pro"]),
              feat("pro_talks", "Live Pro Talks and special reports", ["pro"])],
    recent_changes=[{"date": "2025-01", "summary": "CNBC+ launched as a lower-priced streaming tier without a cable login."}],
    tips=["Jim Cramer's Investing Club is a separate subscription ($49.99/mo or $399.99/yr), not part of Pro.",
          "If you have cable or a live-TV streamer, CNBC is already included.",
          "Overlaps with WSJ for market news; most people need one, not both."],
    sources=["https://apps.apple.com/app/id398018310", "https://agoodmovietowatch.com/platforms/cnbc/", "https://www.newscaststudio.com/2025/01/02/cnbc-plus-launch"])

svc(id="aaa", name="AAA Membership", category="auto", user_listed=True,
    value_model="insurance", use_unit="service call (tow, jump, lockout)", use_period="year",
    benchmark={"good_at_or_below": 75, "poor_at_or_above": 150},
    plans=[plan("classic", "Classic", None, 72, note="Prices vary by regional club; Hoosier club shown."),
           plan("plus", "Plus", None, 157), plan("premier", "Premier", None, 246)],
    default_plan="classic",
    features=[feat("tow", "Towing (3 / 100 / 200 miles)", overlap="roadside"),
              feat("roadside", "Jump start, flat tire, fuel delivery, lockout (4 calls/yr)", overlap="roadside"),
              feat("discounts", "Hotel, rental car and retail discounts"),
              feat("travel", "Trip interruption coverage"),
              feat("extra_cards", "2 extra household cardholders"),
              feat("home_lockout", "Home lockout reimbursement", ["premier"])],
    recent_changes=[],
    tips=["Car insurance roadside add-ons, new-car warranties and some credit cards cover tows; check before renewing.",
          "Plus/Premier mostly pay off if you drive long distances or rural roads (longer tows)."],
    sources=["https://www.hoosier.aaa.com/membership/compare-aaa-membership-plans"])

svc(id="icloud", name="Apple iCloud+", category="storage", user_listed=True,
    value_model="storage", use_unit="GB stored", use_period="month",
    benchmark=None,
    plans=[plan("50gb", "50 GB", 0.99, note="storage_gb=50"), plan("200gb", "200 GB", 2.99, note="storage_gb=200"),
           plan("2tb", "2 TB", 9.99, note="storage_gb=2000"), plan("6tb", "6 TB", 29.99, note="storage_gb=6000"),
           plan("12tb", "12 TB", 59.99, note="storage_gb=12000")],
    default_plan="200gb",
    features=[feat("storage", "Cloud storage and device backup", overlap="cloud_storage"),
              feat("hide_email", "Hide My Email aliases", overlap="email_alias"),
              feat("relay", "iCloud Private Relay", overlap="vpn"),
              feat("custom_domain", "Custom email domain"),
              feat("homekit", "HomeKit Secure Video"),
              feat("family", "Share with up to 5 family members")],
    recent_changes=[],
    tips=["Already included in Apple One (50 GB / 200 GB / 2 TB); don't pay for both.",
          "Check Settings > iCloud to see how much you use; many people can drop a tier."],
    sources=["https://blog.internxt.com/apple-icloud-pricing/"])

svc(id="m365", name="Microsoft 365", category="productivity", user_listed=True,
    value_model="usage", use_unit="day you used Office/Outlook/OneDrive", use_period="month",
    benchmark={"good_at_or_below": 0.5, "poor_at_or_above": 2.0},
    plans=[plan("personal", "Personal", 9.99, 99.99), plan("family", "Family (up to 6)", 12.99, 129.99),
           plan("premium", "Premium", 19.99, 199.99),
           plan("classic_personal", "Personal Classic (no Copilot)", None, 69.99,
                note="Hidden plan; reachable by starting to cancel.")],
    default_plan="personal",
    features=[feat("apps", "Desktop Word, Excel, PowerPoint"), feat("onenote", "OneNote", overlap="notes"),
              feat("onedrive", "1 TB OneDrive per person", overlap="cloud_storage"),
              feat("copilot", "Copilot AI in Office apps (60 credits/mo)", ["personal", "family", "premium"], overlap="ai_assistant"),
              feat("defender", "Microsoft Defender", overlap="antivirus"),
              feat("outlook", "Ad-free Outlook"), feat("clipchamp", "Clipchamp premium video editing")],
    recent_changes=[{"date": "2025-01", "summary": "Copilot bundled in; prices rose $3/mo. Classic plans without AI kept at old price."}],
    tips=["Don't use Copilot? Switch to Personal Classic at $69.99/yr (start the cancel flow to see it).",
          "Family covers 6 people with 1 TB each for $30/yr more than Personal."],
    sources=["https://office-watch.com/2026/microsoft-365-plans-overview/"])

svc(id="cloaked", name="Cloaked", category="privacy", user_listed=True,
    value_model="insurance", use_unit="time you used an alias or masked number", use_period="month",
    benchmark={"good_at_or_below": 1.0, "poor_at_or_above": 3.0},
    plans=[plan("individual", "Individual", 14.99, 119.99, note="$119.99/yr when billed annually ($10.00/mo).")],
    default_plan="individual",
    features=[feat("aliases", "Unlimited email and phone aliases", overlap="email_alias"),
              feat("data_removal", "Data broker removal (350+ brokers)", overlap="data_removal"),
              feat("call_guard", "Call Guard spam blocking"),
              feat("password", "Password manager", overlap="password_manager"),
              feat("vpn", "VPN", overlap="vpn"),
              feat("dark_web", "Dark web monitoring", overlap="identity_monitoring"),
              feat("insurance", "$1M identity theft insurance", overlap="identity_insurance")],
    recent_changes=[],
    tips=["Overlaps heavily with McAfee+ (VPN, passwords, data cleanup, monitoring). Pick one.",
          "iCloud+ Hide My Email gives free email aliases if you're on Apple."],
    sources=["https://allaboutcookies.org/cloaked-review"])

svc(id="southwest_card", name="Southwest Rapid Rewards Card (Chase)", category="travel", user_listed=True,
    value_model="perks", use_unit="dollars of perks used", use_period="year",
    benchmark=None,
    plans=[plan("plus", "Plus", None, 99), plan("premier", "Premier", None, 149), plan("priority", "Priority", None, 229)],
    default_plan="plus",
    features=[feat("anniversary", "Anniversary points (3k / 6k / 7.5k)"),
              feat("bag", "Free first checked bag for you + up to 8 companions"),
              feat("boarding", "Group 5 boarding"),
              feat("companion_boost", "10k points toward Companion Pass"),
              feat("discount", "Flight discount (10% / 15%)", ["plus", "premier"]),
              feat("seats", "Seat selection / Extra Legroom upgrades")],
    recent_changes=[{"date": "2025-07", "summary": "Fees raised (Priority to $229) after Southwest began charging $35 for a first checked bag."},
                    {"date": "2027-01", "summary": "Announced Rapid Rewards changes take effect; re-check value then."}],
    tips=["Value check: (checked bags you'd pay $35 each for) + (anniversary points at ~1.3¢) + discounts vs. the fee.",
          "Rapid Rewards membership itself is free; only the card has a fee."],
    sources=["https://nerdwallet.com/credit-cards/news/southwest-cards-hike-fees-and-welcome-offers-add-perks-and-bonus-categories"])

svc(id="mcafee", name="McAfee+", category="privacy", user_listed=True,
    value_model="insurance", use_unit="month protected", use_period="month",
    benchmark=None,
    plans=[plan("essential", "Essential", None, 39, verified=False, note="First-year price; renewal not confirmed."),
           plan("premium", "Premium Individual", None, 149, intro="$49 first year"),
           plan("advanced", "Advanced Individual", None, 199.99, verified=False, intro="$89 first year",
                note="Renewal price estimated.")],
    default_plan="premium",
    features=[feat("antivirus", "Antivirus", overlap="antivirus"),
              feat("vpn", "Unlimited Secure VPN", overlap="vpn"),
              feat("password", "Password manager", overlap="password_manager"),
              feat("monitoring", "Identity / dark web monitoring", overlap="identity_monitoring"),
              feat("data_cleanup", "Personal Data Cleanup", ["premium", "advanced"], overlap="data_removal"),
              feat("insurance", "$1M identity theft coverage", ["advanced"], overlap="identity_insurance"),
              feat("credit", "Credit lock and transaction monitoring", ["advanced"])],
    recent_changes=[],
    tips=["Renewal jumps ~3x after year one; call or chat to ask for the first-year price again.",
          "Windows Defender (free) and Microsoft 365's Defender cover basic antivirus."],
    sources=["https://tomsguide.com/computing/antivirus/mcafee-plus-premium-review-2026"])

svc(id="chatgpt", name="ChatGPT", category="ai", user_listed=True,
    value_model="usage", use_unit="day you used it", use_period="month",
    benchmark={"good_at_or_below": 0.75, "poor_at_or_above": 3.0},
    plans=[plan("go", "Go", 8.0, verified=False), plan("plus", "Plus", 20.0),
           plan("pro100", "Pro 100", 100.0, verified=False), plan("pro", "Pro 200", 200.0),
           plan("pro500", "Pro 500", 500.0, verified=False)],
    default_plan="plus",
    features=[feat("models", "Advanced reasoning models", overlap="ai_assistant"),
              feat("deep_research", "Deep Research", ["plus", "pro100", "pro", "pro500"]),
              feat("images", "Image generation"), feat("voice", "Advanced voice"),
              feat("agent", "Agent mode", ["plus", "pro100", "pro", "pro500"]), feat("gpts", "Custom GPTs and projects"),
              feat("codex", "Codex coding agent", ["plus", "pro100", "pro", "pro500"]), feat("sora", "Sora video", ["plus", "pro100", "pro", "pro500"])],
    recent_changes=[{"date": "2025-2026", "summary": "Lower-priced Go tier added; Free and Go may show ads."},
                    {"date": "2026-09-29", "summary": "Pro split into Pro 100, Pro 200 and a new Pro 500 tier."}],
    tips=["Paying for ChatGPT and Claude (and Copilot in Microsoft 365) is the most common AI overlap.",
          "If you use it a few times a week, Free or Go may be enough."],
    sources=["https://www.cometapi.com/chatgpt-pricing-2026-free-vs-go-vs-plus-vs-pro/"])

svc(id="claude", name="Claude", category="ai", user_listed=True,
    value_model="usage", use_unit="day you used it", use_period="month",
    benchmark={"good_at_or_below": 0.75, "poor_at_or_above": 3.0},
    plans=[plan("pro", "Pro", 20.0, 200.0), plan("max5", "Max 5x", 100.0), plan("max20", "Max 20x", 200.0)],
    default_plan="pro",
    features=[feat("models", "Latest Claude models, higher limits", overlap="ai_assistant"),
              feat("projects", "Projects and memory"), feat("research", "Research"),
              feat("code", "Claude Code"), feat("connectors", "Connectors (Gmail, Drive, etc.)")],
    recent_changes=[],
    tips=["Annual Pro is $200/yr ($16.67/mo), saving $40 vs monthly.",
          "If you keep both Claude and ChatGPT, note which one you reach for each day for a month."],
    sources=["https://www.eesel.ai/blog/claude-pro-pricing"])

# Popular extras (not on Cuong's list)
svc(id="youtube_premium", name="YouTube Premium", category="video", user_listed=False,
    value_model="usage", use_unit="day you watched", use_period="month",
    benchmark={"good_at_or_below": 0.5, "poor_at_or_above": 1.5},
    plans=[plan("individual", "Individual", 15.99, 159.99, verified=False), plan("family", "Family", 26.99, verified=False), plan("lite", "Premium Lite", 8.99, verified=False)],
    default_plan="individual",
    features=[feat("ad_free", "Ad-free video"), feat("background", "Background play"),
              feat("downloads", "Downloads"), feat("music", "YouTube Music Premium", ["individual", "family"], overlap="music")],
    recent_changes=[{"date": "2026-04", "summary": "US prices rose: Individual $15.99, Family $26.99, Lite $8.99; $159.99/yr annual option."}],
    tips=["Includes a full music service; overlaps with Spotify and Apple Music."],
    sources=[])

svc(id="amazon_prime", name="Amazon Prime", category="shopping", user_listed=False,
    value_model="usage", use_unit="order or stream", use_period="month",
    benchmark={"good_at_or_below": 1.5, "poor_at_or_above": 5.0},
    plans=[plan("monthly", "Prime (monthly)", 14.99), plan("annual", "Prime (annual)", None, 139.0),
           plan("video_only", "Prime Video only", 8.99)],
    default_plan="annual",
    features=[feat("shipping", "Free fast shipping"), feat("video", "Prime Video (with ads)", overlap="video_streaming"),
              feat("ad_free_video", "Prime Video ad-free (+$2.99)"), feat("music", "Amazon Music Prime", overlap="music"),
              feat("photos", "Unlimited photo storage", overlap="cloud_storage"),
              feat("grubhub", "Grubhub+ delivery"), feat("rx", "RxPass"), feat("gaming", "Prime Gaming")],
    recent_changes=[], tips=["Annual billing saves about $41/yr vs monthly."],
    sources=["https://stream-wiser.com/prices"])

svc(id="disney_plus", name="Disney+ (and bundles)", category="video", user_listed=False,
    value_model="usage", use_unit="evening/title watched", use_period="month",
    benchmark={"good_at_or_below": 1.0, "poor_at_or_above": 4.0},
    plans=[plan("basic", "Disney+ Basic (ads)", 12.49), plan("premium", "Disney+ Premium", 21.49, 214.99),
           plan("duo_ads", "Disney+ / Hulu (ads)", 12.99), plan("trio_ads", "Disney+ / Hulu / HBO Max (ads)", 21.99),
           plan("trio_noads", "Disney+ / Hulu / HBO Max (no ads)", 34.99)],
    default_plan="basic",
    features=[feat("disney", "Disney, Pixar, Marvel, Star Wars", overlap="video_streaming"),
              feat("hulu", "Hulu", ["duo_ads", "trio_ads", "trio_noads"]),
              feat("max", "HBO Max", ["trio_ads", "trio_noads"])],
    recent_changes=[], tips=["The Disney+/Hulu bundle costs almost the same as Disney+ alone."],
    sources=["https://stream-wiser.com/prices"])

svc(id="hbo_max", name="HBO Max", category="video", user_listed=False,
    value_model="usage", use_unit="evening/title watched", use_period="month",
    benchmark={"good_at_or_below": 1.0, "poor_at_or_above": 4.0},
    plans=[plan("basic", "Basic (ads)", 10.99, 109.99), plan("standard", "Standard", 18.49, 184.99), plan("premium", "Premium (4K)", 22.99, 229.99)],
    default_plan="standard",
    features=[feat("catalog", "HBO, Warner Bros., DC", overlap="video_streaming"), feat("uhd", "4K", ["premium"])],
    recent_changes=[], tips=["Cheaper inside the Disney+/Hulu/HBO Max bundle if you want all three."],
    sources=["https://stream-wiser.com/prices"])

svc(id="google_ai_pro", name="Google AI Pro (Google One)", category="ai", user_listed=False,
    value_model="usage", use_unit="day you used Gemini or storage", use_period="month",
    benchmark={"good_at_or_below": 0.75, "poor_at_or_above": 3.0},
    plans=[plan("ai_pro", "AI Pro", 19.99)],
    default_plan="ai_pro",
    features=[feat("gemini", "Gemini Pro, Deep Research", overlap="ai_assistant"),
              feat("storage", "5 TB Google storage, shareable with family", overlap="cloud_storage"),
              feat("notebooklm", "NotebookLM expanded"), feat("workspace_ai", "Gemini in Gmail and Docs")],
    recent_changes=[{"date": "2026", "summary": "Storage raised from 2 TB to 5 TB at the same price."}],
    tips=["Combines an AI assistant and cloud storage; could replace both ChatGPT Plus and iCloud 2 TB for some people."],
    sources=["https://www.techradar.com/ai-platforms-assistants/google-has-doubled-its-storage-allowance-for-its-ai-pro-plan-and-its-just-one-upped-chatgpt-heres-how-they-compare"])

svc(id="apple_one", name="Apple One", category="bundle", user_listed=False,
    value_model="usage", use_unit="day you used an included service", use_period="month",
    benchmark={"good_at_or_below": 0.75, "poor_at_or_above": 2.0},
    plans=[plan("individual", "Individual", 21.95), plan("family", "Family", 27.95), plan("premier", "Premier", 39.95)],
    default_plan="individual",
    features=[feat("music", "Apple Music", overlap="music"), feat("tv", "Apple TV", overlap="video_streaming"),
              feat("arcade", "Apple Arcade"), feat("icloud", "iCloud+ (50 GB / 200 GB / 2 TB)", overlap="cloud_storage"),
              feat("news", "Apple News+", ["premier"], overlap="business_news"), feat("fitness", "Fitness+", ["premier"])],
    recent_changes=[{"date": "2026-08-28", "summary": "All plans up $2/mo (Individual $21.95, Family $27.95, Premier $39.95)."}],
    tips=["Only worth it if you'd use 2+ included services; otherwise buy iCloud+ alone."],
    sources=["https://blog.internxt.com/apple-icloud-pricing/"])

OVERLAPS = [
    {"tag": "ai_assistant", "label": "AI assistant", "advice": "Most people need one paid AI assistant. Keep the one you open daily; drop the other or move it to a free tier."},
    {"tag": "cloud_storage", "label": "Cloud storage", "advice": "You may be paying for storage in more than one place (iCloud+, OneDrive, Google). Consolidate where your photos and backups live."},
    {"tag": "vpn", "label": "VPN", "advice": "VPN is bundled in several services; you only need one."},
    {"tag": "password_manager", "label": "Password manager", "advice": "Apple Passwords and Google Password Manager are free; paid ones in security suites overlap."},
    {"tag": "identity_monitoring", "label": "Identity / dark web monitoring", "advice": "Monitoring from two providers gives the same alerts twice."},
    {"tag": "data_removal", "label": "Data broker removal", "advice": "Two removal services hit mostly the same broker list."},
    {"tag": "identity_insurance", "label": "Identity theft insurance", "advice": "You can only claim a loss once; duplicate policies rarely add value. Check your homeowner's/renter's policy too."},
    {"tag": "email_alias", "label": "Email aliases", "advice": "iCloud+ Hide My Email already gives unlimited aliases on Apple devices."},
    {"tag": "notes", "label": "Notes app", "advice": "OneNote comes with Microsoft 365, and Apple Notes is free."},
    {"tag": "business_news", "label": "Business news", "advice": "WSJ, CNBC and Apple News+ cover the same market news; pick the format you actually use."},
    {"tag": "music", "label": "Music streaming", "advice": "Apple One, YouTube Premium and Amazon Prime each include a music service."},
    {"tag": "video_streaming", "label": "Video streaming", "advice": "Rotate video services month to month instead of holding all of them."},
    {"tag": "antivirus", "label": "Antivirus", "advice": "Microsoft Defender is free on Windows and included in Microsoft 365."},
    {"tag": "roadside", "label": "Roadside assistance", "advice": "Check your car insurance, vehicle warranty and credit cards before renewing AAA."},
]


OFFICIAL = {
    "spotify": "https://www.spotify.com/us/premium/",
    "netflix": "https://help.netflix.com/en/node/24926",
    "evernote": "https://evernote.com/compare-plans",
    "wsj": "https://store.wsj.com/",
    "cnbc": "https://www.cnbc.com/",
    "aaa": "https://www.aaa.com/membership",
    "icloud": "https://support.apple.com/en-us/108047",
    "m365": "https://www.microsoft.com/en-us/microsoft-365/buy/compare-all-microsoft-365-products",
    "cloaked": "https://www.cloaked.com/pricing",
    "southwest_card": "https://creditcards.chase.com/travel-credit-cards/southwest",
    "mcafee": "https://www.mcafee.com/",
    "chatgpt": "https://openai.com/chatgpt/pricing/",
    "claude": "https://claude.com/pricing",
    "youtube_premium": "https://www.youtube.com/premium",
    "amazon_prime": "https://www.amazon.com/amazonprime",
    "disney_plus": "https://www.disneyplus.com/",
    "hbo_max": "https://www.hbomax.com/",
    "google_ai_pro": "https://one.google.com/about/plans",
    "apple_one": "https://www.apple.com/apple-one/",
}
REGIONAL = {"aaa"}  # price set by each regional club
for s in S:
    s["checked_at"] = "2026-10-19"
    s["official_url"] = OFFICIAL[s["id"]]
    s["varies_by_region"] = s["id"] in REGIONAL


# Structured intro prices (plan-level), keyed by (service, plan)
INTRO = {
    ("wsj", "digital"): {"price": 4.0, "period": "month", "months": 12, "kind": "intro", "new_customers_only": True},
    ("mcafee", "premium"): {"price": 49.0, "period": "year", "months": 12, "kind": "intro", "new_customers_only": True},
    ("mcafee", "advanced"): {"price": 89.0, "period": "year", "months": 12, "kind": "intro", "new_customers_only": True},
}
# Typical free trials; not confirmed on official sites (blocked from build env)
TRIALS = {"spotify": 30, "youtube_premium": 30, "apple_one": 30, "amazon_prime": 30, "google_ai_pro": 30}

def d(type, label, amount=None, percent=None, note=None, verified=True):
    x = {"type": type, "label": label, "verified": verified}
    if amount is not None: x["amount"] = amount
    if percent is not None: x["percent"] = percent
    if note: x["note"] = note
    return x

# amount = USD saved per year unless the note says otherwise
DISCOUNTS = {
    "spotify": [d("student", "Student plan $6.99/mo", amount=72.0, note="vs Individual; needs student verification"),
                d("family", "Duo or Family plan shared with others", note="Family $21.99 split 6 ways is about $3.67 each")],
    "netflix": [d("carrier", "Included with some phone plans (e.g. T-Mobile)", note="Check your carrier plan", verified=False)],
    "evernote": [d("annual", "Pay yearly ($99/yr Starter)", note="Monthly billing costs more")],
    "cnbc": [d("annual", "CNBC Pro billed yearly ($299.99/yr)", amount=119.89)],
    "wsj": [d("retention", "Ask for a retention rate when cancelling", note="Often near the intro price", verified=False)],
    "aaa": [d("autopay", "Enrollment fee waived with auto-renew", note="Promo seen at AAA Hoosier; varies by club")],
    "icloud": [d("family", "Share any 200 GB+ plan with up to 5 family members")],
    "m365": [d("annual", "Pay yearly instead of monthly", amount=19.89, note="Personal; Family saves $25.89"),
             d("retention", "Personal Classic without Copilot, $69.99/yr", amount=30.0, note="Shown when you start to cancel"),
             d("family", "Family plan covers 6 people for $30/yr more than Personal")],
    "cloaked": [d("annual", "Pay yearly ($119.99/yr)", amount=59.89),
                d("family", "Couple or Family plan", note="Price not confirmed", verified=False)],
    "mcafee": [d("retention", "Ask for the first-year price again at renewal", note="Renewal is about 3x the intro", verified=False)],
    "claude": [d("annual", "Pro billed yearly ($200/yr)", amount=40.0)],
    "youtube_premium": [d("family", "Family plan for up to 6 people"),
                        d("student", "Student plan", note="Price not confirmed", verified=False)],
    "amazon_prime": [d("annual", "Pay yearly ($139/yr)", amount=40.88),
                     d("student", "Prime Student", note="Discounted rate for students; price not confirmed", verified=False)],
    "disney_plus": [d("bundle", "Disney+/Hulu bundle costs about the same as Disney+ alone", note="$12.99 vs $12.49 with ads")],
    "hbo_max": [d("bundle", "Disney+/Hulu/HBO Max bundle", note="$21.99 with ads for all three")],
    "apple_one": [d("family", "Family plan shares with up to 5 people")],
}
for s in S:
    for p in s["plans"]:
        if (s["id"], p["id"]) in INTRO: p["intro"] = INTRO[(s["id"], p["id"])]
    if s["id"] in TRIALS:
        s["free_trial_days"] = TRIALS[s["id"]]; s["free_trial_verified"] = False
    s["discounts"] = DISCOUNTS.get(s["id"], [])


# Pause policies: from general knowledge, none confirmed on official sites (verified=False)
def pp(can_pause, notes, max_months=None, fee=None, restart=None, keeps=None, resets=None):
    return {"can_pause": can_pause, "max_months": max_months, "fee_while_paused": fee, "restart_fee": restart,
            "keeps_price_on_restart": keeps, "billing_date_resets": resets, "notes": notes, "verified": False}
NO_PAUSE = "No pause option; cancel and resubscribe later at the current list price."
PAUSE = {
    "spotify": pp(False, "No pause; after cancelling, the account and playlists stay on the free tier.", keeps=True, resets=True),
    "netflix": pp(False, "No pause; profiles and history are kept for about 10 months after cancelling.", keeps=True, resets=True),
    "evernote": pp(False, NO_PAUSE + " Account drops to Free and its 50-note limit.", resets=True),
    "wsj": pp(False, "Digital has no pause (print has vacation holds). Cancelling ends the intro rate.", keeps=False, resets=True),
    "cnbc": pp(False, NO_PAUSE, keeps=True, resets=True),
    "aaa": pp(False, "No pause; a lapsed membership may owe the club's enrollment fee again to rejoin.", keeps=None),
    "icloud": pp(False, "No pause; you can downgrade any time. Backups stop if you're over the new limit.", fee=0, keeps=True),
    "m365": pp(False, "No pause. The hidden Classic plan may not be offered again after cancelling.", keeps=False, resets=True),
    "cloaked": pp(None, "Pause policy unknown."),
    "southwest_card": pp(False, "Card fees can't be paused; ask Chase for a product change to avoid the fee.", keeps=None),
    "mcafee": pp(False, "No pause; the first-year intro price is lost once it renews.", keeps=False, resets=True),
    "chatgpt": pp(False, "No pause; cancel at the end of the billing period and resubscribe any time.", keeps=True, resets=True),
    "claude": pp(False, "No pause; cancel at the end of the billing period and resubscribe any time.", keeps=True, resets=True),
    "youtube_premium": pp(True, "Pause for 1 to 6 months from membership settings; billing resumes automatically.", max_months=6, fee=0, restart=0, keeps=True, resets=True),
    "amazon_prime": pp(False, "No pause; you may get a partial refund on cancel if benefits are unused.", keeps=True, resets=True),
    "disney_plus": pp(False, "Disney+ has no pause; Hulu standalone has offered pauses of up to 12 weeks.", keeps=True, resets=True),
    "hbo_max": pp(False, NO_PAUSE, keeps=True, resets=True),
    "google_ai_pro": pp(False, NO_PAUSE + " Files over the free 15 GB become read-only.", keeps=True, resets=True),
    "apple_one": pp(False, NO_PAUSE, keeps=True, resets=True),
}
for s in S:
    s["pause_policy"] = PAUSE[s["id"]]

# Normalise plan storage notes into a field
for s in S:
    for p in s["plans"]:
        n = p.get("note", "")
        if n.startswith("storage_gb="):
            p["storage_gb"] = int(n.split("=")[1]); del p["note"]

out = {
    "schema_version": 1,
    "generated_at": "2026-10-19",
    "currency": "USD", "region": "US",
    "notes": "List prices before tax. Plans with verified=false are estimates to confirm. effective_monthly = price_monthly, or price_annual/12 when the plan is annual-only. checked_at is when prices were last researched; official_url is the company pricing page (not link-checked from the build environment); sources are the pages the prices were read from.",
    "value_models": {
        "usage": "cost per use = annual cost / uses per year; compared to the service's benchmark.",
        "insurance": "value comes from protection, not frequent use; judged mainly by overlaps and claims.",
        "storage": "judged by whether a smaller storage tier would fit what you store.",
        "perks": "net value = dollar value of perks used per year minus the annual fee."
    },
    "overlap_tags": OVERLAPS,
    "services": S,
}
json.dump(out, open(sys.argv[1], "w"), indent=2)
print(len(S), "services")
