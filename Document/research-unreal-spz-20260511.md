# Research: Unreal Engine에서 SPZ 처리 경로 사전 조사

작성일: 2026-05-11
연계 문서: `design-20260511-110946.md` The Assignment 액션 1
목적: Unreal 에디터에서 실제 시도하기 전, plugin 후보 4가지의 현재 상태를 사전 조사해 결정 트리를 채운다.

---

## 핵심 결론 (1줄)

**Unreal에서 SPZ를 직접 다루는 plugin은 사실상 존재하지 않는다. 모든 경로가 "SPZ → PLY 변환 후 UE plugin으로 import"로 수렴한다.** 다만 변환 도구가 풍부해서 1일차 검증 자체는 어렵지 않다.

---

## 후보별 현재 상태 (2026-05 기준)

### 후보 1: Niantic 공식 Unreal Plugin

**결론: 존재하지 않음.**

- Niantic SDK는 여전히 Unity 우선. Unreal 지원은 커뮤니티 요청 단계.
- 공식 GitHub: `github.com/nianticlabs/spz` — 포맷 사양 + 변환 도구만 공개. Engine plugin 아님.
- Niantic Community에 "Support for unreal engine" 피처 요청 스레드 존재. 공식 응답으로 "지원 예정" 같은 명시 없음.

→ 액션 1의 후보 (1)을 **SKIP**.

### 후보 2: Luma AI Unreal Plugin

**결론: 존재함. 무료. 매우 성숙. 그러나 SPZ를 직접 import하지 않음 — PLY 또는 .luma 포맷 사용.**

- UE Marketplace(Fab)에서 무료 배포. 상업적 사용 허용.
- 드래그앤드롭으로 `.ply` 또는 `.luma` import → 자동으로 Blueprint 생성.
- 정리(크롭/컬링), 라이팅(analytical/sun lights), VFX 통합 도구 포함.
- 60fps 기준 1M Gaussian 이하 씬은 미드레인지 GPU에서 실시간 렌더 가능.
- 제약: 그림자 렌더링 미지원, 2M Gaussian 초과 시 chunking 필요(seam 발생 가능).

→ **SPZ를 PLY로 변환 후 적재하면 작동할 가능성 높음.** 1차 시도 후보.

### 후보 3: UE5 GS 커뮤니티 Plugin

**결론: 여러 개 존재. 대부분 PLY 입력. SPZ 직접 지원 명시 없음.**

발견된 plugin:
- **`mlslabs/MLSLabsGaussianSplattingRenderer-UE`** — 고성능 UE5 plugin. 3DGS + 4DGS(volumetric video) 지원. .sog 포맷 추가 지원. SPZ 명시 없음.
- **`xverse-engine/XScene-UEPlugin`** — 실시간 시각화, 관리, 편집, 하이브리드 렌더링. PLY 중심.
- **`JI20/unreal-splat`** — 표준 GS training output(.ply) 만 지원. SPZ 명시 없음.

→ Luma 외 대안. Luma가 안 되면 차순위 시도.

### 후보 4: SPZ → 변환 후 적재

**결론: 가장 확실한 경로. 변환 도구가 풍부함.**

변환 도구:

| 도구 | 형태 | 지원 형식 | 비고 |
|---|---|---|---|
| **`nianticlabs.github.io/spz`** | 브라우저 WASM | SPZ ↔ PLY, 메타데이터 검사 | **설치 불필요. 1차 시도용 최적.** |
| **`playcanvas/splat-transform`** | CLI + 라이브러리 | PLY, Compressed PLY, SOG, SPZ, SPLAT, KSPLAT, LCC → PLY, Compressed PLY, SOG, SPZ, **GLB**, CSV, HTML Viewer, LOD, Voxel | **SPZ → GLB 직접 변환 가능.** 디자인 v2의 GLB 변환 파이프라인 이슈 #1 해결 후보. |
| **`francescofugazzi/3dgsconverter`** | Python CLI | 3DGS(.ply), KSplat, SOG, SPZ, Splat, CloudCompare, Parquet, Compressed PLY 간 N-to-N | GPU 가속 필터링(SOR, Density) 포함. 가장 풍부한 옵션. |
| **`tumluliu/spz-converter`** | CLI | PLY/SPLAT → SPZ | 단방향 (역방향 아님). 비채택. |

---

## 추가 발견 (풀 시스템 단계에 영향)

### glTF 표준에 SPZ 확장 추가

2025년 후반에 `KHR_gaussian_splatting` + `KHR_gaussian_splatting_compression_spz` 두 확장이 glTF 표준에 추가됨.

→ 미래의 GLB는 SPZ를 그대로 담을 수 있게 됨.
→ 디자인 v2의 풀 시스템 단계에서 "JSON + GLB" 워크플로가 자연스럽게 SPZ도 흡수 가능.
→ vertical slice 단계에서는 아직 실용화 안 됐을 가능성 큼. 1차 검증은 변환 도구 사용.

