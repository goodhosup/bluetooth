[[TIP("📘 규격 · 버전")]]
Mesh Model v1.1 (Generic, Sensor, Time and Scenes, Lighting 모델) · Mesh Protocol v1.1 (Access 계층, 요소, Composition Data, Foundation Model: Configuration·Health) · NLC 프로파일 v1.0 (Networked Lighting Control, 2023)
Mesh Model 1.0 (2017) → Mesh Model 1.1 (2023, 모델 메타데이터 등) · NLC 프로파일 6종 (2023)
[[/TIP]]

[TOC]


[[TIP("🟢 한눈에 보기")]]
**모델(model)**은 "무엇을 할 수 있는 기기인가"를 표준화한 부품입니다. 각 모델은 **상태(state)**, 그 상태를 읽고 바꾸는 **메시지(opcode)**, 상태가 바뀔 때의 **동작**을 정의합니다.

1. **서버 모델** — 상태를 가짐 (전구의 Generic OnOff Server: 켜짐/꺼짐)
2. **클라이언트 모델** — 상태가 없고 서버에 Get/Set을 보냄 (스위치의 Generic OnOff Client)
3. **컨트롤 모델** — 서버이면서 클라이언트처럼 다른 노드를 제어 (조명 제어기 Light LC Server가 센서 값을 받고 조명을 조절)

한 노드에는 여러 **요소(element)**가 있고, 요소마다 유니캐스트 주소가 하나씩입니다. 2구 스위치라면 버튼마다 요소를 두어 각 버튼이 독립된 주소로 발행합니다.
[[/TIP]]

## 요소와 Composition Data (🔵 중급)

같은 모델은 한 요소에 하나만 둘 수 있으므로, 같은 기능이 여러 개인 기기(멀티 소켓, 2구 스위치, 여러 채널 조명)는 요소를 나눕니다. 첫 요소(**primary element**)의 주소가 노드 주소가 되고, 나머지 요소는 연속된 주소를 받습니다.

| 개념 | 설명 |
|---|---|
| 요소 (element) | 주소를 가진 모델 묶음. 위치를 나타내는 `Location`(GATT Namespace Descriptor 값) 포함 |
| **Composition Data** | 노드의 회사 ID(CID)·제품 ID(PID)·버전(VID)·재생 보호 목록 크기·기능 비트, 요소별 SIG/Vendor 모델 목록. `Config Composition Data Get`으로 읽음 |
| 모델 ID | SIG 모델 16비트, Vendor 모델 32비트(회사 ID 16 + 모델 16) |
| 확장(extend) | 상위 모델이 하위 모델 상태를 공유 (예: Light Lightness Server는 Generic Level·OnOff를 확장) |
| 바인딩 | 모델마다 사용할 AppKey를 `Config Model App Bind`로 지정 |

## 대표 모델 (🔵 중급)

| 모델 (Server ID) | 주요 상태 | 대표 메시지 | 쓰임 |
|---|---|---|---|
| Configuration Server (`0x0000`) / Client (`0x0001`) | 키 목록, 발행·구독, Relay·Proxy·Friend 설정 | `Config AppKey Add`, `Config Model Publication Set` | 모든 노드 필수(Server). DevKey로만 접근 |
| Health Server (`0x0002`) / Client (`0x0003`) | 고장(fault) 목록, Attention | `Health Fault Get`, `Health Attention Set` | 진단. 모든 노드의 primary element에 필수 |
| Generic OnOff Server (`0x1000`) / Client (`0x1001`) | Generic OnOff (0/1) | `Generic OnOff Get/Set/Set Unacknowledged/Status` | 스위치·콘센트 |
| Generic Level Server (`0x1002`) | Generic Level (부호 있는 16비트) | `Generic Level Set`, `Generic Delta Set`, `Generic Move Set` | 디머 다이얼, 블라인드 |
| Light Lightness Server (`0x1300`) | Lightness Actual/Linear, Last, Default, Range | `Light Lightness Set` | 밝기 조절 조명 |
| Light CTL Server (`0x1303`) | Lightness + 색온도(Temperature) + Delta UV | `Light CTL Set` | 색온도 가변 조명 |
| Light HSL Server (`0x1307`) | Hue, Saturation, Lightness | `Light HSL Set` | 컬러 조명 |
| Light LC Server (`0x130F`) | LC Mode, Occupancy Mode, Light OnOff, 상태 기계·조도 PI 제어 | `Light LC Mode Set`, 센서 상태 수신 | 재실·조도 연동 자동 조명 (컨트롤 모델) |
| Sensor Server (`0x1100`) | Sensor Descriptor, Sensor Data(Property ID별 값), Cadence | `Sensor Get`, `Sensor Status` | 재실·조도·온도·전력 센서 |
| Scene Server (`0x1203`) | Scene Register (최대 저장 장면), Current Scene | `Scene Store`, `Scene Recall` | "회의 모드" 같은 장면 일괄 호출 |

