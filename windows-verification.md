# Windows verification for the ball-to-plate bevel

The desktop application and CLI were built from Git tree `2ec6267d0ecabb6e34f95ab13db7b76ff119e4b8`.

The released 0.45.0 application refuses to heal the bevel because its neighbour is spherical. On the original kernel the same operation returned six faces, including the plate disc inside the sphere and the spherical cap inside the plate. The volume grew from 497.418837 mm³ to 515.221195 mm³.

The repaired kernel returns one connected solid with four faces. The volume is 485.899664 mm³ and the area is 552.920307 mm². Both agree with the independently constructed sharp union. The removed bevel is a separate valid, outward-facing solid of volume 11.519173 mm³.

| Windows application input | Selectable faces after healing | Shells | Four retained face names | Saved design reopened |
|---|---:|---:|---|---|
| Native feature history | 4 | 1 | Preserved | Passed |
| Design saved in 0.45.0 | 4 | 1 | Preserved | Passed |
| Reimported STEP | 4 | 1 | Preserved | Passed |
| Rotated 90° and translated | 4 | 1 | Preserved | Passed |
| Oblique plate and translation | 4 | 1 | Preserved | Passed |

Each CLI case ran with per-step validation and checked seven points, including the former buried cap and central disc. Exporting the healed native, STEP and oblique cases to STEP and opening each in a fresh session again gave four faces, the same measurements and all seven expected point classifications.

The standalone Windows desktop also opened the released design, removed the named conical face, preserved the four remaining face names and rendered both stages on its GPU.

Two negative cases cut a 0.1 mm spherical void into the original bevel. At a center height of 0 mm the command reported that the replacement patch intersects the retained face. At 0.25 mm it reported that the patch would enclose that face. In both live sessions the measured body, all selectable faces, the point classifications and the feature history matched their pre-command values after the refusal.

`bevel-removal-inspection.sc` contains all three measured stages and opens in SolidCraft 0.45.0. The comparison image shows the original input, the old kernel result and the corrected kernel result in the same view and axial section.

[Desktop before removal](desktop-before.png) · [Desktop after removal](desktop-after.png) · [Windows command measurements](windows-command-results.json) · [Comparison with editable Delete Face feature](bevel-removal-comparison.sc)
