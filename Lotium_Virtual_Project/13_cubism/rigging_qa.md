# Rigging QA — Lotium

**이번 세션에서 Cubism Editor를 실제로 조작하지 않았습니다.** 이 컨테이너는 화면 없는 Linux이고 Cubism Editor(Windows/macOS 전용)와 데스크톱 제어 도구가 없습니다. 아래 표의 상태는 사실 그대로입니다.

범례: **DONE** = 이 저장소에 실제 파일로 완료·검증 · **SPEC** = Editor 작업용 명세 완료(미실행) · **BLOCKED** = Cubism Editor 필요

| 항목 | 상태 | 근거 / 파일 |
|---|---|---|
| PSD Import | SPEC | PSD v003 149레이어·16그룹 재오픈 검증 완료 (Import 자체는 미실행) |
| ArtMesh | SPEC | `artmesh_plan.csv` 149행, 10개 메시 프리셋 |
| Z-order | DONE (PSD) | 그룹 01(뒤)→16(앞), PSD 재오픈 검증 |
| Deformer hierarchy | SPEC | `deformer_hierarchy.md` |
| Angle X / Y / Z | SPEC | `keyform_spec.md` 수치 |
| Body X / Y / Z | SPEC | 〃 |
| Eye Blink L / R | SPEC | 〃 (독립, Smile과 2축) |
| EyeBall X / Y | SPEC | 〃 + 흰자 클리핑 |
| Brow | SPEC | 〃 |
| Mouth Open / Form / Lip Sync | SPEC + DONE | 키폼 명세 / `model3.json` LipSync 그룹=ParamMouthOpenY |
| Breath | SPEC + DONE | 키폼 명세 / idle.motion3.json |
| Hair / Cable / Pip / Ring physics | DONE (파일) | `physics3.json` 12그룹, 파라미터 ID 참조 오류 0 |
| Core Glow | SPEC + DONE | ParamCoreGlow, idle 모션 펄스 |
| Headset / UI / Game / Mobile / Low Battery / Glitch / Overclock 토글 | SPEC | `rigging_parameter_map.md` 토글 규칙 |
| 14 Expressions | DONE (파일) | `expressions/*.exp3.json` 14개, 파라미터 ID 참조 오류 0 |
| Expression Reset | DONE (설계) | 모든 표현식 Overwrite + exp_neutral |
| Hotkeys | DONE (문서) | `hotkey_map.md` (F5/F11/F12 충돌 대체키 포함) |
| Extreme Head Angles / Hidden Areas | SPEC | 안전 한계 명세, 가려진 부분은 v003에서 재작화 완료 |
| Clipping | SPEC | 눈 마스크 6개 |
| Texture Atlas | BLOCKED | 4096×2 계획만 |
| moc3 Export | BLOCKED | Cubism Editor 필요 |
| VTube Studio 로드 | BLOCKED | moc3 필요 (나머지 JSON은 준비됨) |

## 남은 WARN
- 몸 파츠 해상도(1024×1536 마스터 ×3) — 방송 크기에선 허용, 확대 시 부드러움.
- physics3.json 값은 표준 샘플 모델 범위로 잡은 초기값 — Editor 미리보기에서 미세 조정 필요.
