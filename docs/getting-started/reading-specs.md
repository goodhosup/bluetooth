# 규격 문서 읽는 법

!!! spec "규격 · 버전"
    Bluetooth Core Specification v6.x — Vol 0 (목차·Core 구성), Vol 1 Part A (Architecture), Part C (Change History) · Assigned Numbers · Core Specification Supplement(CSS)
    3,000쪽이 넘는 단일 문서. 버전마다 통째로 다시 나오며, 예전에는 정오표(ESR)·부록(CSA)이 따로 나왔음

!!! basic "한눈에 보기"
    Core Specification은 한 권짜리 거대한 문서지만 구조는 단순합니다. **Volume(권) → Part(부) → 절** 순으로 나뉘고, Volume은 "누가 담당하느냐"로 나뉩니다.

    - BR/EDR **Controller**(Vol 2), **Host**(Vol 3), 둘 사이 **HCI**(Vol 4), LE **Controller**(Vol 6)
    - 처음에는 **Vol 1 Part A (Architecture)** 하나만 읽어도 전체 그림이 잡힙니다
    - 그다음 관심 있는 계층의 Part를 골라 읽고, 나머지는 사전처럼 찾아봅니다

    인용할 때는 "Core v6.0 Vol 6 Part B §4.4"처럼 **버전 + Vol + Part + 절**로 씁니다.

## Volume·Part 구조 { .l2 }

아래는 Core 6.x 기준입니다. AMP(3.0 + HS)를 규격에서 뺀 뒤로 관련 Part는 "더 이상 사용하지 않음"으로 남아 있어 Part 문자가 건너뛰는 곳이 있습니다.

| Vol | 제목 | 주요 Part | 이 책에서 |
|---|---|---|---|
| 0 | 통합 목차, 감사의 글, Core 구성 | A 목차 · C 버전 이력 · D Core Configurations | — |
| 1 | Architecture, Change History, Conventions | **A Architecture** · B 약어 · C 변경 이력 · E 용어와 해석 | [Host·Controller·HCI](../basics/architecture.md) |
| 2 | **BR/EDR Controller** | A Radio · B Baseband · C LMP · F 메시지 시퀀스 차트 · G 샘플 데이터 · H Security | [Classic](../classic/index.md) |
| 3 | **Host** | A L2CAP · B SDP · C GAP · D Test Support · F ATT · G GATT · H SMP | [LE 호스트](../host/index.md) |
| 4 | **Host Controller Interface** | A–D 전송 계층(UART, USB, SD, Three-wire UART) · **E HCI 기능 규격** | [HCI 명령과 이벤트](../practice/hci.md) |
| 5 | (AMP Controller) | AMP 제거로 내용 없음 | — |
| 6 | **Low Energy Controller** | A Radio · **B Link Layer** · C 샘플 데이터 · D 메시지 시퀀스 차트 · E LE Security · F Direct Test Mode · 이후 ISOAL, Channel Sounding 관련 Part 추가 | [LE 컨트롤러](../le/index.md) |
| 7 | Wireless Coexistence Signaling and Interfaces | A MWS 공존 논리 신호 · B WCI-1 전송 · C WCI-2 전송 | [Wi-Fi와의 공존](../basics/coexistence.md) |

!!! tip "LE 개발자가 가장 자주 여는 곳"
    Vol 6 Part B (Link Layer: 광고·연결·제어 절차), Vol 4 Part E (HCI 명령·이벤트), Vol 3 Part F·G (ATT·GATT), Vol 3 Part H (SMP), Vol 3 Part C (GAP: 광고 데이터, 모드·절차, 주소). LE 관련 질문 대부분은 이 다섯 곳에서 답을 찾을 수 있습니다.

Core 밖에 있는 것도 알아 두세요. 광고 데이터 타입별 형식은 **CSS**에, UUID·회사 ID·AD Type 번호는 **Assigned Numbers**에, 오디오·심박계 같은 응용 규칙은 각 **프로파일·서비스 규격**에 있습니다.

## 버전, 정오표, 부록 { .l2 }

