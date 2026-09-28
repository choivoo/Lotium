# Parts QA — PHASE 7

검증 수단: `assemble_psd.py` 검증(빈 레이어·중복 픽셀·캔버스 이탈 거부) + PSD 재오픈 검사(psd-tools) + 토글 합성 시트 `qa_toggle_preview.png` + 커버리지 갭 검사.

| 항목 | 결과 | 근거 |
|---|---|---|
| 모든 레이어가 실제 시각 파츠 | PASS | 149/149 비어있지 않음, 전부 마스터 픽셀 추출·복원·키잉 또는 팔레트 드로잉 |
| 빈 레이어 / 중복 레이어 | PASS | empty 0 / dup 0 (PSD 재오픈 검사) |
| 레이어 수 120~150 | PASS | 149 |
| Face Master와 동일 인물 | PASS | 머리 파츠 전부 LTM_FACE_MASTER 픽셀을 3점 아핀(눈2+턱)으로 배치 |
| 좌우 눈 독립 제어 | PASS | Eye_R_* / Eye_L_* 각 9레이어(흰자·홍채·동공·하이라이트·윗선·아랫선·감은선·^·눈꺼풀) |
| 입 리깅 가능 | PASS | Inside/Tongue/Teeth U·L/Line U·L + 대체 입 4종 |
| 머리카락 물리 분리 | PASS | 앞 L/C/R+가닥+ahoge, 관자놀이 2, 옆 상·하 4, 뒤 3 |
| 팔/몸 회전 시 빈 공간 없음 | PASS | 몸통·안감·팔 아래·소매 안·허리 복원 |
| 의상 뒤 몸체 복원 | PASS | hidden_area_validation.md |
| 케이블/Pip/Spirit Ring 독립 | PASS | 케이블 3마디+포트, Pip 4파츠+호버링, 링 4세그먼트 |
| 표정 토글 | PASS | qa_toggle_preview: 미소·울음·무표정·분노·반짝 |
| Overclock = 동일 캐릭터 + FX | PASS | 헤어·의상 변경 없음, 전신 오라 없음(림라이트 얇게) |
| 투명 PNG 가장자리 | PASS | 1px 내부 오버랩으로 인접 파츠 이음새 제거, 외곽 안티에일리어싱 |
| PSD Z-order | PASS | 그룹 01(뒤)→16(앞), 재오픈 시 최하단 Ring_Spirit_Seg1 / 최상단 OC_Body_Rimlight |
| Hood_Up 토글 품질 | WARN | 머리 외곽 테두리형 — 실제 후드 형태는 원화 보정 권장 |
| Hair_Headset_Press 품질 | WARN | 인페인트 채움이 약간 어두움 |
| 해상도 | WARN | 몸은 1024×1536 마스터 3배 확대(부드러움), 머리는 Face Master 기반으로 선명 |
| 마스터 대비 차이 | WARN | Spirit ring은 마스터 기준 4분할·머리 위 기울어진 링(스펙 "3분할, 머리 뒤"와 다름 → 마스터 우선) |

**종합: FAIL 0 / WARN 4 — 리깅 투입 가능(WARN 항목은 원화 보정 권장).**
