# Windows verification for the ball-to-plate bevel

The Windows CLI and desktop were built from Git tree `59b86910bef91667a8b9e8dbb0de8ffc8e6065f4`, based on upstream commit `40c61c35383d697b06a026462ee1ef8a2328a4ab`.

The beveled part has five faces and a volume of 497.418837 mm³. Removing the conical face gives one closed shell with four selectable faces. Its volume of 485.899664 mm³ and area of 552.920307 mm² agree with the independent sharp part. Seven point classifications check the outer boundary and both surfaces formerly buried inside the solid.

| Input to Delete Face | Faces after healing | Original four face names preserved | Saved design reopened |
|---|---:|---|---|
| Native feature history | 4 | Yes | Passed |
| Design saved by SolidCraft 0.45.0 | 4 | Yes | Passed |
| Reimported STEP | 4 | Yes | Passed |
| Plate rotated 90° and translated | 4 | Yes | Passed |
| Oblique plate translated away from the origin | 4 | Yes | Passed |

The native and transformed designs retained `F1:bottom`, `F1:side`, `F1:top` and `F2:face:3`. In the imported STEP these same four faces retained `F3:face:2`, `F3:face:0`, `F3:face:1` and `F3:face:3`. Each case ran with per-step validation. Reopening each design reproduced its face names, feature history and measurements.

The standalone desktop removed the bevel by its saved name from the 0.45.0 design and rendered both states on the GPU. Exporting the healed native, STEP and oblique designs to STEP and opening them in fresh sessions reproduced the four faces, mass properties and seven point classifications.

Two negative cases cut a spherical void of radius 0.1 mm into the bevel. With its center on the replacement plane the command reported that the patch intersects retained face 5. With its center 0.25 mm above the plane the command reported that the patch would enclose that face. Each refusal preserved all selectable faces, mass properties, point classifications and feature history in the same live session.

The posted inspection model opened from an otherwise empty directory in both SolidCraft 0.45.0 and this build. The editable comparison file also reopened, with **Add the bevel** and **Remove the bevel** in its feature history. The five-case measurement summary, both desktop GPU captures and the comparison preview were byte-identical to the previous Windows verification.

The Windows CLI SHA-256 is `fe0ff00bba97ca9996a709baf88f961af81d416b7d8f6841523f855ce803a152`.

[Desktop before removal](desktop-before.png) · [Desktop after removal](desktop-after.png) · [Windows command measurements](windows-command-results.json) · [Comparison with editable Delete Face feature](bevel-removal-comparison.sc)
