# Cloud Clash campaigns for SC-900, AZ-104 and SC-500.
# One world per exam domain. Each world: a deploy card, four counter cards, one utility card,
# four threats, and three levels (two fights and a boss). Run directly, or call apply(data)
# from a pack build script. AZ-900 keeps its own campaign (camp_data.py).
import json, os

def W(name, boss, rivals, deploy, counters, util):
    return dict(n=name, boss=boss, rivals=rivals, deploy=deploy, counters=counters, util=util)

def dep(i, n, tag, topic, ic, text):
    return (i, dict(n=n, tag=tag, cost=1, kind='deploy', topic=topic, ic=ic, tp=2, text='Deploy. 2 throughput each turn. ' + text))

def ctr(i, n, tag, topic, ic, fx, threat, text):
    return (i, dict(n=n, tag=tag, cost=1, kind='action', topic=topic, ic=ic, fx=fx, counters=[threat[0]], text=text), threat)

def utl(i, n, tag, topic, ic, fx, text):
    return (i, dict(n=n, tag=tag, cost=0 if fx[0][0] == 'credits' else 1, kind='action', topic=topic, ic=ic, fx=fx, text=text))

B4 = [['block', 4]]; B5 = [['block', 5]]; D3 = [['dmg', 3]]; DB = [['dmg', 2], ['block', 2]]; H3 = [['heal', 3]]
CR = [['credits', 1]]; DR = [['draw', 1], ['dmg', 1]]

