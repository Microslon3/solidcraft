# Reproduce SolidCraft tangent-chain removal

The four `*-full-replay.json` command files build their parts from SolidCraft primitives in an empty document. The three STEP inputs contain the rounded geometry. Each STEP replay selects the round faces by points on the imported body, runs Delete Face with healing enabled and measures the result.

Run these commands from this directory with the SolidCraft CLI you want to test.

```console
solidcraft-cli run block-step-replay.json --in block-rounded.step --validation each_step --results --save block-healed.sc
solidcraft-cli run hemisphere-step-replay.json --in hemisphere-rounded.step --validation each_step --results --save hemisphere-healed.sc
solidcraft-cli run open-bore-step-replay.json --in open-bore-rounded.step --validation each_step --results --save open-bore-healed.sc
solidcraft-cli run ball-plate-full-replay.json --validation each_step --results --save ball-plate-healed.sc
```

| Part | Selected rounds | Expected volume (mm³) | Expected surface area (mm²) |
| --- | ---: | ---: | ---: |
| Rounded block, closed top rim | 8 | 1858.1946710585 | 935.3451151369 |
| Hemisphere, rim split at the seam | 2 | 261.7993877991 | 235.6194490192 |
| Open rim with a through hole | 5 | 1849.8274273594 | 1016.6869335978 |
| Ball on a plate | 2 | 485.8996637552 | 552.9203070318 |

SolidCraft 0.45.0 and the installed Windows release 0.46.2 each refused all eight selections across the four native designs and their STEP versions. The reports record the command errors, selected faces and unhealed controls. [0.45.0 results](release-0.45.0-results.json), [0.46.2 results and installed binary SHA-256](release-0.46.2-results.json)

The Windows build of source tree `b11669277fd6e2405f41fcde5da1ee78876b96c5` healed all eight selections. Each saved design reopened with the same retained face names, solid measurements and point classifications. Five incomplete or disconnected selections left the original design intact. Each pair of `*-rounded.png` and `*-healed.png` images shows the input and the actual operation result from the same camera. The four healed images match the corresponding sharp reference models pixel for pixel. [Windows measurements and binary SHA-256](windows-results.json)

The kernel logs cover all six reported models and a separate open chain, including comparison against independently constructed sharp solids. [Original kernel refusals](kernel-before.txt), [healed solids](kernel-after.txt), [record round trips](kernel-record-roundtrip.txt), [import and reopen checks](imported-and-reopened.txt), [turned and spherical STEP cases](turned-and-spherical-step.txt)

The local test receipt includes the command tests and both runs of the two golden corpora. [Test results](local-checks.txt)
