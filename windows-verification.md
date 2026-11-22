# Windows verification for the ball-to-plate bevel

The Windows CLI and desktop were built from Git tree `fc42ae996783eee526eed280f26f8afc0e7d8393` on upstream base `2da9f89fc1c2111174abab7360c838b5ab3343fc`. The locked CI-profile build finished on 22 November 2026 at 12:07:15 UTC after 35 minutes 3 seconds. Relative to the previously tested tree `307501661385453d96cda2f63fa01144b84bbd11`, one unit-test assertion now reads the documented comparison status.

| Windows artifact | SHA-256 |
|---|---|
| CLI | `b31ffc421f92f83f4a4017de9a0b85ea305575dfc3cad3657a0287bed59ca1c4` |
| Desktop | `992bc6cb9a5e80b70e4aebae276952a6b67acdc66d8244d9a895fb34ebc56752` |
| Editable comparison design | `0cede4b79ba8b5e5a0debf9781c90345993ab3acd90aee5f7d16f00ded0eadbf` |

The beveled part has five faces and a volume of 497.418837 mm³. Removing the conical face produced one closed shell with four selectable faces. Its volume of 485.899664 mm³ and area of 552.920307 mm² agree with the independently constructed sharp part.

| Input to Delete Face | Faces after healing | Original four face names preserved | Saved design reopened |
|---|---:|---|---|
| Native feature history | 4 | Yes | Passed |
| Design saved by SolidCraft 0.45.0 | 4 | Yes | Passed |
| Reimported STEP | 4 | Yes | Passed |
| Plate rotated 90° and translated | 4 | Yes | Passed |
| Oblique plate translated away from the origin | 4 | Yes | Passed |

Each case ran with per-step validation. Seven points checked the rebuilt boundary, the former buried cap and central disc, and the space left by the removed bevel. Each saved design reopened with its measurements, classifications, face names and feature history intact.

The standalone Windows desktop opened the 0.45.0 design, removed the conical face by its saved name and rendered both stages on the GPU. Exporting the healed native, STEP and oblique designs to STEP and opening them in fresh sessions reproduced the four faces, mass properties and seven point classifications.

## Clearance to a spherical void

Each model had a 0.1 mm radius void at the same position in the plate. The heights locate its center relative to the replacement plane.

| Center height | Condition | Result |
|---:|---|---|
| 0.25 mm | Void lies inside the removed material | Refused because the patch would enclose retained face 5 |
| 0 mm | Void crosses the replacement plane | Refused because the patch intersects retained face 5 |
| −0.100 mm | Void touches the replacement plane at one point | Refused because the patch intersects retained face 5 |
| −0.105 mm | Void clears the replacement plane by 0.005 mm | Accepted. The rebuilt top plane and original inner spherical boundary are both present |

In all three refusals, the same live session returned identical mass properties, selectable faces, control-point classifications and feature history before and after the command. With 0.005 mm of clearance, the original cavity face retained its name, `F4:face:5`. The repaired solid was closed and had five faces across its outer and inner shells. Its measured volume was 485.895474965 mm³ and its area was 553.045970738 mm². Saving and reopening this design reproduced the face properties, point classifications, feature history and measurements.

The posted inspection model opened from an otherwise empty directory in SolidCraft 0.45.0 and in the final build. The editable comparison file reopened with **Add the bevel** and **Remove the bevel** in its feature history. The measurement summaries, both desktop GPU captures and the comparison preview were byte-identical to the previous Windows verification.

[Tested source commit](https://github.com/tangency-labs/solidcraft/commit/c0feda913219c85205c50ef8f584db4f16e41213) · [Desktop before removal](desktop-before.png) · [Desktop after removal](desktop-after.png) · [Windows command measurements](windows-command-results.json) · [Tangent and clearance measurements](windows-contact-results.json) · [Overview of the three shapes](comparison-in-solidcraft.png) · [Comparison with editable Delete Face feature](bevel-removal-comparison.sc)
