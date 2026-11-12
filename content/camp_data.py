import json
P='src/data_packs.json';d=json.load(open(P));pk=d['packs']['az900']
C={
 'vm':   dict(n='Virtual Machine',tag='IaaS',cost=1,kind='deploy',topic='Service types',ic='server',tp=2,layers='iaas',text='Deploy. Deals 2 throughput each turn. You patch its OS.'),
 'payg': dict(n='Pay-as-you-go',tag='Consumption',cost=0,kind='action',topic='Cost model',ic='coin',fx=[['credits',1]],counters=['capex'],text='+1 credit. Counters Upfront Hardware Bill.'),
 'scale':dict(n='Autoscale',tag='Scalability',cost=1,kind='action',topic='Benefits',ic='bolt',fx=[['boost',2]],counters=['spike'],text='Deployed throughput x2 this turn. Counters Traffic Spike.'),
 'ha':   dict(n='Second Instance',tag='High availability',cost=1,kind='action',topic='Benefits',ic='copy',fx=[['block',4]],counters=['crash'],text='Block 4. Counters Server Crash.'),
 'patch':dict(n='Patch the OS',tag='Shared responsibility',cost=1,kind='action',topic='Shared responsibility',ic='wrench',fx=[['dmg',2]],counters=['patch'],text='2 damage. Counters Unpatched OS.'),
 'app':  dict(n='App Service',tag='PaaS',cost=2,kind='deploy',topic='Service types',ic='box',tp=3,layers='paas',guard=['patch'],text='Deploy. 3 throughput. Microsoft patches the OS, so Unpatched OS never hits it.'),
 'geo':  dict(n='Geo-distribution',tag='Global reach',cost=1,kind='action',topic='Benefits',ic='globe',fx=[['dmg',3]],counters=['latency'],text='3 damage. Counters Faraway Users.'),
 'shared':dict(n='Own Your Data',tag='Shared responsibility',cost=1,kind='action',topic='Shared responsibility',ic='shield',fx=[['block',5]],counters=['breach'],text='Block 5. Counters Data Breach. Your data is always your job.'),
 'hybrid':dict(n='Hybrid Cloud',tag='Cloud models',cost=2,kind='deploy',topic='Cloud models',ic='link',tp=1,layers='hybrid',guard=['residency'],text='Deploy. 1 throughput. Keeps regulated data on-premises, so Data Residency never hits.'),
 'gov':  dict(n='Governance Templates',tag='Security and governance',cost=1,kind='action',topic='Benefits',ic='doc',fx=[['block',3]],counters=['drift'],text='Block 3. Counters Config Drift.'),
 'mon':  dict(n='Monitoring Alerts',tag='Predictability',cost=1,kind='action',topic='Benefits',ic='chart',fx=[['draw',1],['block',3]],counters=['surprise'],text='Draw 1, block 3. Counters Silent Failure.'),
 'dr':   dict(n='Backup and DR',tag='Reliability',cost=2,kind='action',topic='Benefits',ic='cloud',fx=[['heal',4]],counters=['disaster'],text='Heal 4 uptime. Counters Datacenter Disaster.'),
 'saas': dict(n='Microsoft 365',tag='SaaS',cost=1,kind='action',topic='Service types',ic='users',fx=[['heal',3],['dmg',1]],text='Heal 3, 1 damage. You manage only data, devices and identities.'),
 'multi':dict(n='Multi-cloud',tag='Cloud models',cost=1,kind='action',topic='Cloud models',ic='clouds',fx=[['dmg',2],['block',2]],text='2 damage, block 2. Spreads risk across providers.'),
}
T={
 'hit':      dict(n='Outage Ping',dmg=3,learn='A plain attack. Block reduces it.'),
 'capex':    dict(n='Upfront Hardware Bill',dmg=5,learn='CapEx means paying upfront for hardware. The cloud\'s consumption model (pay-as-you-go) has no upfront cost.'),
 'spike':    dict(n='Traffic Spike',dmg=6,learn='Scalability (autoscale) adds resources when demand rises.'),
 'crash':    dict(n='Server Crash',dmg=4,destroy=1,learn='High availability keeps a second instance running. Without it, a crash takes a resource down.'),
 'patch':    dict(n='Unpatched OS',dmg=2,perVM=2,learn='With IaaS you patch the OS. PaaS and SaaS shift patching to Microsoft.'),
 'latency':  dict(n='Faraway Users',dmg=4,learn='Geo-distribution puts apps in regional datacenters close to users.'),
 'breach':   dict(n='Data Breach',dmg=7,learn='Under shared responsibility, your data, devices, accounts and identities are always yours to protect.'),
 'residency':dict(n='Data Residency Rule',dmg=6,learn='Hybrid cloud keeps some data and workloads on-premises while using public cloud for the rest.'),
 'drift':    dict(n='Config Drift',dmg=5,learn='Governance in the cloud uses templates and policies to keep deployments compliant.'),
 'surprise': dict(n='Silent Failure',dmg=6,learn='Predictability comes from monitoring: you see problems before users do.'),
 'disaster': dict(n='Datacenter Disaster',dmg=9,destroy=9,learn='Reliability means recovering from failures: backups, replication and disaster recovery.'),
}
L=[
 dict(id=1,n='Hello, Cloud',teach='Pay-as-you-go beats the Upfront Hardware Bill.',unlock=['vm','payg'],foe=['rv',1,'CapEx Imp'],hp=10,up=20,intents=['capex','hit','capex']),
 dict(id=2,n='Rush Hour',teach='Autoscale handles a Traffic Spike.',unlock=['scale'],foe=['rv',1,'CapEx Imp'],hp=13,up=20,intents=['hit','spike','capex','spike']),
 dict(id=3,n='Server Down',teach='A second instance keeps you up when a server crashes.',unlock=['ha'],foe=['rv',2,'Lag Gremlin'],hp=14,up=20,intents=['crash','spike','hit','crash']),
 dict(id=4,n='Who Patches?',teach='With IaaS, you patch the OS. More VMs, bigger hit.',unlock=['patch'],foe=['rv',2,'Lag Gremlin'],hp=15,up=20,intents=['patch','crash','hit','patch']),
 dict(id=5,n='Platform Shift',teach='PaaS: Microsoft patches the OS for you.',unlock=['app'],foe=['rv',2,'Lag Gremlin'],hp=17,up=20,intents=['patch','spike','patch','capex']),
 dict(id=6,n='Faraway Users',teach='Geo-distribution brings apps close to users.',unlock=['geo'],foe=['rv',2,'Latency Gremlin'],hp=18,up=20,intents=['latency','spike','crash','latency']),
 dict(id=7,n='Your Data, Your Job',teach='Data is always the customer\'s responsibility.',unlock=['shared','saas'],foe=['rv',3,'Breach Phantom'],hp=19,up=22,intents=['breach','patch','hit','breach']),
 dict(id=8,n='Stay On-Prem',teach='Hybrid cloud keeps regulated data on-premises.',unlock=['hybrid','multi'],foe=['rv',3,'Breach Phantom'],hp=20,up=22,intents=['residency','breach','spike','residency']),
 dict(id=9,n='Steady State',teach='Governance and monitoring keep things predictable.',unlock=['gov','mon'],foe=['rv',3,'Misconfig Phantom'],hp=22,up=22,intents=['drift','surprise','breach','spike','drift']),
 dict(id=10,n='BOSS: CapEx Colossus',teach='Everything from World 1, plus Datacenter Disaster.',unlock=['dr'],foe=['boss',1,'CapEx Colossus'],hp=34,up=26,intents=['capex','disaster','spike','crash','breach','surprise','disaster','patch','drift']),
]
# enemy HP as retuned after the scripted 40-level playthrough
for lv,hp in zip(L,[18,26,32,34,38,42,46,50,46,72]):lv['hp']=hp
pk['campaign']={'worlds':[{'id':1,'n':'World 1: Cloud Concepts','d':1}],'cards':C,'threats':T,'levels':L}
for l in L:
    for k in l['intents']: assert k in T,k
    for c in l['unlock']: assert c in C
for k in T:
    if k!='hit': assert any(k in c.get('counters',[])+c.get('guard',[]) for c in C.values()),k
json.dump(d,open(P,'w'),ensure_ascii=False);print('ok',len(C),len(T),len(L))