SC900 = [
 W('World 1: Security Concepts', 'Perimeter Golem', ['Trust Imp', 'Spoof Gremlin'],
   dep('did', 'Defense in Depth', 'Layered security', 'Security concepts', 'shield', 'Many layers, so one breach is not the end.'),
   [ctr('verify', 'Verify Explicitly', 'Zero Trust', 'Security concepts', 'check', B4,
        ('trust', 'Implicit Trust', 5, 'Zero Trust never trusts a request because of where it comes from. Verify explicitly every time.'), 'Block 4. Counters Implicit Trust.'),
    ctr('least', 'Least Privilege', 'Zero Trust', 'Security concepts', 'lock', D3,
        ('overperm', 'Over-permissioned Account', 6, 'Least privilege gives just enough access, just in time.'), '3 damage. Counters Over-permissioned Account.'),
    ctr('encrypt', 'Encryption', 'Data protection', 'Security concepts', 'lock', B5,
        ('sniff', 'Traffic Sniffer', 6, 'Encryption in transit (TLS) makes intercepted data unreadable.'), 'Block 5. Counters Traffic Sniffer.'),
    ctr('authn', 'Authentication', 'Identity', 'Identity concepts', 'users', DB,
        ('spoof', 'Impersonation', 5, 'Authentication proves who you are. Authorization decides what you can do.'), '2 damage, block 2. Counters Impersonation.')],
   utl('idp', 'Identity Provider', 'Modern auth', 'Identity concepts', 'link', CR, '+1 credit. One trusted provider issues the tokens.')),
 W('World 2: Microsoft Entra', 'Token Hydra', ['Spray Imp', 'Guest Phantom'],
   dep('entra', 'Microsoft Entra ID', 'Cloud identity', 'Entra ID and identities', 'users', 'Cloud identity for users, groups and apps.'),
   [ctr('mfa', 'MFA', 'Authentication', 'Authentication', 'phone', B5,
        ('spray', 'Password Spray', 6, 'MFA asks for a second factor, so a stolen password alone is not enough.'), 'Block 5. Counters Password Spray.'),
    ctr('ca', 'Conditional Access', 'Access policy', 'Access management', 'flag', D3,
        ('risky', 'Risky Sign-in', 6, 'Conditional Access uses signals like user, location and risk to allow, block or require MFA.'), '3 damage. Counters Risky Sign-in.'),
    ctr('pim', 'PIM', 'Just-in-time admin', 'Identity governance', 'star', DB,
        ('standing', 'Standing Admin', 5, 'Privileged Identity Management gives admin roles just in time, with approval and expiry.'), '2 damage, block 2. Counters Standing Admin.'),
    ctr('review', 'Access Review', 'Governance', 'Identity governance', 'check', B4,
        ('stale', 'Stale Guest Access', 5, 'Access reviews let owners confirm or remove access on a schedule.'), 'Block 4. Counters Stale Guest Access.')],
   utl('hello', 'Passwordless', 'Windows Hello', 'Authentication', 'bolt', CR, '+1 credit. Windows Hello and passkeys replace the password.')),
 W('World 3: Security Solutions', 'Kill Chain Wyrm', ['Flood Imp', 'Port Gremlin'],
   dep('sentinel', 'Microsoft Sentinel', 'SIEM and SOAR', 'Microsoft Sentinel', 'chart', 'Collects data, detects threats, responds.'),
   [ctr('ddos', 'DDoS Protection', 'Network defense', 'Azure infrastructure security', 'shield', B5,
        ('flood', 'DDoS Flood', 7, 'Azure DDoS Protection absorbs and filters flood traffic aimed at public IPs.'), 'Block 5. Counters DDoS Flood.'),
    ctr('bastion', 'Azure Bastion', 'Secure access', 'Azure infrastructure security', 'lock', D3,
        ('rdp', 'Open RDP Port', 5, 'Azure Bastion gives RDP and SSH from the portal over TLS. The VM needs no public IP.'), '3 damage. Counters Open RDP Port.'),
    ctr('score', 'Secure Score', 'CSPM', 'Defender for Cloud', 'chart', B4,
        ('misconf', 'Misconfiguration', 5, 'Defender for Cloud finds weak settings and gives recommendations. Fixing them raises secure score.'), 'Block 4. Counters Misconfiguration.'),
    ctr('xdr', 'Defender XDR', 'Unified incidents', 'Defender XDR', 'sword', DB,
        ('xattack', 'Cross-domain Attack', 6, 'Defender XDR correlates email, endpoint, identity and app alerts into one incident.'), '2 damage, block 2. Counters Cross-domain Attack.')],
   utl('playbook', 'Playbook', 'SOAR', 'Microsoft Sentinel', 'wrench', H3, 'Heal 3. Sentinel playbooks automate the response.')),
 W('World 4: Compliance Solutions', 'Audit Leviathan', ['Leak Imp', 'Insider Phantom'],
   dep('purview', 'Compliance Manager', 'Microsoft Purview', 'Compliance management', 'check', 'Tracks controls and gives a compliance score.'),
   [ctr('label', 'Sensitivity Label', 'Information protection', 'Information protection', 'flag', B4,
        ('overshare', 'Overshared File', 5, 'Sensitivity labels classify content and can encrypt it or add markings.'), 'Block 4. Counters Overshared File.'),
    ctr('dlp', 'DLP Policy', 'Data loss prevention', 'Information protection', 'shield', D3,
        ('exfil', 'Card Numbers Emailed', 6, 'Data loss prevention finds sensitive info like card numbers and blocks or warns on sharing.'), '3 damage. Counters Card Numbers Emailed.'),
    ctr('irm', 'Insider Risk', 'Risk management', 'Insider risk, eDiscovery, audit', 'users', DB,
        ('insider', 'Departing Employee', 6, 'Insider Risk Management spots risky activity, like data theft by a departing user.'), '2 damage, block 2. Counters Departing Employee.'),
    ctr('hold', 'eDiscovery Hold', 'Legal hold', 'Insider risk, eDiscovery, audit', 'lock', B5,
        ('legal', 'Lawsuit Notice', 6, 'eDiscovery cases can place holds so content is kept for a legal matter.'), 'Block 5. Counters Lawsuit Notice.')],
   utl('stp', 'Service Trust Portal', 'Trust and privacy', 'Trust and privacy', 'doc', DR, 'Draw 1, 1 damage. Microsoft audit reports and compliance docs.')),
]

