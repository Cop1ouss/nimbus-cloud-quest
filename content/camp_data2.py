import json
P='src/data_packs.json';d=json.load(open(P));cp=d['packs']['az900']['campaign'];C=cp['cards'];T=cp['threats']
cp['levels']=[l for l in cp['levels'] if l['id']<=10]
for l in cp['levels']: l['world']=1
cp['worlds']=[{'id':1,'n':'World 1: Cloud Concepts','d':1},{'id':2,'n':'World 2: Architecture and Services','d':2},{'id':3,'n':'World 3: Management and Governance','d':3},{'id':4,'n':'World 4: Exam Day','d':0}]
def card(i,**k): C[i]=k
# ---- World 2 cards
card('vm2',n='Virtual Machine',tag='Compute · IaaS',cost=1,kind='deploy',topic='Compute',ic='server',tp=2,layers='iaas',text='Deploy to the selected zone. 2 throughput.')
card('az',n='Availability Zones',tag='Regions and zones',cost=1,kind='action',topic='Regions and zones',ic='copy',fx=[['block',4]],counters=['zoneout'],text='Block 4. Counters Zone Outage: zones are separate datacenters in one region.')
card('vmss',n='VM Scale Set',tag='Compute',cost=2,kind='deploy',topic='Compute',ic='server',tp=3,zr=True,layers='iaas',guard=['spike'],text='Deploy across all zones. 3 throughput. Scales out, so Traffic Spike never hits.')
card('func',n='Azure Functions',tag='Compute · serverless',cost=1,kind='action',topic='Compute',ic='bolt',fx=[['dmg',4]],text='4 damage. Event-driven code, no servers to manage.')
card('aci',n='Container Instances',tag='Compute · containers',cost=1,kind='deploy',topic='Compute',ic='box',tp=2,layers='paas',text='Deploy to the selected zone. 2 throughput. No VM to manage.')
card('pair',n='Region Pair',tag='Regions and zones',cost=2,kind='action',topic='Regions and zones',ic='globe',fx=[['heal',4]],counters=['region'],text='Heal 4. Counters Region Outage: a paired region in the same geography takes over.')
card('vpn',n='VPN Gateway',tag='Networking',cost=1,kind='action',topic='Networking',ic='link',fx=[['dmg',2]],counters=['onprem'],text='2 damage. Counters On-Prem Cut Off: encrypted tunnel over the internet.')
card('er',n='ExpressRoute',tag='Networking',cost=2,kind='action',topic='Networking',ic='link',fx=[['block',5]],counters=['onprem'],text='Block 5. Counters On-Prem Cut Off with a private link that skips the internet.')
card('peer',n='VNet Peering',tag='Networking',cost=1,kind='action',topic='Networking',ic='link',fx=[['dmg',2]],counters=['isolated'],text='2 damage. Counters Isolated VNets: traffic stays on the Microsoft backbone.')
card('pe',n='Private Endpoint',tag='Networking',cost=1,kind='action',topic='Networking',ic='lock',fx=[['block',4]],counters=['exposed'],text='Block 4. Counters Public Exposure: a private IP inside your VNet.')
card('dns',n='Azure DNS',tag='Networking',cost=1,kind='action',topic='Networking',ic='globe',fx=[['draw',1]],counters=['dnsfail'],text='Draw 1. Counters Name Lookup Fails. Hosts DNS domains (you cannot buy domains here).')
card('grs',n='GRS Storage',tag='Storage · redundancy',cost=2,kind='deploy',topic='Storage',ic='cloud',tp=1,zr=True,layers='paas',guard=['region'],text='Deploy. 1 throughput. Copies to the paired region, so Region Outage never hits.')
card('arch',n='Archive Tier',tag='Storage · access tiers',cost=0,kind='action',topic='Storage',ic='box',fx=[['credits',1]],counters=['storebill'],text='+1 credit. Counters Storage Bill: lowest cost, offline, 180-day minimum.')
card('databox',n='Azure Data Box',tag='Storage · migration',cost=1,kind='action',topic='Storage',ic='box',fx=[['block',4]],counters=['bigmove'],text='Block 4. Counters Huge Migration: a physical device ships your data.')
card('mfa',n='MFA',tag='Identity',cost=1,kind='action',topic='Identity',ic='shield',fx=[['block',5]],counters=['brute'],text='Block 5. Counters Password Spray: something you know plus something you have.')
card('ca',n='Conditional Access',tag='Identity',cost=1,kind='action',topic='Identity',ic='shield',fx=[['block',4]],counters=['risky'],text='Block 4. Counters Risky Sign-in: uses signals like location to require MFA or block.')
card('connect',n='Entra Connect',tag='Identity · hybrid',cost=1,kind='action',topic='Identity',ic='users',fx=[['heal',3]],counters=['hybridid'],text='Heal 3. Counters Split Identities: syncs on-prem AD users to Entra ID.')
card('rbac',n='RBAC Least Privilege',tag='Security',cost=1,kind='action',topic='Security',ic='lock',fx=[['block',4]],counters=['insider'],text='Block 4. Counters Over-Privileged Account: give only the access needed.')
card('defender',n='Defender for Cloud',tag='Security',cost=2,kind='deploy',topic='Security',ic='shield',tp=1,zr=True,layers='paas',guard=['vuln'],text='Deploy. 1 throughput. Continuously checks posture, so Unpatched Weakness never hits.')
card('zt',n='Zero Trust',tag='Security',cost=1,kind='action',topic='Security',ic='shield',fx=[['block',3],['dmg',2]],text='Block 3, 2 damage. Verify explicitly, least privilege, assume breach.')
# ---- World 3 cards
card('budget',n='Budget Alert',tag='Cost Management',cost=0,kind='action',topic='Cost',ic='coin',fx=[['credits',1]],counters=['billshock'],text='+1 credit. Counters Bill Shock: alerts when spend hits your threshold.')
card('resv',n='Reservations',tag='Cost',cost=1,kind='action',topic='Cost',ic='coin',fx=[['credits',2]],text='+2 credits. Commit 1 or 3 years for steady workloads and save.')
card('tags',n='Resource Tags',tag='Cost · organizing',cost=0,kind='action',topic='Cost',ic='doc',fx=[['draw',1]],counters=['untagged'],text='Draw 1. Counters Mystery Costs: tag by cost center to see who spends what.')
card('calc',n='Pricing Calculator',tag='Cost',cost=1,kind='action',topic='Cost',ic='chart',fx=[['block',3]],counters=['estimate'],text='Block 3. Counters Surprise Estimate: price new services before you deploy.')
card('lock',n='Resource Lock',tag='Governance',cost=1,kind='action',topic='Governance',ic='lock',fx=[['block',3]],counters=['delete'],text='Block 3. Counters Accidental Delete. A Delete lock still allows changes; ReadOnly blocks both.')
card('policy',n='Azure Policy',tag='Governance',cost=1,kind='deploy',topic='Governance',ic='doc',tp=1,zr=True,layers='paas',guard=['rogue'],text='Deploy. 1 throughput. Denies non-compliant deployments, so Rogue Deploy never hits.')
card('purview',n='Microsoft Purview',tag='Governance',cost=1,kind='action',topic='Governance',ic='doc',fx=[['block',4]],counters=['datamap'],text='Block 4. Counters Unknown Data: discover and classify data everywhere.')
card('stp',n='Service Trust Portal',tag='Governance',cost=0,kind='action',topic='Governance',ic='doc',fx=[['heal',2]],counters=['audit'],text='Heal 2. Counters Audit Request: Microsoft compliance reports live here.')
card('arm',n='ARM Template',tag='Management',cost=1,kind='action',topic='Management',ic='doc',fx=[['dmg',3]],counters=['snowflake'],text='3 damage. Counters Hand-Built Snowflake: declarative, repeatable deployments.')
card('arc',n='Azure Arc',tag='Management',cost=1,kind='action',topic='Management',ic='link',fx=[['dmg',2]],counters=['unmanaged'],text='2 damage. Counters Unmanaged Servers outside Azure.')
card('shell',n='Cloud Shell',tag='Management',cost=0,kind='action',topic='Management',ic='doc',fx=[['draw',2]],text='Draw 2. Bash or PowerShell in the browser, nothing to install.')
card('monitor',n='Azure Monitor Alert',tag='Monitoring',cost=1,kind='action',topic='Monitoring',ic='chart',fx=[['block',4]],counters=['blind'],text='Block 4. Counters Nobody Noticed: alert when CPU or errors cross a threshold.')
card('health',n='Service Health',tag='Monitoring',cost=1,kind='action',topic='Monitoring',ic='heart',fx=[['heal',3]],counters=['maint'],text='Heal 3. Counters Surprise Maintenance: personalized service issues and planned maintenance.')
card('advisor',n='Azure Advisor',tag='Monitoring',cost=1,kind='action',topic='Monitoring',ic='star',fx=[['credits',1],['block',2]],counters=['overprov'],text='+1 credit, block 2. Counters Idle VMs: recommendations in five categories.')
# ---- threats
def th(k,n,dmg,learn,**x): T[k]=dict(n=n,dmg=dmg,learn=learn,**x)
th('zoneout','Zone Outage',5,'A zone outage takes down one datacenter in a region. Spread resources across availability zones, or use zone-redundant services.',lane=True)
th('region','Region Outage',8,'If a whole region fails, a paired region or geo-redundant storage (GRS) keeps you running.',destroy=9)
th('onprem','On-Prem Cut Off',5,'VPN Gateway (encrypted, over the internet) or ExpressRoute (private, not over the internet) connects on-premises to Azure.')
th('isolated','Isolated VNets',4,'Virtual network peering connects VNets directly over the Microsoft backbone.')
th('exposed','Public Exposure',6,'A private endpoint gives a service a private IP in your VNet, so it is not reachable from the internet.')
th('dnsfail','Name Lookup Fails',4,'Azure DNS hosts your DNS domains and supports private zones. You buy domain names from a registrar.')
th('storebill','Storage Bill',5,'Access tiers: hot (frequent), cool (30 days), cold (90 days), archive (180 days, offline, cheapest to store).')
th('bigmove','Huge Migration',6,'Azure Data Box ships a physical device for moving large amounts of data when the network is too slow.')
th('brute','Password Spray',6,'Multifactor authentication requires more than a password.')
th('risky','Risky Sign-in',6,'Conditional Access uses signals such as location and device to allow, block or require MFA.')
th('hybridid','Split Identities',5,'Microsoft Entra Connect syncs on-premises Active Directory identities to Microsoft Entra ID.')
th('insider','Over-Privileged Account',6,'RBAC grants only the access each role needs, at a chosen scope.')
th('vuln','Unpatched Weakness',5,'Microsoft Defender for Cloud monitors security posture and recommends fixes.')
th('billshock','Bill Shock',6,'Cost Management budgets and alerts warn you when spending reaches a threshold.')
th('untagged','Mystery Costs',4,'Tags (name-value pairs) let you group costs by department, project or environment.')
th('estimate','Surprise Estimate',4,'The pricing calculator estimates new Azure costs. The TCO calculator compares on-premises with Azure.')
th('delete','Accidental Delete',6,'Resource locks (Delete or ReadOnly) protect existing resources, even from Owners.',destroy=1)
th('rogue','Rogue Deploy',5,'Azure Policy evaluates and enforces rules on what can be deployed, such as allowed sizes and regions.')
th('datamap','Unknown Data',5,'Microsoft Purview discovers, classifies and governs data across on-premises, multicloud and SaaS.')
th('audit','Audit Request',4,'The Service Trust Portal holds Microsoft\'s compliance reports such as ISO and SOC.')
th('snowflake','Hand-Built Snowflake',5,'ARM templates and Bicep describe infrastructure declaratively, so every deployment is the same.')
th('unmanaged','Unmanaged Servers',5,'Azure Arc extends Azure management to servers outside Azure.')
th('blind','Nobody Noticed',6,'Azure Monitor collects metrics and logs and can alert on thresholds.')
th('maint','Surprise Maintenance',5,'Azure Service Health shows service issues, planned maintenance and health advisories for the services and regions you use.')
th('overprov','Idle VMs',4,'Azure Advisor recommends cost savings such as resizing or shutting down underused VMs.')
L=cp['levels']
def lv(i,w,n,teach,unlock,foe,hp,up,intents,deck=None):
    x=dict(id=i,world=w,n=n,teach=teach,unlock=unlock,foe=foe,hp=hp,up=up,intents=intents)
    if deck: x['deck']=deck
    L.append(x)
