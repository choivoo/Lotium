# 12_rig — Lotium 웹 리그 (Galaxy Tab S6 기준)

`web/index.html` + `web/rig.json` + `web/parts/*.png`(149, 50% 해상도) — 브라우저에서 도는 Live2D 방식 리그.

- 머리 XY 패럴랙스(레이어 깊이별), 머리/몸 Z 회전, 호흡, 자동 깜빡임, 눈동자 이동(흰자 마스크)
- 립싱크: 말하기 버튼(Space) / 음성 파일 분석
- 물리: 앞·옆·뒷머리, ahoge, 드로스트링, 밑단, 소매, 스트랩, 케이블 3마디, Pip 안테나, 마이크 (스프링 진자)
- 표정 14 (F1–F12, Shift+F1/F2), 토글 14 (Ctrl+1–0 등), 방송 세트 6, 전기광 약/중/강, 전신/상반신/얼굴 프레이밍, 그린·블루백
- 카메라 얼굴 추적(MediaPipe, `face_landmarker.task` 동봉): https로 호스팅한 페이지에서만 동작. Claude 아티팩트 뷰어는 카메라를 차단.

Tab S6 최적화: 텍스처 50%, 렌더 해상도 최대 1.5x, WebGL(Pixi 7.4.2), 가로 화면 1280×800 레이아웃, 화면 꺼짐 방지(wake lock).

한계: Cubism `.moc3`가 아니므로 VTube Studio 등 Live2D 앱에는 넣을 수 없음. `.moc3`는 Cubism Editor(Windows/Mac)에서 `06_psd_parts/LTM_LIVE2D_MASTER_v001.psd`로 제작해야 함.

재생성: `08_live2d_notes/parts_assembly_manifest.json` → 이 폴더의 export 스크립트(세션 기록 참조) 또는 parts를 0.5배로 리사이즈.
