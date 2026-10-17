[[TIP("📘 규격 · 버전")]]
Core v6.0 Vol 3 Part C (Generic Access Profile) · AD Type 정의: Core Specification Supplement (CSS) Part A · Appearance 값: Assigned Numbers
Core 4.0 LE 역할·모드·절차 → 4.1 역할 동시 수행 → 5.0 확장 광고·Coded PHY용 타이밍 → 5.4 PAwR·암호화된 광고 관련 절차
[[/TIP]]

[TOC]


[[TIP("🟢 한눈에 보기")]]
**GAP**(Generic Access Profile)는 "Bluetooth 기기라면 누구나 지켜야 할 만남의 예절"입니다.

1. **역할(Role)**: 광고만 하는가(Broadcaster), 듣기만 하는가(Observer), 연결을 받는가(Peripheral), 연결을 거는가(Central)
2. **모드(Mode)**: 지금 남에게 보이는가(발견 가능), 연결을 받는가(연결 가능), 페어링 정보를 저장하는가(본딩 가능)
3. **절차(Procedure)**: 기기 찾기, 이름 알아내기, 연결하기, 본딩하기를 어떤 순서·타이밍으로 할지
4. 모든 GATT 서버에 들어가는 **GAP 서비스(0x1800)**: 기기 이름, 외형(Appearance) 등

링크 계층이 "광고 PDU를 어떻게 보내나"를 정한다면, GAP는 "언제, 어떤 플래그로, 얼마나 오래 보내야 상대가 찾을 수 있나"를 정합니다.
[[/TIP]]

## 네 가지 역할 (🔵 중급)

| 역할 | 송신 | 수신 | 연결 | 예 |
|---|---|---|---|---|
| **Broadcaster** | 광고 | — | 불가 | 비콘, 온도 태그 |
| **Observer** | — | 스캔 | 불가 | 비콘 수집 게이트웨이 |
| **Peripheral** | 연결 가능 광고 | — | 연결을 받음 (LL Peripheral) | 심박계, 키보드, 이어버드 |
| **Central** | — | 스캔 | 연결을 시작 (LL Central) | 휴대폰, PC, 허브 |

4.1부터 한 기기가 여러 역할을 동시에 수행할 수 있습니다. 예를 들어 스마트워치는 휴대폰에 대해서는 Peripheral, 심박 벨트에 대해서는 Central이 됩니다. 역할 이름은 5.3 무렵부터 규격 용어가 Master/Slave에서 **Central/Peripheral**로 바뀌었습니다.

## 모드와 절차 (🔵 중급)

| 구분 | 모드 (상대에게 어떻게 보이나) | 대응 절차 (상대가 하는 일) |
|---|---|---|
| 발견 | 비발견(Non-discoverable) / **제한 발견(Limited)** / **일반 발견(General)** 가능 모드 | 제한 발견 / 일반 발견 절차 |
| 연결 | 비연결 / 지향성(Directed) 연결 가능 / 비지향성 연결 가능 모드 | 자동·일반·선택적·직접 연결 수립 절차 |
| 본딩 | 비본딩 / 본딩 가능 모드 | 본딩 절차 (SMP 페어링 + 키 저장) |
| 기타 | — | 이름 발견, 연결 파라미터 갱신, 연결 종료 절차 |

발견 모드는 광고 데이터의 **Flags** AD 구조로 표시합니다. 제한 발견 모드는 LE Limited Discoverable 비트를, 일반 발견 모드는 LE General Discoverable 비트를 켭니다. 일반 발견 절차를 수행하는 Central은 두 비트 중 하나라도 켜진 기기를 보여 주고, 제한 발견 절차는 Limited 비트만 봅니다. 제한 발견 모드는 버튼을 누른 직후처럼 짧은 시간(최대 TGAP(lim_adv_timeout) = 180초)만 유지합니다. → **광고 데이터 형식**

## 권장 타이밍 파라미터 (TGAP) (🔵 중급)

GAP는 사용자 체감 속도와 전력을 맞추기 위한 권장값을 정의합니다. 핵심 아이디어는 **처음 30초 정도는 빠르게, 그 뒤로는 느리게**입니다.

| 파라미터 | 권장값 | 의미 |
|---|---|---|
| TGAP(adv_fast_period) | 30 s | 빠른 광고를 유지하는 시간 |
| TGAP(adv_fast_interval1) | 30–60 ms | 사용자가 기다리는 상황의 연결 가능 광고 간격 |
| TGAP(adv_fast_interval2) | 100–150 ms | 백그라운드 빠른 광고 간격 |
| TGAP(adv_slow_interval) | 1–1.2 s | 느린 광고 간격 |
| TGAP(scan_fast_period) | 30.72 s | 빠른 스캔 유지 시간 |
| TGAP(scan_fast_interval) / window | 30–60 ms / 30 ms | 빠른 스캔 (듀티 50–100 %) |
| TGAP(scan_slow_interval1) / window1 | 1.28 s / 11.25 ms | 백그라운드 스캔 |
| TGAP(scan_slow_interval2) | 2.56 s | 더 느린 백그라운드 스캔 |
| TGAP(lim_adv_timeout) | 180 s | 제한 발견 모드 최대 시간 |
| TGAP(gen_disc_scan_min) / TGAP(lim_disc_scan_min) | 10.24 s | 발견 절차의 최소 스캔 시간 |

