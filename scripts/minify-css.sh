#!/bin/sh
# Regenerates assets/css/*.min.css from the readable source files.
# The pages load the .min.css versions, so run this after editing any CSS:
#   sh scripts/minify-css.sh
cd "$(dirname "$0")/../assets/css" || exit 1
for f in *.css; do
  case "$f" in *.min.css) continue ;; esac
  npx -y esbuild@0.25 "$f" --minify --log-level=warning --outfile="${f%.css}.min.css" --allow-overwrite
done
ls -l *.min.css
