[[TIP("📘 규격 · 버전")]]
GATT 구조: Core v6.0 Vol 3 Part G · 서비스·특성 UUID: Assigned Numbers · 특성 값 형식: GATT Specification Supplement (GSS) · 개별 서비스 규격: Battery Service (BAS), Device Information Service (DIS), Heart Rate Service (HRS)/Profile (HRP), HID Service (HIDS)/HID over GATT Profile (HOGP), Current Time Service (CTS)
Core 4.0과 함께 2011년 무렵부터 서비스 규격이 순차 공개 → LE Audio(2022 전후)의 PACS·ASCS·BASS 등으로 확장
[[/TIP]]

[TOC]


[[TIP("🟢 한눈에 보기")]]
GATT는 "폴더와 파일" 구조만 정합니다. 어떤 폴더에 어떤 파일이 있어야 하는지는 **서비스 규격**이 정합니다.

1. **서비스(Service) 규격** — 서버가 노출할 특성과 그 형식. 예: Battery Service = Battery Level 특성(0–100 %)
2. **프로파일(Profile) 규격** — 클라이언트와 서버가 그 서비스를 어떻게 쓰는지, 보안·광고 요구 사항. 예: HOGP = HID + Battery + Device Information 서비스를 묶어 키보드·마우스를 정의
3. 표준 서비스는 **16비트 UUID**를 받고, 회사 고유 기능은 **128비트 커스텀 UUID**를 직접 만듭니다.

표준 서비스를 쓰면 OS와 범용 앱(nRF Connect 등)이 값을 바로 해석해 주고, 호환성 시험이 쉬워집니다.
[[/TIP]]

## 서비스 UUID 표 (🔵 중급)

| UUID | 서비스 | 주요 특성 (UUID) | 비고 |
|---|---|---|---|
| 0x1800 | **GAP** | Device Name (0x2A00), Appearance (0x2A01), Peripheral Preferred Connection Parameters (0x2A04) | 모든 LE GATT 서버 필수 |
| 0x1801 | **GATT** | Service Changed (0x2A05), Client Supported Features (0x2B29), Database Hash (0x2B2A), Server Supported Features (0x2B3A) | 캐싱·EATT 협상 |
| 0x180F | **Battery** | Battery Level (0x2A19, uint8 0–100 %) | Read 필수, Notify 선택 |
| 0x180A | **Device Information** | Manufacturer Name (0x2A29), Model Number (0x2A24), Serial Number (0x2A25), Hardware/Firmware/Software Revision (0x2A27/0x2A26/0x2A28), System ID (0x2A23), PnP ID (0x2A50) | 모두 읽기 전용 |
| 0x180D | **Heart Rate** | Heart Rate Measurement (0x2A37, Notify), Body Sensor Location (0x2A38), Heart Rate Control Point (0x2A39) | |
| 0x1812 | **HID** | HID Information (0x2A4A), Report Map (0x2A4B), HID Control Point (0x2A4C), Report (0x2A4D), Protocol Mode (0x2A4E), Boot Keyboard Input Report (0x2A22) | HOGP의 핵심 |
| 0x1813 | Scan Parameters | Scan Interval Window, Scan Refresh | HOGP 선택 |
| 0x1805 | **Current Time** | Current Time (0x2A2B, Read/Notify) | 시계·센서 시간 동기 |
| 0x1802 / 0x1803 / 0x1804 | Immediate Alert / Link Loss / Tx Power | Alert Level, Tx Power Level | 분실 방지 태그(FMP·PXP) |
| 0x181A | Environmental Sensing | 온도·습도·기압 등 | |
| 0x1844 / 0x1846 / 0x184E / 0x184F / 0x1850 | VCS / CSIS / ASCS / BASS / PACS | — | LE Audio → **PACS와 ASCS** |
| 0x1854 / 0x1855 | HAS / TMAS | — | 보청기, TMAP 역할 표시 |

서비스·특성 UUID와 회사 ID, AD Type 번호는 모두 SIG의 **Assigned Numbers** 문서에 모여 있고, 특성 값의 바이트 형식은 **GATT Specification Supplement**(GSS)가 정의합니다. 같은 특성 UUID는 서비스가 달라도 같은 형식을 씁니다.

## 예 1 — Heart Rate Measurement 해석 (🔵 중급)

| 바이트 | 필드 | 설명 |
|---|---|---|
| 0 | Flags | bit 0: 심박값 형식 (0 = uint8, 1 = uint16) · bit 1–2: 센서 접촉 상태 · bit 3: Energy Expended 존재 · bit 4: RR-Interval 존재 |
| 1 (또는 1–2) | Heart Rate Value | bpm |
| (선택) 2 B | Energy Expended | kJ |
| (선택) 2 B × n | RR-Interval | 1/1024 s 단위 |

