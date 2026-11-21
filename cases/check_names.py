from pathlib import Path
import argparse, json, math, subprocess

def case(cli, root, name, commands, inp, save=None, want=True):
    script=root/f"{name}.commands.json"
    out=root/f"{name}.results.json"
    script.write_text(json.dumps({"commands":commands},indent=2),encoding="utf-8")
    cmd=[str(cli),"run",str(script),"--in",str(inp),"--results","--json-out",str(out)]
    if save: cmd.extend(["--save",str(save)])
    p=subprocess.run(cmd,capture_output=True,encoding="utf-8",errors="replace",timeout=90)
    if want:
        if p.returncode: raise RuntimeError(f"{name}: {p.stderr.strip()}")
        return json.loads(out.read_text())
    return {"exit":p.returncode,"stderr":p.stderr.strip()}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--cli",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    args.out.mkdir(exist_ok=True,parents=True)
    db=Path(__file__).parent.resolve()
    out=args.out.resolve()
    faces=json.loads((db/"old-rect-names.json").read_text())[-1]["faces"]
    by_z=sorted(faces,key=lambda f:round(f["centroid"][2],5))
    bottom,lower,back,gfloor,front,upper,top=(x["name"] for x in by_z)
    body="Turned part"
    c=lambda command,**params:{"command":command,"params":params}
    healed=out/"name-tested-cylinder.sc"
    report={}
    rows=case(args.cli,out,"heal-by-name",[c("face.delete",faces=[front,back,gfloor],body=body),c("model.faces",body=body),c("inspect.measure",bodies=[body])],db/"old-grooved-shaft.sc",healed)
    healed_faces=rows[-2]["faces"]
    ordered=[f["name"] for f in healed_faces]
    report["healed"]=dict(names=ordered,exact=[f["exact"] for f in healed_faces],volume=rows[-1]["bodies"][0]["volume_mm3"])
    assert len(healed_faces)==3 and all(f["exact"] for f in healed_faces)
    assert bottom in ordered and top in ordered
    wall=next(f["name"] for f in healed_faces if abs(f.get("cylinder",{}).get("radius",0)-5)<1e-8)
    assert math.isclose(report["healed"]["volume"],500*math.pi,rel_tol=1e-10)
    reopened=case(args.cli,out,"reopened",[c("model.faces",body=body)],healed)
    assert [f["name"] for f in reopened[-1]["faces"]]==ordered and all(f["exact"] for f in reopened[-1]["faces"])
    report["reopened_names"]=ordered
    r=5-20*math.tan(math.radians(2))
    expected=math.pi*20*(25+5*r+r*r)/3
    rows=case(args.cli,out,"draft-current-wall",[c("solid.draft",faces=[wall],angle="2 deg",neutral="XY",body=body),c("inspect.measure",bodies=[body])],healed)
    actual=rows[-1]["bodies"][0]["volume_mm3"]
    report["draft-current-wall"]=dict(name=wall,expected=expected,volume=actual)
    assert math.isclose(actual,expected,rel_tol=1e-5),report
    for end,original in (("lower",lower),("upper",upper)):
        if original==wall:
            report["old-"+end]={"name":original,"status":"primary name of merged wall"}
            continue
        response=case(args.cli,out,f"absent-old-support-{end}",[c("solid.draft",faces=[original],angle="2 deg",neutral="XY",body=body)],healed,want=False)
        assert response["exit"]!=0 and original in response["stderr"],(original,response)
        report["old-"+end]=dict(original=original,status="absorbed, fresh selection required",**response)
    rows=case(args.cli,out,"offset-retained-cap",[c("solid.offset_face",faces=[top],distance=2,body=body),c("inspect.measure",bodies=[body])],healed)
    cap=rows[-1]["bodies"][0]
    assert math.isclose(cap["volume_mm3"],550*math.pi,rel_tol=1e-8),cap
    assert abs(cap["bbox"]["max"][2]-22)<1e-8,cap
    report["cap"]={"original":top,"volume":cap["volume_mm3"],"maximum_z":cap["bbox"]["max"][2]}
    for i,removed in enumerate((back,gfloor,front)):
        response=case(args.cli,out,f"absent-groove-face-{i}",[c("solid.draft",faces=[removed],angle="2 deg",neutral="XY",body=body)],healed,want=False)
        assert response["exit"]!=0 and removed in response["stderr"],(removed,response)
        report[f"absent-{i}"]=dict(name=removed,**response)
    print(json.dumps(report,indent=2),flush=True)
    (out/"names-summary.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
if __name__=="__main__":main()
