from pathlib import Path
import argparse, json, math, subprocess

def check_disconnected(cli, source, first_script, out):
    rows = json.loads(first_script.read_text(encoding="utf-8"))["commands"]
    picks = [face for row in rows if row["command"] == "face.delete" for face in row["params"]["faces"]]
    assert len(set(picks)) == 6
    reads = [
        ("model.faces", {"body": "Turned part"}),
        ("inspect.measure", {"bodies": ["Turned part"]}),
        ("inspect.classify_points", {"body": "Turned part", "points": [[4.5, 0, 6], [4.5, 0, 14], [4.5, 0, 10]]}),
        ("model.body_features", {"body": "Turned part"}),
    ]
    steps = [*reads, ("face.delete", {"body": "Turned part", "faces": picks, "heal": True}), *reads]
    messages = [
        {"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "double-groove-check", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
    ]
    for i, (command, params) in enumerate(steps, 1):
        messages.append({"jsonrpc": "2.0", "id": i, "method": "tools/call", "params": {"name": "execute", "arguments": {"command": command, "params": params}}})
    session = subprocess.run(
        [str(cli), "mcp", "--headless", "--in", str(source)],
        input="".join(json.dumps(message) + "\n" for message in messages),
        capture_output=True, encoding="utf-8", timeout=120, check=True,
    )
    replies = {item["id"]: item["result"] for item in map(json.loads, session.stdout.splitlines())}
    assert len(replies) == len(steps) + 1
    attempted = len(reads) + 1
    refusal = replies[attempted]
    assert refusal.get("isError") is True
    rejection = refusal["content"][0]["text"]
    assert "Delete Face" in rejection, rejection
    original = {}
    for i, (command, _) in enumerate(reads, 1):
        before, after = replies[i], replies[attempted + i]
        assert not before.get("isError") and not after.get("isError"), command
        original[command] = json.loads(before["content"][0]["text"])
        assert original[command] == json.loads(after["content"][0]["text"]), command
    body = original["inspect.measure"]["bodies"][0]
    classes = [item["class"] for item in original["inspect.classify_points"]["results"]]
    assert classes == ["outside", "outside", "inside"]
    assert body["closed"] and body["faces"] == 11 and math.isclose(body["volume_mm3"], 428 * math.pi, rel_tol=1e-10)
    assert all(face["exact"] for face in original["model.faces"]["faces"])
    proof = {"picked": picks, "refusal": rejection, "unchanged_queries": list(original), "before_and_after": original}
    (out / "disconnected-same-session.json").write_text(json.dumps(proof, indent=2), encoding="utf-8")
    return {"refusal": rejection, "faces": body["faces"], "edges": body["edges"], "volume": body["volume_mm3"], "classifications": classes, "unchanged_queries": list(original)}
p=argparse.ArgumentParser()
p.add_argument("--cli",type=Path,required=True)
p.add_argument("--out",type=Path,required=True)
a=p.parse_args()
a.out.mkdir(exist_ok=True,parents=True)
root=Path(__file__).parent
summary={}
for first in (4,12):
    batch=root/f"double-groove-{first}.json"
    out=a.out/f"double-groove-{first}-result.json"
    saved=a.out/f"double-groove-{first}.sc"
    checks=[str(a.cli),"run",str(batch),"--in",str(root/"old-double-groove.sc"),"--results","--json-out",str(out),"--save",str(saved)]
    r=subprocess.run(checks,timeout=120,capture_output=True,encoding="utf-8",errors="replace")
    if r.returncode: raise RuntimeError(f"{first} {r.stderr}")
    rows=json.loads(out.read_text()); smooth=rows[-1]["faces"]
    commands=json.loads(batch.read_text())["commands"]
    seq=[reply["bodies"][0] for command,reply in zip(commands,rows,strict=True) if command["command"]=="inspect.measure"]
    assert len(seq)==2
    for result,n,k in zip(seq,[7,3],[464,500]):
        assert result["faces"]==n and result["closed"] and math.isclose(result["volume_mm3"],k*math.pi,rel_tol=1e-10),result
    shape=[(f["name"],f["index"],round(f["area"],4),round(f["centroid"][2],5)) for f in smooth]
    assert all(f["exact"] for f in smooth)
    reopened=a.out/f"double-groove-{first}-reopened.json"
    empty=a.out/"query-faces.json"
    empty.write_text(json.dumps({"commands":[{"command":"model.faces","params":{"body":"Turned part"}}]}))
    subprocess.run([str(a.cli),"run",str(empty),"--in",str(saved),"--results","--json-out",str(reopened)],timeout=120,check=True)
    again=json.loads(reopened.read_text())[0]["faces"]
    assert [(f["name"],f["index"],round(f["area"],4),round(f["centroid"][2],5)) for f in again]==shape
    assert {f["name"] for f in smooth if f.get("plane_normal") is not None}=={"F2:side:l1","F2:side:l11"}
    summary[first]={"selection_order":[first,16-first],"volumes":[s["volume_mm3"] for s in seq],"faces":[s["faces"] for s in seq],"edges":[s["edges"] for s in seq],"reopened_faces":shape}
summary["disconnected"]=check_disconnected(a.cli,root/"old-double-groove.sc",root/"double-groove-4.json",a.out)
print(json.dumps(summary,indent=2))
(a.out/"double-order-summary.json").write_text(json.dumps(summary,indent=2))

