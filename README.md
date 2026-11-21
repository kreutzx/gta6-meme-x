# gta6-meme-x

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/kreutzx/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/kreutzx/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

An original meme for make.fun's "Post a GTA 6 meme on X" bounty: a rental
return receipt from **Leonida Rentals, Vice City Int'l Airport**. The car
went out in Los Santos on Sep 17, 2013 and came back in Vice City on
Nov 19, 2026 — so the receipt itemises the thirteen-year wait for GTA 6 as
charges (a one-way drop fee, a late fee of 4,745 days at trailer rates, two
rescheduling fees for the promised "Fall 2025" and "May 2026" returns,
unlisted drivers Jason & Lucia, and cleaning an alligator off the back
seat), stamped **13 YEARS LATE**, totalling exactly $2,026.00. The bill is
paid in full in the payment band by the driver's AI agent, out of the
bounty payout it earned on make.fun — ghost, magenta coin and all.

The picture is drawn from scratch with Python and PIL (`make_receipt.py`);
no stock art and no game assets, and the build is deterministic — the same
script always writes the same `meme.png`. The post's text is in `post.txt`,
and once the post is live its address goes into `POST.json`, which is all
the entry program hands in. (The earlier entry, a sunset poster of the
ghost waiting on a Leonida beach, was drawn by `make_meme.py`.)

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

That copies `POST.json` to `out/POST.json`, after checking it holds one
well-formed X post address.

---
<sub>Entered on [make.fun](https://make.fun/?ref=24q484pk&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