AZ104 = [
 W('World 1: Identity and Governance', 'Sprawl Titan', ['Owner Imp', 'Untagged Gremlin'],
   dep('mg', 'Management Group', 'Scope', 'Governance', 'grid', 'Policy and RBAC flow down to subscriptions.'),
   [ctr('policy', 'Azure Policy', 'Governance', 'Governance', 'doc', B4,
        ('sprawl', 'Untagged Sprawl', 5, 'Azure Policy can deny, audit or modify resources, like requiring a tag.'), 'Block 4. Counters Untagged Sprawl.'),
    ctr('lock', 'Delete Lock', 'Resource lock', 'Governance', 'lock', B5,
        ('delete', 'Accidental Delete', 6, 'A CanNotDelete lock stops deletes even for Owners until the lock is removed.'), 'Block 5. Counters Accidental Delete.'),
    ctr('rbac', 'Scoped Role', 'Azure RBAC', 'Azure RBAC', 'users', D3,
        ('owners', 'Owner for Everyone', 6, 'Azure RBAC: give the smallest role at the smallest scope, like Reader on one resource group.'), '3 damage. Counters Owner for Everyone.'),
    ctr('dyn', 'Dynamic Group', 'Entra ID', 'Entra users and groups', 'users', DB,
        ('joiner', 'New Hire No Access', 5, 'Dynamic groups add users by rule, like department. They need Entra ID P1.'), '2 damage, block 2. Counters New Hire No Access.')],
   utl('budget', 'Budget Alert', 'Cost Management', 'Governance', 'coin', CR, '+1 credit. Budgets alert when spend crosses a threshold.')),
 W('World 2: Storage', 'Blob Kraken', ['Key Imp', 'Tier Gremlin'],
   dep('sa', 'Storage Account', 'General-purpose v2', 'Storage accounts', 'box', 'Blobs, files, queues and tables.'),
   [ctr('rotate', 'Key Rotation', 'Access keys', 'Storage access', 'wrench', B4,
        ('keyleak', 'Leaked Access Key', 6, 'Each account has two keys, so you can rotate one while apps use the other.'), 'Block 4. Counters Leaked Access Key.'),
    ctr('sfw', 'Storage Firewall', 'Network rules', 'Storage access', 'shield', D3,
        ('anyip', 'Open to Any Network', 5, 'Storage firewall rules limit access to selected VNets and IP ranges.'), '3 damage. Counters Open to Any Network.'),
    ctr('grs', 'Geo-redundancy', 'GRS', 'Storage accounts', 'globe', B5,
        ('regionout', 'Region Outage', 7, 'GRS copies data to the paired region. LRS and ZRS stay in one region.'), 'Block 5. Counters Region Outage.'),
    ctr('life', 'Lifecycle Rule', 'Access tiers', 'Files and Blob', 'chart', DB,
        ('hotcost', 'Old Data on Hot', 5, 'Lifecycle management moves blobs to Cool, Cold or Archive by age.'), '2 damage, block 2. Counters Old Data on Hot.')],
   utl('azcopy', 'AzCopy', 'Data transfer', 'Files and Blob', 'arrows', DR, 'Draw 1, 1 damage. Command-line copy to and from storage.')),
 W('World 3: Compute', 'Release Hydra', ['Drift Imp', 'Zone Gremlin'],
   dep('vmss', 'VM Scale Set', 'Virtual machines', 'Virtual machines', 'server', 'Identical VMs that scale out.'),
   [ctr('zones', 'Availability Zones', 'Resilience', 'Virtual machines', 'copy', B5,
        ('zonefail', 'Datacenter Fails', 7, 'Spreading VMs across availability zones survives a datacenter failure.'), 'Block 5. Counters Datacenter Fails.'),
    ctr('bicep', 'Bicep Template', 'Infrastructure as code', 'ARM and Bicep', 'doc', D3,
        ('handbuilt', 'Hand-built Drift', 5, 'Bicep and ARM templates are declarative and repeatable, so every deploy matches.'), '3 damage. Counters Hand-built Drift.'),
    ctr('slot', 'Slot Swap', 'Deployment slots', 'App Service', 'arrows', H3,
        ('badrel', 'Bad Release', 6, 'Deploy to a staging slot, test, then swap. Swap back to roll back.'), 'Heal 3. Counters Bad Release.'),
    ctr('acr', 'Container Registry', 'ACR', 'Containers', 'box', DB,
        ('pullfail', 'Image Pull Fails', 5, 'Azure Container Registry stores images. Grant AcrPull so the host can pull them.'), '2 damage, block 2. Counters Image Pull Fails.')],
   utl('aci', 'Container Instances', 'ACI', 'Containers', 'bolt', CR, '+1 credit. Run a container fast with no VM to manage.')),
 W('World 4: Networking', 'Subnet Serpent', ['Port Imp', 'Island Gremlin'],
   dep('vnet', 'Virtual Network', 'VNet', 'Virtual networks', 'link', 'Private network for your resources.'),
   [ctr('nsg', 'NSG Rule', 'Network security', 'Network security', 'shield', B4,
        ('openport', 'Port 3389 Open', 5, 'NSGs allow or deny traffic by priority. Lower numbers are checked first.'), 'Block 4. Counters Port 3389 Open.'),
    ctr('peer', 'VNet Peering', 'Connectivity', 'Virtual networks', 'link', D3,
        ('island', 'Isolated VNets', 5, 'Peering connects two VNets over the Microsoft backbone. It is not transitive.'), '3 damage. Counters Isolated VNets.'),
    ctr('lb', 'Load Balancer', 'Layer 4', 'DNS and load balancing', 'arrows', DB,
        ('overload', 'One Server Overloaded', 6, 'Azure Load Balancer spreads TCP and UDP traffic across healthy backends.'), '2 damage, block 2. Counters One Server Overloaded.'),
    ctr('pdns', 'Private DNS Zone', 'Name resolution', 'DNS and load balancing', 'globe', B5,
        ('noname', 'Names Will Not Resolve', 6, 'A private DNS zone linked to the VNet resolves private names.'), 'Block 5. Counters Names Will Not Resolve.')],
   utl('udr', 'Route Table', 'User-defined routes', 'Virtual networks', 'arrows', CR, '+1 credit. Send traffic through a firewall with a custom route.')),
 W('World 5: Monitor and Maintain', 'Silent Outage', ['Spike Imp', 'Blind Phantom'],
   dep('law', 'Log Analytics', 'Workspace', 'Monitoring', 'chart', 'Stores logs you query with KQL.'),
   [ctr('alert', 'Alert Rule', 'Azure Monitor', 'Monitoring', 'sound', B4,
        ('cpuspike', 'Silent CPU Spike', 5, 'An alert rule watches a metric or log and calls an action group.'), 'Block 4. Counters Silent CPU Spike.'),
    ctr('soft', 'Backup Soft Delete', 'Recovery Services', 'Backup and recovery', 'heart', B5,
        ('wipe', 'Backups Deleted', 7, 'Soft delete keeps deleted backup data for 14 days so it can be recovered.'), 'Block 5. Counters Backups Deleted.'),
    ctr('asr', 'Site Recovery', 'Disaster recovery', 'Backup and recovery', 'cloud', H3,
        ('regiondown', 'Region Down', 6, 'Azure Site Recovery replicates VMs to another region and fails over.'), 'Heal 3. Counters Region Down.'),
    ctr('nw', 'Network Watcher', 'Diagnostics', 'Monitoring', 'monitor', D3,
        ('blind', 'Cannot Find the Fault', 5, 'Network Watcher tools like IP flow verify show why traffic is blocked.'), '3 damage. Counters Cannot Find the Fault.')],
   utl('kql', 'KQL Query', 'Log queries', 'Monitoring', 'grid', DR, 'Draw 1, 1 damage. Search logs in the workspace.')),
]

