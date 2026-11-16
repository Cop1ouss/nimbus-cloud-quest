import random
R=random.Random(500)
CARDS=[];QS=[];DUELS=[]
TOP={1:"Entra access",2:"Key Vault",3:"Governance and compliance",4:"Storage security",5:"Database security",6:"Network security",7:"Security for AI",8:"Servers and VMs",9:"App platform security",10:"Defender for Cloud posture",11:"Microsoft Sentinel",12:"Security Copilot"}
DOM={1:1,2:1,3:1,4:2,5:2,6:2,7:3,8:3,9:3,10:4,11:4,12:4}
def C(s,front,back):
    CARDS.append(dict(id='c%03d'%(len(CARDS)+1),d=DOM[s],topic=TOP[s],front=front,back=back,miss=False))
def _q(s,**k):
    d=dict(id='q%03d'%(len(QS)+1),d=DOM[s],topic=TOP[s]);d.update(k);d['miss']=False;QS.append(d)
def Q(s,q,right,wrong,why):
    if isinstance(right,str):right=[right]
    opts=right+wrong;assert len(opts)==4 and len(set(opts))==4,q
    R.shuffle(opts)
    if len(right)==2:assert 'TWO' in q,q
    _q(s,q=q,opts=opts,ans=sorted(opts.index(r) for r in right),why=why,kind='one' if len(right)==1 else 'two')
def YN(s,stmts,ans,why):
    assert len(stmts)==len(ans)==3
    _q(s,type='yn',kind='yn',q='For each statement, select Yes if it is true. Otherwise, select No.',stmts=stmts,ans=ans,why=why)
def M(s,q,pairs,why):
    rows=[p[0] for p in pairs];ch=[p[1] for p in pairs];order=ch[:];R.shuffle(order)
    _q(s,type='match',kind='match',q=q,rows=rows,choices=order,ans=[order.index(c) for c in ch],why=why)
def D(s,a,b,clue,ans,why):
    assert ans in (0,1)
    DUELS.append(dict(id='d%03d'%(len(DUELS)+1),d=DOM[s],a=a,b=b,clue=clue,ans=ans,why=why,miss=False))
