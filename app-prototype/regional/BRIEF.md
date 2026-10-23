# Regional provider research brief

Goal: a US subscription-tracker app lists REGIONAL subscription providers (ones that serve only some states) so users see local options. National providers are already covered; skip them. Today is 2026-10-19. Price accuracy matters most: prefer official pages; otherwise mark "verified": false. Never guess; null price + note when unknown. Use WebFetch/WebSearch.

Do NOT read or write anything under /mnt/project-files. Write ONLY your output file.

Output: JSON array, one object per provider:
{
  "id": "giant_food_delivery", "name": "Giant Food (Delivery Pass / Giant Delivers)", "category": "<one of: food, internet, fitness, news, home, lawn_pest, child_care, home_security, auto, shopping, mobile, elder_care>",
  "alternative_to": [], "kind": "direct",
  "service_states": ["MD","VA","DC","DE","PA"],     // US state codes where it is actually offered
  "service_area_note": "Short description, e.g. 'Stores and delivery in the Baltimore-Washington area'",
  "official_url": "https://...",
  "plans": [{"id":"...","name":"...","price_monthly":null,"price_annual":null,"effective_monthly":null,"verified":true,"note":"..."}],
  "default_plan": "...",
  "features": [{"id":"...","name":"...","plans":"all","overlap_tag":null}],
  "best_for": "one short sentence",
  "free_trial_days": null, "varies_by_region": true, "regions": "US only",
  "tips": ["optional"],
  "sources": [{"label":"...","url":"https://..."}],
  "checked_at": "2026-10-19"
}
Rules: only real subscription or membership products (delivery passes, memberships, monthly plans), not one-off purchases. Include a provider only if it serves at least one state in your region; list ALL states it serves in service_states (even outside the region). Aim 15-30 providers. Keep text short. Validate with python3 json.load and reply with a short summary (count per category, unverified count).
