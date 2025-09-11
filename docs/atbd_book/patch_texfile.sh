#!/bin/sh

# Defaults
DOC="preamble.tex"
REPLACE="cover_and_toc.tex"
N=6
PREAMBLE=""

# Parse args
while getopts "p:d:r:n:" opt; do
  case "$opt" in
    p) PREAMBLE="$OPTARG" ;;
    d) DOC="$OPTARG" ;;
    r) REPLACE="$OPTARG" ;;
    n) N="$OPTARG" ;;
    *) echo "Usage: $0 [-p preamble.tex] [-d doc.tex] [-r replace.tex] [-n N]" >&2; exit 1 ;;
  esac
done

# If -p not given, auto-detect the only .tex under _build/latex
if [ -z "$PREAMBLE" ]; then
  TEXCOUNT=$(ls _build/latex/*.tex 2>/dev/null | wc -l)
  if [ "$TEXCOUNT" -eq 1 ]; then
    PREAMBLE=$(ls _build/latex/*.tex)
  else
    echo "Error: -p not specified and could not uniquely determine .tex in _build/latex" >&2
    exit 1
  fi
fi

# Validate inputs
[ ! -f "$DOC" ] && { echo "Error: $DOC not found" >&2; exit 1; }
[ ! -f "$REPLACE" ] && { echo "Error: $REPLACE not found" >&2; exit 1; }
[ ! -f "$PREAMBLE" ] && { echo "Error: $PREAMBLE not found" >&2; exit 1; }

TMPFILE=$(mktemp /tmp/merge_tex.XXXXXX)

# Merge files into temp file
cat "$DOC" > "$TMPFILE"
echo "" >> "$TMPFILE"

awk -v repl="$REPLACE" -v n="$N" -v out="$TMPFILE" '
  BEGIN { after=0; count=0 }
  {
    if (after==0 && /\\begin{document}/) {
      print >> out
      after=1
      if (n > 0 && repl != "") {
        while ((getline line < repl) > 0) {
          print line >> out
        }
        close(repl)
      }
      next
    }
    if (after==1 && count < n) {
      count++
      next
    }
    if (after==1) {
      print >> out
    }
  }
' "$PREAMBLE"

# Overwrite original file
mv "$TMPFILE" "$PREAMBLE"


# Copy PDF and PNG files from _static to _build/latex
if [ -d "_static" ]; then
  cp _static/cover.pdf _static/logo.png _build/latex/ 2>/dev/null
fi
