# 규격 인덱스

!!! spec "규격 · 버전"
    Bluetooth Core Specification v6.0 (권·Part 구성) · Core Specification Supplement (CSS) · Assigned Numbers · 프로파일·서비스 규격 (각자 독립 버전) — 모두 bluetooth.com/specifications 에서 공개
    Core 4.0 이후 Vol 6 (LE Controller) 추가 → 5.2 Vol 6 Part G (ISOAL) → 5.3 AMP 관련 내용 제거 → 6.0 Vol 6 Part H (Channel Sounding)

!!! basic "한눈에 보기"
    Bluetooth 규격은 **하나의 큰 Core 규격**과 **수십 개의 작은 프로파일·서비스 규격**으로 나뉩니다.

    1. **Core**는 무선·링크·HCI·L2CAP·ATT/GATT·SMP·GAP처럼 모든 기기가 공유하는 바탕입니다. 권(Volume)과 부(Part)로 나뉩니다.
    2. **프로파일**은 "이 용도에서는 어떤 역할과 절차로 쓴다"를, **서비스**는 GATT 서버가 노출하는 데이터 구조를 정합니다.
    3. 숫자 상수(UUID, AD 타입, 회사 ID, 코덱 ID)는 별도 문서 **Assigned Numbers**에 모여 있습니다.

    규격 문서를 처음 읽는 요령은 [규격 문서 읽는 법](../getting-started/reading-specs.md)을 참고하십시오.

## Core 규격 구성 { .l2 }

| Vol | 이름 | 주요 Part | 이 책 페이지 |
|---|---|---|---|
| 1 | Architecture, Mixing, and Conventions | A 아키텍처, C 버전별 변경, F Controller 오류 코드 | [Host·Controller·HCI](../basics/architecture.md), [HCI 명령과 이벤트](../practice/hci.md) |
| 2 | BR/EDR Controller | A Radio, B Baseband, C LMP, H Security | [피코넷과 기저대역](../classic/baseband.md), [링크 관리자 (LMP)](../classic/lmp.md), [Classic 보안 (SSP)](../security/classic-security.md) |
| 3 | Host | A L2CAP, B SDP, C GAP, F ATT, G GATT, H SMP | [L2CAP](../host/l2cap.md), [L2CAP·SDP·RFCOMM](../classic/l2cap-sdp-rfcomm.md), [GAP](../host/gap.md), [ATT](../host/att.md), [GATT](../host/gatt.md), [LE 페어링과 본딩](../security/le-pairing.md) |
| 4 | Host Controller Interface | A UART 전송, B USB 전송, D 3-wire UART, E HCI 기능 규격 | [HCI 명령과 이벤트](../practice/hci.md) |
| 5 | (AMP Controller) | 3.0 + HS의 AMP — 5.3에서 제거 | [Bluetooth 세대와 Core 버전](../getting-started/generations.md) |
| 6 | Low Energy Controller | A PHY, B Link Layer, E LL 보안, F Direct Test Mode, G ISOAL, H Channel Sounding | [LE PHY (1M·2M·Coded)](../le/phy.md), [링크 계층 상태 기계](../le/link-layer-states.md), [등시성 채널 (CIS·BIS)](../le/iso.md), [Channel Sounding](../le/channel-sounding.md), [RF 시험과 안테나](../practice/rf-testing.md) |
| 7 | Wireless Coexistence | MWS 공존 신호, 공존 인터페이스(WCI) | [Wi-Fi와의 공존](../basics/coexistence.md) |
| — | Core Specification Supplement (CSS) | 광고 데이터(AD) 타입 형식 등 | [광고 데이터 형식 (AD Type)](../host/ad-types.md) |

Part 문자는 버전에 따라 추가·삭제되며 바뀔 수 있습니다. 인용할 때는 규격 버전을 함께 적습니다(예: "Core v6.0 Vol 6 Part B").

## 주요 프로파일·서비스 규격 { .l2 }

**Classic 프로파일**

