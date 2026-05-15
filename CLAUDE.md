# CLAUDE.md — spzFirst 프로젝트 운영 규칙

이 파일은 Claude Code가 매 세션 시작 시 자동으로 읽어들이는 프로젝트 지침이다.
이 프로젝트에서 Claude는 다음 규칙을 **반드시** 따른다.

---

## 1. 세션 시작 시 (필수)

작업을 시작하기 전에 무조건 `Document/todo.md` 파일을 읽고 다음을 확인한다.

- 모든 대화는 한국어로 진행 한다
- 마지막 세션까지 완료된 작업
- 진행 중이거나 다음에 해야 할 작업
- 미해결 / 차후 고려 항목
- 결정 이력 (왜 지금 이 스택·방식으로 가고 있는지)

todo.md를 읽지 않고 작업을 진행하지 말 것. 사용자가 "그냥 시작해" 같이 말해도, 먼저 todo.md를 읽고 1~2줄로 "현재 상태: ..." 요약한 뒤 진행한다.

## 2. 작업 진행 중 (필수)

작업이 의미 있게 진척될 때마다 `Document/todo.md`를 즉시 갱신한다.

"의미 있는 진척"의 기준:
- 한 단계의 코드 변경 (기능 추가, 버그 수정, 리팩터링)
- 기술 결정의 변경 (스택 교체, 라이브러리 선택 등)
- 외부 협의 결과 반영 (PM·영업·모델러와의 결정)
- 검증 결과 (스파이크 통과/실패)

갱신 규칙:
- **완료 항목**: "완료된 작업" 섹션으로 이동, 날짜 표시.
- **새 발견 작업**: "진행 중 / 다음 작업"에 추가.
- **부수적 항목**: "미해결 / 차후 고려"에 기록.
- **결정 변경**: "결정 이력" 표에 한 줄 추가 (날짜 / 결정 / 이유).

여러 작업을 한 세션에 처리할 경우 마지막에 한꺼번에 갱신하지 말고 단계별로 갱신한다. 중간에 세션이 끊겨도 다음 세션이 정확히 이어받을 수 있도록.

## 3. 산출물 저장 위치

새 디자인 문서, 플랜, 회고, 분석 리포트 등 모든 사용자 산출물은 `Document/` 폴더에 저장한다. `~/.gstack/projects/`는 사용하지 않는다.

예외:
- `CLAUDE.md` (이 파일): 프로젝트 루트에 위치 — Claude Code 자동 로드 위치라 변경 불가.
- `index.html`, `test.spz` 등 실행 코드·자산: 프로젝트 루트.
- 내부 추적 파일 (gstack 분석 jsonl 등): `~/.gstack/`에 그대로 둠.

## 4. 프로젝트 컨텍스트 (요약)

- **프로젝트**: SPZ(3D Gaussian Splatting) 웹 뷰어. Unity WebGL 대체.
- **현재 스파이크 스택**: Three.js 0.180.0 + `@sparkjsdev/spark` + 자체 1인칭 컨트롤 + esm.sh CDN.
- **디자인 문서 권고 스택**: PlayCanvas (UI 에디터 + 게임 인터랙션). 풀 시스템화 시 재검증 예정.
- **1차 데모 합격 기준**: 잃은 10억 클라이언트 의사결정자가 데모 보고 "다시 진행해도 좋다" 표현.
- **상세 디자인**: `Document/design-20260508-164539.md`.

## 5. 코드·구현 가이드라인

- 한국어 주석을 우선한다 (사용자 한국어 작업).
- WHY가 비자명한 곳에만 주석 (`F 키 토글: 다른 SPZ 좌표계 비교용` 등). WHAT은 코드명에 맡긴다.
- em 대시(`—`) 사용 금지. 쉼표나 마침표로 대체.
- 빌드 도구 없이 단일 HTML 유지 (스파이크 단계). 1500줄 초과 시 Vite 등 도입 검토.

## 6. 사용자 작업 환경

- OS: Windows 11 / PowerShell 기본.
- 셸 명령은 PowerShell 또는 Bash(WSL/Git Bash) 둘 다 가능. 경로는 `D:\GitHub\Work\spzFirst\` 또는 `/d/GitHub/Work/spzFirst/`.
- Node.js v24, Python 3.13 사용 가능.
- 한글 IME 사용 가능성 있음. 키보드 이벤트는 항상 `e.code` (물리 키) 사용.

---

## 우선순위

규칙 1, 2가 가장 중요하다. todo.md를 읽지 않으면 컨텍스트 손실로 잘못된 결정을 내릴 위험이 크다. todo.md를 갱신하지 않으면 다음 세션이 컨텍스트를 잃는다.

세션 종료 시점에 todo.md가 현재 상태를 정확히 반영하는지 한 번 더 확인한다.

---

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool. The
skill has multi-step workflows, checklists, and quality gates that produce better
results than an ad-hoc answer. When in doubt, invoke the skill. A false positive is
cheaper than a false negative.

Key routing rules:
- Product ideas, "is this worth building", brainstorming → invoke /office-hours
- Strategy, scope, "think bigger", "what should we build" → invoke /plan-ceo-review
- Architecture, "does this design make sense" → invoke /plan-eng-review
- Design system, brand, "how should this look" → invoke /design-consultation
- Design review of a plan → invoke /plan-design-review
- Developer experience of a plan → invoke /plan-devex-review
- "Review everything", full review pipeline → invoke /autoplan
- Bugs, errors, "why is this broken", "wtf", "this doesn't work" → invoke /investigate
- Test the site, find bugs, "does this work" → invoke /qa (or /qa-only for report only)
- Code review, check the diff, "look at my changes" → invoke /review
- Visual polish, design audit, "this looks off" → invoke /design-review
- Developer experience audit, try onboarding → invoke /devex-review
- Ship, deploy, create a PR, "send it" → invoke /ship
- Merge + deploy + verify → invoke /land-and-deploy
- Configure deployment → invoke /setup-deploy
- Post-deploy monitoring → invoke /canary
- Update docs after shipping → invoke /document-release
- Weekly retro, "how'd we do" → invoke /retro
- Second opinion, codex review → invoke /codex
- Safety mode, careful mode, lock it down → invoke /careful or /guard
- Restrict edits to a directory → invoke /freeze or /unfreeze
- Upgrade gstack → invoke /gstack-upgrade
- Save progress, "save my work" → invoke /context-save
- Resume, restore, "where was I" → invoke /context-restore
- Security audit, OWASP, "is this secure" → invoke /cso
- Make a PDF, document, publication → invoke /make-pdf
- Launch real browser for QA → invoke /open-gstack-browser
- Import cookies for authenticated testing → invoke /setup-browser-cookies
- Performance regression, page speed, benchmarks → invoke /benchmark
- Review what gstack has learned → invoke /learn
- Tune question sensitivity → invoke /plan-tune
- Code quality dashboard → invoke /health
