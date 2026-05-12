# spzFirst — 작업 진행 현황

> Claude가 작업 시작 시 반드시 읽고, 진척이 있을 때마다 갱신한다. 운영 규칙은 프로젝트 루트의 `CLAUDE.md` 참조.

---

## 프로젝트 개요

- **목적**: Unity WebGL 기반 파노라마 서비스를 SPZ(3D Gaussian Splatting) 기반 인터랙티브 웹 뷰어로 전환.
- **핵심 가치**: 잃은 10억 카테고리(실시간 3D 모델 배치 + 퀄리티 일관성) 회복.
- **합격 기준 (다층화, 2026-05-11 세션 2부터)**:
  1. **첫 vertical slice (이번 1~2주)**: Unreal에서 옮긴 모델 위치가 웹에 그대로 반영된다 + JSON 스키마 v0.1 문서화.
  2. **풀 시스템 (시점 미정, PM 합의 필요)**: 회사 표준 콘텐츠 파이프라인 + myWorkTodo.md 12개 요구사항 모두 작동 + 잃은 클라이언트(또는 동급)가 시연 후 발주 의사 표현.
  3. **사용자 학습 (암묵)**: 풀 시스템 종료 시 사용자 본인이 다음 작업을 주도 가능한 수준.
- **운영 모드**: "급하지 않게 완성도 우선". 절대 데드라인 없음. (세션 2 결정)
- **콘텐츠 도구**: Unreal. (세션 2 결정, Unity 변경)
- **상세 디자인 문서**: `Document/design-20260511-110946.md` (현행) / `Document/design-20260508-164539.md` (세션 1, supersedes됨)

---

## 완료된 작업

### 2026-05-11 (세션 2)

- [x] `/office-hours` 세션 2 진행. myWorkTodo.md(사용자 요구사항 문서) 검토 + 디자인 문서 v1 대조.
- [x] **큰 결정 3건**:
  1. 시간 압박 폐기 (Premise 5 폐기), 완성도 우선.
  2. myWorkTodo.md 12개 요구사항을 풀 시스템 단계 입력값으로 격상.
  3. 콘텐츠 도구를 Unity → Unreal로 변경.
- [x] **다음 1~2주 vertical slice 결정**: Unreal → JSON → 웹 끝-에서-끝 관통 prototype.
- [x] 디자인 문서 v2 작성: `Document/design-20260511-110946.md`. 세션 1 문서 supersedes.
- [x] Spec review loop 2회 iteration: 17개 이슈 → 13개 수정 → 9/10 PASS. 디자인 문서 Status: APPROVED.
- [x] **액션 1 사전 조사 + 1차 도구 준비 완료**:
  - `Document/research-unreal-spz-20260511.md` 작성. Niantic 공식 Unreal plugin 부재 확인, 실용 경로 = "SPZ → PLY → Luma/XScene plugin 적재".
  - 디자인 문서 Premise 7, Open Questions #1, The Assignment 액션 1, Dependencies 사전 조사 결과로 업데이트.
  - 사용자가 PLY 파일 변환 완료.
  - 사용자가 UE5 + Gaussian Splatting plugin 설치 완료 (다음 세션 시 어떤 plugin인지 확인 필요).

### 2026-05-08 (세션 1)

- [x] `/office-hours` 진단 진행. 모델러 가설 검증, 시장 신호 확인(잃은 10억 + 카테고리 자진 퇴장).
- [x] 디자인 문서 작성: `Document/design-20260508-164539.md`.
- [x] **미니 스파이크 1단계** — SPZ를 웹에서 렌더링 가능한지 기술 검증 통과.
  - Three.js 0.180.0 + `@sparkjsdev/spark` + esm.sh CDN 임포트맵 조합. 빌드 도구 없이 단일 HTML.
  - test.spz (78MB) 브라우저에서 정상 렌더링 확인.
  - Three.js 인스턴스 dedup 이슈 해결 (`?deps=three@0.180.0`).
  - Niantic SPZ 좌표계 보정: X축 180° 회전(`F` 키로 토글 가능).
