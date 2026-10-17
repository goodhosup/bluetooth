# Bluetooth Handbook — Classic · LE · LE Audio

Bluetooth Classic(BR/EDR)과 Low Energy, LE Audio, Mesh, Core 6.x의 Channel Sounding까지 다루는 한글 블루투스 핸드북입니다.
각 페이지는 **기초 → 중급 → 전문가** 순서로 깊어집니다.

- 웹 사이트: https://goodhosup.github.io/bluetooth/
- 자매 핸드북: [Cellular Handbook](https://goodhosup.github.io/cellular/) (LTE · 5G NR · 6G) · [Wi-Fi Handbook](https://goodhosup.github.io/wifi/) (IEEE 802.11)

## 로컬 실행

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python tools/build_figures.py   # 그림 생성
.venv/bin/mkdocs serve                    # http://127.0.0.1:8000
```

## 폴더 구조

| 경로 | 내용 |
|---|---|
| `mkdocs.yml` | 사이트 설정과 **전체 목차(nav)** — 페이지 추가는 여기서 시작 |
| `docs/` | 본문 마크다운 |
| `docs/assets/figures/` | 스크립트로 생성한 SVG 그림 (직접 수정하지 않음) |
| `diagrams/scripts/` | 그림 생성 스크립트 (matplotlib). 공통 색·스타일은 `style.py` |
| `includes/abbreviations.md` | 사이트 전체 약어 툴팁 (`tools/gen_abbreviations.py`가 약어 사전에서 생성) |
| `tools/bt_numbers.py` | **수치의 단일 출처** — 채널 주파수, 패킷 airtime, 처리량 계산과 본문 검산(`--check`) |
| `tools/scaffold.py` | nav에 있는데 파일이 없는 페이지를 스텁으로 생성 |
| `tools/build_figures.py` | 모든 그림 스크립트 실행 |
| `tools/gen_abbreviations.py` | `docs/reference/glossary.md` 표 → 약어 툴팁 파일 생성 |
| `tools/make_cover.py` | 위키독스 표지 이미지 생성 |
| `tools/export_wikidocs.py` | 위키독스 책 형식으로 내보내기 (`--render`로 Mermaid PNG) |
| `tools/publish_wikidocs.py` | 위키독스 API로 업로드 (`WIKIDOCS_TOKEN` 환경 변수) |
| `docs/javascripts/diagrams.mjs` | Mermaid 렌더러 (큰 다이어그램 가독성, 다크 모드, 전체 화면) |
| `docs/javascripts/calculators.js` | 레퍼런스 > 계산기 페이지 스크립트 |

## 페이지 작성 규칙

1. 맨 위에 `!!! spec "규격 · 버전"` 박스로 관련 Core Specification의 Vol/Part(확실할 때만 절 번호)와 기능이 들어온 Core 버전, 해당하면 프로파일·서비스 규격 이름과 버전을 적습니다.
2. 본문은 세 단계로 씁니다.
    - `!!! basic "한눈에 보기"` — 개념과 비유 (수식 없이)
    - 본문 `## 제목 { .l2 }` (헤딩 옆에 중급 배지) — 구조, 파라미터 표, 그림
    - `??? expert "전문가 노트 — …"` — 접히는 전문가 노트 (규격 수식, 예외 처리, 버전별 차이, 실무 팁)
3. 끝에는 해당하면 **Classic ↔ LE 비교** 표와 **관련 페이지** 링크를 붙입니다.
4. 절차는 Mermaid 시퀀스 다이어그램으로(라벨에 괄호가 있으면 따옴표로 감쌈), 채널·타이밍·패킷 그림은 `diagrams/scripts/`의 스크립트로 그립니다.
5. airtime·처리량·채널 주파수 같은 수치는 `tools/bt_numbers.py`로 계산해 넣고 `--check`로 검산합니다.
6. 아직 규격이 나오지 않은 기술(HDT, 상위 대역 확장 등)은 "논의 중"으로 쓰고 단정하지 않습니다.
7. Bluetooth SIG 규격의 그림·문장을 복사하지 않습니다. 규격은 문서 이름과 Vol/Part/절만 인용합니다.

## 배포

`main` 브랜치에 push하면 GitHub Actions(`.github/workflows/deploy.yml`)가 그림을 생성하고 사이트를 빌드해 GitHub Pages에 올립니다.
저장소의 **Settings → Pages → Source**를 `GitHub Actions`로 설정하세요.
