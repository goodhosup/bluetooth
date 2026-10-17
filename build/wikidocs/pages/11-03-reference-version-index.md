[[TIP("📘 규격 · 버전")]]
Bluetooth Core Specification 1.1 ~ 6.3 · 각 버전의 변경 내역은 해당 Core 규격 Vol 1 Part C(Changes)와 SIG의 기능 개요 문서
2024년 6.0 이후 SIG는 Core 개정을 더 자주(대략 반년 단위) 발행하고 있습니다 — 6.1 (2025.5), 6.2 (2025.11), 6.3 (2026.5)
[[/TIP]]

[TOC]


[[TIP("🟢 한눈에 보기")]]
"이 기능은 몇 버전부터인가?"와 "이 책 어디에 설명되어 있나?"를 한 표에서 찾는 페이지입니다.

1. Core 버전은 **기능의 묶음**이지 제품 등급이 아닙니다. "Bluetooth 5.3 칩"이라도 5.3의 선택 기능을 모두 지원하는 것은 아닙니다.
2. 실제 지원 여부는 Controller의 **지원 기능 비트**(`HCI_LE_Read_Local_Supported_Features`)와 Host 스택으로 확인합니다.
3. 연도별 개요는 **Bluetooth 세대와 Core 버전**에서 이야기 형식으로 볼 수 있습니다.
[[/TIP]]

## Classic 시대 (1.1–3.0) (🔵 중급)

| 버전 | 연도 | 기능 | 이 책 페이지 |
|---|---|---|---|
| 1.1 | 2001 | IEEE 802.15.1-2002의 기반, 피코넷·주파수 도약 | **피코넷과 기저대역** |
| 1.2 | 2003 | AFH (적응형 주파수 도약) | **주파수 도약과 AFH** |
| 1.2 | 2003 | eSCO (재전송 가능한 음성 링크) | **ACL과 SCO/eSCO** |
| 1.2 | 2003 | 빠른 연결 (조회 개선) | **조회와 페이징** |
| 2.0 + EDR | 2004 | EDR 2/3 Mbps (π/4-DQPSK, 8DPSK) | **디지털 변조 (GFSK·DPSK)** |
| 2.1 + EDR | 2007 | SSP (Secure Simple Pairing) | **Classic 보안 (SSP)** |
| 2.1 + EDR | 2007 | EIR (확장 조회 응답) | **조회와 페이징** |
| 2.1 + EDR | 2007 | Sniff Subrating | **링크 관리자 (LMP)** |
| 3.0 + HS | 2009 | AMP (802.11 이용 고속 전송) — 5.3에서 규격에서 제거 | **Bluetooth 세대와 Core 버전** |

## LE 4.x–5.x (🔵 중급)

| 버전 | 연도 | 기능 | 이 책 페이지 |
|---|---|---|---|
| 4.0 | 2010 | Bluetooth Low Energy (PHY, LL, ATT/GATT, SMP) | **LE 컨트롤러**, **GATT** |
| 4.1 | 2013 | LE 역할 동시 수행, LE L2CAP CoC | **링크 계층 상태 기계**, **L2CAP** |
| 4.2 | 2014 | LE Data Length Extension | **데이터 길이 확장 (DLE)** |
| 4.2 | 2014 | LE Secure Connections | **LE 페어링과 본딩** |
| 4.2 | 2014 | LE Privacy 1.2 (Controller 주소 해석) | **프라이버시와 RPA** |
| 5.0 | 2016 | LE 2M PHY, LE Coded PHY | **LE PHY (1M·2M·Coded)** |
| 5.0 | 2016 | 확장 광고 | **확장 광고** |
| 5.0 | 2016 | 주기적 광고 | **주기적 광고와 PAwR** |
| 5.0 | 2016 | 채널 선택 알고리즘 #2 | **채널 선택 알고리즘** |
| 5.1 | 2019 | 방향 탐지 (AoA/AoD, CTE) | **방향 탐지 (AoA·AoD)** |
| 5.1 | 2019 | GATT Caching | **GATT** |
| 5.1 | 2019 | 광고 채널 인덱스 무작위화 | **레거시 광고** |
| 5.2 | 2019.12 | LE 등시성 채널 (CIS/BIS) | **등시성 채널 (CIS·BIS)** |
| 5.2 | 2019.12 | EATT | **EATT** |
| 5.2 | 2019.12 | LE 전력 제어 | **LE 전력 제어** |
| 5.3 | 2021 | 연결 서브레이팅 | **연결 이벤트와 파라미터** |
| 5.3 | 2021 | 주기적 광고 강화 (ADI) | **주기적 광고와 PAwR** |
| 5.3 | 2021 | 채널 분류 강화 | **채널 선택 알고리즘** |
| 5.3 | 2021 | 암호 키 길이 제어 | **키 계층과 CTKD** |
| 5.4 | 2023 | PAwR (응답 슬롯이 있는 주기적 광고) | **주기적 광고와 PAwR** |
| 5.4 | 2023 | 암호화된 광고 데이터 | **암호화된 광고 데이터** |
| 5.4 | 2023 | LE GATT Security Levels 특성 | **GATT** |
| 5.4 | 2023 | 광고 코딩 선택 | **확장 광고** |

