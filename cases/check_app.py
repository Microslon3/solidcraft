"""Check the reported operation through the public SolidCraft app command."""
import argparse
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).parent
# References from areas of disks, circular annuli and a conical frustum.
CASES = {
    "rect": (3, 500.0, (5, 5, 20)),
    "v": (3, 500.0, (5, 5, 20)),
    "round": (3, 500.0, (5, 5, 20)),
    "frustum": (3, 1520.0 / 3.0, (6, 6, 20)),
    "bore": (4, 800.0, (7, 7, 20)),
    "shoulder": (5, 596.0, (7, 7, 20)),
    "tilted": (3, 500.0, (5, 5, 20)),
    "imported": (3, 500.0, (5, 5, 20)),
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--expect", choices=["refusal", "fixed"], required=True)
    arg = parser.parse_args()
    arg.out.mkdir(exist_ok=True, parents=True)
    summary = {}
    failed = []
    for case, (faces, volume_coefficient, maximum) in CASES.items():
        dest = arg.out / (case + ".json")
        command = [arg.cli, "run", str(ROOT / f"ui-{case}-delete.json")]
        if case == "imported":
            command.extend(["--in", str(ROOT / "grooved-shaft.step")])
        run = subprocess.run(
            [*command, "--json-out", str(dest)],
            text=True, capture_output=True, encoding="utf-8", errors="replace",
            timeout=90, cwd=ROOT,
        )
        item = {"exit": run.returncode}
        if run.stderr:
            item["stderr"] = run.stderr.strip()
        if arg.expect == "refusal":
            item["passed"] = run.returncode != 0 and "only planar neighbours" in run.stderr
        elif run.returncode == 0:
            bodies = json.loads(dest.read_text(encoding="utf-8"))["bodies"]
            if len(bodies) != 1:
                item["passed"] = False
                item["bodies"] = len(bodies)
            else:
                body = bodies[0]
                bounds = body["bbox"]
                expected_volume = volume_coefficient * math.pi
                volume = body["volume_mm3"]
                extents = list(zip(bounds["min"], bounds["max"]))
                expected = [(-maximum[0], maximum[0]), (-maximum[1], maximum[1]), (0, maximum[2])]
                if case == "tilted":
                    # Axis (0,0.6,0.8), base (31,-17,9), radius 5, axial length 20.
                    expected = [(26,36), (-21,-1), (6,28)]
                item.update(faces=body["faces"], closed=body["closed"], volume=volume,
                            expected_volume=expected_volume, extents=extents,
                            volume_difference=volume - expected_volume,
                            face_types=body["face_types"])
                item["passed"] = (
                    body["faces"] == faces
                    and body["closed"]
                    and math.isclose(volume, expected_volume, rel_tol=1e-9, abs_tol=1e-8)
                    and all(abs(a - b) <= 1e-8 for measured, ref in zip(extents, expected)
                            for a, b in zip(measured, ref))
                )
        else:
            item["passed"] = False
        summary[case] = item
        if not item["passed"]:
            failed.append(case)
        print(f"{case}: {json.dumps(item, ensure_ascii=False)}", flush=True)
    (arg.out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return int(bool(failed))

if __name__ == "__main__":
    raise SystemExit(main())