### Cesium for Unreal의 3D Gaussian Splat Tilesets

대용량 GS 데이터셋 LOD 스트리밍 지원. 본 프로젝트(단일 씬, 단일 SPZ 파일)에는 과한 도구지만 풀 시스템 단계에서 LOD가 필요해질 때 후보.

---

## 권장 1일차 검증 절차 (액션 1 구체화)

**가장 빠르고 가벼운 검증 경로:**

```
[step 1] (10분) test.spz를 nianticlabs.github.io/spz 에 업로드
         → PLY로 변환 → test.ply 다운로드
         → 변환 성공 여부 + 메타데이터 확인 (Gaussian 개수, 파일 크기)

[step 2] (30분~1시간) Unreal Engine 5 설치 확인 + Luma AI Unreal Plugin 설치
         → UE Marketplace(Fab) 에서 "Luma AI" 검색 → 무료 설치
         → 새 프로젝트 생성 또는 빈 씬 열기

[step 3] (10분) test.ply를 Unreal 콘텐츠 브라우저에 드래그앤드롭
         → Luma plugin이 자동으로 Blueprint 생성 → 뷰포트에 배치
         → 카메라 컨트롤로 둘러보기

[step 4] (검증 판정)
         합격: 정상 렌더링 + 카메라 컨트롤 가능 → 액션 1 통과, 1주차 단계로 진입
         부분 합격: 렌더는 되나 색상/스케일/좌표계 이상 → 좌표계 변환 메모 남기고 진행
         실패: import 안 됨 또는 렌더 깨짐 → 후보 3 plugin(MLSLabs/XScene)으로 차순위 시도
```

**예상 소요 시간**: 1~2시간 (Unreal 설치 시간 제외). 디자인 문서가 "1~3일"로 잡은 것보다 훨씬 빠를 가능성 큼.

**만약 모든 plugin이 실패하면**: Approach B 회전. Unreal 트랙은 별도 분리. 단 더미 JSON은 v0.1 스키마 문서를 따라 작성.

---

## 검증 시 같이 답해야 할 부수 질문

1. **Luma plugin이 .luma 포맷을 별도로 받는가?** Luma AI 서비스를 거치지 않은 자체 SPZ→PLY 변환물이 정상 작동하는지 확인.
2. **PLY 파일 크기는 얼마나 커지는가?** SPZ가 10배 압축이라 PLY는 대략 10배 커짐. test.spz 78MB → PLY ~780MB 가능성. 1차 검증에는 무리 없으나 풀 시스템에서는 부담.
3. **변환 후 Gaussian 개수 보존되는가?** WASM 변환 도구의 정확도 확인.
4. **playcanvas/splat-transform 의 SPZ → GLB 변환 결과가 Unreal에서 import되는가?** 만약 된다면 GLB 변환 파이프라인 + Unreal SPZ 처리가 동시에 해결됨. 별도 시도 가치 있음.

---

## 디자인 v2 업데이트 권장 사항

본 조사 결과로 디자인 문서의 다음 부분 업데이트 필요:

1. **The Assignment 액션 1**: plugin 후보 순서를 (1) Luma AI → (2) MLSLabs/XScene → (3) SPZ→GLB(via splat-transform)→Luma 로 수정. Niantic 공식 후보 제거.
2. **Premise 7**: "Niantic 공식 SDK는 Unity 우선" 다음에 "공식 Unreal plugin 부재 확인됨(2026-05)" 추가.
3. **Open Questions #1**: 본 조사 결과 요약 1줄 추가.
4. **Dependencies**: SPZ → PLY 변환 도구(`nianticlabs.github.io/spz` 또는 `playcanvas/splat-transform`) 사용 명시.

---

## 참고 자료 (검증 시 직접 방문)

- Niantic SPZ: https://github.com/nianticlabs/spz
- SPZ WASM 변환기: https://nianticlabs.github.io/spz
- Luma AI Unreal Plugin (Fab): https://www.fab.com/listings/b52460e0-3ace-465e-a378-495a5531e318
- Luma AI Unreal Plugin 문서: https://lumaai.notion.site/Luma-Unreal-Engine-Plugin-0-41-8005919d93444c008982346185e933a1
- PlayCanvas splat-transform: https://github.com/playcanvas/splat-transform
- 3dgsconverter: https://github.com/francescofugazzi/3dgsconverter
- MLSLabs GS Renderer: https://github.com/mlslabs/MLSLabsGaussianSplattingRenderer-UE
- XScene UE Plugin: https://github.com/xverse-engine/XScene-UEPlugin
- unreal-splat: https://github.com/JI20/unreal-splat
- Niantic SPZ 4 발표: https://www.nianticspatial.com/blog/spz4
- Cesium for Unreal 3DGS: https://cesium.com/blog/2026/04/27/3d-gaussian-splats-lod/