- [x] 1인칭 카메라 컨트롤 자체 구현.
  - yaw/pitch Euler `YXZ` 기반.
  - WASD + 화살표 이동, Q/E 상하, Shift 가속(3x).
  - 휠로 속도 조절, `[` / `]` 키로 1.5배 증감.
  - 한글 IME 영향 없게 `e.code` 사용.
- [x] 디버그 HUD 추가 (fit 상태, 속도값, 마지막 키 코드 시각화).
- [x] CLAUDE.md + todo.md 운영 체계 도입.
- [x] 세션 1 종료. 다음 세션은 사용자가 가져올 개발 요구사항 문서 검토부터 시작.

---

## 진행 중 / 다음 작업

우선순위 높은 순. 디자인 문서 v2 (`design-20260511-110946.md`) The Assignment 섹션 기반.

### 🔴 1일차 즉시 (단 하루 안)

- [x] **액션 1 사전 조사 완료** (2026-05-11). 결과: `Document/research-unreal-spz-20260511.md`.
  - Niantic 공식 Unreal plugin 부재 확인.
  - 실용 경로 = "SPZ → PLY 변환 → Luma AI Unreal Plugin(무료) 적재".
  - 디자인 문서 Premise 7, Open Questions #1, The Assignment 액션 1 업데이트 완료.
- [ ] **액션 1 실제 검증** (사용자 또는 Unreal 담당자, 1~2시간):
  - [x] **step 1: SPZ → PLY 변환** (2026-05-11 사용자 측에서 완료, PLY 파일 보유).
  - [x] **step 2: UE5 + Gaussian Splatting plugin 설치** (2026-05-11 완료).
    - 어떤 plugin을 설치했는지 다음 세션 시작 시 사용자에게 확인 필요 (Luma AI / XScene / MLSLabs 중 하나).
    - 참고: Luma plugin은 Epic Launcher 안 Fab 탭에서 받는 구조 + UE 5.4+ 호환 이슈 있음. XScene은 GitHub clone으로 Fab 우회 가능 (Apache 2.0).
  - [ ] **step 3: PLY 드래그앤드롭으로 Unreal 뷰포트 import** (다음 작업 시작점).
  - [ ] **step 4: 정상 렌더링 + 카메라 컨트롤 + 좌표계/색상 확인**.
    - 보고 항목: Gaussian 개수, PLY 파일 크기, 렌더 FPS, 색상 톤(원본 SPZ 대비), 좌표계 정합성.
    - 합격 → 1주차 단계 진입 (액션 2: JSON 스키마 합의 회의).
    - 부분 합격 → 좌표계 변환 메모 후 진행.
    - 실패 → 차순위 plugin 또는 Approach B 회전.

### 🟠 1주차

- [ ] **Unreal 측 JSON export prototype 작성**.
  - 씬 안 모델의 좌표/회전/스케일/모델 식별자를 JSON으로 export.
  - 합격: `scene00.json` + `scene00.glb` 작업 폴더에 저장.
- [ ] **JSON 스키마 v0.1 초안 1쪽짜리 마크다운**.
  - 위치: `Document/json-schema-v0.1.md`.
  - 필드 후보: `scene_id`, `models[]` (각 모델 `id`, `glb_path`, `position`, `rotation`, `scale`).
  - Unreal export 코드와 웹 측 로더 둘 다 이 문서를 계약서로 본다.

### 🟡 2주차

- [ ] **웹 측 JSON 로더 + 모델 배치 코드** (`index.html` 확장).
  - JSON fetch + 파싱 + GLB 모델 로더 + Three.js scene 배치.
  - 합격: Unreal에서 옮긴 모델 위치가 웹 새로고침 시 정확히 반영.

### 🔵 병행 (PM/영업)

- [ ] **PM에게 Unity → Unreal 변경 합의 + 모델러 Unreal 합류 가능성 공식 확인**.
- [ ] **합격 기준 다층화의 PM/스폰서 합의** (세션 1 단일 기준에서 변경됨).
- [ ] **카테고리 시장 신호 시한 확인**: 자진 퇴장 동안 다른 회사 진입 위험.
- [ ] **잃은 클라이언트 재미팅 가능성 + 카테고리 연간 발주 건수/단가 데이터** (세션 1에서 미해결).

### 🟢 2주차 종료 후

