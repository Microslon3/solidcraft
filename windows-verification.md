# Windows verification for the ball-to-plate bevel

The Windows desktop and CLI were built from Git tree `c93aa5a831370720dfe1363fb9dcf04dd88bb6c7` on upstream base `4c275ffb7dbde7a8d686b7b69e1debc1087d8f66`.

The original beveled model has five faces and a volume of 497.418837 mm³. Removing the selected bevel produced one closed shell with four selectable faces. Its volume of 485.899664 mm³ and area of 552.920307 mm² agree with the independently constructed sharp part.

| Input to Delete Face | Faces after healing | Original four face names preserved | Saved design reopened |
|---|---:|---|---|
| Native feature history | 4 | Yes | Passed |
| Design saved by SolidCraft 0.45.0 | 4 | Yes | Passed |
| Reimported STEP | 4 | Yes | Passed |
| Plate rotated 90° and translated | 4 | Yes | Passed |
| Oblique plate translated away from the origin | 4 | Yes | Passed |

All five cases ran with per-step validation. Seven point classifications verified the exposed surface, the former buried cap and disc, and the space left by the removed bevel. The same geometry, point classifications, retained face names and feature history were recovered when each saved design reopened.

The standalone Windows desktop opened the original 0.45.0 design, removed the conical face by its saved name and rendered both stages on its GPU. The healed native, STEP and oblique designs were each exported to STEP and read into a fresh application session. All three readbacks had four faces and the expected volume, area and seven point classifications.

Two negative cases put a spherical void of radius 0.1 mm inside the original bevel. At a center height of 0 mm the command reported that the patch intersects retained face 5. At 0.25 mm it reported that the patch would enclose retained face 5. Both refusals preserved the measured body, all selectable faces, control-point classifications and the existing feature history in the same live session.

The posted `bevel-removal-inspection.sc` was reopened from otherwise empty directories using both SolidCraft 0.45.0 and this candidate. All four displayed bodies matched their expected volumes and were closed. The rebuilt editable comparison also reopened with its Delete Face feature intact.

The Windows CLI SHA-256 is `a78652a7cd0ac1185d4982c7cc1b0385890f48ccdc7d24f955b61335736ab6ef`.

[Desktop before removal](desktop-before.png) · [Desktop after removal](desktop-after.png) · [Windows command measurements](windows-command-results.json) · [Comparison with editable Delete Face feature](bevel-removal-comparison.sc)
