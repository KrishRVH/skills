"""Build the voice packet page from its template.

Injects the twelve scenarios and the four model drafts the writer reworks.
The other eight drafts stay out of the page: the writer never sees them.

Usage:
  python build_packet.py OUT.html
"""

import json
import pathlib
import sys

voice = here = pathlib.Path(__file__).resolve().parent
out = pathlib.Path(sys.argv[1])
TITLES = {
    "w1": "Email to your team after a call with a supplier",
    "w2": "Chat reply: why the newsletter went out late",
    "w3": "Follow-up to all staff about an overbooked workshop",
    "w4": "Describing a change for the colleague who approves it",
    "w5": "Email turning down a request",
    "w6": "Weekly status update to your manager",
    "w7": "Chat reply: feedback on a junior colleague's draft",
    "w8": "Opening of a short opinion piece",
    "e1": "Email asking a team to review a handbook",
    "e2": "Chat reply: why the office move was pushed back",
    "e3": "Follow-up after a planning meeting",
    "e4": "Opening of a blog post",
}
scen = [json.loads(l) for l in (voice / "scenarios.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
drafts = {r["id"]: r["text"] for r in map(json.loads, (voice / "drafts.jsonl").read_text(encoding="utf-8").splitlines())}
data = {"write": [], "edit": []}
for s in scen:
    item = {"id": s["id"], "title": TITLES[s["id"]], "situation": s["situation"], "notes": s["notes"], "words": s["words"]}
    if s["part"] == "edit":
        item["draft"] = drafts[s["id"]].strip()
    data[s["part"]].append(item)
assert len(data["write"]) == 8 and len(data["edit"]) == 4
blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
tpl = (here / "packet.template.html").read_text(encoding="utf-8")
assert tpl.count("/*__DATA__*/null") == 1
out.write_text(tpl.replace("/*__DATA__*/null", blob), encoding="utf-8")
print(f"wrote {out} with {len(blob)} bytes of scenario data")