- [ ] **다음 office-hours 세션**: 풀 시스템 디자인 본격 작성.
  - myWorkTodo.md 12개 요구사항 전체 통합 설계.
  - 에디터 모드, 다국어, 씬 시스템, PC/모바일 분기, 2D 스프라이트, 클릭 인터랙션 등.
  - cross-model 리뷰(Codex 또는 Claude 서브에이전트) 권장.

---

## 미해결 / 차후 고려

- [ ] 빌드 시스템 도입 (Vite 등). 단일 HTML이 1500줄 넘어가면 관리 어려움.
- [ ] 모바일 브라우저 호환성·성능 테스트 (iOS Safari, Android Chrome).
- [ ] 풀 시스템 아키텍처 설계 (CMS, 콘텐츠 업로드 UI, 권한, 다중 사용자) — 1차 데모 합격 후 별도 `/office-hours` 권장.
- [ ] PlayCanvas 호스팅 비용·라이선스 회사 정책 적합성 확인 (Approach A 채택 시).
- [ ] 모델러의 SPZ 출력 파이프라인이 Niantic 표준 호환인지 확인.
- [ ] AR/모바일 확장 검토 (현재는 웹 브라우저만 타겟이지만 향후 가능성).

---

## 결정 이력

| 일자 | 결정 | 이유 |
|---|---|---|
| 2026-05-08 | 스파이크 단계 한정으로 PlayCanvas → Three.js + Spark | PlayCanvas의 GS 베타가 SPZ 직접 지원 안 함. Spark가 SPZ 네이티브라 더 빠른 검증 경로. 풀 시스템화 시 PlayCanvas 재검증 예정. |
| 2026-05-08 | 산출물은 `Document/` 폴더에 저장 (`~/.gstack/projects/` 사용 안 함) | 사용자 선호. 산출물이 프로젝트와 함께 살아야 함. |
| 2026-05-08 | OrbitControls → 자체 1인칭 yaw/pitch 컨트롤 | 사용자 요구: "카메라가 자기 위치에서 회전". OrbitControls는 타겟 점 주위 공전 방식이라 부적합. |
| 2026-05-08 | 사용자가 다음 세션에 개발 요구사항 문서 반입 예정 | 기존 office-hours 진단은 모델러 가설 + 시장 신호 추론 기반. 사용자 본인의 정리된 요구사항으로 검증·보강 필요. 그 문서가 차기 작업의 1차 기준이 됨. |
| 2026-05-11 | 디자인 문서 v1의 Premise 5 폐기 ("3명 팀이 풀 시스템부터 만드는 건 부적절") | 사용자가 "급하지 않게 완성도 우선" 결정. 시간을 외부 제약이 아닌 자기 자원으로 가져감. |
| 2026-05-11 | 1차 데모 = 단일 영업 URL 정의 폐기 | myWorkTodo.md 12개 요구사항이 1차 데모에 포함되어야 한다는 사용자 결정. 풀 시스템 부분집합으로 시연 가능 상태가 되면 그게 영업 자료. |
| 2026-05-11 | 콘텐츠 도구 Unity → Unreal | 사용자 결정. 모델러/팀 합의는 PM 협의로 별도 확인 필요. Unreal SPZ 호환성은 미검증 (1일차 검증 항목). |
| 2026-05-11 | 다음 1~2주 vertical slice = Unreal → JSON → 웹 끝-에서-끝 관통 | 한 슬라이스로 3개 미지수(Unreal SPZ 호환성, JSON 스키마 최소 필드, 웹 로더 설계) 동시 해소. 깨지면 Approach B로 회전. |
| 2026-05-11 | Unreal SPZ 처리 경로 = "SPZ → PLY 변환 → PLY 입력 plugin 적재" 확정 | 사전 조사 결과 Niantic 공식 Unreal SDK 부재, 모든 plugin이 PLY 중심. 변환 도구는 `nianticlabs.github.io/spz` 또는 `playcanvas/splat-transform`. |

---

## 참고 자료

- 디자인 문서: `Document/design-20260508-164539.md`
- 현재 스파이크 코드: `index.html` (프로젝트 루트)
- 테스트 SPZ 파일: `test.spz` (~78MB, gzip 압축 SPZ)
- 운영 규칙: `CLAUDE.md` (프로젝트 루트)
