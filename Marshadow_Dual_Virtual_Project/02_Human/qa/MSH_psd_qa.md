# PSD QA — Marshadow_Human_Live2D_Master_v001.psd

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
| canvas size | PASS | (3072, 4608) |
| group order | PASS | ['00_GUIDE', '01_BACK_FX', '02_SHADOW_POOL', '03_BACK_HAIR', '04_HOOD_BACK', '05_BODY', '06_CLOTHES', '07_ARMS', '08_FACE', '09_EYES', '10_BROWS', '11_MOUTH', '12_FRONT_HAIR', '13_HOOD_UP', '14_SHADOW', '15_FRONT_FX', '16_EXPRESSIONS', '17_OVERDRIVE'] |
| layer count matches manifest | PASS | 166 vs 166 |
| reopened layer name/group/Z-order/blend/visibility/offset/pixels | PASS | [] |
| reopened PSD composite == Fullbody Master | PASS | mean abs diff 0.004/255, p99.9 1.0 |
| restored parts have real hidden area | PASS | [] |
| hidden-area restoration count | PASS | 40 restored parts |
| face/body sharpness parity (native-res parts, no upscale) | PASS | body/face edge crispness 1.06 |
| anti-alias edges (no white halo) | PASS | [] |

- Layers: 166  · Groups: 18  · Hidden by default: 86
- Add/Screen FX: 17  · Multiply: 4
- PSD size: 77.6 MB

## Hidden-area restoration

| Part | Restored region | Solid px | Hidden in default pose |
|---|---|---|---|
| Hair_FrontR2 | root under cap | 20761 | 60.0% |
| Hair_FrontR1 | root under cap | 15516 | 66.4% |
| Hair_FrontL2 | root under cap | 20711 | 49.4% |
| Hair_FrontL1 | root under cap | 19339 | 49.1% |
| Hair_SideR | root under front cap | 50407 | 57.1% |
| Hair_SideL | root under front cap | 48351 | 40.2% |
| EyeR_Iris | full iris circle under lids | 7348 | 25.4% |
| EyeR_Sclera | full sclera under lids/lashes | 9894 | 73.5% |
| EyeL_Iris | full iris circle under lids | 7348 | 34.0% |
| EyeL_Sclera | full sclera under lids/lashes | 9895 | 73.4% |
| Face_Base | forehead + temples under bangs | 219230 | 69.6% |
| Ear_R | ear root under side hair | 7408 | 100.0% |
| Ear_L | ear root under side hair | 7409 | 100.0% |
| HandR | palm root under cuff | 30001 | 72.9% |
| SleeveLowerR | elbow overlap under upper sleeve | 88716 | 8.1% |
| SleeveUpperR | cap continues under collar | 130101 | 7.0% |
| HandL | palm root under cuff | 29996 | 72.8% |
| SleeveLowerL | elbow overlap under upper sleeve | 88715 | 8.1% |
| SleeveUpperL | cap continues under collar | 130100 | 7.0% |
| JacketR | panel continues under collar + sleeve | 320149 | 27.2% |
| JacketL | panel continues under collar + sleeve | 320184 | 27.1% |
| InnerCollar | collar back behind neck | 25219 | 38.1% |
| Inner | full shirt behind jacket panels | 432782 | 86.5% |
| PantsR | hip overlap + upper leg under jacket/belt | 337605 | 20.2% |
| PantsL | hip overlap + upper leg under jacket/belt | 338916 | 25.0% |
| ShoeR | ankle under pants hem | 76468 | 13.2% |
| ShoeL | ankle under pants hem | 76593 | 14.7% |
| JacketBack | inside/back of jacket behind torso | 745621 | 99.7% |
| Forearm_R | forearm inside sleeve + wrist under cuff | 49130 | 100.0% |
| UpperArm_R | upper arm inside sleeve | 65540 | 100.0% |
| Shoulder_R | shoulder joint under sleeve cap | 35173 | 100.0% |
| Forearm_L | forearm inside sleeve + wrist under cuff | 49130 | 100.0% |
| UpperArm_L | upper arm inside sleeve | 65540 | 100.0% |
| Shoulder_L | shoulder joint under sleeve cap | 35186 | 100.0% |
| Torso | whole torso under jacket + arms | 483798 | 99.6% |
| Neck | neck under hair, jaw and collar | 33406 | 96.5% |
| HoodDown | full fold behind neck/hair | 134273 | 80.1% |
| Hair_BackR | root under back main | 38083 | 41.8% |
| Hair_BackL | root under back main | 36796 | 38.8% |
| Hair_BackMain | full back-of-head mass behind face / hood | 484039 | 79.2% |
