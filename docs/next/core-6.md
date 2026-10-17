# Core 6.0–6.3

!!! spec "규격 · 버전"
    Bluetooth Core Specification v6.0 (2024.9) · v6.1 (2025.5) · v6.2 (2025.11) · v6.3 (2026.5) — 근거: Bluetooth SIG의 버전별 Feature Overview·블로그
    5.4 (2023, PAwR·암호화된 광고 데이터) → **6.0** Channel Sounding 등 6개 기능 → **6.1** Randomized RPA Updates → **6.2** Shorter Connection Intervals 등 4개 기능 → 6.3 CS 개선·HCI 확장

!!! basic "한눈에 보기"
    Core 6.x는 "숫자 앞자리가 바뀔 만큼" 큰 기능인 **Channel Sounding**(정밀 거리 측정)으로 시작했고, 이후 버전은 실사용 개선에 집중합니다.

    1. **6.0 (2024.9)** — 거리 측정(Channel Sounding), 똑똑한 스캔(광고 필터링·광고자 모니터링), 프레임 간격 조정
    2. **6.1 (2025.5)** — 주소 바꾸는 시점을 무작위로 해서 추적을 더 어렵게 하고, 그 일을 컨트롤러가 맡아 전력 절약
    3. **6.2 (2025.11)** — 연결 간격을 최소 375 µs까지 줄여 반응성 향상, Channel Sounding 공격 방어 강화, USB HCI·시험 모드 개선
    4. **6.3 (2026.5)** — Channel Sounding 정확도 개선, HCI 확장, BR/EDR·LE RF 요구 정리

    SIG는 2024년부터 Core 규격을 대략 반년 주기로 발표하고 있습니다. 아래 내용은 SIG 공개 자료로 확인한 범위이며, 세부 수치는 해당 규격 원문으로 확인해야 합니다.

## Core 6.0 (2024.9) { .l2 }

