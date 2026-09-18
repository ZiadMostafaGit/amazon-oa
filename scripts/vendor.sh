#!/bin/sh
# Build a self-contained copy of the site into $1 (default: dist/).
#
# The source tree loads CodeMirror, JetBrains Mono and Pyodide from CDNs, which
# is right for opening site/index.html directly. The container should not depend
# on the network, so this fetches those assets and rewrites the two files that
# name them. Run it from the repo root.
set -eu
OUT="${1:-dist}"
CM_VER=5.65.16
PY_VER=0.26.4
CM_CDN="https://cdnjs.cloudflare.com/ajax/libs/codemirror/$CM_VER"
PY_CDN="https://cdn.jsdelivr.net/pyodide/v$PY_VER/full"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
# --retry-all-errors + -C - matter here: the 10 MB Pyodide runtime regularly
# dies mid-stream on a flaky link, and plain --retry does not resume a TLS
# error. A half-written pyodide.asm.wasm is exactly how a container ends up
# serving a runtime that never instantiates.
fetch() { curl -fsSL --retry 5 --retry-delay 2 --retry-all-errors -C - -A "$UA" "$1" -o "$2"; }

rm -rf "$OUT"
mkdir -p "$OUT/site/vendor/codemirror" "$OUT/site/vendor/pyodide" "$OUT/site/vendor/fonts"
cp -r site/*.html site/*.js site/*.md "$OUT/site/"
cp -r images "$OUT/images"
cp -r video  "$OUT/video"

echo "→ CodeMirror $CM_VER"
# take the exact file list from index.html so this cannot drift out of sync
grep -o "$CM_CDN/[A-Za-z0-9./_-]*" site/index.html | sort -u | while read -r url; do
  rel="${url#"$CM_CDN"/}"
  mkdir -p "$OUT/site/vendor/codemirror/$(dirname "$rel")"
  fetch "$url" "$OUT/site/vendor/codemirror/$rel"
  echo "   $rel"
done

echo "→ Pyodide $PY_VER (core only)"
for f in pyodide.js pyodide.asm.js pyodide.asm.wasm python_stdlib.zip pyodide-lock.json; do
  fetch "$PY_CDN/$f" "$OUT/site/vendor/pyodide/$f"
  echo "   $f"
done

# a truncated runtime must fail the build, not ship
WASM="$OUT/site/vendor/pyodide/pyodide.asm.wasm"
size=$(wc -c < "$WASM")
magic=$(head -c 4 "$WASM" | od -An -tx1 | tr -d ' \n')
if [ "$magic" != "0061736d" ] || [ "$size" -lt 5000000 ]; then
  echo "!! $WASM is not a complete WebAssembly module (magic=$magic, $size bytes)" >&2
  exit 1
fi
echo "   verified: $size bytes, WebAssembly magic ok"

echo "→ JetBrains Mono (latin subset)"
CSS="$OUT/site/vendor/fonts/jetbrains-mono.css"
fetch "https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,500;0,700;1,400&display=swap" "$CSS.raw"
# keep only the latin blocks, then localise every gstatic URL
awk 'BEGIN{RS="";ORS="\n\n"} /\/\* latin/' "$CSS.raw" > "$CSS"
[ -s "$CSS" ] || cp "$CSS.raw" "$CSS"
i=0
for url in $(grep -o 'https://fonts.gstatic.com/[^)]*' "$CSS" | sort -u); do
  i=$((i+1)); name="jbmono-$i.woff2"
  fetch "$url" "$OUT/site/vendor/fonts/$name"
  sed -i "s|$url|$name|g" "$CSS"
  echo "   $name"
done
rm -f "$CSS.raw"

echo "→ rewriting asset URLs to local paths"
sed -i \
  -e "s|$CM_CDN/|vendor/codemirror/|g" \
  -e "s|<link rel=\"preconnect\"[^>]*>||g" \
  -e "s|https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,500;0,700;1,400\&display=swap|vendor/fonts/jetbrains-mono.css|g" \
  "$OUT/site/index.html"
sed -i "s|https://cdn.jsdelivr.net/pyodide/v$PY_VER/full/|vendor/pyodide/|g" "$OUT/site/pyrun.js"

left=$(grep -oE 'https://(cdnjs\.cloudflare\.com|cdn\.jsdelivr\.net|fonts\.(googleapis|gstatic)\.com)[^"'"'"' )]*' \
        "$OUT/site/index.html" "$OUT/site/pyrun.js" "$OUT/site/app.js" 2>/dev/null | wc -l)
if [ "$left" -ne 0 ]; then
  echo "!! $left CDN reference(s) still present:" >&2
  grep -onE 'https://(cdnjs|cdn\.jsdelivr|fonts\.(googleapis|gstatic))[^"'"'"' )]*' \
    "$OUT/site/index.html" "$OUT/site/pyrun.js" "$OUT/site/app.js" >&2 || true
  exit 1
fi
echo "✓ $OUT is self-contained ($(du -sh "$OUT" | cut -f1))"
