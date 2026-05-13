# spzFirst — 작업 진행 현황

> Claude가 작업 시작 시 반드시 읽고, 진척이 있을 때마다 갱신한다. 운영 규칙은 프로젝트 루트의 `CLAUDE.md` 참조.

---

## 프로젝트 개요

- **목적**: Unity WebGL 기반 파노라마 서비스를 SPZ(3D Gaussian Splatting) 기반 인터랙티브 웹 뷰어로 전환.
- **핵심 가치**: 잃은 10억 카테고리(실시간 3D 모델 배치 + 퀄리티 일관성) 회복.
- **합격 기준 (다층화, 2026-05-11 세션 2부터)**:
  1. **첫 vertical slice**: Unreal에서 옮긴 모델 위치가 웹에 그대로 반영된다 + JSON 스키마 v0.1 문서화.
  2. **풀 시스템 (시점 미정, PM 합의 필요)**: 회사 표준 콘텐츠 파이프라인 + myWorkTodo.md 12개 요구사항 모두 작동 + 잃은 클라이언트(또는 동급)가 시연 후 발주 의사 표현.
  3. **사용자 학습 (암묵)**: 풀 시스템 종료 시 사용자 본인이 다음 작업을 주도 가능한 수준.
- **운영 모드**: "급하지 않게 완성도 우선". 절대 데드라인 없음. (세션 2 결정)
- **콘텐츠 도구**: Unreal. (세션 2 결정)
- **Unreal 워크플로**: 프록시(저폴리 GLB·BBox 등)로 배치 작업 + 좌표 JSON export. 실제 SPZ 시각화는 웹에서만. (세션 3 결정, Premise 7 폐기)
- **상세 디자인 문서**: `Document/design-20260513-104744.md` (**현행 v3, NanoGS 부활 + 충돌 메쉬 통합 vertical slice**). v2 `Document/design-20260511-110946.md` supersedes. v1 `Document/design-20260508-164539.md` supersedes (v2 거쳐).
- **상태 (2026-05-13 종료 시점)**: office-hours 세션 4 완료 + **1주차 Step 1 spike 끝-에서-끝 관통 통과**. 좌표계 yaw -90° 보정 확정 + 풀 시스템 변환 chain 1차 굳음. 다음 작업: JSON 스키마 v0.1 1쪽 문서화 + 모델 1개 추가 배치 + JSON export 코드.

---

## 완료된 작업

### 2026-05-13 (세션 4 — 완료)

- [x] `/office-hours` 세션 4 재개 + 완료. P1–P7 premise 동의 + Approach B 채택 + 디자인 v3 작성.
- [x] **Premise P1–P6 동의 확정 + P7 신규 추가** (충돌 메쉬 처리 1주차 슬라이스 통합).
- [x] **Phase 4 alternatives 3개 비교 후 Approach B 채택**: Unreal collision proxy 통합 export.
  - SPZ 공간용 collision mesh + 모델 BBox/collider를 Unreal에서 작성, 같은 좌표계로 export.
  - JSON 스키마 v0.1에 `collision_path` 필드 자리 마련 + 모델별 `collision_type`("bbox"/"mesh") 자리 마련.
  - 한 vertical slice에서 좌표 + 충돌 + 클릭까지 끝-에서-끝 관통.
- [x] **디자인 문서 v3 작성**: `Document/design-20260513-104744.md`. v2 supersedes.
  - narrowest wedge 확장: "Unreal 좌표 + collision proxy → 웹 위치 반영 + 1인칭 충돌 + 클릭 raycast".
  - 1주차 합격 기준 신규 추가: 1인칭 이동 시 SPZ 공간 통과하지 않음 + 모델 클릭 시 콘솔 출력.
  - 액션 4건 정리: JSON 스키마 v0.1 / NanoGS collision 가용성 검증 / Unreal export prototype / 모델러 회신용 문서 1쪽 축소.

### 2026-05-13 (세션 4 — 부분 진행, 중단)