Set 메시지는 **Acknowledged**(Status 응답 있음)와 **Unacknowledged** 두 형태가 있습니다. 그룹 주소로 수십 개 조명을 제어할 때는 응답 폭주를 피하려고 Unacknowledged를 반복 송신하는 것이 일반적입니다. 대부분의 Set에는 `TID`(중복 판별), `Transition Time`(전환 시간), `Delay` 파라미터가 붙습니다.

## NLC 프로파일 (🔵 중급)

모델만으로는 "어떤 조명 제품이 어떤 모델 조합을 갖춰야 하는가"가 정해지지 않아 상호운용 수준이 제품마다 달랐습니다. SIG는 2023년 **NLC**(Networked Lighting Control) 프로파일을 발표해 상업용 조명 기기 유형별 필수 모델·동작을 정했습니다.

| NLC 프로파일 | 기기 역할 |
|---|---|
| Basic Lightness Controller (BLCNLCP) | 조명 제어기 — Light Lightness, Light LC 등으로 재실·조도 연동 |
| Occupancy Sensor (OCSNLCP) | 재실 센서 |
| Ambient Light Sensor (ALSNLCP) | 조도 센서 |
| Dimming Control (DICNLCP) | 벽 스위치·디머 |
| Basic Scene Selector (BSSNLCP) | 장면 선택 스위치 |
| Energy Monitor (ENMNLCP) | 에너지 계측 |

각 프로파일의 필수 모델 목록은 해당 프로파일 규격 원문에서 확인해야 합니다.

[[TIP("🔴 전문가 노트 — opcode, 상태 바인딩, Light LC")]]
**opcode 형식.** 1바이트(`0xxxxxxx`, `0x7F` 예약), 2바이트(`10xxxxxx` …, SIG 모델), 3바이트(`11xxxxxx` + 16비트 회사 ID, Vendor 모델)입니다. 예: Generic OnOff Get/Set/Set Unacknowledged/Status = `0x8201`/`0x8202`/`0x8203`/`0x8204`. 비분할 메시지의 Access 페이로드는 최대 11바이트이므로, 2바이트 opcode면 파라미터는 9바이트 이하여야 한 패킷에 들어갑니다.

**상태 바인딩.** Light Lightness Actual은 Generic Level과 $\text{Level} = \text{Lightness} - 32768$ 관계로 묶이고, Generic OnOff Set(1)은 Lightness를 Last 또는 Default 값으로 복원합니다. 서로 다른 제조사의 디머(Generic Level Client)가 조명(Light Lightness Server)을 제어할 수 있는 이유가 이 바인딩입니다. Lightness Linear와 Actual은 제곱 관계(인지 밝기 보정)입니다.

**Light LC.** 재실 감지 → Fade On → Run → Fade → Prolong → Fade Standby 같은 상태 기계와 조도 센서 피드백 PI 제어기를 포함합니다. LC Server는 Light Lightness Server와 **다른 요소**에 있어야 합니다(같은 Generic OnOff 상태를 겹쳐 쓰지 않도록).

**Publish 주기와 Sensor Cadence.** 센서는 값 변화량·범위에 따라 발행 주기를 빠르게 바꾸는 Cadence를 지원합니다. 배터리 센서는 LPN으로 동작하면서 발행만 하는 구성이 흔합니다.
[[/TIP]]

## 관련 페이지

- **네트워크·전송·접근 계층** — opcode가 실리는 Access 계층
- **Mesh 1.1** — Opcodes Aggregator, Large Composition Data, 모델 메타데이터
- **프로비저닝** — 설정(Configuration) 단계로 이어지는 흐름
- **대표 GATT 서비스** — 연결 기반 LE의 서비스 모델과 비교