| 문서 | 성격 | 지금의 위치 |
|---|---|---|
| Core vX.Y | 전체를 다시 낸 정식 버전 | 6.1부터 연 2회(봄·가을) 릴리스 |
| ESR (Errata Service Release) | 이전 버전에 대한 정오 모음 | 4.x 이전 버전에서 주로 쓰임. 지금은 다음 Core 버전에 반영 |
| Errata Correction (개별 정정) | 특정 오류 하나의 정정. 일부는 적합성 주장에 필수로 지정 | 규격 페이지에 함께 게시 |
| CSA (Core Specification Addendum) | 다음 버전 전에 기능을 덧붙이는 부록 | 4.x 시절 사용, 이후 Core에 흡수 |
| CSS (Core Specification Supplement) | AD Type 형식 등 데이터 정의 | 독립 문서로 계속 개정 (v11, v12 …) |

새 Core 버전에서 무엇이 바뀌었는지는 **Vol 1 Part C (Core Specification Change History)**에 정리되어 있습니다. 기능 추가뿐 아니라 "이 동작은 이제 금지" 같은 변경도 여기서 찾을 수 있으니 버전을 올릴 때 꼭 확인하세요.

## 원문 구하는 법 { .l2 }

| 경로 | 내용 |
|---|---|
| bluetooth.com → Specifications | 채택된 Core·프로파일·서비스 규격 PDF, 최근 버전은 **HTML판**도 제공 (절 링크를 공유하기 편함) |
| Assigned Numbers | 문서(PDF/HTML)와 YAML 저장소. 스크립트로 UUID·회사 ID를 읽을 때 유용 |
| 기능 개요(Feature Overview) 문서 | 새 Core 버전마다 SIG가 내는 해설 자료. 동기와 사용 예가 있어 원문 전에 읽기 좋음 |
| 테스트 규격(TS)·ICS | 규격 페이지에 함께 게시. "규격의 이 문장을 실제로 어떻게 시험하나"를 볼 수 있음 |
| 개발 중 초안 | Associate 이상 회원만 열람 |

??? expert "전문가 노트 — 읽는 요령, 자주 헷갈리는 표기"
    **요구 수준 단어.** 규격은 *shall*(필수), *should*(권장), *may*(허용)를 엄격히 구분합니다. 구현 분쟁은 대부분 "should를 shall로 읽었다" 혹은 그 반대에서 나옵니다. Vol 1 Part E에 용어 해석 규칙이 있습니다.

    **M/O/C/X 표.** 기능 지원 요구는 표에서 M(필수), O(선택), C.n(조건부: 표 아래 조건 n 참조), X(금지), E(제외)로 표기합니다. 조건부 C 항목의 조건 문구를 반드시 읽어야 합니다. "기능 A를 지원하면 기능 B도 필수" 같은 의존 관계가 여기에 숨어 있습니다.

    **비트·바이트 순서.** 무선 구간은 **LSB 먼저** 전송하고, 다중 바이트 필드는 리틀 엔디언입니다. 반면 규격 그림의 필드 배치는 LSB가 왼쪽입니다. 로그 도구가 보여 주는 16진수 문자열과 규격 그림을 대조할 때 순서를 착각하기 쉽습니다.

    **이름이 바뀐 용어.** 5.3부터 master/slave가 Central/Peripheral로, 그 밖의 표현도 SIG의 용어 정비 방침에 따라 바뀌었습니다. 예전 버전 문서·로그·소스 코드에는 옛 이름이 그대로 남아 있습니다(예: `LL_SLAVE_FEATURE_REQ` → `LL_PERIPHERAL_FEATURE_REQ`).

    **HCI 명령 찾기.** Vol 4 Part E는 명령을 OGF(그룹)별로 모아 둡니다. 이름 대신 OpCode(예: 0x2006)로 찾으면 빠릅니다. 이벤트는 LE Meta Event(0x3E) 아래 하위 이벤트 코드로 나뉩니다.

    **샘플 데이터와 MSC.** Vol 2 Part G·Vol 6 Part C의 샘플 데이터(암호화·CRC·화이트닝 예제 값)는 구현 검증에 매우 유용하고, 메시지 시퀀스 차트(MSC) Part는 절차의 정상 흐름을 빠르게 보여 줍니다.

## 관련 페이지

- [Bluetooth SIG와 규격 체계](sig-specs.md) — 규격 문서의 종류와 채택 과정
- [Bluetooth 세대와 Core 버전](generations.md) — 버전별 기능
- [규격 인덱스](../reference/spec-index.md) — 이 책에서 인용한 Vol/Part 일람
- [HCI 명령과 이벤트](../practice/hci.md) — Vol 4 Part E 실전
- [참고 자료](../reference/resources.md) — 책·도구·웹 자료
