[[TIP("📘 규격 · 버전")]]
Core v6.0 Vol 2 Part C (Link Manager Protocol Specification) · 기능 비트 정의: Vol 2 Part C · HCI 대응 명령: Vol 4 Part E
Core 1.1 기본 PDU → 1.2 AFH·eSCO PDU, 확장 opcode → 2.0 EDR 패킷 타입 테이블 → 2.1 SSP·Sniff Subrating PDU → 4.1 Secure Connections(AES-CCM) → 5.3 최소 암호 키 길이 제어
[[/TIP]]

[TOC]


[[TIP("🟢 한눈에 보기")]]
**LMP**(Link Manager Protocol)는 두 Classic **컨트롤러끼리** 나누는 관리 대화입니다. 호스트(운영체제의 스택)는 이 대화를 직접 보지 않고, HCI 명령으로 "역할을 바꿔 줘", "Sniff로 들어가" 하고 부탁할 뿐입니다.

1. 연결 직후 서로의 **기능**(EDR 지원? eSCO? Sniff?)과 **버전**을 묻습니다.
2. 필요하면 **역할 전환**, **페어링·인증**, **암호화 시작**을 협상합니다.
3. 양쪽이 `LMP_setup_complete`를 보내면 연결 준비 끝 — 이제 호스트 데이터(L2CAP)가 흐릅니다.
4. 연결 중에도 저전력 모드, 최대 슬롯 수, AFH 채널 맵, 감독 시간을 계속 조정합니다.

LE에서 같은 역할을 하는 것이 링크 계층의 **LL 제어 절차**(`LL_FEATURE_REQ`, `LL_ENC_REQ` 등)입니다.
[[/TIP]]

## LMP의 위치와 전송 (🔵 중급)

| 항목 | 내용 |
|---|---|
| 담당 | Link Manager — 컨트롤러 펌웨어 |
| 운반 | ACL 논리 링크의 제어 채널(**ACL-C**), 페이로드 헤더 `LLID` = 11. 보통 `DM1` 한 패킷 |
| 우선순위 | 사용자 데이터(ACL-U)보다 먼저 전송 |
| 구조 | `TID`(트랜잭션 시작 측) 1비트 + opcode 7비트(확장 opcode는 escape 후 추가 1바이트) + 파라미터 |
| 응답 | `LMP_accepted` / `LMP_not_accepted`(오류 코드 포함) 또는 전용 응답 PDU |
| 응답 시간 제한 | LMP Response Timeout 30 s |

## 주요 PDU (🔵 중급)

| 기능 | 주요 PDU | 대응 HCI 명령 / 이벤트 |
|---|---|---|
| 연결 수립 | `LMP_host_connection_req`, `LMP_setup_complete` | `HCI_Create_Connection` / `HCI_Connection_Complete` |
| 기능 교환 | `LMP_features_req`/`_res`, `LMP_features_req_ext`/`_res_ext` | `HCI_Read_Remote_Supported_Features`, `HCI_Read_Remote_Extended_Features` |
| 버전 | `LMP_version_req`/`_res` (VersNr, CompId, SubVersNr) | `HCI_Read_Remote_Version_Information` |
| 이름 | `LMP_name_req`/`_res` (오프셋 지정, 조각 단위) | `HCI_Remote_Name_Request` |
| 역할 전환 | `LMP_slot_offset`, `LMP_switch_req` | `HCI_Switch_Role` / `HCI_Role_Change` |
| 인증 (레거시) | `LMP_au_rand`, `LMP_sres` | `HCI_Authentication_Requested` |
| SSP | `LMP_io_capability_req`/`_res`, `LMP_encapsulated_header`(공개키), `LMP_simple_pairing_confirm`, `LMP_DHkey_check` | `HCI_IO_Capability_Request` 등 |
| 암호화 | `LMP_encryption_mode_req`, `LMP_encryption_key_size_req`, `LMP_start_encryption_req`, `LMP_stop_encryption_req` | `HCI_Set_Connection_Encryption` / `HCI_Encryption_Change` |
| Sniff | `LMP_sniff_req`, `LMP_unsniff_req`, `LMP_sniff_subrating_req`/`_res` | `HCI_Sniff_Mode`, `HCI_Exit_Sniff_Mode`, `HCI_Sniff_Subrating` / `HCI_Mode_Change` |
| 링크 품질 | `LMP_max_slot`, `LMP_packet_type_table_req`(EDR on/off), `LMP_set_AFH`, `LMP_channel_classification`, `LMP_supervision_timeout` | `HCI_Change_Connection_Packet_Type` 등 |
| 동기 링크 | `LMP_SCO_link_req`, `LMP_eSCO_link_req`, `LMP_remove_eSCO_link_req` | `HCI_Enhanced_Setup_Synchronous_Connection` |
| 연결 해제 | `LMP_detach` (사유 코드) | `HCI_Disconnect` / `HCI_Disconnection_Complete` |

