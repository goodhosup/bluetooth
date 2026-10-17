# L2CAP·SDP·RFCOMM

!!! spec "규격 · 버전"
    Core v6.0 Vol 3 Part A (L2CAP) · Vol 3 Part B (SDP) · RFCOMM with TS 07.10 1.2 (RFCOMM 규격, ETSI TS 07.10 기반) · 할당 번호(PSM, UUID): Bluetooth SIG Assigned Numbers
    Core 1.1 L2CAP Basic 모드·SDP → 1.2 재전송/흐름 제어 모드 → 3.0 ERTM·Streaming 모드 → 4.1 LE 크레딧 기반 → 5.2 Enhanced Credit Based 모드 · RFCOMM 1.1 크레딧 기반 흐름 제어

!!! basic "한눈에 보기"
    Classic 연결이 생긴 뒤 "어떤 서비스와 이야기할지" 찾아가는 세 겹의 주소 체계입니다. 건물(ACL 링크)에 들어온 뒤 층(PSM), 안내 데스크(SDP), 방 번호(RFCOMM 채널)를 차례로 찾는 것과 비슷합니다.

    1. **L2CAP** — 하나의 ACL 링크 위에 여러 논리 채널을 만듭니다. 채널을 열 때 **PSM**으로 "어느 프로토콜"인지 지정합니다(예: AVDTP, HID, RFCOMM).
    2. **SDP** — 상대가 어떤 서비스를 제공하는지, 그 서비스에 가려면 어떤 PSM·RFCOMM 채널을 써야 하는지 묻는 안내 데스크입니다.
    3. **RFCOMM** — 한 L2CAP 채널 안에 여러 개의 가상 **시리얼 포트**(RS-232)를 만듭니다. HFP의 AT 명령, SPP가 이 위로 갑니다.

## L2CAP (Classic) { .l2 }

| 채널 ID (CID) | 용도 |
|---|---|
| `0x0001` | L2CAP 시그널링 (BR/EDR) |
| `0x0002` | 비연결형 채널 (그룹 전송) |
| `0x0007` | BR/EDR Security Manager (Classic 위 SMP, CTKD에 사용) |
| `0x0040`–`0xFFFF` | 동적 채널 (연결마다 할당) |

| PSM | 프로토콜 | PSM | 프로토콜 |
|---|---|---|---|
| `0x0001` | SDP | `0x0017` | AVCTP (AVRCP 제어) |
| `0x0003` | RFCOMM | `0x0019` | AVDTP (A2DP) |
| `0x000F` | BNEP (PAN) | `0x001B` | AVCTP Browsing |
| `0x0011` | HID Control | `0x001F` | ATT (BR/EDR 위 GATT) |
| `0x0013` | HID Interrupt | `0x1001`– | 동적 PSM (SDP로 알림) |

채널 수립은 `L2CAP_CONNECTION_REQ`(PSM, 소스 CID) → `L2CAP_CONNECTION_RSP` → 양방향 `L2CAP_CONFIGURATION_REQ`/`_RSP`(MTU, Flush Timeout, 모드, FCS 옵션) 순서입니다. BR/EDR의 기본 MTU는 672바이트, 최소 48바이트입니다.

| 모드 | 재전송 | 흐름 제어 | 대표 사용 |
|---|---|---|---|
| **Basic** | 없음 (ACL 기저대역 ARQ에 의존) | 없음 | SDP, RFCOMM, AVDTP, HID 대부분 |
| **ERTM** (Enhanced Retransmission) | I-프레임 순번, S-프레임 RR/REJ/SREJ | 송신 창 | 신뢰성이 필요한 채널, 예전 AMP 채널 |
| **Streaming** | 없음 (FCS로 오류 프레임 폐기) | 없음 | 지연이 중요한 스트림 |
| Retransmission / Flow Control (1.2) | 레거시 | 레거시 | ERTM으로 대체 |

## SDP — 서비스 발견 { .l2 }

SDP 서버는 **서비스 레코드**의 목록을 가집니다. 각 레코드는 (속성 ID, 값) 쌍의 집합이고, 값은 UUID·정수·문자열·시퀀스를 담는 **데이터 요소**(data element) 형식으로 인코딩됩니다.

| 속성 ID | 이름 | 예 (HFP Hands-Free 측) |
|---|---|---|
| `0x0000` | ServiceRecordHandle | `0x00010003` |
| `0x0001` | ServiceClassIDList | Handsfree `0x111E`, GenericAudio `0x1203` |
| `0x0004` | ProtocolDescriptorList | L2CAP(`0x0100`) → RFCOMM(`0x0003`), 채널 3 |
| `0x0005` | BrowseGroupList | PublicBrowseRoot |
| `0x0009` | BluetoothProfileDescriptorList | Handsfree, 버전 0x0109 (1.9) |
| `0x0100` | ServiceName (언어 기준 0x0100 + 0) | "Hands-Free unit" |
| `0x0311` | SupportedFeatures (프로파일별 속성) | 광대역 음성 등 비트 |