| 기능 | 무엇이 바뀌나 | 주요 PDU·HCI | 이 책의 페이지 |
|---|---|---|---|
| **Channel Sounding** | 연결된 두 기기가 위상 기반 거리 측정(PBR)과 왕복 시간(RTT)으로 안전하게 거리를 잼 | CS Capabilities Exchange, CS Configuration, CS Security Start 절차, CS 전용 채널 선택 알고리즘(CSA #3a/#3b/#3c), LE 2M 2BT PHY | [Channel Sounding](../le/channel-sounding.md), [활용](cs-applications.md) |
| **결정 기반 광고 필터링** (DBAF) | 스캐너가 1차 광고 채널 패킷의 "결정 데이터"를 보고 2차 채널 패킷을 받을지 결정 → 불필요한 스캔 감소 | `ADV_DECISION_IND`, `HCI_LE_Set_Decision_Data`, `HCI_LE_Set_Decision_Instructions` | [스캔과 필터](../le/scanning.md), [확장 광고](../le/extended-advertising.md) |
| **Monitoring Advertisers** | 컨트롤러가 지정한 광고자가 범위를 벗어나거나 다시 들어올 때만 호스트에 알림 → 호스트 깨움 감소 | LE Monitored Advertisers List 명령, LE Monitored Advertisers Report 이벤트 | [스캔과 필터](../le/scanning.md) |
| **ISOAL 강화** | 등시성 적응 계층에 새 프레이밍 모드 추가 → 지연에 민감한 오디오의 지연·신뢰성 개선 | — (공개 개요에 PDU 이름 없음) | [등시성 채널](../le/iso.md) |
| **LL Extended Feature Set** | 늘어난 기능 비트를 교환할 수 있도록 링크 계층 기능 교환 확장 | — | [LL 제어 절차](../le/ll-control.md) |
| **Frame Space Update** | 고정 150 µs였던 T_IFS를 연결·CIS에서 협상해 더 짧게 또는 길게 | — | [연결 이벤트와 파라미터](../le/connection-events.md) |

## Core 6.1 (2025.5) { .l2 }

6.1의 새 기능은 **Randomized RPA Updates** 하나이며, SIG는 이를 HCI 수준 개선으로 설명합니다. 이 밖에 오류 수정(errata)이 포함되었습니다.

| 항목 | 기존 (v1) | 6.1 (v2) |
|---|---|---|
| HCI 명령 | `HCI_LE_Set_Resolvable_Private_Address_Timeout` — 고정 `RPA_Timeout` | 같은 명령의 [v2] — `RPA_Timeout_Min`, `RPA_Timeout_Max` |
| 값 범위 | 1–3600 s, 기본 900 s | 각각 1–3600 s, 기본 Min 480 s · Max 900 s |
| 갱신 시점 | 일정한 주기 → 주소 변경 시점으로 같은 기기를 연결 추적 가능 | Min–Max 구간에서 **균등 분포 무작위** 시점 |
| 누가 관리 | 호스트가 주기적으로 개입하는 구현이 흔함 | **컨트롤러가 자율적으로** 갱신 → 호스트 깨움 감소 |
| 기본 동작 | — | 기능을 지원하는 컨트롤러는 명령을 보내지 않아도 기본으로 무작위화 |

Min > Max이거나 범위를 벗어나면 `Invalid HCI Command Parameters`(0x12) 오류입니다. 지원 여부는 `HCI_Read_Local_Supported_Commands`로 확인합니다. → [프라이버시와 RPA](../security/privacy.md)

## Core 6.2 (2025.11) { .l2 }

| 기능 | 무엇이 바뀌나 | 주요 PDU·HCI | 이 책의 페이지 |
|---|---|---|---|
| **Shorter Connection Intervals** (SCI) | 최소 연결 간격 7.5 ms → **375 µs**, 단위 125 µs. 기존 범위(7.5 ms 이상, 1.25 ms 단위), SCI 지원 시 필수인 1.25 ms 이상 범위, 선택적인 375 µs 이상·125 µs 단위 범위로 구분 | `LL_CONNECTION_RATE_REQ`/`LL_CONNECTION_RATE_IND`, `HCI_LE_Connection_Rate_Request`, `HCI_LE_Set_Default_Rate_Parameters`, `HCI_LE_Read_Minimum_Supported_Connection_Interval`, LE Connection Rate Change 이벤트 | [연결 이벤트와 파라미터](../le/connection-events.md) |
| **CS 진폭 기반 공격 내성** | 주기적으로 진폭을 조작하는 공격을 탐지하도록 NADM 지표 보강, 시험 기준 추가 | CS 능력 비트 (`LL_CS_CAPABILITIES_REQ/RSP`, HCI CS 능력 명령·이벤트) | [Channel Sounding](../le/channel-sounding.md) |
| **HCI USB LE 등시성 지원** | USB 전송에서 ISO 데이터를 포함한 모든 HCI 패킷을 하나의 Bulk 스트림으로 직렬화하는 선택 모드 → 이벤트·데이터 순서 뒤바뀜 해소 | 패킷 앞 1바이트 지시자(0x05 = ISO) | [HCI 명령과 이벤트](../practice/hci.md) |
| **LE 시험 모드 강화** (UTP) | DTM과 동등한 Unified Test Protocol: UART·HCI·**무선(OTA)** 전송, BER 측정 | `HCI_LE_UTP_Send`, `LL_OTA_UTP_IND` (암호화된 연결에서만 처리) | [RF 시험과 안테나](../practice/rf-testing.md) |

## Core 6.3 (2026.5) { .l2 }

SIG 기술 개요에서 확인한 범위만 적었습니다. 명령·PDU 이름과 세부 값은 규격 원문 확인이 필요합니다.

| 기능 | 무엇이 바뀌나 | 이 책의 페이지 |
|---|---|---|
| **CS Inline PCT Transfer** | Channel Sounding 위상 보정 정보(PCT)를 절차 안에서 바로 전달해, 측정 후 결과를 따로 주고받는 부담을 줄임 | [Channel Sounding](../le/channel-sounding.md) |
| **PHY별 RTT 정확도** | 왕복 시간(RTT) 정확도를 PHY마다 따로 알릴 수 있게 함 | [Channel Sounding](../le/channel-sounding.md) |
| **HCI 확장** | 지원 명령 비트맵과 LE 이벤트 마스크가 꽉 차서 더 큰 형식([v2] 명령)을 추가 | [HCI 명령과 이벤트](../practice/hci.md) |
| **BR/EDR·LE RF 요구 정렬** | BR/EDR의 인접 채널 전력(ACP)·C/I 요구를 LE 쪽과 맞춰 완화 | [RF 시험과 안테나](../practice/rf-testing.md) |

??? expert "전문가 노트 — 6.x를 제품에 반영할 때"
    **기능 비트로 확인.** 6.x 기능은 모두 선택 사항입니다. "Bluetooth 6.0 지원" 표기만으로 Channel Sounding이 된다고 볼 수 없으며, `HCI_LE_Read_Local_Supported_Features`(및 6.0의 확장 기능 집합)와 원격 기능 교환 결과로 확인해야 합니다. CS는 새 PHY 모드와 RF 요구가 있어 기존 칩에 펌웨어만으로 추가되지 않는 경우가 많습니다.

    **SCI의 제약.** 짧은 간격은 지연을 줄이지만 다른 연결·스캔과 스케줄이 충돌하기 쉽고 전력이 늘어납니다. SIG 개요는 서브레이팅 계수와 Peripheral latency의 곱에 상한(SubrateFactorMax × (Max_Latency + 1) ≤ 500)을 두었다고 설명합니다. 6.2는 LE ACL에서 Flushable 데이터 표시도 정리했습니다(`HCI_Write_Automatic_Flush_Timeout`).

    **T_IFS 변경의 파급.** Frame Space Update로 T_IFS가 150 µs가 아닐 수 있게 되었으므로, 스니퍼·분석 도구와 airtime 계산이 "항상 150 µs"를 가정하면 틀릴 수 있습니다. 협상 전 기본값은 150 µs입니다.

## 관련 페이지

- [Channel Sounding](../le/channel-sounding.md) — 6.0 핵심 기능의 원리
- [Channel Sounding 활용](cs-applications.md) — 응용 분야와 생태계
- [프라이버시와 RPA](../security/privacy.md) — 6.1 Randomized RPA Updates
- [연결 이벤트와 파라미터](../le/connection-events.md) — 6.2 짧은 연결 간격
- [스캔과 필터](../le/scanning.md) — DBAF, Monitoring Advertisers
- [Core 버전별 기능 인덱스](../reference/version-index.md) — 1.1부터의 전체 표