- [x] `/office-hours` 세션 4 진행. 사용자가 새 plugin 발견 보고. 디자인 방향 재검토 시작.
- [x] **NanoGS plugin 발견 + 사용자 5단계 검증 OK**.
  - Repo: https://github.com/TimChen1383/NanoGaussianSplatting (MIT license, source 전체 공개).
  - 새 작업 폴더: `D:\Temp\plyTest_5_7\` (UE 5.7. plugin이 UE 5.6, 5.7 지원 명시).
  - 사용자 검증 단계: 시각적 정상 + 설치(level placement) + 이동/회전/스케일 + 실시간 fps 모두 OK.
- [x] **NanoGS source 코드 분석 (PLYFileReader.cpp + NanoGS.uplugin)**.
  - 결정적 차이: **속성 이름 기반 조회** (`PropertyOffsets.Find`). 이전 Luma/XV3dGS가 거부한 PLY property 순서 제약이 NanoGS에선 무관. PlayCanvas 변형 PLY도 그대로 받음.
  - 표준 INRIA spec 준수: `x,y,z,opacity,scale_0..2,rot_0..3` + `f_dc_0..2` + `f_rest_*`. SH bands 자동 감지(1/2/3 bands).
  - normal/RGB uchar 불필요 (세션 3 XV3dGS 우회 시도가 NanoGS에선 필요 없었음).
  - 좌표계 변환: COLMAP/OpenCV(Y-down) → UE(Z-up) 자동 + 100x scale (meters → cm) 가정.
  - 리스크: `IsBetaVersion: true`. 안정성 장기 모니터링 필요. MIT 라이선스 + source 공개로 자체 fork/patch 가능.
- [x] **세션 4 phase 3까지 진행: premise 6개 정리 (P1–P6)**. 사용자 동의는 다음 세션으로 미룸.
  - P1: NanoGS plugin이 길 A를 안정적으로 가능하게 한다 (5단계 검증 OK).
  - P2: 모델러 회신 대기 의미 절반 축소. 정보 수집용으로만 (모델러 SPZ 도구가 NanoGS 호환 PLY를 출력하는가).
  - P3: 길 B(메쉬 프록시) 폐기. fallback 안 둠. (옵션: BBox만 종이 문서에 fallback으로 남길지 사용자 확인 대기)
  - P4: 디자인 v3는 v2(길 A) 부활/개선 형태.
  - P5: 1주차 vertical slice = Unreal NanoGS PLY → coord JSON export → 웹 SPZ 동일 위치 표시.
  - P6: 좌표계(COLMAP/Y-down vs PlayCanvas 변형) 일치 검증은 1주차 webview 동기화 시점에 자연 검증.

### 2026-05-12 (세션 3)

- [x] `/office-hours` 세션 3 진행. Unreal에서 SPZ 직접 시각화 시도 + 실패 + 디자인 결정 변경.
- [x] **Unreal plugin 식별 + 작업 공간 정리**.
  - 작업 공간: `D:\Temp\plyTest_5_3_2\` (UE 5.3, First Person 템플릿) + `D:\Temp\plyTest_5_4_2\` (UE 5.4, C++).
  - Luma plugin 4개 변형(Baked/Dynamic × TAA/No_TAA) 의미 정리. 기본 사용 = `*_Baked`, 웹 비교 = `*_Baked_No_TAA`.
- [x] **길 A 시도 (Unreal에서 SPZ 직접 시각화) 7종 PLY 변형 모두 실패**.
  1. 원본 `test.ply` + Luma plugin → 알록달록 / 검정.
  2. PLY 헤더 검사로 **PlayCanvas 생태계(SPZ + splat-transform + SuperSplat)가 모두 비표준 property 순서**임 확인.
  3. Luma plugin → XV3dGS(=XScene by XVERSE) plugin으로 전환. UE 5.3 / 5.4 양쪽 설치 완료. 모든 PLY 변형이 `ply properties header format invalid`로 거부.
  4. `tools/ply_reorder_to_inria.py` 작성 → INRIA 표준 순서로 재정렬한 PLY (`test_inria_ordered.ply`)도 거부.
  5. plugin binary `strings`로 GSImporter.dll 안의 PLY parser 기대 spec 추출: INRIA + `nx,ny,nz` + `red,green,blue` uchar.
  6. `tools/ply_for_xv3dgs.py` 작성 → normal + RGB uchar 추가한 PLY (`test_xv3dgs.ply`, 65 properties, 716MB)도 거부.
  7. plugin source closed + docs Google Docs 권한 차단 + 샘플 PLY 없음으로 외부 spec 역공학 한계 도달.
- [x] **결정: 길 A 폐기 + Premise 7 폐기 + 길 B 채택**.
  - 신 워크플로: Unreal에서는 SPZ 직접 안 본다. 프록시로 배치, 웹에서만 SPZ 렌더링.
  - 길 B 세부(프록시 형태) 결정은 모델러 측 회신 후 다음 세션에서.
- [x] **잔존물 보존**: `Plugins/XV3dGS/`(45.8MB·UE 5.3 / 59.8MB·UE 5.4) + 5종 PLY 파일 + plugin spec 분석 결과. 미래 plugin spec 명문화 시 재시도용.

### 2026-05-11 (세션 2)

- [x] `/office-hours` 세션 2 진행. myWorkTodo.md(사용자 요구사항 문서) 검토 + 디자인 문서 v1 대조.
- [x] **큰 결정 3건**: 시간 압박 폐기 / 합격 기준 다층화 / 콘텐츠 도구 Unity → Unreal.
- [x] 디자인 문서 v2 작성: `Document/design-20260511-110946.md`. Spec review 9/10 PASS.
- [x] 사전 조사: `Document/research-unreal-spz-20260511.md`. Niantic 공식 Unreal SDK 부재, 모든 plugin이 PLY 중심임 확인.
- [x] 사용자가 PLY 파일 변환 + UE5 + Gaussian Splatting plugin 설치 완료.

### 2026-05-08 (세션 1)

- [x] `/office-hours` 진단 진행. 모델러 가설 검증, 시장 신호 확인.
- [x] 디자인 문서 작성: `Document/design-20260508-164539.md` (이후 v2에 supersedes됨).
- [x] **미니 스파이크 1단계** — SPZ를 웹에서 렌더링 가능 검증.
  - Three.js 0.180.0 + `@sparkjsdev/spark` + esm.sh CDN. 빌드 도구 없이 단일 HTML.
  - test.spz (78MB) 브라우저 정상 렌더링. Three.js 인스턴스 dedup 해결(`?deps=three@0.180.0`).
  - SPZ 좌표계 보정: X축 180° 회전(`F` 키 토글).
- [x] 1인칭 카메라 컨트롤 자체 구현 (yaw/pitch Euler YXZ, WASD + 화살표 + Shift 가속, `e.code` 사용).
- [x] 디버그 HUD 추가. CLAUDE.md + todo.md 운영 체계 도입.

---

## 진행 중 / 다음 작업

### 🟢 다음 세션 시작점 (2026-05-13 종료 시점, 다음 세션 1순위)

오늘 세션의 후속 작업. 이 순서로 진행:

1. **JSON 스키마 v0.1 1쪽 문서화** (`Document/json-schema-v0.1.md`).
   - 디자인 v3 "JSON 스키마 v0.1 (collision 포함 확장)" 섹션을 1쪽 마크다운으로 추출.
   - 좌표계 결정사항 포함: `coord_system: "ue"`, `unit: "cm"`, `space.rotation_y_deg: -90` (오늘 검증값).
   - Unreal export 코드와 웹 로더가 둘 다 이 문서를 계약서로 본다.
2. **추가 모델 1개 GLB export + JSON에 models[] 1개 추가**. 의자·상자 등 단순한 것 1개.
3. **Unreal Editor Python script로 JSON export 자동화**. 씬 내 액터 자동 순회.
4. **index.html 정리**: 디버그 로그 줄이기 + collision GLB 옵션 toggle (디버그 wireframe ON/OFF).

### 🔴 1주차 액션 4건 (디자인 v3 the assignment) — 진행 현황

- [ ] **액션 1 (0일차, 0.5일)**: JSON 스키마 v0.1 합의 회의 + `Document/json-schema-v0.1.md` 초안 작성.
  - 사용자 + Unreal 담당자 30분.
  - 디자인 v3의 "JSON 스키마 v0.1" 골자 사용. `schema_version`, `scene_id`, `coord_system`, `unit`, `space.spz_path`, `space.collision_path`, `models[]` (`id`, `type`, `glb_path`, `position`, `rotation` quaternion, `scale`, `collision_type`).
  - UTF-8 without BOM.
- [x] **액션 2 (1일차) 통과 (2026-05-13)**: collision 작업 도구 + GLB export 도구 결정.
  - 결정: **Unreal Modeling Mode + glTF Exporter plugin** (Step 1 spike 통과로 확정).
  - NanoGS auto collision 분기 폐기 (사용자 결정: "충돌 메쉬는 언리얼에서 작업해서 던저 주는 방식").
  - 검증: `samples/test_collision.glb` + `samples/scene00_collision.glb` 둘 다 Three.js 적재·시각화 OK.
- [ ] **액션 3 (1주차 1~5일)**: Unreal NanoGS 배치 + collision proxy 작성 + JSON export 코드 + scene00 묶음 저장.
  - SPZ 공간용 collision mesh (BSP brush 또는 simple low-poly) + 모델 1개 + BBox/box collider.
  - Unreal Datasmith Exporter 또는 glTF Exporter로 collision mesh를 GLB로 export.
  - JSON export: `scene00.json` (좌표·회전·스케일·collision_path 포함).
  - 합격: `D:\Temp\plyTest_5_7\Content\Output\scene00\` 또는 `D:\GitHub\Work\spzFirst\samples\scene00\`에 `scene00.json`, `scene00_space.ply`, `scene00_collision.glb`, `model_chair.glb` 저장.
- [x] **액션 4 (병행 1~3일) — 1쪽 축소 완료 (2026-05-13 세션 4)**: `Document/modeler-consult-20260512.md` 1쪽으로 축소.
  - 길 B 관련 옵션 A/B/C/D 질문 제거됨.
  - NanoGS가 받는 PLY spec(INRIA + property 자유 + normal/RGB 불필요 + 좌표계 자동 변환) 명시됨.
  - 모델러 측 SPZ 출력 도구의 PLY export 가능 여부 질문 1건만 남김.
  - **남은 사용자 액션**: 모델러 발송 + 회신 대기 (회신 안 와도 1주차 진행 가능).

### 🟠 1주차 보조

- [ ] **PLY 호환성 매트릭스 검증 (1회성)**.
  - `D:\Temp\plyTest_5_7\Content\Ply\` 5종 PLY 중 NanoGS에서 시각적·좌표 정상으로 보이는 것 표로 정리.
  - 결과를 디자인 v3 또는 별도 `Document/ply-compat-20260513.md`에 기록.
- [x] **Matic01.ply → NanoGS 시각 검증 통과 (2026-05-13)**.
  - `D:\GitHub\Work\spzFirst\Matic01.ply` (958.9MB, Postshot v1.0.110 출력, 표준 INRIA, 4.26M vertex)를 NanoGS plugin에 import.
  - **합격**. Postshot → INRIA PLY → NanoGS chain 신뢰도 확보.
- [x] **Matic01.ply → SPZ 1.x(version 3) 다운컨버트 (2026-05-13, 변환 완료)**.
  - 1차 시도 `--spz-version 3` (SH 3 bands 그대로) → **WASM Aborted**. SPZ v3가 SH 3 못 받거나 splat-transform v2.1.1 버그.
  - 2차 시도 `-H 1 --spz-version 3` (SH 1로 다운그레이드) → **성공**. 결과 `Matic01_v3.spz` (81.8MB, gzip 매직 OK).
  - **풀 시스템 변환 chain 표준 명령 확정**: `npx splat-transform <input.ply> -H 1 <output_v3.spz> --spz-version 3 -w`.
- [ ] **Matic01_v3.spz 웹 시각 검증** (사용자, 5분).
  - `index.html`에서 `Matic01.spz` → `Matic01_v3.spz`로 파일명 변경 → 새로고침.
  - 합격: 로딩 OK + 1인칭 카메라 동작 + 시각 품질 평가 (SH 1 다운그레이드 영향 무광택 실내라면 거의 차이 없음).
- [ ] **SH 3 full quality 보존 트랙 (선택, 풀 시스템 단계)**.
  - SPZ v3 + SH 3 또는 NGSP(v4) 지원 웹 라이브러리 검토. Spark 업그레이드 / 대안 라이브러리 / 자체 PLY 로더.
  - 1차 데모 합격엔 영향 없음. 풀 시스템에서 시각 품질 정밀화 필요 시 트리거.

### 🟡 2주차 (1주차 합격 후 시작)

- [ ] **웹 측 JSON 로더 + 모델 배치 + 충돌 + 클릭** (`index.html` 확장, 사용자 주체).
  - **2주차 전반(0.5주)**: JSON fetch + 파싱 + GLTFLoader + NanoGS PLY 로더 결정.
    - 결정 포인트: NanoGS 출력 PLY를 SPZ로 재변환해서 Spark에 먹일지, 웹 측에서 PLY 직접 파싱할지 (PLY → SPZ 재변환이 단순).
  - **2주차 중반(0.3주)**: collision mesh 로드 + Three.js Scene invisible material + Raycaster 설정.
  - **2주차 후반(0.2주)**: 1인칭 이동에 충돌 raycast 통합 + 모델 클릭 이벤트 (콘솔 출력만, UI는 다음 slice).
  - **2주차 합격 기준**:
    - Unreal에서 옮긴 모델 위치가 웹 새로고침 시 정확히 반영.
    - 1인칭 이동 시 SPZ 공간 통과하지 않음.
    - 모델 클릭 시 모델 ID가 콘솔에 출력.

### 🔵 병행 (PM/영업)

- [ ] **PM에게 Unity → Unreal 변경 합의 + 모델러 Unreal 합류 가능성 공식 확인** (세션 2부터 미해결).
- [ ] **합격 기준 다층화의 PM/스폰서 합의** (세션 2부터 미해결).
- [ ] **카테고리 시장 신호 시한 확인**: 자진 퇴장 동안 다른 회사 진입 위험.
- [ ] **잃은 클라이언트 재미팅 가능성 + 카테고리 연간 발주 건수/단가 데이터** (세션 1부터 미해결).

### 🟢 1차 데모 합격 후

- [ ] **다음 office-hours 세션**: 풀 시스템 디자인 본격 작성.
  - myWorkTodo.md 12개 요구사항 전체 통합 설계.
  - 에디터 모드, 다국어, 씬 시스템, PC/모바일 분기, 2D 스프라이트, 클릭 인터랙션 등.
  - cross-model 리뷰(Codex 또는 Claude 서브에이전트) 권장.

---

## 미해결 / 차후 고려

- [ ] 빌드 시스템 도입 (Vite 등). 단일 HTML이 1500줄 넘어가면 관리 어려움.
- [ ] 모바일 브라우저 호환성·성능 테스트 (iOS Safari, Android Chrome).
- [ ] 풀 시스템 아키텍처 설계 (CMS, 콘텐츠 업로드 UI, 권한, 다중 사용자) — 1차 데모 합격 후 별도 `/office-hours` 권장.
- [ ] PlayCanvas 호스팅 비용·라이선스 회사 정책 적합성 확인 (필요 시).
- [ ] 모델러의 SPZ 출력 파이프라인이 Niantic 표준 호환인지 확인.
- [ ] AR/모바일 확장 검토 (현재는 웹 브라우저만 타겟이지만 향후 가능성).
- [ ] **XV3dGS plugin 재시도 트리거**: plugin 저자가 spec 공식 문서화하거나 sample PLY를 공개하면 길 A 부활 검토. GitHub repo 모니터링 가치 있음. (현재 길 A는 NanoGS로 부활 — 이 항목은 NanoGS 실패 시 fallback 카드로 보존.)
- [ ] **NanoGS plugin 안정성 모니터링**: `IsBetaVersion: true`. 실 작업 중 크래시·렌더링 결함·빌드 깨짐 발생 시 issue 추적. MIT 라이선스 + source 공개로 직접 fix/fork 가능. fallback 두지 않기로 결정(P3)했으므로 발생 시 office-hours 세션 5 트리거.
- [ ] **NanoGS 좌표계 변환 가정 검증**: COLMAP/OpenCV(Y-down) + meters 가정. PlayCanvas 변환 PLY가 이 가정과 일치하는지 1주차 webview 동기화 시점에 자연 검증. 어긋남 발생 시 export 코드에서 보정.
- [ ] **NanoGS PLY → 웹 적재 경로 결정**: PLY → SPZ 재변환 후 Spark에 먹임(가장 단순) vs 웹에서 PLY 직접 파싱. 2주차 1일차 결정이지만, 1주차 export 단계에서 미리 도구 결정 권장.
- [ ] **collision mesh GLB export 도구 결정**: Unreal Datasmith Exporter / glTF Exporter plugin / FBX → GLB 외부 변환. 1주차 0일차 결정.

---

## 결정 이력

| 일자 | 결정 | 이유 |
|---|---|---|
| 2026-05-08 | 스파이크 단계 한정으로 PlayCanvas → Three.js + Spark | PlayCanvas의 GS 베타가 SPZ 직접 지원 안 함. Spark가 SPZ 네이티브라 더 빠른 검증 경로. 풀 시스템화 시 PlayCanvas 재검증 예정. |
| 2026-05-08 | 산출물은 `Document/` 폴더에 저장 (`~/.gstack/projects/` 사용 안 함) | 사용자 선호. 산출물이 프로젝트와 함께 살아야 함. |
| 2026-05-08 | OrbitControls → 자체 1인칭 yaw/pitch 컨트롤 | 사용자 요구: "카메라가 자기 위치에서 회전". OrbitControls는 타겟 점 주위 공전 방식이라 부적합. |
| 2026-05-08 | 사용자가 다음 세션에 개발 요구사항 문서 반입 예정 | 기존 office-hours 진단은 모델러 가설 + 시장 신호 추론 기반. 사용자 본인의 정리된 요구사항으로 검증·보강 필요. |
| 2026-05-11 | 디자인 문서 v1의 Premise 5 폐기 ("3명 팀이 풀 시스템부터 만드는 건 부적절") | 사용자가 "급하지 않게 완성도 우선" 결정. 시간을 외부 제약이 아닌 자기 자원으로 가져감. |
| 2026-05-11 | 1차 데모 = 단일 영업 URL 정의 폐기 | myWorkTodo.md 12개 요구사항이 1차 데모에 포함되어야 한다는 사용자 결정. |
| 2026-05-11 | 콘텐츠 도구 Unity → Unreal | 사용자 결정. 모델러/팀 합의는 PM 협의로 별도 확인 필요. |
| 2026-05-11 | 다음 1~2주 vertical slice = Unreal → JSON → 웹 끝-에서-끝 관통 | 한 슬라이스로 3개 미지수(Unreal SPZ 호환성, JSON 스키마 최소 필드, 웹 로더 설계) 동시 해소. |
| 2026-05-11 | Unreal SPZ 처리 경로 = "SPZ → PLY 변환 → PLY 입력 plugin 적재" 확정 | 사전 조사 결과 Niantic 공식 Unreal SDK 부재, 모든 plugin이 PLY 중심. |
| 2026-05-12 | Unreal plugin = Luma AI Unreal Plugin 확정 + 기본 사용 변형 = `*_Baked` | PLY import 산출물 prefix `Luma_test_80`로 plugin 식별. 환경 라이팅 반응 불필요. 웹 Spark 비교 시점에만 `*_Baked_No_TAA`. |
| 2026-05-12 | Unreal 엔진 버전 = 5.3 | Luma plugin UE 5.4+ 호환 이슈 회피. UE 5.4도 별도 검증했으나 동일 plugin spec 문제 확인. |
| 2026-05-12 | **Premise 7 폐기 (Unreal에서 SPZ 직접 시각화 경로)** | Luma + XV3dGS 양쪽 plugin이 PlayCanvas 계열 PLY 거부. property 순서 재정렬 + normal + RGB uchar 추가 (binary spec 분석) 후에도 거부. plugin source closed + docs 권한 차단으로 spec 역공학 한계. **세션 3에서 길 A 폐기 + 길 B(메쉬 프록시) 채택 확정.** 프록시 세부 형태는 모델러 회신 후 결정. |
| 2026-05-12 | LumaAIPlugin disabled / XV3dGS enabled 유지 | 두 plugin 모두 미작동이지만 plugin spec 재시도 시 자산 충돌 회피 + 잔존물 보존. |
| 2026-05-13 | **NanoGS plugin 발견 + 5단계 검증 OK. Premise 7 부활 가능성 매우 높음.** | github TimChen1383/NanoGaussianSplatting (MIT, source 공개). UE 5.6/5.7 지원. 사용자가 시각 정상 + 설치 + 실시간 fps 5단계 검증. source 분석상 PLY property 순서 자유 + 표준 INRIA spec 준수. 디자인 v3 정식 변경은 office-hours 세션 4 재개 후 확정 (premise P1–P6 동의 → alternatives 선택). |
| 2026-05-13 | UE 5.7 + plyTest_5_7 작업 폴더로 이관 | NanoGS plugin이 UE 5.6, 5.7 지원. 사용자가 NanoGS 검증을 UE 5.7에서 수행. 5.3·5.4 작업 공간(plyTest_5_3_2, plyTest_5_4_2)은 Luma/XV3dGS 실패 잔존물로 보존. |
| 2026-05-13 | **Premise P1–P6 동의 + P7 신규 추가 (충돌 메쉬 처리 1주차 통합)** | 세션 4 phase 3 정리한 6개 premise 모두 동의. 추가로 사용자가 "충돌 메쉬 처리도 작업에 포함" 요구. myWorkTodo.md 1인칭 이동 + 클릭 가능이 1차 데모 합격 기준에 명시되어 있어 1주차 vertical slice에 통합. fallback(P3)은 두지 않음. |
| 2026-05-13 | **Approach B 채택: Unreal collision proxy 통합 export** | 디자인 v3 alternatives 3개(A 웹 BBox / B Unreal collision proxy 통합 / C 점진적 통합) 중 B 선택. 회사 표준 워크플로(콘텐츠 제작자가 Unreal에서 모든 결정)에 부합 + JSON 스키마 v0.1이 처음부터 완전한 모습 + 한 슬라이스에서 끝-에서-끝 관통 검증. NanoGS collision 가용성은 1주차 0~1일차에 결정. |
| 2026-05-13 | **디자인 문서 v3 발효, v2 supersedes** | `Document/design-20260513-104744.md`. v3 narrowest wedge = "Unreal 좌표 + collision proxy → 웹 위치 반영 + 1인칭 충돌 + 클릭 raycast". 1주차 합격 기준 신규: 1인칭 SPZ 공간 통과 안 함 + 모델 클릭 콘솔 출력. |
| 2026-05-13 | **모델러 협의 가이드 1쪽 축소** | `Document/modeler-consult-20260512.md` 길 B 옵션 A/B/C/D 질문 제거. NanoGS PLY spec 명시 + 모델러 SPZ 도구의 PLY export 가능 여부 1건만 질문. 회신 안 와도 1주차 진행 가능 (우리 측 변환 도구로 처리). |
| 2026-05-13 | **충돌 메쉬 source = Unreal 명시 작업 단일 경로 확정** | 사용자 결정: "충돌 메쉬는 언리얼에서 작업해서 던저 주는 방식". NanoGS auto collision 분기 폐기. 콘텐츠 제작자가 Unreal에서 collision mesh 직접 작성(권장: Modeling Mode) → GLB export. 자동/수동 혼재 안 함. 풀 시스템 단계에서도 동일 방식 일관 적용. 액션 2의 의미가 "NanoGS collision 가용성 검증"에서 "Unreal collision 작업 도구 + GLB export 도구 결정"으로 변경. P7 보강. |
| 2026-05-13 | **모델러 도구 = Postshot v1.0.110 확인** | `Matic01.ply` 헤더의 `comment Postshot v1.0.110`로 정체 확인. Postshot이 **표준 INRIA Gaussian Splatting PLY를 직접 출력**(4.26M vertex, 59 properties, SH 3 bands, normal/RGB 없음) → NanoGS와 spec 100% 일치. 액션 4(모델러 회신용 정보 수집)의 큰 질문 하나가 사실상 풀림. Postshot이 출력하는 SPZ는 **SPZ 2.0(NGSP, version 4)** 포맷이고 현재 `@sparkjsdev/spark`(SPZ 1.x = version 3 가정)는 못 받음. 웹 적재용은 `splat-transform --spz-version 3`으로 다운컨버트 또는 Spark 업그레이드 검토 필요. |
| 2026-05-13 | **splat-transform 도구 검증 통과** | `npx splat-transform` (v2.1.1) 호출 OK. SPZ 1.x(version 3) ↔ SPZ 2.0(version 4, NGSP) 양방향 변환 지원. PLY/SOG/GLB/SPZ/CSV 멀티포맷. 부수 기능 `--collision-mesh` (SPZ→collision GLB 자동 생성) 존재하나 P7 결정(Unreal 명시 작업)에 따라 본 디자인 채택 안 함. 정보만 보존. |
| 2026-05-13 | **데이터 파일 전부 `samples/` 폴더로 이관** | 루트가 `.spz`/`.ply`로 어수선해져서 정리. `samples/`에 test.spz, Matic01.spz, Matic01.ply, Matic01_v3.spz, test_collision.glb 통합. `index.html`의 url path도 `samples/Matic01_v3.spz`로 갱신. 풀 시스템 단계의 콘텐츠 폴더 구조 시작점. |
| 2026-05-13 | **SPZ 좌표계 기본값 변경: X축 180° 회전 → 회전 없음 (옵션 A)** | Postshot → INRIA PLY → splat-transform chain은 Three.js 표준 Y-up으로 저장됨. 새 표준이 풀 시스템 기준이라 기본값을 회전 없음(`splat.rotation.x = 0`, `flipped = false`)으로. Niantic 원본 SPZ(test.spz 등) 적재 시 F 키 한 번. 풀 시스템 정식 해결은 JSON 스키마 v0.1의 `coord_system` 필드로 모델·씬별 메타데이터 결정. |
| 2026-05-13 | **Step 1 spike 확장: index.html에 collision GLB도 함께 적재** | 박스 보임 (렌더링·좌표계 변환 자체는 정상). 그러나 **Unreal 박스 위치 ≠ SPZ 안 의도 위치**. 디자인 v3 Open Question #2("좌표계 일치 검증은 1주차 webview 동기화 시점에 자연 검증")가 실제 부상. Spike 박스가 빈 Unreal 레벨에서 export된 것이라 SPZ 원점 무관. 본격 해결은 1주차 액션 3에서 진행: Unreal NanoGS 레벨에 SPZ 같이 적재 + SPZ 위에 의도 배치 + export. |
| 2026-05-13 | **좌표계 yaw 보정 -90° 확정** | `scene00_collision.glb` (NanoGS 레벨에서 SPZ 같이 적재 후 export) 적재 후 SPZ가 박스 대비 yaw +90° 어긋남 시각 확인. G 키 cycle 토글(0/90/180/-90)로 4 케이스 시각 비교 → **`splat.rotation.y = -Math.PI / 2` (시계방향 90°)** 정렬 통과. 원인: Postshot → splat-transform → Spark chain의 좌표계 변환이 Unreal NanoGS의 변환과 yaw 90° 차이. index.html 기본값 적용 + G 키 시작점 -90°로 굳힘. 풀 시스템 정식 해결은 JSON 스키마 v0.1의 `space.rotation_y_deg` 필드로 메타데이터화 (모델러 도구별 자동 보정). |
| 2026-05-13 | **풀 시스템 변환 chain 1차 확정** | `Postshot → INRIA PLY → splat-transform -H 0 또는 1 --spz-version 3 → SPZ v3 (gzip) → Spark → Three.js (rotation.y = -Math.PI/2 보정)`. Unreal NanoGS 측은 `INRIA PLY → NanoGS plugin → 시각 + collision proxy export`. 두 trunk가 같은 PLY 원천을 공유. 모든 단계 검증 통과 (시각·위치 정렬). 풀 시스템 자동화 시 이 chain이 콘텐츠 파이프라인의 단일 표준 변환 흐름. |

---

## 참고 자료

### 문서
- 디자인 문서 (**현행 v3, NanoGS 부활 + 충돌 통합**): `Document/design-20260513-104744.md`.
- **학습·공유용 이북 (4개 세션 의사결정 일지, 2026-05-13)**: `Document/spz-web-viewer-journey-20260513.md`.
- 디자인 문서 (세션 2, supersedes됨): `Document/design-20260511-110946.md`.
- 디자인 문서 (세션 1, supersedes됨): `Document/design-20260508-164539.md`.
- 사전 조사: `Document/research-unreal-spz-20260511.md`.
- 사용자 요구사항: `Document/myWorkTodo.md`.
- 모델러 협의 가이드 (1쪽 축소 완료): `Document/modeler-consult-20260512.md`.

### 코드 / 자산
- 웹 측 스파이크 코드: `index.html` (프로젝트 루트). 현재 적재 파일 = `samples/Matic01_v3.spz`.
- Step 1 spike 검증 페이지: `test_collision.html` (collision GLB import 테스트).
- 데이터 파일 (전부 `samples/` 폴더, 2026-05-13 정리):
  - `samples/test.spz` (78MB, gzip SPZ 1.x, 세션 1부터 검증 통과).
  - `samples/Matic01.spz` (103MB, **NGSP / SPZ 2.0**, Postshot 출력, Spark는 못 받음 보존용).
  - `samples/Matic01.ply` (959MB, Postshot 출력 표준 INRIA PLY, NanoGS 적재 검증 통과).
  - `samples/Matic01_v3.spz` (82MB, splat-transform `-H 1 --spz-version 3` 변환, Spark 적재 검증 대기).
  - `samples/test_collision.glb` (4.5KB, Unreal Modeling Mode + glTF Exporter 박스 1개 spike).
- PLY 재정렬 도구: `tools/ply_reorder_to_inria.py` (PlayCanvas → INRIA 순서, NanoGS 이후 사용 빈도 낮음).
- PLY XV3dGS 호환 도구: `tools/ply_for_xv3dgs.py` (INRIA + normal + RGB uchar, XV3dGS 폐기 후 보존용).

### Unreal 작업 공간
- **UE 5.7 (현행, 2026-05-13~)**: `D:\Temp\plyTest_5_7\` (**NanoGS plugin enabled**, 5단계 검증 OK). PLY·SPZ 파일: `D:\Temp\plyTest_5_7\Content\Ply\`.
- UE 5.3 (잔존): `D:\Temp\plyTest_5_3_2\` (LumaAIPlugin disabled + XV3dGS enabled, 모두 실패).
- UE 5.4 (잔존): `D:\Temp\plyTest_5_4_2\` (XV3dGS enabled, 실패).
- PLY·SPZ 파일 보존 (UE 5.3 시절): `D:\Temp\plyTest_5_3_2\Content\StarterContent\Ply\`.
  - `test.spz` (원본 SPZ, 81.6MB, 웹 정상 렌더링 확인됨).
  - `test.ply` (원본 PLY, 673MB, PlayCanvas 순서, 변환 도구 추정 = nianticlabs spz JS).
  - `test_inria.ply` (splat-transform 변환, 673MB, 같은 비표준 순서).
  - `test_savedas.ply` (SuperSplat Save As, 673MB, 같은 비표준 순서).
  - `test.compressed.ply` (SuperSplat Compressed, 183MB).
  - `test_inria_ordered.ply` (수동 INRIA 재정렬, 673MB).
  - `test_xv3dgs.ply` (INRIA + normal + RGB uchar, 716MB).

### Unreal plugin 참조
- **NanoGS (현행)**: https://github.com/TimChen1383/NanoGaussianSplatting (MIT, source 공개, UE 5.6/5.7 지원, BetaVersion).
- LumaAIPlugin (실패, 폐기): closed source.
- XV3dGS / XScene by XVERSE (실패, 폐기): closed source.

### 운영
- 운영 규칙: `CLAUDE.md` (프로젝트 루트).