| 약어 | 이름 | 이 책 페이지 |
|---|---|---|
| A2DP | Advanced Audio Distribution Profile | [오디오 프로파일 (A2DP·AVRCP·HFP)](../classic/audio-profiles.md) |
| AVRCP | Audio/Video Remote Control Profile | [오디오 프로파일 (A2DP·AVRCP·HFP)](../classic/audio-profiles.md) |
| HFP | Hands-Free Profile | [오디오 프로파일 (A2DP·AVRCP·HFP)](../classic/audio-profiles.md) |
| SPP | Serial Port Profile | [데이터 프로파일 (SPP·HID·PAN)](../classic/data-profiles.md) |
| HID | Human Interface Device Profile | [데이터 프로파일 (SPP·HID·PAN)](../classic/data-profiles.md) |
| PAN | Personal Area Networking Profile | [데이터 프로파일 (SPP·HID·PAN)](../classic/data-profiles.md) |

**LE·GATT 기반**

| 약어 | 이름 | 이 책 페이지 |
|---|---|---|
| HOGP | HID over GATT Profile | [대표 GATT 서비스](../host/gatt-services.md) |
| HRS / HRP | Heart Rate Service / Profile | [대표 GATT 서비스](../host/gatt-services.md) |
| BAS | Battery Service | [대표 GATT 서비스](../host/gatt-services.md) |
| DIS | Device Information Service | [대표 GATT 서비스](../host/gatt-services.md) |
| RAS / RAP | Ranging Service / Ranging Profile (Channel Sounding) | [Channel Sounding 활용](../next/cs-applications.md) |

**LE Audio**

| 약어 | 이름 | 이 책 페이지 |
|---|---|---|
| LC3 | Low Complexity Communication Codec | [LC3 코덱](../audio/lc3.md) |
| BAP | Basic Audio Profile | [BAP (Unicast·Broadcast)](../audio/bap.md) |
| PACS / ASCS | Published Audio Capabilities Service / Audio Stream Control Service | [PACS와 ASCS](../audio/pacs-ascs.md) |
| BASS | Broadcast Audio Scan Service | [Auracast 브로드캐스트](../audio/auracast.md) |
| PBP | Public Broadcast Profile | [Auracast 브로드캐스트](../audio/auracast.md) |
| CAP | Common Audio Profile | [CAP과 CSIP](../audio/cap-csip.md) |
| CSIP / CSIS | Coordinated Set Identification Profile / Service | [CAP과 CSIP](../audio/cap-csip.md) |
| VCP, MCP, CCP, MICP | Volume / Media / Call Control, Microphone Control Profile | [볼륨·통화·미디어 제어](../audio/control.md) |
| TMAP | Telephony and Media Audio Profile | [LE Audio 개요](../audio/overview.md) |
| HAP / HAS | Hearing Access Profile / Service | [보청기 프로파일 (HAP)](../audio/hap.md) |

**Mesh**

| 약어 | 이름 | 이 책 페이지 |
|---|---|---|
| MshPRT | Mesh Protocol (1.1부터 이 이름, 이전 Mesh Profile) | [Mesh 개요와 관리형 플러딩](../mesh/overview.md), [Mesh 1.1](../mesh/mesh-1-1.md) |
| MshMDL | Mesh Model | [모델](../mesh/models.md) |

??? expert "전문가 노트 — 규격 문서를 찾고 인용할 때"
    **버전 고정.** 프로파일·서비스 규격은 Core와 독립된 버전을 가집니다(예: BAP 1.0.x, HFP 1.9). 인증 시험(TCRL)은 특정 버전 조합을 기준으로 하므로, 구현 문서에는 "어느 버전의 어느 규격"인지 꼭 적습니다.

    **수정 사항(Errata).** 발행 후 발견된 오류는 Errata Correction으로 반영되고, 다음 개정판에 통합됩니다. 오래된 PDF만 보고 구현하면 이미 고쳐진 오류를 그대로 재현할 수 있습니다.

    **상수는 Assigned Numbers에서.** UUID, AD 타입, Appearance, Company Identifier, 코덱 ID 등은 규격 본문이 아니라 Assigned Numbers 문서(및 YAML 저장소)가 기준입니다. → [참고 자료](resources.md)

## 관련 페이지

- [Bluetooth SIG와 규격 체계](../getting-started/sig-specs.md) — 규격이 만들어지는 과정
- [규격 문서 읽는 법](../getting-started/reading-specs.md) — Vol/Part 읽기 요령
- [Core 버전별 기능 인덱스](version-index.md) — 버전별 기능
- [참고 자료](resources.md) — 다운로드 링크
