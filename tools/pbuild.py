# -*- coding: utf-8 -*-
"""Selects the final 3000 cards and writes the deck file."""
from __future__ import print_function
import io, sys, collections

import pgen
from pron import PERSONS

PORDER = [k for (k, p, n, g) in PERSONS]

# how many cards each family contributes, split evenly between singular and
# plural referents; the case totals are 1200 / 1600 / 200
QUOTA = [
    ('nom_fix', 240), ('nom_q', 64), ('nom_be', 64), ('nom_pred', 32),
    ('nom_thing', 36), ('nom_thing_pred', 48), ('nom_obj', 300),
    ('dikos_pred', 200), ('dikos_nom', 216),

    ('acc_weak', 234), ('acc_weak_thing', 86), ('acc_weak_place', 528),
    ('acc_prep', 202), ('acc_emph', 80), ('dikos_acc', 470),

    ('gen_io', 50), ('gen_io_obj', 30), ('gen_aresei', 30),
    ('gen_poss', 60), ('dikos_gen', 30),
]


def pick(cands, want):
    """Round-robin over frames, persons and nouns, so nothing clusters."""
    byframe = collections.defaultdict(lambda: collections.defaultdict(list))
    for c in cands:
        byframe[c['frame']][c['key']].append(c)
    for f in byframe:
        for j, k in enumerate(PORDER):
            L = byframe[f][k]
            if L:
                off = (j * 7) % len(L)
                byframe[f][k] = L[off:] + L[:off]
    order = sorted(byframe)
    pos = {}
    out = []
    while len(out) < want:
        moved = False
        for f in order:
            pk = byframe[f]
            live = [k for k in PORDER if pk[k]]
            if not live:
                continue
            i = pos.get(f, 0)
            pos[f] = i + 1
            k = live[i % len(live)]
            out.append(pk[k].pop(0))
            moved = True
            if len(out) >= want:
                break
        if not moved:
            break
    return out


def main(path):
    cards = pgen.build_all()
    byfam = collections.defaultdict(lambda: collections.defaultdict(list))
    for c in cards:
        byfam[c['family']][c['num']].append(c)

    chosen = []
    for family, total in QUOTA:
        for num in ('sg', 'pl'):
            want = total // 2
            got = pick(byfam[family][num], want)
            if len(got) < want:
                print(u'! %s/%s: wanted %d, only %d available'
                      % (family, num, want, len(got)))
            chosen.extend(got)

    # interleave the families so a study session does not meet them in blocks
    chosen.sort(key=lambda c: (c['frame'], c['key'], c['family']))
    seen, out = set(), []
    for c in chosen:
        line = u'%s (%s)' % (c['prompt'], c['hint'])
        if line in seen:
            continue
        seen.add(line)
        out.append((line, c))

    blocks = []
    for i, (line, c) in enumerate(out, 1):
        blocks.append(u'%d\n%s\n%s\n%s — %s'
                      % (i, line, c['answer'], c['en'], c['expl']))
    body = u'\n\n'.join(blocks) + u'\n'
    # UTF-8 with a BOM and CRLF line endings, like the other dictionaries
    with io.open(path, 'w', encoding='utf-8-sig', newline='\r\n') as fh:
        fh.write(body)

    stats = collections.Counter()
    for _l, c in out:
        stats[c['case']] += 1
        stats[c['num']] += 1
        stats[c['family']] += 1
    print(u'cards: %d' % len(out))
    print(u'case : nom %d  acc %d  gen %d'
          % (stats['nom'], stats['acc'], stats['gen']))
    print(u'num  : sg %d  pl %d' % (stats['sg'], stats['pl']))
    for family, _t in QUOTA:
        print(u'  %-16s %d' % (family, stats[family]))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'deck.txt')
