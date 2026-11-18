# Dajoni's Microsoft practice assessment results, shipped with the app so every copy shows them.
# The app adds any entry the browser does not already have (matched by date and score, counting repeats).
#   python3 content/ms_log.py && python3 build.py
import json, os
P = os.path.join(os.path.dirname(__file__), '..', 'src', 'data_packs.json')
LOG = {'az900': [  # dom: {domain: [right, total]} where the answer summary was reviewed
    dict(t='2026-11-05', pct=70, src='ms', dom={'1': [12, 14], '2': [12, 19], '3': [11, 17]}),
    dict(t='2026-11-13', pct=54, src='ms'),
    dict(t='2026-11-17', pct=70, src='ms', dom={'1': [10, 14], '2': [16, 19], '3': [9, 17]}),
    dict(t='2026-11-18', pct=70, src='ms'),
    dict(t='2026-11-18', pct=70, src='ms', dom={'1': [9, 14], '2': [16, 19], '3': [10, 17]}),
]}
data = json.load(open(P, encoding='utf-8'))
for cert, log in LOG.items():
    for e in log:
        if 'dom' in e: assert sum(r for r, _ in e['dom'].values()) * 2 == e['pct'], e
    data['packs'][cert]['meta']['msLog'] = log
json.dump(data, open(P, 'w', encoding='utf-8'), ensure_ascii=False)
print({c: len(l) for c, l in LOG.items()}, 'practice results logged')
