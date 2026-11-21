// Entry program for make.fun's "Post a GTA 6 meme on X" bounty
// (gta6-meme-x-01). The X post itself is the entry; this program's whole
// job is to hand the post's address to the grader by copying the
// repository's POST.json into the output directory, untouched.
// The current entry is the Leonida Rentals return-receipt meme —
// see make_receipt.py (which draws it) and post.txt (its caption).
//
// Run it the way the kit describes:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { writeFileSync } from "node:fs";
import { createHash } from "node:crypto";

const botDir = process.env.MAKEFUN_BOT_DIR ?? ".";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const postFile = join(botDir, "POST.json");

if (!existsSync(postFile)) {
  console.error(`main.ts: no POST.json found in ${botDir}`);
  process.exit(1);
}

// Read the post file once before copying, so a malformed hand-in fails
// here with a clear message instead of confusing the grader later.
let post: { url?: unknown };
try {
  post = JSON.parse(readFileSync(postFile, "utf8")) as { url?: unknown };
} catch {
  console.error("main.ts: POST.json is not valid JSON");
  process.exit(1);
}

if (typeof post.url !== "string" || post.url.length === 0) {
  console.error('main.ts: POST.json must hold a "url" string');
  process.exit(1);
}

// The address must be one X post: https://x.com/<handle>/status/<id>,
// with the id in digits. Anything else is a hand-in mistake, so say so.
const postUrlPattern =
  /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/[^/]+\/status\/\d+$/;
const bareUrl = post.url.split(/[?#]/)[0];
if (!postUrlPattern.test(bareUrl)) {
  console.error(`main.ts: not an X post address: ${post.url}`);
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
const target = join(outputDir, "POST.json");
copyFileSync(postFile, target);
console.log(`main.ts: copied ${postFile} -> ${target} (${post.url})`);

// Beside the copied POST.json, leave a small manifest in the output
// directory so anyone checking the hand-in can confirm, without opening
// the post, exactly which image and caption the entry consists of.
const memeFile = join(botDir, "meme.png");
const captionFile = join(botDir, "post.txt");
for (const needed of [memeFile, captionFile]) {
  if (!existsSync(needed)) {
    console.error(`main.ts: entry file missing: ${needed}`);
    process.exit(1);
  }
}

const memeDigest = createHash("sha256")
  .update(readFileSync(memeFile))
  .digest("hex");
const captionText = readFileSync(captionFile, "utf8").trim();

const manifest = {
  post_url: post.url,
  meme_file: "meme.png",
  meme_sha256: memeDigest,
  caption_chars: captionText.length,
};
const manifestTarget = join(outputDir, "entry.json");
writeFileSync(manifestTarget, JSON.stringify(manifest, null, 2) + "\n");
console.log(
  `main.ts: wrote ${manifestTarget} (sha256 ${memeDigest.slice(0, 12)}…, ` +
    `caption ${captionText.length} chars)`,
);
