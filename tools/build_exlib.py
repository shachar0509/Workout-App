#!/usr/bin/env python3
"""Build exercises-data.json from hasaneyldrm/exercises-dataset (data/exercises.json) + Hebrew names.
Media (images/GIFs) is NOT copied: the app hot-links it at the pinned commit (c) from raw.githubusercontent.com.
Usage: python3 -I tools/build_exlib.py <dataset/data/exercises.json> <he_names.json: name -> {h, i} or name -> str> <commit_sha> <out.json> [scores.json: name -> {p, c}]
Score k (0-100) = 7*popularity + 3*translation-confidence (both 1-10); the app lists exercises by k, highest first."""
import json, re, sys

src, hef, sha, out = sys.argv[1:5]
sc = json.load(open(sys.argv[5], encoding='utf-8')) if len(sys.argv) > 5 else {}
score = lambda n: round(0.7 * sc[n]['p'] * 10 + 0.3 * sc[n]['c'] * 10) if n in sc else 0
d = json.load(open(src, encoding='utf-8'))
he = json.load(open(hef, encoding='utf-8'))

def title(s):
    return re.sub(r"(^|[\s\-/(])([a-z])", lambda m: m.group(1) + m.group(2).upper(), s.strip())

T = sorted({e['target'] for e in d})
Q = sorted({e['equipment'] for e in d})
B = sorted({e['body_part'] for e in d})
seen, xs = set(), []
for e in d:
    n = title(e['name'])
    if n.lower() in seen: continue
    seen.add(n.lower())
    x = {'n': n, 'm': e['media_id'] and f"{e['id']}-{e['media_id']}",
         't': T.index(e['target']), 'e': Q.index(e['equipment']), 'b': B.index(e['body_part']),
         's': [s for s in e.get('secondary_muscles', []) if s],
         'i': [re.sub(r'\s+', ' ', s).strip() for s in e['instruction_steps']['en'] if s.strip()]}
    t = he.get(n)
    if isinstance(t, str): t = {'h': t}
    if t and t.get('h'): x['h'] = t['h']
    if t and len(t.get('i') or []) == len(x['i']) and x['i']: x['ih'] = t['i']  # Hebrew steps, same count
    if score(n): x['k'] = score(n)
    xs.append(x)
base = {x['n'].lower() for x in xs}
extra = {k: (v['h'] if isinstance(v, dict) else v) for k, v in he.items() if k.lower() not in base}  # Hebrew for default names outside the library
json.dump({'v': 1, 'u': f'https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/{sha}/',
           'mu': T, 'eq': Q, 'bp': B, 'x': xs, 'h': extra,
           'hk': {k: score(k) for k in extra if score(k)}},
          open(out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(xs), 'exercises;', sum(1 for x in xs if 'h' in x), 'with Hebrew;', len(extra), 'extra names')
