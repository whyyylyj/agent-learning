# -*- coding: utf-8 -*-
"""全站断链检查：python3 tools/check_links.py"""
import os, re, sys
BASE = os.environ.get("KB_SITE") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
bad = []
for root, _, files in os.walk(BASE):
    for fn in files:
        if not fn.endswith(".html"): continue
        path = os.path.join(root, fn)
        for m in re.finditer(r'href="([^"#]+?)(?:#[^"]*)?"', open(path, encoding="utf-8").read()):
            u = m.group(1)
            if u.startswith(("http", "mailto:")): continue
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), u))):
                bad.append((os.path.relpath(path, BASE), u))
print("broken internal links:", len(bad))
for b in bad: print(" ", b)
sys.exit(1 if bad else 0)
