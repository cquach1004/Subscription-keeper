# Value tracker data

`services.json` (schema v1, prices checked 2026-10-18, US list prices) is the source of truth for the value tracker and the app prototype. Regenerate it with `python3 build_services.py services.json`.

## Shape
- `services[]`: `id`, `name`, `category`, `user_listed` (true = on Cuong's own list), `value_model`, `use_unit`, `use_period` (`month`|`year`), `benchmark` (`good_at_or_below` / `poor_at_or_above`, $ per use, or null), `plans[]`, `default_plan`, `features[]`, `recent_changes[]`, `tips[]`, `sources[]` (third-party pages prices were read from), `checked_at` (YYYY-MM-DD, last price research), `official_url` (company pricing page, not link-checked), `varies_by_region` (true when price depends on location, e.g. AAA clubs).
- `plans[]`: `id`, `name`, `price_monthly`, `price_annual` (either may be null), `effective_monthly` (always set), `verified` (false = estimate), optional `intro_offer` (text), `intro` ({price, period: month|year, months, kind: trial|intro, new_customers_only}), `note`, `storage_gb`.
- `features[]`: `id`, `name`, `plans` (`"all"` or list of plan ids), optional `overlap_tag`.
- `overlap_tags[]`: `tag`, `label`, `advice`. Two active services sharing a tag = an overlap.

## Value models
- `usage`: cost per use = annual cost / uses per year, rated against `benchmark`.
- `insurance`: protection value; judged mostly by overlaps (AAA, Cloaked, McAfee).
- `storage`: compare GB stored to plan `storage_gb`; suggest the smallest tier that fits.
- `perks`: net value = perks used per year ($) minus annual fee.

Benchmarks are rules of thumb (inferred, not sourced), meant to be tuned.

## Trials and discounts
- `free_trial_days` + `free_trial_verified` (service level, only where a trial is typical; all currently unverified).
- `discounts[]`: `type` (autopay|annual|student|family|carrier|card_perk|retention|bundle), `label`, optional `amount` (USD saved per year) or `percent`, `note`, `verified`.

## Pausing
- `pause_policy`: {can_pause, max_months, fee_while_paused, restart_fee, keeps_price_on_restart, billing_date_resets, notes, verified}. null = unknown. All entries are from general knowledge and `verified: false`.
