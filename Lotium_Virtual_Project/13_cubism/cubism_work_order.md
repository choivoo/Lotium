# Cubism Work Order — PC(Windows/macOS)에서 그대로 따라 하기

입력: `06_psd_parts/LTM_LIVE2D_MASTER_v003.psd` (v001은 이중 턱 버그가 있어 사용하지 않음. 원본 PSD는 수정하지 않음)
프로젝트: `LTM_Lotium_Model_v001.cmo3` → v002 → v003 → `LTM_Lotium_Model_FINAL.cmo3`

| # | 단계 | 사용할 파일 | 완료 기준 |
|---|---|---|---|
| 1 | Cubism Editor 5 → 새 모델 → PSD 드래그 | PSD v003 | 파츠 149, 그룹 16 (psd_tree_final.md와 일치) |
| 2 | 파라미터 일괄 생성 | `parameters.csv` (66개, ID·범위 그대로) | ID 중복 0 |
| 3 | ArtMesh 자동 생성 → 프리셋별 보정 | `artmesh_plan.csv` 의 mesh_preset/mesh_recipe | face_fine·eye_fine·mouth_fine 수동 정밀화 |
| 4 | 디포머 트리 생성 | `deformer_hierarchy.md` | 이름·부모 일치 |
| 5 | 클리핑 | 홍채·동공·하이라이트 → 같은 눈 White / Core_Glow → 없음 | 마스크 6개 |
| 6 | Add 블렌드 26개 확인 | `artmesh_plan.csv` blend=Additive | 기본 상태 과노출 없음 |
| 7 | 키폼: Angle X/Y/Z → Body → 눈 → 눈썹 → 입 → 호흡 | `keyform_spec.md` 수치 | 각 극값 스크린샷 확인 |
| 8 | 토글 키폼(불투명도 0/1) | `rigging_parameter_map.md` 토글 규칙, `artmesh_plan.csv` toggle 열 | 모든 토글 ON/OFF |
| 9 | 물리 | `LTM_Lotium.physics3.json` 을 Physics 설정 창에서 Import(또는 표 값 입력) | 12그룹 |
| 10 | 텍스처 아틀라스 | 4096×4096 ×2장: 얼굴·눈·머리·입 = 1장(해상도 100%), 몸·의상·FX·UI = 1장(75%) | 여백 8px |
| 11 | moc3 Export (Cubism 5 SDK 형식) | 출력 폴더 `LTM_VTubeStudio_Export/` | `LTM_Lotium.moc3` + textures |
| 12 | 이 폴더의 model3/physics3/cdi3/exp3/motion3 를 그대로 사용 | 이미 생성됨 | VTube Studio에서 모델 로드 |
| 13 | VTS: 핫키 등록 | `hotkey_map.md` | 14 표정 + 토글 13 |
| 14 | QA | `rigging_qa.md` 체크리스트 | FAIL 0 |

주의
- 파라미터 ID는 이 폴더의 JSON과 **정확히 같아야** 합니다(physics3/exp3가 ID로 연결).
- `model3.json`의 텍스처 경로는 Export 결과 폴더명(`LTM_Lotium.4096/`)에 맞춰 수정.
- 후드(Hood_Up)는 v003에서 재작화 완료 → 보조 토글이 아닌 정식 토글로 사용 가능. `Hair_Headset_Press`는 v003에서 `Hair_Under_Headset`(재작화)로 대체되어 색 보정 불필요.
