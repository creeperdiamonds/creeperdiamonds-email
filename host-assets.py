#!/usr/bin/env python3
"""
Rewrite the templates' relative asset paths to absolute hosted URLs.

    python host-assets.py https://creeperdiamonds.github.io/email-assets

Source files keep their relative paths so they stay previewable by opening them
from disk. This writes send-ready copies into dist/ instead of editing in place.

Relative paths work only when the HTML sits next to its assets/ folder. In an
inbox there is no "next to" - not on your phone, not anywhere. Every image
reference has to be an absolute https:// URL served from a public host.
"""
import os, re, sys

FILES = ('creeperdiamonds-email.html', 'personal-note.html')
OUT   = 'dist'

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    base = sys.argv[1].rstrip('/')

    if not base.startswith('https://'):
        sys.exit(f"Refusing: base must start with https://\n  got: {base}\n"
                 "  Gmail proxies images over https and many clients refuse http.")

    os.makedirs(OUT, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    total = 0

    for name in FILES:
        src = os.path.join(here, name)
        if not os.path.exists(src):
            print(f"  skip {name} (not found)"); continue
        s = open(src, encoding='utf-8').read()

        refs = set(re.findall(r'assets/[A-Za-z0-9._-]+', s))
        for r in sorted(refs):
            local = os.path.join(here, r)
            if not os.path.exists(local):
                print(f"  WARNING {name}: {r} referenced but missing on disk")
            s = s.replace(r, f'{base}/{os.path.basename(r)}')

        left = re.findall(r'(?:src|background)="(?!https?:|cid:|\{)[^"]+"', s)
        left += re.findall(r"url\('(?!https?:)[^']+'\)", s)
        if left:
            print(f"  WARNING {name}: still relative -> {left}")

        if 'placehold.co' in s:
            print(f"  NOTE {name}: hero still points at placehold.co - swap in real key art")

        dst = os.path.join(here, OUT, name)
        open(dst, 'w', encoding='utf-8').write(s)
        n = sum(s.count(f'{base}/{os.path.basename(r)}') for r in refs)
        total += n
        print(f"  {name}: {len(refs)} asset(s), {n} reference(s) rewritten -> {OUT}/{name}")

    print(f"\nDone. {total} references now point at {base}/")
    print("Upload everything in assets/ to that location, then send from dist/.")
    print("\nSanity check before sending - each of these must return 200 and an image/* type:")
    for f in sorted(os.listdir(os.path.join(here, 'assets'))):
        print(f"  curl -sI {base}/{f} | head -1")

if __name__ == '__main__':
    main()
