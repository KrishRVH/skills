"""Build the voice packet page from its template.

Injects the scenarios, the four model drafts the writer reworks, and the six
pairs the writer compares. Each pair is a model draft beside the skill's
revision of it. `reads.jsonl` fixes which of the two the page shows as
version A, and the page carries the two texts without saying which is which.
The drafts for the written and rough pieces stay out of the page: the writer
never sees them.

Usage:
  python build_packet.py OUT.html
"""

import json
import pathlib
import sys

here = pathlib.Path(__file__).resolve().parent
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
    "r1": "Chat reply: is the volunteer briefing still on",
    "r2": "Email to a venue about moving a booking",
    "r3": "Status update on the annual report",
    "r4": "Email to a freelancer who was paid twice",
    "r5": "Chat handover of a press release",
    "r6": "Announcement to all staff: expense claims go online",
    "r7": "Reply to a complaint about a cancelled tour",
    "r8": "Recommendation on a stock-photo subscription",
    "e1": "Email asking a team to review a handbook",
    "e2": "Chat reply: why the office move was pushed back",
    "e3": "Follow-up after a planning meeting",
    "e4": "Opening of a blog post",
    "c1": "Email to a board about a new membership database",
    "c2": "Chat reply about a printer order",
    "c3": "Weekly update on summer program sign-ups",
    "c4": "Follow-up after the donation page was down",
    "c5": "Describing a shared-drive reorganization",
    "c6": "Opening of a blog post about volunteers",
}
WHAT = {
    "c1": "An email asking a board to approve a new membership database.",
    "c2": "A chat reply to a teammate who asked what happened with the printer order.",
    "c3": "A weekly update to a manager on sign-ups for a summer program.",
    "c4": "A follow-up to all staff after the donation page was down.",
    "c5": "A description of a shared-drive reorganization, for the colleague who approves it.",
    "c6": "The opening of a blog post for people who run volunteer programs.",
}


def rows(name):
    return [json.loads(line) for line in (here / name).read_text(encoding="utf-8").splitlines() if line.strip()]


drafts = {r["id"]: r["text"].strip() for r in rows("drafts.jsonl")}
reads = {r["id"]: r for r in rows("reads.jsonl")}
data = {"write": [], "rough": [], "edit": [], "read": []}
for s in rows("scenarios.jsonl"):
    item = {"id": s["id"], "title": TITLES[s["id"]]}
    if s["part"] == "read":
        pair = {"draft": drafts[s["id"]], "revised": reads[s["id"]]["revised"].strip()}
        first = reads[s["id"]]["a"]
        second = "revised" if first == "draft" else "draft"
        assert pair[first] != pair[second], s["id"]
        item.update(what=WHAT[s["id"]], a=pair[first], b=pair[second])
    else:
        item.update(situation=s["situation"], notes=s["notes"], words=s["words"])
        if s["part"] == "edit":
            item["draft"] = drafts[s["id"]]
    data[s["part"]].append(item)
assert [len(data[p]) for p in ("write", "rough", "edit", "read")] == [8, 8, 4, 6]
assert sorted(r["a"] for r in reads.values()) == ["draft"] * 3 + ["revised"] * 3
blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
tpl = (here / "packet.template.html").read_text(encoding="utf-8")
assert tpl.count("/*__DATA__*/null") == 1
out.write_text(tpl.replace("/*__DATA__*/null", blob), encoding="utf-8")
print(f"wrote {out} with {len(blob)} bytes of scenario data")
