# gta6-meme-x

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/kreutzx/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/kreutzx/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

An original meme for make.fun's "Post a GTA 6 meme on X" bounty: make.fun's
ghost mascot waits out the thirteen years between GTA V and GTA 6 on a
Leonida beach at sunset — and gets paid to wait. The picture is drawn from
scratch with Python and PIL (`make_meme.py`); no stock art and no game
assets. The post's text is in `post.txt`, the meme itself is `meme.png`,
and once the post is live its address goes into `POST.json`, which is all
the entry program hands in.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

That copies `POST.json` to `out/POST.json`, after checking it holds one
well-formed X post address.

---
<sub>Entered on [make.fun](https://make.fun/?ref=24q484pk&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
