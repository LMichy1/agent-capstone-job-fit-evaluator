import json, re, sys
a = json.load(open('assessment.json', encoding='utf-8'))
cv = open('candidate_cv.md', encoding='utf-8').read().replace('\r\n', '\n')
jd = open('job_description.md', encoding='utf-8').read().replace('\r\n', '\n')
errs = []
top = {"schema_version","candidate_id","sources_inspected","sources_excluded","additional_requirements","assessments","positioning","application_brief","uncertainties"}
if set(a) - top: errs.append(f"unknown top keys {set(a)-top}")
assert a["schema_version"] == 1
for k in ("candidate_id","positioning","application_brief"):
    if not a[k].strip(): errs.append(f"empty {k}")
# headings -> sections
lines = cv.split('\n'); sections = {}; stack = {}
cur = []
heads = []
for i,l in enumerate(lines):
    m = re.match(r'^(#+)\s+(.*)$', l)
    if m: heads.append((i, len(m.group(1)), m.group(2)))
for idx,(i,lvl,t) in enumerate(heads):
    end = len(lines)
    for j,l2,_ in heads[idx+1:]:
        if l2 <= lvl: end = j; break
    sections[t] = '\n'.join(lines[i+1:end])
    # parent
    for j,l2,t2 in reversed(heads[:idx]):
        if l2 < lvl:
            sections[f"{t2} → {t}"] = sections[t]; break
ids = re.findall(r'\*\*([MP]\d+)\*\*', jd)
aids = [r["id"] for r in a["additional_requirements"]]
for r in a["additional_requirements"]:
    if set(r) != {"id","type","text","source_quote"}: errs.append(f"bad addreq keys {r}")
    if not re.fullmatch(r'A\d+', r["id"]): errs.append("bad id")
    if r["type"] not in ("mandatory","preferred"): errs.append("bad type")
    if r["source_quote"].strip() not in jd: errs.append(f"JD quote missing: {r['source_quote']}")
seen = [x["requirement_id"] for x in a["assessments"]]
if sorted(seen) != sorted(ids + aids) or len(set(seen)) != len(seen): errs.append(f"coverage {seen} vs {ids+aids}")
allowed = {"requirement_id","status","evidence_grade","evidence","rationale","uncertainty","verification_question"}
for x in a["assessments"]:
    if set(x) - allowed: errs.append(f"unknown keys {x['requirement_id']}")
    s, g, ev = x["status"], x["evidence_grade"], x["evidence"]
    if s not in ("SUPPORTED","PARTIALLY_SUPPORTED","UNSUPPORTED","UNCLEAR") or g not in "ABC": errs.append("bad enum")
    if s != "UNSUPPORTED" and not ev: errs.append(f"{x['requirement_id']} no evidence")
    if s == "UNSUPPORTED" and g != "C": errs.append("unsupported grade")
    if s == "SUPPORTED" and g == "C": errs.append("supported C")
    if s == "UNCLEAR" and not x.get("verification_question","").strip(): errs.append("unclear q")
    if not x["rationale"].strip(): errs.append("rationale")
    for e in ev:
        if set(e) != {"location","quote"}: errs.append("ev keys")
        if e["location"] not in sections: errs.append(f"bad location {e['location']!r}")
        elif e["quote"].strip() not in sections[e["location"]]: errs.append(f"quote not in section: {e['quote']!r}")
print("\n".join(errs) or "OK", ids, aids)
