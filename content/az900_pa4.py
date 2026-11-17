# AZ-900 Practice Assessment 4 (Nov 17, 2026, 70%): one item set per miss, all flagged weak (miss=True)
# so drills serve them first. Own wording, not Microsoft's. Re-running replaces the earlier pa4 items.
#   python3 content/az900_pa4.py && python3 build.py
import json, random, os
P = os.path.join(os.path.dirname(__file__), '..', 'src', 'data_packs.json')
R = random.Random(1117)
CARDS, QS, DUELS = [], [], []
QT = {'benefits': (1, 'Benefits', 'Benefits of the cloud'), 'types': (1, 'Service types', 'Service types'),
      'shared': (1, 'Shared responsibility', 'Shared responsibility'),
      'regions': (2, 'Regions and zones', 'Regions and zones'), 'hier': (2, 'Hierarchy', 'Management hierarchy'), 'compute': (2, 'Compute', 'Compute'),
      'cost': (3, 'Cost', 'Cost management'), 'gov': (3, 'Governance', 'Governance'), 'mgmt': (3, 'Management', 'Managing and deploying'), 'mon': (3, 'Monitoring', 'Monitoring')}
TAG = dict(miss=True, pa4=True)

def C(t, front, back):
    d, _, ct = QT[t]; CARDS.append(dict(id='c%d' % (401 + len(CARDS)), d=d, topic=ct, front=front, back=back, **TAG))
def _q(t, **k):
    d, qt, _ = QT[t]; x = dict(id='q%d' % (401 + len(QS)), d=d, topic=qt); x.update(k); x.update(TAG); QS.append(x)
def Q(t, q, right, wrong, why):
    right = [right] if isinstance(right, str) else right
    opts = right + wrong; assert len(opts) == 4 and len(set(opts)) == 4, q
    if len(right) == 2: assert 'TWO' in q, q
    R.shuffle(opts); _q(t, q=q, opts=opts, ans=sorted(opts.index(r) for r in right), why=why, kind='one' if len(right) == 1 else 'two')
def M(t, q, pairs, why):
    rows = [a for a, _ in pairs]; ch = [b for _, b in pairs]; order = ch[:]; R.shuffle(order)
    _q(t, type='match', kind='match', q=q, rows=rows, choices=order, ans=[order.index(c) for c in ch], why=why)
def D(t, a, b, clue, ans, why):
    DUELS.append(dict(id='d%d' % (401 + len(DUELS)), d=QT[t][0], a=a, b=b, clue=clue, ans=ans, why=why, **TAG))

# ---------- Domain 1 (Q7, Q9, Q11, Q13) ----------
Q('benefits', "A web app is slow at peak hours. You add three more VMs behind the load balancer. What is this called?", "Horizontal scaling (scaling out)", ["Vertical scaling (scaling up)", "Agility", "High availability"], "Adding more instances is horizontal scaling. Adding CPU or RAM to one VM is vertical scaling.")
Q('benefits', "You resize one VM from 4 GB to 16 GB of RAM. What is this called?", "Vertical scaling (scaling up)", ["Horizontal scaling (scaling out)", "Elasticity", "Geo-distribution"], "Making one machine bigger is vertical. More machines is horizontal.")
D('benefits', "Horizontal scaling", "Vertical scaling", "Add two more virtual machines to the app.", 0, "More instances = horizontal (out). Bigger instance = vertical (up).")
Q('shared', "In PaaS, which TWO are the cloud provider's responsibility?", ["The operating system", "The physical network"], ["Your data", "User accounts and access"], "In PaaS, Microsoft runs the OS, hosts, network and datacenter. You always keep your data, accounts and access.")
Q('types', "Your developers want to build a custom app without configuring or patching servers. Which service model fits?", "PaaS", ["SaaS", "IaaS", "On-premises"], "PaaS gives you a managed platform to build on. SaaS is a finished app you just use. IaaS still leaves the OS to you.")
D('types', "PaaS", "SaaS", "We are writing our own app and do not want to manage servers.", 0, "Building your own app = PaaS. Using someone else's finished app = SaaS.")
Q('types', "Which is an IaaS offering?", "Azure Virtual Machines", ["Azure Cosmos DB", "Azure App Service", "Microsoft 365"], "VMs are IaaS: you manage the OS. Cosmos DB and App Service are PaaS. Microsoft 365 is SaaS.")
M('types', "Match each service to its model.", [("Azure Virtual Machines", "IaaS"), ("Azure Cosmos DB", "PaaS"), ("Microsoft 365", "SaaS")], "You manage the OS only in IaaS. PaaS gives you a managed platform. SaaS is a finished app.")
C('types', "IaaS, PaaS or SaaS: quick test?", "**Do you patch the OS?** IaaS (VMs, virtual networks). **Do you write the app but not run servers?** PaaS (App Service, Cosmos DB, Azure SQL Database, Functions). **Do you just use the app?** SaaS (Microsoft 365).")

