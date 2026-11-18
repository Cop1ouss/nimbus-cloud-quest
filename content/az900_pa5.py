# AZ-900 Practice Assessment 5 (Nov 18, 2026, 70%) plus the fresh rule-check scenarios: one item set per miss, all flagged weak (miss=True)
# so drills serve them first. Own wording, not Microsoft's. Re-running replaces the earlier pa4 items.
#   python3 content/az900_pa5.py && python3 build.py
import json, random, os
P = os.path.join(os.path.dirname(__file__), '..', 'src', 'data_packs.json')
R = random.Random(1118)
CARDS, QS, DUELS = [], [], []
QT = {'benefits': (1, 'Benefits', 'Benefits of the cloud'), 'types': (1, 'Service types', 'Service types'),
      'shared': (1, 'Shared responsibility', 'Shared responsibility'),
      'regions': (2, 'Regions and zones', 'Regions and zones'), 'hier': (2, 'Hierarchy', 'Management hierarchy'), 'compute': (2, 'Compute', 'Compute'),
      'cost': (3, 'Cost', 'Cost management'), 'gov': (3, 'Governance', 'Governance'), 'mgmt': (3, 'Management', 'Managing and deploying'), 'mon': (3, 'Monitoring', 'Monitoring'),
      'costmodel': (1, 'Cost model', 'Pricing and cost model'), 'sec': (2, 'Security', 'Identity and security'), 'id': (2, 'Identity', 'Identity and security')}
TAG = dict(miss=True, pa5=True)

def C(t, front, back):
    d, _, ct = QT[t]; CARDS.append(dict(id='c%d' % (501 + len(CARDS)), d=d, topic=ct, front=front, back=back, **TAG))
def _q(t, **k):
    d, qt, _ = QT[t]; x = dict(id='q%d' % (501 + len(QS)), d=d, topic=qt); x.update(k); x.update(TAG); QS.append(x)
def Q(t, q, right, wrong, why):
    right = [right] if isinstance(right, str) else right
    opts = right + wrong; assert len(opts) == 4 and len(set(opts)) == 4, q
    if len(right) == 2: assert 'TWO' in q, q
    R.shuffle(opts); _q(t, q=q, opts=opts, ans=sorted(opts.index(r) for r in right), why=why, kind='one' if len(right) == 1 else 'two')
def M(t, q, pairs, why):
    rows = [a for a, _ in pairs]; ch = [b for _, b in pairs]; order = ch[:]; R.shuffle(order)
    _q(t, type='match', kind='match', q=q, rows=rows, choices=order, ans=[order.index(c) for c in ch], why=why)
def D(t, a, b, clue, ans, why):
    DUELS.append(dict(id='d%d' % (501 + len(DUELS)), d=QT[t][0], a=a, b=b, clue=clue, ans=ans, why=why, **TAG))

# ---------- rule-check scenarios (fresh wording) ----------
Q('gov', "Your production database must not be deleted by anyone, even an Owner, until the safeguard is removed. What should you apply?", "A resource lock (CanNotDelete)", ["Azure Policy", "Azure RBAC", "Azure Advisor"], "A lock protects something that already exists. Policy controls what can be deployed or how it must be configured.")
Q('gov', "You must find every existing resource missing a CostCenter tag and block new ones without it. What should you use?", "Azure Policy", ["Azure Advisor", "A resource lock", "Microsoft Entra ID"], "Policy audits existing resources and can deny new ones. Advisor only gives Microsoft's recommendations; it never enforces your standards.")
Q('mgmt', "Linux servers in your datacenter and in another cloud must show in the Azure portal and get Azure Policy, without moving them. What should you use?", "Azure Arc", ["Azure Advisor", "Azure Monitor", "Azure Migrate"], "Arc brings servers outside Azure into Azure management. Migrate would move them.")
Q('mon', "An Azure outage hits a region you use. You want an email whenever that happens. Which service?", "Azure Service Health", ["Application Insights", "Azure Advisor", "Azure Arc"], "Azure's own problems in your regions = Service Health. Monitor and Application Insights watch your resources.")
Q('mon', "Microsoft will retire a feature you use and you must act first. What kind of Service Health event is this?", "Health advisory", ["Service issue", "Planned maintenance", "Security advisory"], "Health advisories: retirements and breaking changes you must act on. Service issues: outages now. Planned maintenance: Microsoft's scheduled work.")
Q('shared', "Your web app runs on App Service (PaaS). Who patches its operating system?", "Microsoft", ["You", "Both, equally", "Whoever deployed the app"], "You manage the OS only in IaaS. In PaaS and SaaS, Microsoft does.")
Q('shared', "In IaaS, PaaS and SaaS alike, which is always the customer's job?", "Your information and data", ["The operating system", "The physical network", "The physical hosts"], "Data, devices, and accounts and identities are always yours. So data is never the provider's answer in a PaaS question.")
Q('mgmt', "Your admins write Bash scripts on macOS and Linux to manage Azure. What should they use?", "Azure CLI", ["Azure PowerShell", "Azure Arc", "Azure Advisor"], "Azure CLI runs in Bash. Azure PowerShell is for PowerShell cmdlets. Match the shell the team uses.")
Q('mon', "A scale set should add a VM when CPU stays above 75% for 10 minutes. What provides the metrics and threshold?", "Azure Monitor", ["Application Insights", "Azure Advisor", "Azure Service Health"], "Monitor collects metrics like CPU and drives autoscale and alerts. Application Insights is app performance, like web app anomalies.")
Q('mon', "Which task can Azure Advisor do?", "Recommend resizing underused VMs to save money", ["Block VMs outside East US", "Stop a storage account from being deleted", "Manage on-premises servers from the portal"], "Advisor only advises. Blocking is Policy, stopping deletion is a lock, outside servers is Arc.")