lv(11,2,'Three Zones','Spread across availability zones. A Zone Outage hits one zone.',['vm2','az'],['rv',1,'Outage Imp'],22,20,['zoneout','hit','zoneout'])
lv(12,2,'Scale Out','Scale sets span zones and scale with demand.',['vmss'],['rv',1,'Outage Imp'],26,20,['spike','zoneout','hit','spike'])
lv(13,2,'Serverless','Functions run event-driven code with no servers.',['func','aci'],['rv',1,'Outage Imp'],28,20,['zoneout','spike','hit','zoneout'])
lv(14,2,'Whole Region Down','Region pairs and GRS survive a region outage.',['pair','grs'],['rv',2,'Region Gremlin'],32,22,['region','zoneout','spike','region'])
lv(15,2,'Connect Home','VPN Gateway vs ExpressRoute for on-premises links.',['vpn','er'],['rv',2,'Packet Gremlin'],32,22,['onprem','zoneout','onprem','hit'])
lv(16,2,'Talk Between VNets','VNet peering joins virtual networks.',['peer'],['rv',2,'Packet Gremlin'],34,22,['isolated','onprem','zoneout','isolated'])
lv(17,2,'Close the Door','Private endpoints keep services off the internet.',['pe'],['rv',2,'Packet Gremlin'],36,22,['exposed','isolated','onprem','exposed'])
lv(18,2,'Names Matter','Azure DNS hosts domains.',['dns'],['rv',2,'Packet Gremlin'],36,22,['dnsfail','exposed','zoneout','dnsfail'])
lv(19,2,'Tier Down','Pick the right access tier.',['arch'],['rv',2,'Storage Gremlin'],38,22,['storebill','region','storebill','spike'])
lv(20,2,'Move the Mountain','Data Box moves huge data offline.',['databox'],['rv',2,'Storage Gremlin'],38,22,['bigmove','storebill','zoneout','bigmove'])
lv(21,2,'Password Spray','MFA stops password-only attacks.',['mfa'],['rv',3,'Sign-in Phantom'],40,22,['brute','exposed','brute','hit'])
lv(22,2,'Risky Sign-in','Conditional Access reacts to signals.',['ca'],['rv',3,'Sign-in Phantom'],40,22,['risky','brute','risky','zoneout'])
lv(23,2,'Two Directories','Entra Connect syncs hybrid identities.',['connect'],['rv',3,'Sign-in Phantom'],42,22,['hybridid','risky','brute','hybridid'])
lv(24,2,'Too Much Access','RBAC least privilege.',['rbac','zt'],['rv',3,'Insider Phantom'],44,24,['insider','hybridid','risky','insider'])
lv(25,2,'Posture Check','Defender for Cloud watches security posture.',['defender'],['rv',3,'Insider Phantom'],46,24,['vuln','insider','brute','vuln'])
lv(26,2,'BOSS: Zone Hydra','Every World 2 threat, three heads at once.',[],['boss',2,'Zone Hydra'],80,28,['zoneout','region','brute','exposed','spike','zoneout','insider','onprem','storebill','risky','zoneout','vuln'])
lv(27,3,'Budget Day','Budget alerts catch Bill Shock.',['budget','resv','vm2'],['rv',1,'Bill Shock Imp'],26,22,['billshock','hit','billshock'])
lv(28,3,'Who Spent That?','Tags group costs by team.',['tags'],['rv',1,'Bill Shock Imp'],30,22,['untagged','billshock','untagged','hit'])
lv(29,3,'Price It First','Pricing calculator before you deploy.',['calc'],['rv',1,'Bill Shock Imp'],32,22,['estimate','untagged','billshock','estimate'])
lv(30,3,'Oops, Deleted','Resource locks stop accidental deletes.',['lock'],['rv',3,'Misconfig Phantom'],34,22,['delete','billshock','delete','hit'])
lv(31,3,'Rules of the Road','Azure Policy decides what can be deployed.',['policy'],['rv',3,'Misconfig Phantom'],36,22,['rogue','delete','rogue','untagged'])
lv(32,3,'Data and Audits','Purview governs data. The Service Trust Portal has the reports.',['purview','stp'],['rv',3,'Misconfig Phantom'],38,22,['datamap','audit','rogue','datamap'])
lv(33,3,'Same Every Time','ARM templates make deployments repeatable.',['arm','shell'],['rv',2,'Ops Gremlin'],40,24,['snowflake','delete','rogue','snowflake'])
lv(34,3,'Beyond Azure','Azure Arc manages servers anywhere.',['arc'],['rv',2,'Ops Gremlin'],42,24,['unmanaged','snowflake','audit','unmanaged'])
lv(35,3,'Eyes On','Monitor alerts and Service Health.',['monitor','health','advisor'],['rv',2,'Ops Gremlin'],44,24,['blind','maint','overprov','blind'])
lv(36,3,'BOSS: Policy Warden','Every World 3 threat. Policy decides; locks protect.',[],['boss',3,'Policy Warden'],80,28,['rogue','delete','billshock','blind','snowflake','untagged','maint','delete','rogue','audit','overprov','unmanaged'])
w1=['payg','scale','ha','shared','dr','geo','vm','app']
w2=['az','vmss','pair','grs','vpn','er','pe','mfa','ca','rbac']
w3=['budget','tags','lock','policy','arm','monitor','health','advisor']
lv(37,4,'Exam Day: Concepts','Mixed World 1 threats with a full deck.',[],['rv',1,'Exam Imp'],40,24,['capex','spike','crash','breach','disaster','latency','patch'],deck=w1)
lv(38,4,'Exam Day: Architecture','Mixed World 2 threats.',[],['rv',2,'Exam Gremlin'],48,24,['zoneout','region','onprem','exposed','brute','risky','insider'],deck=w2+['vm2'])
lv(39,4,'Exam Day: Governance','Mixed World 3 threats.',[],['rv',3,'Exam Phantom'],48,24,['billshock','untagged','delete','rogue','snowflake','blind','maint'],deck=w3)
lv(40,4,'FINAL: The Exam','All three domains at once. Read each threat, pick the right service.',[],['boss',1,'Elder CapEx Colossus',3],110,32,['capex','zoneout','delete','brute','billshock','region','rogue','spike','breach','blind','exposed','disaster','insider','maint'],deck=['payg','scale','ha','shared','dr','az','vmss','pair','grs','pe','mfa','rbac','budget','lock','policy','monitor','health','vm2'])
# self-check: every threat in a level has a counter available in that level's deck
def deck(l):
    if l.get('deck'): return set(l['deck'])
    ids=set()
    for x in L:
        if x['world']==l['world'] and x['id']<=l['id']: ids|=set(x['unlock'])
    return ids
for l in L:
    dk=deck(l);assert dk,l['id']
    for k in l['intents']:
        assert k in T,(l['id'],k)
        if k=='hit': continue
        assert any(k in C[c].get('counters',[])+C[c].get('guard',[]) for c in dk),(l['id'],k,'no counter in deck')
    for c in l['unlock']+l.get('deck',[]): assert c in C,c
assert [l['id'] for l in L]==list(range(1,41))
json.dump(d,open(P,'w'),ensure_ascii=False);print('ok',len(C),'cards',len(T),'threats',len(L),'levels')
