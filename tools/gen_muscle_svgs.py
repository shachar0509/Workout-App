#!/usr/bin/env python3
"""Generate muscles/<target>.svg from the body model of react-body-highlighter (MIT, (c) 2020 GV79).
Usage: python3 -I tools/gen_muscle_svgs.py <path to unpacked react-body-highlighter package> <out dir>"""
import re, sys, os
pkg, out = sys.argv[1:3]
src = open(os.path.join(pkg, 'src/assets/index.ts'), encoding='utf-8').read()

def model(name):
    body = src.split(f'export const {name}')[1]
    body = body.split('export const ')[0]
    res = []
    for m in re.finditer(r"muscle: MuscleType\.(\w+),\s*svgPoints: \[(.*?)\],\s*\}", body, re.S):
        pts = re.findall(r"'([^']+)'", m.group(2))
        res.append((m.group(1), [[tuple(map(float, p.split()[i:i + 2])) for i in range(0, len(p.split()), 2)] for p in pts]))
    return res

M = {'a': model('anteriorData'), 'p': model('posteriorData')}
# dataset target -> (view, [model muscles]); the model has no lats / serratus / levator, so the nearest region is used
MAP = {
    'abs': ('a', ['ABS']), 'pectorals': ('a', ['CHEST']), 'biceps': ('a', ['BICEPS']), 'delts': ('a', ['FRONT_DELTOIDS']),
    'quads': ('a', ['QUADRICEPS']), 'forearms': ('a', ['FOREARM']), 'adductors': ('a', ['ABDUCTORS']),
    'serratus anterior': ('a', ['OBLIQUES']),
    'glutes': ('p', ['GLUTEAL']), 'triceps': ('p', ['TRICEPS']), 'upper back': ('p', ['UPPER_BACK', 'TRAPEZIUS']),
    'lats': ('p', ['UPPER_BACK']), 'calves': ('p', ['CALVES', 'LEFT_SOLEUS', 'RIGHT_SOLEUS']), 'hamstrings': ('p', ['HAMSTRING']),
    'spine': ('p', ['LOWER_BACK']), 'traps': ('p', ['TRAPEZIUS']), 'abductors': ('p', ['ABDUCTOR']),
}
BODY, HI = '#3a3d45', '#ff2a45'
os.makedirs(out, exist_ok=True)
for name, (v, hl) in MAP.items():
    polys, xs, ys = [], [], []
    for mus, shapes in M[v]:
        on = mus in hl
        for sh in shapes:
            polys.append(f'<polygon points="{" ".join(f"{x:g},{y:g}" for x, y in sh)}" fill="{HI if on else BODY}"/>')
            if on:
                xs += [p[0] for p in sh]; ys += [p[1] for p in sh]
    # same zoom for every image: full body width, a 100x100 window centred on the highlighted muscle
    cy = (min(ys) + max(ys)) / 2
    x0, side = 0.0, 100.0
    y0 = min(max(cy - side / 2, 0), 200 - side)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {y0:.1f} {side:.1f} {side:.1f}">{"".join(polys)}</svg>'
    open(os.path.join(out, name.replace(' ', '-') + '.svg'), 'w', encoding='utf-8').write(svg)
print(len(MAP), 'svgs')
