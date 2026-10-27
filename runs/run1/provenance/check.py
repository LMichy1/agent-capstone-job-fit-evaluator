import json,re
d="/home/ngetich_flow/HamanLabs/agent-capstone-run1/"
cv=open(d+"candidate_cv.md",encoding="utf-8").read().replace("\r\n","\n")
j=json.load(open(d+"assessment.json",encoding="utf-8"))
# sections by heading
lines=cv.split("\n"); secs={}; stack=[]
for i,l in enumerate(lines):
    m=re.match(r"^(#+)\s+(.*)$",l)
    if m:
        lvl=len(m.group(1)); h=m.group(2)
        # section text until next heading of same or higher level
        body=[]
        for l2 in lines[i+1:]:
            m2=re.match(r"^(#+)\s",l2)
            if m2 and len(m2.group(1))<=lvl: break
            body.append(l2)
        stack=[s for s in stack if s[0]<lvl]; 
        txt="\n".join(body)
        secs[h]=txt
        if stack: secs[stack[-1][1]+" → "+h]=txt
        stack.append((lvl,h))
top=set(["schema_version","candidate_id","sources_inspected","sources_excluded","additional_requirements","assessments","positioning","application_brief","uncertainties"])
assert set(j)<=top, set(j)-top
ak={"requirement_id","status","evidence_grade","evidence","rationale","uncertainty","verification_question"}
ids=[a["requirement_id"] for a in j["assessments"]]
assert sorted(ids)==sorted(["M1","M2","M3","M4","M5","M6","P1","P2","P3","P4","P5","P6"]) and len(set(ids))==12
for a in j["assessments"]:
    assert set(a)<=ak and a["rationale"].strip()
    s,g=a["status"],a["evidence_grade"]
    if s!="UNSUPPORTED": assert a["evidence"]
    if s=="UNSUPPORTED": assert g=="C"
    if s=="SUPPORTED": assert g!="C"
    if s=="UNCLEAR": assert a.get("verification_question","").strip()
    for e in a["evidence"]:
        assert set(e)=={"location","quote"}
        assert e["location"] in secs, e["location"]
        assert e["quote"].strip() in secs[e["location"]], (a["requirement_id"],e["quote"])
print("all checks pass")