SC500 = [
 W('World 1: Identity and Governance', 'Privilege Titan', ['Secret Imp', 'Purge Gremlin'],
   dep('kv', 'Key Vault', 'Secrets and keys', 'Key Vault', 'lock', 'Keys, secrets and certificates in one vault.'),
   [ctr('mi', 'Managed Identity', 'No stored secrets', 'Entra access', 'users', D3,
        ('incode', 'Secret in Code', 6, 'A managed identity gets tokens from Entra ID, so there is no secret to store.'), '3 damage. Counters Secret in Code.'),
    ctr('purge', 'Purge Protection', 'Key Vault', 'Key Vault', 'shield', B5,
        ('purged', 'Vault Purged', 7, 'With purge protection, a deleted vault cannot be purged until retention ends.'), 'Block 5. Counters Vault Purged.'),
    ctr('pim', 'PIM', 'Just-in-time roles', 'Entra access', 'star', DB,
        ('standing', 'Standing Global Admin', 6, 'PIM makes admin roles eligible, then active on request with MFA and approval.'), '2 damage, block 2. Counters Standing Global Admin.'),
    ctr('init', 'Policy Initiative', 'Regulatory compliance', 'Governance and compliance', 'doc', B4,
        ('drift', 'Noncompliant Resources', 5, 'Policy initiatives group policies, and regulatory compliance maps them to standards.'), 'Block 4. Counters Noncompliant Resources.')],
   utl('ca', 'Conditional Access', 'Access policy', 'Entra access', 'flag', CR, '+1 credit. Require MFA or a compliant device by policy.')),
 W('World 2: Data and Network', 'Exfil Kraken', ['Inject Imp', 'Endpoint Gremlin'],
   dep('fw', 'Azure Firewall', 'Network security', 'Network security', 'flame', 'Stateful firewall for the hub VNet.'),
   [ctr('dsql', 'Defender for SQL', 'Threat detection', 'Database security', 'sword', D3,
        ('sqli', 'SQL Injection', 6, 'Defender for SQL alerts on SQL injection and odd access to the database.'), '3 damage. Counters SQL Injection.'),
    ctr('ae', 'Always Encrypted', 'Client-side encryption', 'Database security', 'lock', B5,
        ('dbapeek', 'DBA Reads Card Data', 6, 'Always Encrypted keeps keys on the client, so the database engine never sees plaintext.'), 'Block 5. Counters DBA Reads Card Data.'),
    ctr('pe', 'Private Endpoint', 'Private Link', 'Storage security', 'link', B4,
        ('publicep', 'Public Endpoint', 5, 'A private endpoint gives the service a private IP in your VNet.'), 'Block 4. Counters Public Endpoint.'),
    ctr('waf', 'Web Application Firewall', 'WAF', 'Network security', 'shield', DB,
        ('owasp', 'Web App Attack', 6, 'WAF on Application Gateway or Front Door blocks common web attacks like XSS.'), '2 damage, block 2. Counters Web App Attack.')],
   utl('cmk', 'Customer-managed Key', 'Encryption at rest', 'Storage security', 'lock', DR, 'Draw 1, 1 damage. You control the key in Key Vault.')),
 W('World 3: Compute and AI', 'Prompt Hydra', ['Port Imp', 'Shadow Phantom'],
   dep('dfs', 'Defender for Servers', 'Workload protection', 'Servers and VMs', 'server', 'Threat protection for VMs and servers.'),
   [ctr('jit', 'Just-in-time Access', 'VM access', 'Servers and VMs', 'lock', B4,
        ('mgmtport', 'Open Management Ports', 5, 'JIT keeps RDP and SSH closed and opens them only on approved request, for a set time.'), 'Block 4. Counters Open Management Ports.'),
    ctr('aks', 'Disable Local Accounts', 'AKS', 'App platform security', 'users', D3,
        ('aksadmin', 'Cluster Admin Cert', 6, 'Disable AKS local accounts so all access goes through Entra ID and RBAC.'), '3 damage. Counters Cluster Admin Cert.'),
    ctr('shields', 'Prompt Shields', 'Content Safety', 'Security for AI', 'shield', B5,
        ('inject', 'Prompt Injection', 7, 'Prompt Shields in Azure AI Content Safety detect jailbreak and indirect prompt attacks.'), 'Block 5. Counters Prompt Injection.'),
    ctr('aispm', 'AI Posture', 'Defender CSPM', 'Security for AI', 'chart', DB,
        ('shadowai', 'Unknown AI Apps', 5, 'AI security posture management in Defender CSPM finds AI workloads and their risks.'), '2 damage, block 2. Counters Unknown AI Apps.')],
   utl('easyauth', 'App Service Auth', 'Built-in sign-in', 'App platform security', 'check', CR, '+1 credit. Sign-in for the app with no code.')),
 W('World 4: Posture and Monitoring', 'Breach Leviathan', ['Config Imp', 'Path Phantom'],
   dep('sentinel', 'Microsoft Sentinel', 'SIEM', 'Microsoft Sentinel', 'chart', 'Collects security data and runs detections.'),
   [ctr('recs', 'Recommendations', 'Secure score', 'Defender for Cloud posture', 'check', B4,
        ('misconf', 'Misconfiguration', 5, 'Defender for Cloud recommendations fix weak settings and raise secure score.'), 'Block 4. Counters Misconfiguration.'),
    ctr('apath', 'Attack Path Analysis', 'Defender CSPM', 'Defender for Cloud posture', 'arrows', D3,
        ('path', 'Path to Crown Jewels', 7, 'Attack path analysis in Defender CSPM shows how an attacker could reach key assets.'), '3 damage. Counters Path to Crown Jewels.'),
    ctr('rule', 'Analytics Rule', 'Detection', 'Microsoft Sentinel', 'flag', DB,
        ('noalert', 'Logs but No Alerts', 6, 'Sentinel analytics rules run queries on your data and raise incidents.'), '2 damage, block 2. Counters Logs but No Alerts.'),
    ctr('copilot', 'Security Copilot', 'AI assistant', 'Security Copilot', 'spark', H3,
        ('slowtriage', 'Slow Triage', 6, 'Security Copilot summarizes incidents and suggests next steps in plain language.'), 'Heal 3. Counters Slow Triage.')],
   utl('auto', 'Automation Rule', 'SOAR', 'Microsoft Sentinel', 'wrench', DR, 'Draw 1, 1 damage. Assign, tag or close incidents automatically.')),
]

