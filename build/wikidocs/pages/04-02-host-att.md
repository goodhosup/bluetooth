[[TIP("📘 규격 · 버전")]]
Core v6.0 Vol 3 Part F (Attribute Protocol) · 전송: Vol 3 Part A (L2CAP CID 0x0004 / Enhanced Credit Based 채널) · UUID 할당: Assigned Numbers
Core 4.0 도입 (LE·BR/EDR 공통) → 5.1 오류 코드 Database Out Of Sync·Value Not Allowed 추가 → 5.2 EATT, `ATT_READ_MULTIPLE_VARIABLE_REQ`, `ATT_MULTIPLE_HANDLE_VALUE_NTF`
[[/TIP]]

[TOC]


[[TIP("🟢 한눈에 보기")]]
**ATT**(Attribute Protocol)는 서버가 가진 **속성 표(attribute table)** 하나를 클라이언트가 원격으로 읽고 쓰는 아주 작은 프로토콜입니다. 엑셀 시트를 떠올리면 쉽습니다.

1. 각 행이 **속성(attribute)** 하나: 행 번호 = **핸들**, 열 = **타입(UUID)**, **값**, **권한**
2. 클라이언트는 "핸들 0x0012를 읽어 줘", "타입이 0x2803인 행을 다 보여 줘"처럼 요청합니다.
3. 서버는 값이 바뀌면 먼저 **알림(Notification)**이나 **지시(Indication)**로 밀어 줄 수 있습니다.
4. 요청은 **한 번에 하나**만 진행합니다(응답을 받아야 다음 요청). 단순한 대신 느릴 수 있습니다.

서비스·특성 같은 "의미"는 ATT가 아니라 그 위의 **GATT**가 붙입니다.
[[/TIP]]

## 속성의 네 요소 (🔵 중급)

| 요소 | 크기 | 설명 |
|---|---|---|
| **핸들(Handle)** | 2 B | 0x0001–0xFFFF. 0x0000은 예약. 서버 안에서 유일하고 오름차순으로 탐색됨 |
| **타입(Type)** | 16 또는 128비트 UUID | 이 행이 무엇인지. 예: 0x2800 = Primary Service 선언, 0x2A19 = Battery Level |
| **값(Value)** | 0–512 B | 바이트 배열. 해석은 타입이 정함. 길이가 ATT_MTU를 넘으면 Read Blob/Prepare Write로 나눠 처리 |
| **권한(Permissions)** | (전송 안 됨) | 읽기/쓰기 가능 여부, 암호화·인증·인가 필요 여부, 암호 키 길이. 서버 내부 정책 |

16비트 UUID는 **Bluetooth Base UUID** `0000xxxx-0000-1000-8000-00805F9B34FB`의 `xxxx` 자리에 들어가는 축약형입니다. ATT PDU는 16비트와 128비트 UUID만 다룹니다(32비트 UUID는 광고 데이터용이며 ATT에서는 128비트로 펼쳐서 씁니다).

## PDU 종류 (🔵 중급)

ATT PDU는 **Opcode(1 B) + 파라미터 + (선택) 서명 12 B**입니다. Opcode의 bit 6은 Command 플래그(응답 없음), bit 7은 인증 서명 플래그입니다.

| Opcode | PDU | 방향 | 응답/확인 |
|---|---|---|---|
| 0x01 | `ATT_ERROR_RSP` | S→C | — |
| 0x02 / 0x03 | `ATT_EXCHANGE_MTU_REQ` / `_RSP` | C→S | 요청-응답 |
| 0x04 / 0x05 | `ATT_FIND_INFORMATION_REQ` / `_RSP` | C→S | 핸들 범위의 (핸들, UUID) 목록 |
| 0x06 / 0x07 | `ATT_FIND_BY_TYPE_VALUE_REQ` / `_RSP` | C→S | 특정 UUID 서비스 찾기 |
| 0x08 / 0x09 | `ATT_READ_BY_TYPE_REQ` / `_RSP` | C→S | 특성 선언 탐색, UUID로 값 읽기 |
| 0x0A / 0x0B | `ATT_READ_REQ` / `_RSP` | C→S | 핸들로 읽기 |
| 0x0C / 0x0D | `ATT_READ_BLOB_REQ` / `_RSP` | C→S | 오프셋부터 이어 읽기 |
| 0x0E / 0x0F | `ATT_READ_MULTIPLE_REQ` / `_RSP` | C→S | 고정 길이 값 여러 개 |
| 0x10 / 0x11 | `ATT_READ_BY_GROUP_TYPE_REQ` / `_RSP` | C→S | 1차 서비스 탐색 |
| 0x12 / 0x13 | `ATT_WRITE_REQ` / `_RSP` | C→S | 쓰기 + 확인 |
| 0x52 | `ATT_WRITE_CMD` | C→S | 없음 (Write Without Response) |
| 0xD2 | `ATT_SIGNED_WRITE_CMD` | C→S | 없음, CSRK 서명 12 B 포함 |
| 0x16 / 0x17 | `ATT_PREPARE_WRITE_REQ` / `_RSP` | C→S | 긴 값·원자적 다중 쓰기 준비 |
| 0x18 / 0x19 | `ATT_EXECUTE_WRITE_REQ` / `_RSP` | C→S | 큐 실행 또는 취소 |
| 0x1B | `ATT_HANDLE_VALUE_NTF` | S→C | 없음 (Notification) |
| 0x1D / 0x1E | `ATT_HANDLE_VALUE_IND` / `ATT_HANDLE_VALUE_CFM` | S→C / C→S | 확인 필요 (Indication) |
| 0x20 / 0x21 | `ATT_READ_MULTIPLE_VARIABLE_REQ` / `_RSP` | C→S | 가변 길이 값 여러 개 (5.2) |
| 0x23 | `ATT_MULTIPLE_HANDLE_VALUE_NTF` | S→C | 여러 핸들 한 번에 알림 (5.2) |

