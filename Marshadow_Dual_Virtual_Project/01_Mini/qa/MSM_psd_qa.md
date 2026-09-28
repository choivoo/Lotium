# PSD QA — Marshadow_Mini_Live2D_Master_v001.psd

**PASS 16 / WARN 0 / FAIL 0**

| Check | Result | Detail |
|---|---|---|
| empty layers = 0 | PASS | 0 [] |
| fake transparent layers = 0 | PASS | 0 [] |
| exact duplicate layers = 0 | PASS | [] |
| unexpected canvas offsets = 0 | PASS | [] |
| wrong-size parts = 0 | PASS | [] |
| manifest missing file = 0 | PASS | [] |
| PSD reopen errors = 0 | PASS | None |
| canvas size | PASS | (3000, 3600) |
| group order | PASS | ['00_GUIDE', '01_BACK_FX', '02_LOWER_SHADOW', '03_BODY', '04_ARMS', '05_SCARF', '06_HEAD', '07_FACE', '08_EYES', '09_MARKS', '10_MOUTH', '11_FRONT_FX', '12_COMBAT'] |
| layer count matches manifest | PASS | 109 vs 109 |
| reopened layer name/group/Z-order/blend/visibility/offset/pixels | PASS | [] |
| reopened PSD composite == Fullbody Master | PASS | mean abs diff 0.007/255, p99.9 1.0 |
| restored parts have real hidden area | PASS | [] |
| hidden-area restoration count | PASS | 21 restored parts |
| face/body sharpness parity (native-res parts, no upscale) | PASS | body/face edge crispness 1.49 |
| anti-alias edges (no white halo) | PASS | [] |

- Layers: 109  · Groups: 13  · Hidden by default: 62
- Add/Screen FX: 18  · Multiply: 1
- PSD size: 62.5 MB

## Hidden-area restoration

| Part | Restored region | Solid px | Hidden in default pose |
|---|---|---|---|
| EyeR_Iris | full oval under socket clip | 25228 | 24.5% |
| EyeR_Socket | full socket under lids | 82383 | 38.4% |
| EyeL_Iris | full oval under socket clip | 25228 | 25.9% |
| EyeL_Socket | full socket under lids | 82316 | 38.5% |
| Head_Base | chin continues under scarf; crown under crest | 1314289 | 32.4% |
| Head_Lobe_R | lobe base continues under head | 148667 | 47.9% |
| Lobe_Tip_R | tip root under lobe | 19283 | 21.2% |
| Head_Lobe_L | lobe base continues under head | 148665 | 47.9% |
| Lobe_Tip_L | tip root under lobe | 19284 | 21.1% |
| Crest_Base | root hidden inside head | 93536 | 39.7% |
| Crest_Tip | curl root continues under crest base | 42551 | 42.9% |
| Scarf_Main | covers chin, full ring drawn | 198567 | 32.0% |
| Arm_R_Fore | elbow overlap; wrist continues under hand | 22369 | 26.7% |
| Arm_R_Upper | shoulder hidden under chest/scarf | 40550 | 28.7% |
| Arm_L_Fore | elbow overlap; wrist continues under hand | 22369 | 26.7% |
| Arm_L_Upper | shoulder hidden under chest/scarf | 40551 | 28.7% |
| Body_Chest | chest top under scarf | 256848 | 45.2% |
| Body_Lower | belly top under chest band | 241023 | 29.2% |
| Leg_R | leg top hidden under lower body | 112568 | 42.5% |
| Leg_L | leg top hidden under lower body | 112556 | 42.5% |
| Shadow_Tail_Tip | overlap under tail base | 8631 | 26.0% |