`LMP_version_res`의 **VersNr**은 Core 버전 번호입니다: 3 = 2.0, 4 = 2.1, 5 = 3.0, 6 = 4.0, 7 = 4.1, 8 = 4.2, 9 = 5.0, 10 = 5.1, 11 = 5.2, 12 = 5.3, 13 = 5.4, 14 = 6.0. 로그에서 상대 칩의 세대를 확인할 때 가장 먼저 보는 값입니다.

## 기능 비트 (🔵 중급)

기능 마스크는 페이지 단위입니다. **페이지 0**은 컨트롤러의 기본 기능(64비트), **페이지 1**은 호스트 기능, **페이지 2**는 이후 추가된 컨트롤러 기능입니다.

| 페이지 | 대표 비트 | 의미 |
|---|---|---|
| 0 | 3-slot / 5-slot packets | DH3·DH5 등 다중 슬롯 패킷 |
| 0 | EDR ACL 2 Mbps / 3 Mbps, 3-slot / 5-slot EDR ACL | 2-DHx, 3-DHx 사용 가능 |
| 0 | Role switch, Sniff mode, Sniff subrating | 역할 전환, 저전력 모드 |
| 0 | eSCO link (EV3), EV4/EV5, EDR eSCO 2/3 Mbps | 음성 링크 종류 |
| 0 | AFH capable / classification (Central, Peripheral) | 적응형 도약 |
| 0 | Extended Inquiry Response, Secure Simple Pairing (Controller) | 2.1 기능 |
| 0 | LE Supported (Controller), Simultaneous LE and BR/EDR (Controller) | 듀얼 모드 |
| 1 | Secure Simple Pairing (Host), LE Supported (Host), Secure Connections (Host) | 호스트가 켰는지 |
| 2 | Secure Connections (Controller), Ping | AES-CCM 암호화, 인증된 페이로드 시간 제한 |

기능은 **양쪽이 모두 지원할 때만** 사용합니다. 예를 들어 한쪽이 EDR 3 Mbps 비트를 내리면 링크는 2-DHx 이하로 운용되고, 호스트가 `HCI_Change_Connection_Packet_Type`으로 허용한 타입 안에서 컨트롤러가 패킷을 고릅니다.

[[TIP("🔴 전문가 노트 — 역할 전환, 암호 키 길이, 충돌")]]
**역할 전환.** Peripheral이 여러 연결을 동시에 관리하려면 자신이 Central이 되는 편이 유리합니다(스캐터넷 단순화). 그래서 헤드셋·차량은 연결 직후 역할 전환을 요청하는 경우가 많습니다. 전환 순간 새 Central의 `FHS`로 클럭과 도약 순서가 바뀌므로, eSCO·A2DP가 흐르는 중에는 거절(`LMP_not_accepted`, Role Switch Not Allowed)되기도 합니다. `HCI_Write_Link_Policy_Settings`의 role switch 비트가 꺼져 있으면 호스트가 막은 것입니다.

**암호 키 길이와 KNOB.** 레거시 E0 암호화는 키 길이를 1–16바이트로 협상할 수 있었고, 2019년 공개된 KNOB 공격은 이를 1바이트로 깎아 내리는 방식이었습니다. 이후 SIG는 최소 7바이트를 요구하도록 규격을 고쳤고, Core 5.3에서 호스트가 최소 길이를 지정하는 `HCI_Set_Min_Encryption_Key_Size`가 추가되었습니다. 암호화 후 `HCI_Read_Encryption_Key_Size`로 실제 길이를 확인하는 것이 권장됩니다. → **알려진 공격과 대응**

**트랜잭션 충돌.** 양쪽이 같은 절차(예: `LMP_switch_req`)를 동시에 시작하면 `TID`로 구분하고, Central이 시작한 쪽이 이깁니다. 진 쪽은 `LMP_not_accepted`(LMP Error Transaction Collision)를 받습니다. 로그에 오류 0x23이 보이면 이 경우입니다.
[[/TIP]]

## Classic ↔ LE 비교

| 항목 | Classic LMP | LE LL 제어 절차 |
|---|---|---|
| 운반 | ACL-C (`LLID` = 11) | LL Control PDU (`LLID` = 11) |
| 기능 교환 | `LMP_features_req` (페이지 0–2) | `LL_FEATURE_REQ` (6.0: 확장 기능 집합) |
| 암호화 시작 | `LMP_start_encryption_req` | `LL_ENC_REQ` / `LL_START_ENC_REQ` |
| 파라미터 변경 | `LMP_sniff_req`, `LMP_max_slot` | `LL_CONNECTION_UPDATE_IND`, `LL_LENGTH_REQ` |
| 응답 제한 | 30 s | 40 s (LL 절차 응답 타임아웃) |

## 관련 페이지

- **조회와 페이징** — LMP가 시작되기 직전
- **Classic 보안 (SSP)** — LMP 위의 페어링
- **LL 제어 절차** — LE의 대응 프로토콜
- **HCI 명령과 이벤트** — 호스트 쪽에서 보는 같은 절차