# ---------- Domain 2 (Q16, Q18, Q21) ----------
Q('regions', "Each Azure region pair is made of two regions in the same what?", "Geography", ["Datacenter", "Availability zone", "Resource group"], "Pairs sit in the same geography (like US or Europe), usually at least 300 miles apart, so one disaster does not hit both.")
D('regions', "Availability zones", "Region pairs", "Protect against a disaster that takes out a whole region.", 1, "Zones are datacenters inside one region. Pairs are two regions in the same geography.")
Q('hier', "You have 30 subscriptions. You need to apply the same policies and access to all of them at once. What should you use?", "Management groups", ["Administrative units", "Resource groups", "Resource tags"], "Management groups sit above subscriptions. Administrative units are an Entra feature for delegating admin of users and groups.")
D('hier', "Management groups", "Administrative units", "Apply one policy across many subscriptions.", 0, "Management groups organize subscriptions. Administrative units scope Entra admins to a set of users or groups.")
C('hier', "Management groups vs administrative units?", "**Management groups:** Azure. Group subscriptions to apply policy and RBAC to all of them. **Administrative units:** Microsoft Entra. Let an admin manage only some users, groups or devices.")
Q('compute', "You need to run a small piece of code when a file is uploaded, with no servers to manage. What should you use?", "Azure Functions", ["Azure Container Instances", "Azure Virtual Machines", "Azure Virtual Desktop"], "Functions is serverless code: it runs on an event and bills per run. Container Instances runs a container you build.")
D('compute', "Azure Functions", "Azure Container Instances", "Run code on an event in a serverless environment.", 0, "Serverless code = Functions. A container image you want to run fast = Container Instances.")