5.0에서는 Coded PHY용으로 이 간격들을 늘린 변형 값(`_coded` 접미사)이 추가되었습니다. 구체적 값은 규격 원문 확인 필요.

## Appearance와 기기 이름 (🔵 중급)

| 항목 | 위치 | 형식 |
|---|---|---|
| **Device Name** | GAP 서비스 특성 0x2A00, 광고의 Local Name AD (0x08/0x09) | UTF-8, 최대 248바이트. 광고에는 줄인 이름(Shortened)을 넣고 연결 후 전체 이름을 읽게 할 수 있음 |
| **Appearance** | GAP 서비스 특성 0x2A01, 광고의 Appearance AD (0x19) | 16비트 = 카테고리(상위 10비트) + 서브카테고리(하위 6비트) |
| Peripheral Preferred Connection Parameters | 특성 0x2A04 (선택) | 선호 연결 간격 최소·최대, 지연, 타임아웃 |
| Central Address Resolution | 특성 0x2AA6 | Central이 RPA를 대상 주소로 한 지향성 광고를 해석할 수 있는지 |

| Appearance 값 | 카테고리.서브 | 의미 |
|---|---|---|
| 0x0000 | 0.0 | Unknown |
| 0x0040 | 1.0 | Generic Phone |
| 0x00C0 | 3.0 | Generic Watch |
| 0x0340 / 0x0341 | 13.0 / 13.1 | Generic Heart Rate Sensor / Heart Rate Belt |
| 0x03C0 / 0x03C1 / 0x03C2 | 15.0 / 15.1 / 15.2 | Generic HID / Keyboard / Mouse |

휴대폰 설정 화면의 기기 아이콘은 주로 Appearance(또는 Classic의 Class of Device)로 고릅니다.

[[TIP("🔴 전문가 노트 — 프라이버시, 이름 노출, 플랫폼 동작")]]
**이름은 개인정보다.** "홍길동의 이어폰" 같은 이름을 광고에 그대로 넣으면 RPA로 주소를 숨겨도 추적이 가능합니다. 프라이버시가 중요한 제품은 광고에서 이름을 빼고, 본딩 후 GATT로만 읽게 하거나 **암호화된 광고 데이터**를 씁니다. 같은 이유로 RPA 갱신 주기 TGAP(private_addr_int)의 권장값은 15분입니다. → **프라이버시와 RPA**

**Device Name 쓰기.** 0x2A00은 쓰기 가능하게 만들 수도 있습니다(사용자가 이름 바꾸기). 이 경우 인증된 연결에서만 쓰기를 허용하는 것이 안전합니다.

**플랫폼의 스캔 동작.** 휴대폰 OS는 앱이 요청한 스캔 파라미터를 그대로 쓰지 않고, 화면 상태·백그라운드 여부에 따라 TGAP 권장값과 비슷한 빠른/느린 스캔을 오갑니다. 그래서 Peripheral은 처음 30초 동안 짧은 간격으로 광고해야 "앱을 열자마자 보이는" 경험을 줍니다. Apple은 별도 가이드(QA1931)에서 처음 30초 동안 20 ms 간격, 이후 152.5 ms·211.25 ms·318.75 ms 등 정해진 간격을 권장합니다.

**연결 파라미터 갱신 절차.** GAP의 Connection Parameter Update 절차는 Peripheral이 L2CAP 시그널링 또는 LL 절차로 요청하고 Central이 최종 결정하는 구조입니다. 갱신 요청은 연결 직후 바로 보내지 말고 TGAP(conn_param_timeout) 30초 정도 기다리라는 권장이 있으며, 탐색이 끝난 뒤 느린 간격으로 바꾸는 것이 일반적입니다.
[[/TIP]]

## Classic ↔ LE 비교 (🔵 중급)

| 항목 | Classic (BR/EDR) | LE |
|---|---|---|
| 발견 | Inquiry / Inquiry Scan, EIR | 광고 / 스캔, AD 구조 |
| 발견 가능 표시 | Inquiry Scan 활성 + IAC(GIAC/LIAC) | Flags AD의 Limited/General 비트 |
| 연결 | Page / Page Scan | 연결 가능 광고 + `CONNECT_IND` |
| 기기 종류 | Class of Device (24비트) | Appearance (16비트) |
| 이름 | Remote Name Request (LMP) | GAP 서비스 Device Name 또는 광고 Local Name |

## 관련 페이지
- **광고 데이터 형식 (AD Type)** — Flags, Local Name, Appearance AD
- **레거시 광고** — 광고 PDU 종류와 간격
- **스캔과 필터** — 스캔 간격·윈도·필터 정책
- **연결 수립** — `CONNECT_IND`와 연결 파라미터
- **LE 페어링과 본딩** — 본딩 절차
