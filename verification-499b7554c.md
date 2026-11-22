# Ring-groove deletion verification

SolidCraft commit `499b7554cfdcd5baa1f513b4c6a3f17cd704ddd2` was tested against base `df08599943d96dfadc331ad6b1e3aee43ad50fc4`. The candidate Git tree was `1b0a4f8d865539851743cb6bb202df6c0c6f0303`. Both operating systems used Rust 1.99.1. The Linux tests used cargo-nextest 0.9.150 and the project's pinned NVIDIA test data at `3fd5b9548d19aa8c12c29bc9637a96d42a06f8a5`. [Source commit](https://github.com/tangency-labs/solidcraft/pull/20541/commits/499b7554cfdcd5baa1f513b4c6a3f17cd704ddd2)

## Reproduction and geometry

On the base, selecting the floor and two walls of a 4 mm wide groove on a 10 mm diameter shaft returned `NotEnclosed`. The seven-face grooved shaft stayed in the model. On the candidate, selecting the same faces restored one cylindrical side and two end caps. The closed solid measured 1570.796326795 mm³ (500π), and the four-face ring recovered by the kernel measured 113.097335529 mm³ (36π). A separate cylinder built directly from the specified dimensions provided the reference. [Reproduction on the base](https://github.com/tangency-labs/solidcraft/issues/19624#issuecomment-7069687181)

## Linux

| Check | Result |
| --- | --- |
| SolidCore tests selected by the change | 9,440 passed across 43 binaries, 81 skipped by the test selection |
| Reference models | 149 of 149 feature-executive cases and 797 of 797 topology cases matched |
| SolidCraft application kernel | 1,052 ran, 1,047 passed, 5 failed, 8 skipped |
| Repository failure-list check on the application JUnit report | All five failures are listed by the project, zero unexpected failures |
| Static checks | Both workspaces passed Clippy with warnings denied. The SolidCore WebAssembly build, repository checks and panic-site audit passed |

The five application failures were `a_long_setback_keeps_the_g2_patch_inside_the_box`, `a_round_ending_in_an_earlier_round_matches_both_together`, `issue2422_vertical_after_separate_bottom_rounds`, `curvature_rounds_meet_at_a_g2_corner` and `the_box_corner_g2_patch_is_a_closed_solid_curvature_continuous_to_its_neighbours`. The upstream baseline job records the same five. [Upstream baseline job](https://github.com/tangency-labs/solidcraft/actions/runs/44950363113/job/136986860110)

The completed full run used `SOLIDCORE_REQUIRE_UPSTREAM=1` and the complete pinned test data. The main nextest run used the project's `ci` profile and `-p solidcraft-kernel --no-fail-fast`. The SolidCore run used the `goldens` Cargo profile with all thirteen packages selected by `xtask fast`. Repository checks ran with `cargo xtask fast --base df08599943d96dfadc331ad6b1e3aee43ad50fc4 --no-tests`. The two reference suites ran separately. [Test runner and grader output](linux-test-results.txt)

## Windows x64

`cargo build --locked --profile ci -p solidcraft -p solidcraft-cli` built the desktop application and CLI from the candidate. Their SHA-256 digests were `a3fd4c82d96efa11fd1234340f58518d6191a3cd331ef7d91928244d1e2767c6` and `eb1cbf17897d1631d8ad33c995ab175325e1624acbc0675351c3b88d5c5e4615`, respectively.

All eight `face.delete` command cases passed with that CLI. Each checked the number of faces, whether the solid was closed, its volume and its bounding box. The cases covered a rectangular groove, a round groove, a V groove, a tapered shaft, an internal bore, a step on a shaft, a tilted shaft and a STEP model read back into SolidCraft. The restored tube measured 2513.274122872 mm³ (800π) with four faces. [Machine-readable measurements](windows-command-results.json) · [Runnable cases and scripts](cases)

A design saved in 0.45.0 reopened with exact face names. Moving its retained end cap by 2 mm put it at z = 22 mm. Two grooves could be removed in either order with separate commands. Each order gave seven faces after the first command and three after the second. Selecting both disconnected grooves in a single command was refused, with the face list, measurements, point classifications and feature history unchanged. [Measurements and refusal](windows-command-results.json)

With the 44 STEP inputs read byte for byte from Git, the Windows application-kernel suite ran 1,052 tests. It passed 1,046, skipped 8 and reported the five known fillet failures plus one STEP export test. The export test compares 45 digests. All 45 matched between the base and candidate on Windows, including the four that differ from the checked-in reference. A separate import test compares its generated string to an embedded STEP file. It failed on both revisions with Git's automatic CRLF checkout and passed on both with the committed LF bytes. [Windows STEP comparison](windows-step-comparison.json)

The Windows reference runner reported differences in `single_face_fillet1019_3` and `fillet_each_fillet1019` on both the base and candidate. The same ten numerical fields had identical values in both runs. The other 147 feature-executive cases and all 797 topology cases matched the reference. This comparison was repeated with the complete pinned test data. [Windows comparison](windows-reference-comparison.txt)

## Pull request

The upstream required `ci` job passed. CodeRabbit covered the tested commit, and all seven review discussions were resolved. The upstream heavy jobs require the maintainer's `approved-for-ci` label. [Required CI](https://github.com/tangency-labs/solidcraft/actions/runs/44966861643/job/137038897897) · [CodeRabbit review](https://github.com/tangency-labs/solidcraft/pull/20541#issuecomment-7069623083)