ICONS = set('arrows bolt box building cart chart chat check cloud clouds coin copy doc flag flame globe grid heart link lock monitor mute phone server shield sound spark star sword ticket users wrench'.split())

def build(worlds, pk):
    topics = {q['topic'] for q in pk['questions']}
    C, T, L, WS = {}, {'hit': dict(n='Outage Ping', dmg=3, learn='A plain attack. Block reduces it.')}, [], []
    lid = 0
    for wi, w in enumerate(worlds, 1):
        WS.append(dict(id=wi, n=w['n'], d=wi))
        di, dc = w['deploy']; C[di] = dc
        ks = []
        for ci, cc, (tk, tn, dmg, learn) in w['counters']:
            C[ci] = cc; T[tk] = dict(n=tn, dmg=dmg, learn=learn); ks.append(tk)
        ui, uc = w['util']; C[ui] = uc
        cs = [c[0] for c in w['counters']]
        bump = 3 * (wi - 1)
        lvs = [
            dict(n=w['n'].split(': ')[1] + ' I', teach='Deploy ' + dc['n'] + ', then counter each incident.', unlock=[di, cs[0], cs[1]],
                 foe=['rv', 1 if wi < 3 else 2, w['rivals'][0]], hp=24 + bump, up=20, intents=[ks[0], 'hit', ks[1], ks[0]]),
            dict(n=w['n'].split(': ')[1] + ' II', teach='Two more counters and ' + uc['n'] + '.', unlock=[cs[2], cs[3], ui],
                 foe=['rv', 2 if wi < 3 else 3, w['rivals'][1]], hp=34 + bump, up=22, intents=[ks[2], ks[3], 'hit', ks[0], ks[2]]),
            dict(n='BOSS: ' + w['boss'], teach='Every incident from this world.', unlock=[],
                 foe=['boss', min(3, wi), w['boss']], hp=56 + 2 * bump, up=24, intents=[ks[0], ks[1], ks[2], 'hit', ks[3], ks[1], ks[2], ks[0]]),
        ]
        for lv in lvs:
            lid += 1; lv['id'] = lid; lv['world'] = wi; L.append(lv)
    for k, c in C.items():
        assert c['topic'] in topics, (k, c['topic'])
        assert c['ic'] in ICONS, (k, c['ic'])
    for k in T:
        if k != 'hit':
            assert sum(k in c.get('counters', []) for c in C.values()) == 1, k
    for lv in L:
        for k in lv['intents']: assert k in T, k
    return dict(worlds=WS, cards=C, threats=T, levels=L, lanes=False)

def apply(data):
    P = data['packs']
    for pid, worlds in (('sc900', SC900), ('az104', AZ104), ('sc500', SC500)):
        if pid in P:
            P[pid]['campaign'] = build(worlds, P[pid])

if __name__ == '__main__':
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'data_packs.json')
    d = json.load(open(p)); apply(d); json.dump(d, open(p, 'w'), ensure_ascii=False)
    for pid in ('sc900', 'az104', 'sc500'):
        c = d['packs'][pid]['campaign']; print(pid, len(c['cards']), 'cards', len(c['threats']), 'threats', len(c['levels']), 'levels')