## MTU 교환 (🔵 중급)

`ATT_MTU`는 ATT PDU 하나의 최대 크기입니다. LE 고정 채널의 기본값은 **23바이트**이고, 연결 직후 클라이언트가 `ATT_EXCHANGE_MTU_REQ`(Client Rx MTU)를 보내면 서버가 `ATT_EXCHANGE_MTU_RSP`(Server Rx MTU)로 답합니다. 이후 양쪽은 **두 값 중 작은 값**을 씁니다. 교환은 연결당 한 번만, 클라이언트만 시작할 수 있습니다.

| ATT_MTU | Notify/Write 최대 값 (MTU − 3) | Read 응답 최대 값 (MTU − 1) |
|---|---|---|
| 23 (기본) | 20 B | 22 B |
| 185 (iOS 기기에서 자주 관찰되는 값) | 182 B | 184 B |
| 247 (LL 251 B에 딱 맞음) | 244 B | 246 B |
| 517 (Android 14+ 요청값) | 514 B (값 최대 512 B로 제한) | 516 B |

## 요청-응답 규칙과 오류 (🔵 중급)

- **순차 규칙**: 한 ATT 베어러에서 클라이언트는 응답을 받기 전에 다음 요청을 보내지 않고, 서버도 확인(`_CFM`)을 받기 전에 다음 Indication을 보내지 않습니다. Command와 Notification은 이 규칙 밖이라 연달아 보낼 수 있습니다.
- **트랜잭션 타임아웃**: 30초 안에 응답이 없으면 그 베어러에서 더 이상 ATT를 쓰지 않습니다(사실상 재연결 필요).

| 코드 | 오류 | 흔한 원인 |
|---|---|---|
| 0x01 | Invalid Handle | 존재하지 않는 핸들 (서버 DB 변경 후 캐시 사용) |
| 0x02 / 0x03 | Read / Write Not Permitted | 권한 없음 |
| 0x05 | Insufficient Authentication | 인증된(MITM) 페어링 필요 → 페어링 트리거 |
| 0x06 | Request Not Supported | 서버가 해당 PDU 미구현 |
| 0x07 | Invalid Offset | Read Blob/Prepare Write 오프셋 초과 |
| 0x08 | Insufficient Authorization | 앱 수준 허가 필요 |
| 0x0A | Attribute Not Found | 탐색 끝 (정상 종료 신호로 쓰임) |
| 0x0C | Encryption Key Size Too Short | 키 길이 부족 |
| 0x0D | Invalid Attribute Value Length | 값 길이 틀림 |
| 0x0F | Insufficient Encryption | 암호화 필요 → 암호화 시작 |
| 0x12 | Database Out Of Sync | GATT Caching: 클라이언트 캐시가 낡음 (5.1) |
| 0x13 | Value Not Allowed | 허용되지 않는 값 (5.1) |
| 0x80–0x9F | 애플리케이션 오류 | 서비스 규격이 정의 |
| 0xE0–0xFF | 공통 프로파일·서비스 오류 | 예: 0xFD CCCD Improperly Configured |

[[TIP("🔴 전문가 노트 — 긴 값, 서명 쓰기, 보안 오류 처리")]]
**긴 값 읽기·쓰기.** 값이 `ATT_MTU − 1`보다 길면 클라이언트는 `ATT_READ_REQ`로 앞부분을 받은 뒤 `ATT_READ_BLOB_REQ`(오프셋)로 이어 읽습니다. 쓰기는 `ATT_PREPARE_WRITE_REQ`로 조각을 서버 큐에 쌓고 `ATT_EXECUTE_WRITE_REQ`(Flags=0x01)로 한꺼번에 반영합니다. 응답에 요청 값이 그대로 되돌아오므로 클라이언트가 전송 오류를 확인할 수 있는 **Reliable Write**로도 쓰입니다.

**보안 오류가 페어링을 부른다.** 많은 스택은 0x05(Insufficient Authentication)나 0x0F(Insufficient Encryption)를 받으면 자동으로 암호화·페어링을 시작하고 같은 요청을 재시도합니다. iOS의 "페어링 요청" 팝업이 특정 특성을 처음 읽을 때 뜨는 이유가 이것입니다. 연결이 암호화되지 않은 상태에서 서버가 0x05를 돌려줄지 0x0F를 돌려줄지는 키 존재 여부에 따라 달라집니다.

**Signed Write.** `ATT_SIGNED_WRITE_CMD`는 암호화 없는 링크에서 CSRK로 서명한 쓰기입니다. 암호화된 링크에서는 쓰지 않으며, EATT 베어러에서는 허용되지 않습니다. 실제 제품에서 쓰이는 일은 드뭅니다.

**Notification 유실.** Notification은 ATT 수준 확인이 없지만 LL은 ACK/재전송을 하므로 연결이 살아 있는 한 무선 구간에서 사라지지는 않습니다. 유실은 대부분 호스트 큐 넘침이나 연결 끊김 시점에 생깁니다. 값마다 확인이 꼭 필요하면 Indication을 쓰되, 한 번에 하나라서 연결 간격당 1개 정도로 느려집니다.
[[/TIP]]

## 관련 페이지
- **L2CAP** — ATT가 올라가는 고정 채널 0x0004
- **GATT** — 속성 표 위의 서비스·특성 구조와 탐색 절차
- **EATT** — 여러 ATT 베어러로 순차 규칙 완화
- **처리량 최적화** — MTU와 Write Without Response
- **LE 페어링과 본딩** — 보안 오류가 촉발하는 페어링