## 6.x (🔵 중급)

| 버전 | 연도 | 기능 | 이 책 페이지 |
|---|---|---|---|
| 6.0 | 2024.9 | Channel Sounding | **Channel Sounding**, **Channel Sounding 활용** |
| 6.0 | 2024.9 | 결정 기반 광고 필터링 | **스캔과 필터** |
| 6.0 | 2024.9 | Monitoring Advertisers | **스캔과 필터** |
| 6.0 | 2024.9 | ISOAL 강화 | **등시성 채널 (CIS·BIS)** |
| 6.0 | 2024.9 | LL 확장 기능 집합, 프레임 간격 갱신 | **LL 제어 절차** |
| 6.1 | 2025.5 | RPA 갱신 시점 무작위화 (Controller가 주소 교체 시점을 무작위로) | **프라이버시와 RPA** |
| 6.2 | 2025.11 | 더 짧은 연결 간격 (최소 375 µs, 125 µs 단위) | **연결 이벤트와 파라미터** |
| 6.2 | 2025.11 | Channel Sounding 진폭 기반 공격 대응 | **Channel Sounding** |
| 6.2 | 2025.11 | HCI USB LE 등시성 지원 (Bulk Serialization Mode) | **HCI 명령과 이벤트** |
| 6.2 | 2025.11 | LE 시험 모드 강화 (Unified Test Protocol, OTA 시험) | **RF 시험과 안테나** |
| 6.3 | 2026.5 | CS Inline PCT Transfer, PHY별 RTT 정확도 | **Channel Sounding** |
| 6.3 | 2026.5 | HCI 지원 명령 비트맵·LE 이벤트 마스크 확장 | **HCI 명령과 이벤트** |
| 6.3 | 2026.5 | BR/EDR·LE RF 요구 정렬 | **RF 시험과 안테나** |
| 6.x 이후 | 논의 중 | 상위 대역 확장, HDT 등 | **HDT와 상위 대역 확장**, **Core 6.0–6.3** |

[[TIP("🔴 전문가 노트 — 버전 표기를 읽는 법")]]
**"5.x 지원"의 실제 의미.** 새 Core 버전의 기능 대부분은 선택(optional)입니다. 제품 사양에 "Bluetooth 5.3"이라고 쓰여 있어도 2M PHY나 확장 광고가 없을 수 있습니다. 인증 목록의 설계 정보(ICS)나 Controller 지원 기능 비트가 실제 판단 근거입니다.

**Host와 Controller 버전 분리.** `HCI_Read_Local_Version_Information`이 돌려주는 HCI·LMP/LL 버전은 Controller 기준입니다. Host 스택이 그 기능을 쓰지 못하면 앱에는 보이지 않습니다. 예를 들어 Controller가 ISO를 지원해도 Host에 LE Audio 프로파일이 없으면 LE Audio를 쓸 수 없습니다.

**기능 이름 변경.** 같은 기능이 버전에 따라 이름이 바뀌기도 합니다(예: Master/Slave → Central/Peripheral 용어 변경, `HCI_LE_Start_Encryption` → `HCI_LE_Enable_Encryption`). 오래된 문서와 새 규격을 비교할 때 주의합니다.
[[/TIP]]

## 관련 페이지

- **Bluetooth 세대와 Core 버전** — 버전의 흐름과 배경
- **Core 6.0–6.3** — 최신 버전 상세
- **규격 인덱스** — 기능이 규격 어디에 있는지
