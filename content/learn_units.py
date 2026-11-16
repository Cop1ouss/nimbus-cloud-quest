"""Microsoft Learn unit links per Codex stop.
python3 content/learn_units.py --fetch   refresh content/learn_units.json from Learn, then apply
python3 content/learn_units.py           apply the cached links to src/data_packs.json
Pack build scripts call apply() too, so a rebuild keeps the links."""
import json,os,re,sys,urllib.request
HERE=os.path.dirname(os.path.abspath(__file__))
CACHE=os.path.join(HERE,'learn_units.json');PACKS=os.path.join(HERE,'..','src','data_packs.json')
SKIP=re.compile(r'^(introduction|summary|knowledge check|module assessment|check your knowledge)',re.I)
def get(u):
    r=urllib.request.Request(u,headers={'User-Agent':'nimbus-cloud-quest'});return urllib.request.urlopen(r,timeout=20).read().decode('utf-8')
def units_for(mod):
    uid=re.search(r'<meta name="uid" content="([^"]+)"',get(mod)).group(1)
    h=json.loads(get('https://learn.microsoft.com/api/hierarchy/modules/%s?locale=en-us'%uid))
    return [{'t':u['title'],'u':'https://learn.microsoft.com/en-us'+u['url'].rstrip('/')} for u in h['units'] if not SKIP.match(u['title'])]
SC500={1:'secure-access-resources-entra',2:'configure-key-vault-security',3:'security-governance-compliance',4:'implement-azure-storage-security',
 5:'implement-azure-sql-database-security',6:'implement-network-security-controls-azure',7:'implement-ai-security',8:'server-vm-security',
 9:'secure-application-platform-services',10:'manage-security-posture-defender-cloud',11:'implement-activity-event-collection-sentinel',12:'deploy-operate-security-copilot'}
def path(slug):
    h=json.loads(get('https://learn.microsoft.com/api/hierarchy/paths/learn.wwl.%s?locale=en-us'%slug))
    return {'mod':'https://learn.microsoft.com/en-us'+h['url'],'modTitle':h['title'],'modLabel':'Learning path',
            'units':[{'t':m['title'],'u':'https://learn.microsoft.com/en-us'+m['url']} for m in h['modules']]}
def fetch(ids):
    data=json.load(open(PACKS));cache=json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    for pid in ids:
        for s in data['packs'][pid]['sections']:
            if '/training/modules/' not in s['mod'] or s['mod'] in cache:continue
            try:cache[s['mod']]=units_for(s['mod']);print('ok',s['mod'],len(cache[s['mod']]))
            except Exception as e:print('skip',s['mod'],e)
    for n,slug in SC500.items():
        k='sc500:s%d'%n
        if k in cache:continue
        try:cache[k]=path(slug);print('ok',k,len(cache[k]['units']))
        except Exception as e:print('skip',k,e)
    json.dump(cache,open(CACHE,'w'),indent=1,ensure_ascii=False)
def apply(data=None,ids=('sc900','az104','sc500')):
    own=data is None;data=data or json.load(open(PACKS))
    cache=json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    for pid in ids:
        if pid not in data['packs']:continue
        for s in data['packs'][pid]['sections']:
            k=pid+':'+s['id']
            if k in cache:s.update(cache[k])
            elif s['mod'] in cache:s['units']=cache[s['mod']]
    if own:json.dump(data,open(PACKS,'w'),ensure_ascii=False)
    return data
if __name__=='__main__':
    if '--fetch' in sys.argv:fetch(('sc900','az104','sc500'))
    apply();print('applied')