# ---------- Nov 18 misses ----------
Q('costmodel', "Which TWO describe a consumption-based model?", ["No upfront costs", "You stop paying for resources you stop using"], ["You buy and manage the physical hardware", "You pay a fixed amount whether or not you use resources"], "Consumption-based: pay only for what you use, nothing up front.")
Q('benefits', "Cloud backup, data replication and geo-distribution are parts of what?", "A disaster recovery plan", ["An elastic configuration", "A governance strategy", "A consumption-based model"], "Disaster recovery keeps data and code safe if a disaster strikes. Elasticity is autoscaling with demand.")
Q('types', "Which cloud service model is usually licensed by a monthly or yearly subscription?", "SaaS", ["PaaS", "IaaS", "Private cloud"], "SaaS is a finished app sold by subscription. IaaS and PaaS are billed by consumption.")
Q('types', "In which model does the customer manage the operating system?", "IaaS", ["PaaS", "SaaS", "None of them"], "Only IaaS leaves the OS to you.")
Q('regions', "Which TWO can be deployed across availability zones?", ["Virtual machines", "Azure SQL databases"], ["Subscriptions", "Resource groups"], "Zones hold real resources like VMs, disks, load balancers and SQL databases. Subscriptions and resource groups are logical containers.")
Q('sec', "What is defense in depth?", "Several layers of protection so one failure does not expose data", ["Recommendations to improve reliability and performance", "A single strong firewall at the perimeter", "Encrypting data at rest only"], "Defense in depth = layers. 'Recommendations' describes Azure Advisor.")
Q('id', "You want users to confirm sign-in with their mobile phone in addition to a password. What should you configure?", "Multifactor authentication (MFA)", ["Microsoft Entra Verified ID", "Single sign-on (SSO)", "Microsoft Entra Domain Services"], "A second factor like a phone = MFA. Verified ID is for issuing and checking digital credentials.")
D('gov', "Resource lock", "Azure Policy", "Prevent accidental deletion of a resource.", 0, "Protect what exists = lock. Control what can be deployed = Policy.")
D('gov', "Azure Policy", "Azure Advisor", "Keep new and existing resources compliant with company standards.", 0, "Policy enforces your rules. Advisor only recommends.")
D('mgmt', "Azure Arc", "Azure Advisor", "Manage and secure on-premises servers from Azure without migrating them.", 0, "Servers outside Azure = Arc.")
D('mgmt', "Azure CLI", "Azure PowerShell", "Linux admins want to manage Azure from Bash.", 0, "Bash = CLI. PowerShell cmdlets = Azure PowerShell.")
D('mon', "Azure Monitor", "Application Insights", "Metric thresholds that trigger autoscaling.", 0, "Platform metrics and autoscale = Monitor. App performance anomalies = Application Insights.")
D('mon', "Health advisories", "Service issues", "Retirements and breaking changes you must act on.", 0, "Advisories need action before a problem. Service issues are outages now.")
D('id', "MFA", "Microsoft Entra Verified ID", "Require a phone code at sign-in.", 0, "Second factor at sign-in = MFA.")
D('types', "SaaS", "PaaS", "Licensed by a monthly or yearly subscription.", 0, "Subscription-licensed finished app = SaaS.")
C('shared', "What is ALWAYS yours, in every model?", "**Information and data, devices, accounts and identities.** You manage the **OS only in IaaS**. In PaaS and SaaS Microsoft runs the OS, hosts, network and datacenter.")
C('mon', "Service Health event types?", "**Service issues:** outages now. **Planned maintenance:** Microsoft's scheduled work. **Health advisories:** retirements and breaking changes you must act on. Also root cause analysis (RCA) reports after outages.")
C('mgmt', "Arc, CLI or PowerShell?", "**Azure Arc:** manage servers outside Azure (on-prem, other clouds). **Azure CLI:** Bash. **Azure PowerShell:** PowerShell cmdlets. Both shells run in Cloud Shell in a browser.")

# ---------- self-checks, then write ----------
data = json.load(open(P, encoding='utf-8')); pk = data['packs']['az900']
for k, new in (('cards', CARDS), ('questions', QS), ('duels', DUELS)):
    base = [x for x in pk[k] if not x.get('pa5')]
    ids = {x['id'] for x in base}; assert not ids & {x['id'] for x in new}, k
    pk[k] = base + new
qt = {t for s in pk['sections'] for t in s['qtopics']}; ct = {t for s in pk['sections'] for t in s['topics']}
assert all(q['topic'] in qt for q in QS), [q['topic'] for q in QS if q['topic'] not in qt]
assert all(c['topic'] in ct for c in CARDS), [c['topic'] for c in CARDS if c['topic'] not in ct]
for d in DUELS: assert d['ans'] in (0, 1) and d['a'] != d['b']
json.dump(data, open(P, 'w', encoding='utf-8'), ensure_ascii=False)
print('az900 pa5:', len(CARDS), 'cards,', len(QS), 'questions,', len(DUELS), 'duels; totals', {k: len(pk[k]) for k in ('cards', 'questions', 'duels')})
