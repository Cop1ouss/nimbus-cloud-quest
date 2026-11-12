import random
R=random.Random(900)
CARDS=[];QS=[];DUELS=[]
TOP={1:"Security concepts",2:"Identity concepts",3:"Entra ID and identities",4:"Authentication",5:"Access management",6:"Identity governance",7:"Azure infrastructure security",8:"Defender for Cloud",9:"Microsoft Sentinel",10:"Defender XDR",11:"Trust and privacy",12:"Compliance management",13:"Information protection",14:"Insider risk, eDiscovery, audit"}
DOM={1:1,2:1,3:2,4:2,5:2,6:2,7:3,8:3,9:3,10:3,11:4,12:4,13:4,14:4}
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