16비트 UUID는 **Bluetooth Base UUID** `00000000-0000-1000-8000-00805F9B34FB`의 앞 32비트 자리에 들어가는 축약형입니다(LE GATT와 같은 규칙). 질의는 `SDP_ServiceSearchRequest`(UUID로 레코드 핸들 찾기), `SDP_ServiceAttributeRequest`(핸들로 속성 읽기), 둘을 합친 `SDP_ServiceSearchAttributeRequest`가 있으며 보통 마지막 것을 씁니다.

## RFCOMM — 시리얼 포트 에뮬레이션 { .l2 }

RFCOMM은 GSM용 다중화 규격 ETSI TS 07.10의 일부를 가져와, 하나의 L2CAP 채널(PSM `0x0003`) 위에 여러 RS-232 회선을 흉내 냅니다.

| 개념 | 내용 |
|---|---|
| 서버 채널 | 1–30. SDP의 ProtocolDescriptorList로 알림 |
| **DLCI** | 데이터 링크 연결 식별자 = (서버 채널 × 2) + 방향 비트. DLCI 0은 다중화 제어 채널 |
| 프레임 | `SABM`(연결), `UA`(수락), `DM`(거절), `DISC`(해제), `UIH`(데이터·제어) |
| 제어 메시지 | `PN`(파라미터 협상: 최대 프레임 크기, 크레딧), `MSC`(모뎀 상태: RTS/CTS/DTR/DSR 대응 신호), `RPN`(보레이트 등 원격 포트 설정), `RLS`(회선 상태) |
| 흐름 제어 | **크레딧 기반**(RFCOMM 1.1): 수신 측이 받을 수 있는 프레임 수를 크레딧으로 나눠 주고, `UIH` 프레임에 추가 크레딧을 실어 보냄 |

연결 순서는 L2CAP 채널(PSM 3) → DLCI 0에 `SABM`/`UA` → `PN`으로 프레임 크기·크레딧 협상 → 대상 DLCI에 `SABM`/`UA` → `MSC` 교환 → 데이터 순서입니다.

??? expert "전문가 노트 — 실무에서 헷갈리는 점"
    **크레딧 고갈.** RFCOMM 크레딧 기반 흐름 제어에서 수신 측이 크레딧을 돌려주지 않으면 송신이 멈춥니다. HFP AT 명령이 몇 개 오간 뒤 응답이 멈추는 문제는 대개 크레딧 반환 누락입니다. `MSC`의 FC 비트 방식(1.0 흐름 제어)과 혼용하지 않도록 `PN`에서 크레딧 방식(CL 필드)을 확인합니다.

    **SDP 캐시와 동적 채널.** RFCOMM 서버 채널 번호와 동적 PSM은 기기 재부팅·앱 설치에 따라 바뀔 수 있으므로, 매 연결마다 SDP를 다시 조회하는 것이 안전합니다. 고정 번호를 하드코딩한 구현은 다른 스택과 만나면 실패합니다.

    **ERTM이 드문 이유.** BR/EDR 기저대역이 이미 ARQ로 오류를 고치므로, Basic 모드로 충분한 경우가 대부분입니다. ERTM은 Flush Timeout으로 기저대역 재전송을 끊은 상황이나 예전 AMP(3.0 + HS, 5.3에서 제거)에서 의미가 있었습니다.

    **GATT over BR/EDR.** ATT는 BR/EDR의 PSM `0x001F` 위에서도 동작하며, SDP 레코드로 GATT 서비스를 알립니다. 실제 제품에서는 드물지만 듀얼 모드 기기의 서비스 발견 로그에 등장할 수 있습니다.

## Classic ↔ LE 비교

| 항목 | Classic (BR/EDR) | LE |
|---|---|---|
| L2CAP 시그널링 CID | `0x0001` | `0x0005` |
| 동적 채널 | 연결 지향 채널(Basic·ERTM·Streaming) | 크레딧 기반 CoC (LE / Enhanced) |
| 서비스 발견 | SDP (레코드·속성) | GATT (서비스·특성 발견) |
| 시리얼 스트림 | RFCOMM | 표준 없음 (벤더 GATT 서비스 또는 CoC) |
| 최소 MTU | 48 B | 23 B (ATT) |

## 관련 페이지

- [L2CAP](../host/l2cap.md) — LE L2CAP과 크레딧 기반 모드
- [GATT](../host/gatt.md) — LE의 서비스 발견
- [오디오 프로파일 (A2DP·AVRCP·HFP)](audio-profiles.md) — AVDTP·AVCTP·RFCOMM 위의 프로파일
- [데이터 프로파일 (SPP·HID·PAN)](data-profiles.md) — RFCOMM·BNEP·HID 채널 사용 예
