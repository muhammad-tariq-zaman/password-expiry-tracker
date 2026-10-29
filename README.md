# password-expiry-tracker

Read a CSV of users (`username,last_changed,max_age_days`) and list
whose passwords are expired, expiring soon, or OK, soonest first. Useful
for helpdesk password-reset planning.

## How to run

```bash
python3 main.py users.csv --as-of 2026-10-27 --warn-days 7
```

## Example output

```text
old: expires 2026-04-01 (-209 days left) [expired]
soon: expires 2026-10-31 (4 days left) [expiring-soon]
```

Standard library only. No network access. Dates are supplied by the
caller, so results are reproducible.