예: `16 48 2C 03 28 03` → Flags 0x16(uint8 값, 접촉 감지됨, RR 있음), 심박 0x48 = 72 bpm, RR = 0x032C = 812/1024 s ≈ 0.793 s, 0x0328 = 808/1024 s ≈ 0.789 s. RR이 여러 개면 기본 MTU(값 최대 20 B)에 다 들어가지 않을 수 있어, 서버는 오래된 RR부터 버립니다.

## 예 2 — HID over GATT (HOGP) (🔵 중급)

| HID Device(키보드)가 갖춰야 할 것 | 내용 |
|---|---|
| HID Service (1개 이상) | Report Map(HID 디스크립터), Input/Output/Feature Report, Protocol Mode(Boot/Report) |
| Battery Service | 배터리 잔량 표시 |
| Device Information Service | PnP ID(Vendor ID, Product ID, Version) — OS가 드라이버·키맵 선택에 사용 |
| 보안 | 암호화된(본딩된) 연결에서만 HID 데이터 접근 |
| 광고 | Appearance(예: 0x03C1 Keyboard)와 HID 서비스 UUID 0x1812 포함이 일반적 |

Input Report는 Notify로 전달되므로, 키 입력 지연은 대략 **연결 간격 + Peripheral Latency 운용**에 좌우됩니다. 휴대폰 OS가 HID 기기에 더 짧은 연결 간격을 허용하는 이유입니다(**처리량 최적화** 참고).

## 커스텀 128비트 UUID 설계 (🔵 중급)

1. **무작위 UUID 하나를 "기반"으로 생성**(UUID v4)하고, 서비스와 특성은 그 기반에서 한 필드(관례상 3–4번째 바이트)만 바꿔 씁니다. 예: `6E40xxxx-B5A3-F393-E0A9-E50E24DCCA9E` 계열(Nordic UART Service가 쓰는 방식).
2. **Bluetooth Base UUID(`0000xxxx-0000-1000-8000-00805F9B34FB`) 위에 임의의 16비트를 얹지 않습니다.** 그 공간은 SIG 할당용이라 미래의 표준 UUID와 충돌합니다.
3. 표준 서비스가 있는 기능(배터리, 기기 정보, 심박)은 표준 서비스를 쓰고, 커스텀 서비스에는 **제품 고유 기능만** 둡니다.
4. 광고 데이터에 128비트 UUID를 넣으면 18바이트를 쓰므로, 휴대폰 필터링에 꼭 필요한 하나만 넣습니다. → **광고 데이터 형식**
5. 앞으로 바뀔 수 있는 명령은 **제어점(Control Point) 특성** 하나에 opcode로 모으면 특성 수를 늘리지 않고 확장할 수 있습니다.

[[TIP("🔴 전문가 노트 — 16비트 회원사 UUID, 버전 관리, 흔한 실수")]]
**16비트 UUID를 직접 받을 수 있다.** SIG 회원사는 비용을 내고 16비트 서비스 UUID(0xFDxx–0xFExx 대역)를 할당받을 수 있습니다. 광고에 넣을 때 16바이트를 아끼기 위한 것으로, 대형 기기 제조사의 고유 서비스가 이 방식을 씁니다. 할당 목록은 Assigned Numbers의 Member UUIDs에 있습니다.

**Battery Service와 HID.** 키보드처럼 여러 배터리를 가진 기기는 Battery Service를 여러 인스턴스로 두고 Characteristic Presentation Format 디스크립터로 구분합니다. HID 서비스의 Report Map은 External Report Reference 디스크립터(0x2907)로 Battery Level 같은 다른 서비스의 특성을 참조할 수 있습니다.

**Device Information의 PnP ID.** Vendor ID Source(1 = SIG 회사 ID, 2 = USB-IF VID) + VID + PID + 버전. 이 값을 비워 두면 일부 OS에서 HID 기기의 키맵이나 아이콘이 기본값으로 떨어집니다.

**흔한 실수.** (1) Battery Level을 Notify로 선언하고 CCCD를 빠뜨림. (2) 문자열 특성에 NUL 종단을 넣어 앱 표시가 깨짐(GATT 문자열은 길이로 끝을 판단). (3) Heart Rate Control Point를 지원하지 않으면서 특성만 노출. (4) 표준 서비스 UUID를 쓰면서 GSS와 다른 형식으로 값을 채움 — 범용 앱이 엉뚱한 값을 보여 줍니다.
[[/TIP]]

## 관련 페이지
- **GATT** — 서비스·특성·디스크립터 구조와 탐색
- **GAP** — GAP 서비스의 Device Name과 Appearance
- **광고 데이터 형식 (AD Type)** — 서비스 UUID를 광고에 넣는 법
- **데이터 프로파일 (SPP·HID·PAN)** — Classic HID와의 비교
- **PACS와 ASCS** — LE Audio 서비스
