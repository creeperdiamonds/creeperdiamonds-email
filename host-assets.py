#!/usr/bin/env python3
"""
Point the templates' image references at a hosted base URL.

    python host-assets.py                 # show where assets currently point
    python host-assets.py pages           # GitHub Pages   (default, recommended)
    python host-assets.py raw             # raw.githubusercontent.com
    python host-assets.py local           # back to relative assets/ paths
    python host-assets.py https://your.cdn/path

Rewrites in place. Handles all four reference types: src="", the background=""
attribute, inline background-image:url(), and the Outlook VML <v:fill src>.

Why not github.com/<user>/<repo>/tree/main/assets/ - that is GitHub's web UI
page for a directory. It returns HTML, so a mail client fetching it gets a
webpage instead of a PNG and the image breaks. Only the two forms below serve
actual image bytes with an image/* content type.
"""
import os, re, sys

USER, REPO, BRANCH = 'creeperdiamonds', 'creeperdiamonds-email', 'main'
PRESETS = {
    'pages': f'https://{USER}.github.io/{REPO}/assets',
    'raw':   f'https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/assets',
    'local': 'assets',
}
FILES = ('creeperdiamonds-email.html', 'personal-note.html')
HERE = os.path.dirname(os.path.abspath(__file__))

# any current base, relative or absolute, ending in a known asset filename
REF = re.compile(r'(?:https?://[^\s"\')]*?/)?assets/([A-Za-z0-9._-]+\.(?:png|gif|jpg|jpeg))')

def current():
    for name in FILES:
        s = open(os.path.join(HERE, name), encoding='utf-8').read()
        bases = {m.group(0).rsplit('/', 1)[0] for m in REF.finditer(s)}
        print(f'  {name}: {sorted(bases) or "no asset references"}')

def main():
    if len(sys.argv) == 1:
        print('Assets currently point at:'); current()
        print('\nPresets:')
        for k, v in PRESETS.items(): print(f'  {k:6} -> {v}')
        return

    arg = sys.argv[1]
    base = PRESETS.get(arg, arg).rstrip('/')
    if base != 'assets' and not base.startswith('https://'):
        sys.exit(f'Refusing: base must be https:// (or a preset)\n  got: {base}\n'
                 '  Gmail proxies images over https and many clients refuse http.')

    on_disk = set(os.listdir(os.path.join(HERE, 'assets')))
    total = 0
    for name in FILES:
        p = os.path.join(HERE, name)
        s = open(p, encoding='utf-8').read()
        missing = {m.group(1) for m in REF.finditer(s)} - on_disk
        for f in sorted(missing):
            print(f'  WARNING {name}: references {f}, not present in assets/')
        s, n = REF.subn(lambda m: f'{base}/{m.group(1)}', s)
        open(p, 'w', encoding='utf-8').write(s)
        total += n
        print(f'  {name}: {n} reference(s) -> {base}/')

    print(f'\nDone. {total} references rewritten in place.')
    if base == 'assets':
        print('Relative paths only resolve when the HTML sits beside assets/.')
        print('They will NOT load in any inbox. Use "pages" before sending.')
    else:
        print('Verify each of these returns 200 with an image/* content type:')
        for f in sorted(on_disk):
            print(f'  curl -sI {base}/{f} | head -1')

if __name__ == '__main__':
    main()