# ---------- Domain 3 (Q36-39, Q43, Q46, Q48, Q50) ----------
Q('cost', "You need to report costs per department without moving any resources. What should you use?", "Resource tags", ["Separate subscriptions", "Resource locks", "Management groups"], "Tags add labels like Department=Finance that Cost Management can group by. Subscriptions would mean moving resources.")
D('cost', "Resource tags", "Subscriptions", "Split costs by department without changing where resources live.", 0, "Tags are labels: nothing moves. Separate subscriptions would require moving resources.")
Q('cost', "Which TWO affect the cost of an Azure resource?", ["The region it is deployed in", "Outbound data transfer"], ["The number of resource groups", "Using ARM templates to deploy it"], "Prices differ by region, and data leaving Azure is billed. Resource groups and templates are free.")
C('cost', "What changes Azure cost (and what does not)?", "**Changes cost:** resource type and size, region, usage time, outbound data, reservations and savings plans. **Free:** resource groups, tags, management groups, ARM templates, Azure Policy.")
Q('gov', "You must make sure VMs can only be created in East US. What should you use?", "Azure Policy", ["A resource lock", "Azure RBAC", "Conditional Access"], "Allowed locations is a built-in policy. Locks only stop deletes or changes to resources that already exist.")
Q('gov', "A dev team must only create VMs of approved sizes. What should you use?", "Azure Policy", ["Conditional Access", "A resource lock", "Microsoft Entra ID roles"], "Allowed VM sizes is a built-in policy. Conditional Access controls sign-ins, not what gets deployed.")
D('gov', "Azure Policy", "Resource locks", "Only allow resources in one region.", 0, "Policy decides what can be deployed. Locks protect what already exists.")
D('gov', "Azure Policy", "Conditional Access", "Limit which VM sizes can be created.", 0, "Policy controls resources. Conditional Access controls sign-ins.")
M('gov', "Match each need to the right tool.", [("Only allow VMs in one region", "Azure Policy"), ("Stop anyone deleting a database", "Resource lock"), ("Let a user manage one resource group", "Azure RBAC"), ("Require MFA when signing in from outside", "Conditional Access")], "Policy: what can be deployed. Locks: protect existing resources. RBAC: who can do what. Conditional Access: sign-in rules.")
C('gov', "Policy, lock, RBAC or Conditional Access?", "**Restrict / only allow / certain size / specific region:** Azure Policy. **Prevent delete or change:** resource lock. **Who can do what:** RBAC. **Sign-in conditions, approved apps, MFA:** Conditional Access.")
Q('mgmt', "What do you use to open Azure Cloud Shell?", "A web browser", ["Azure Resource Manager", "An ARM template", "Azure Arc"], "Cloud Shell runs in the browser, from the portal or shell.azure.com. It has Bash with Azure CLI and PowerShell.")
Q('mon', "You want to be told when there are new recommendations to cut Azure costs. Which tool?", "Azure Advisor", ["Azure Service Health", "Azure Monitor", "Log Analytics"], "Advisor makes the recommendations and can alert you when new ones appear.")
Q('mon', "You need to be notified of an outage in an Azure region you use. Which tool?", "Azure Service Health", ["Azure Monitor", "Azure Advisor", "Application Insights"], "Service Health covers Azure's own issues: outages, planned maintenance and advisories in your regions.")
Q('mon', "Where do you find planned maintenance for the Azure services you use?", "Azure Service Health", ["Log Analytics", "Azure Advisor", "Microsoft Defender for Cloud"], "Planned maintenance is an Azure-side event, so it is in Service Health. Log Analytics queries your own logs.")
D('mon', "Azure Advisor", "Azure Service Health", "New recommendations to reduce costs.", 0, "Recommendations = Advisor. Azure outages and maintenance = Service Health.")
D('mon', "Azure Service Health", "Azure Monitor", "An Azure region you use has an outage.", 0, "Azure's problem = Service Health. Your own resource metrics and alerts = Monitor.")
D('mon', "Azure Service Health", "Log Analytics", "Planned maintenance for Azure services you rely on.", 0, "Maintenance is announced in Service Health. Log Analytics only queries logs you collect.")
C('mon', "Advisor, Service Health or Monitor?", "**Advisor:** recommendations (cost, reliability, security, performance). **Service Health:** Azure's problems (outages, planned maintenance) in your regions. **Monitor:** your resources (metrics, logs, alerts like CPU over 80%).")

# ---------- self-checks, then write ----------
data = json.load(open(P, encoding='utf-8')); pk = data['packs']['az900']
for k, new in (('cards', CARDS), ('questions', QS), ('duels', DUELS)):
    base = [x for x in pk[k] if not x.get('pa4')]
    ids = {x['id'] for x in base}; assert not ids & {x['id'] for x in new}, k
    pk[k] = base + new
qt = {t for s in pk['sections'] for t in s['qtopics']}; ct = {t for s in pk['sections'] for t in s['topics']}
assert all(q['topic'] in qt for q in QS), [q['topic'] for q in QS if q['topic'] not in qt]
assert all(c['topic'] in ct for c in CARDS), [c['topic'] for c in CARDS if c['topic'] not in ct]
for d in DUELS: assert d['ans'] in (0, 1) and d['a'] != d['b']
json.dump(data, open(P, 'w', encoding='utf-8'), ensure_ascii=False)
print('az900 pa4:', len(CARDS), 'cards,', len(QS), 'questions,', len(DUELS), 'duels; totals', {k: len(pk[k]) for k in ('cards', 'questions', 'duels')})
