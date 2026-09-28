# Mini — Hotkeys & Expression Map (VTube Studio, no default-key conflicts)
| Key | Action | Layers ON (OFF) |
|---|---|---|
| F1 | Neutral | reset |
| F2 | Happy | Mouth_Smile, Blush (Mouth_Neutral) |
| F3 | Angry | Eye*_Lid_Angry, Mouth_Grit_Teeth, Mark_Anger_Vein |
| F4 | Sad | Eye*_Lid_Sad, Mouth_Sad |
| F5 | Mischievous | Lid_Angry, Mouth_Smirk, Mouth_Fang |
| Shift+F5 | Big Smile / Surprised / Crying / Sleepy / Confused (expression cycle) | see `EXPR` in mini_model.py |
| **F8** | **Shadow Fighting ON/OFF** | every `mode:fight` layer + fists (Hand_L/R off) |
| **Shift+F8** | **Shadow Rage** | fight + `mode:rage` (Fight_Aura_Pulse, Rage_Mist) + open mouth, fang |
| Ctrl+1 | Eye Glow | EyeL/R_Glow |
| Ctrl+2 | Shadow Flame | Crest_Flame_Fight, Lobe_Flame_L/R, Tail_Flame_Fight |
| Ctrl+3 | Combat Hands | Shadow_Hand_L/R(+Glow), Arm_*_Energy, Hand_*_Fist |
| Ctrl+4 | Attack pose | Arm_R_Attack, Hand_R_Palm_Attack (Arm_R_*, Hand_R off) |

Parameters: Head X/Y/Z, Body X/Y/Z, EyeOpen L/R (Socket+UpperLid deform, Closed swap), EyeBall X/Y (Iris/Core/Highlights),
MouthOpen/Form (Neutral↔Open_Inner/Tongue/Line), Breath (Chest), physics: Crest1/2, LobeTip L/R, Scarf/Tufts/Trail,
Tail1/2, Arm A/B, Wisp1/2, Param_Fight (master opacity for all fight layers).
