# Classic vs LE 비교

!!! spec "규격 · 버전"
    Core v6.0 Vol 2 (BR/EDR Controller: Radio, Baseband, LMP) · Vol 6 (LE Controller: PHY, Link Layer) · Vol 3 (Host: L2CAP, SDP, GAP, ATT/GATT, SMP)
    BR 1.x → EDR 2.0(2004) → SSP 2.1(2007) → LE 4.0(2010) → LE 2M·Coded 5.0(2016) → LE Audio(ISO 5.2, 2019.12) → Channel Sounding 6.0(2024.9)

!!! basic "한눈에 보기"
    Classic(BR/EDR)과 LE는 같은 2.4 GHz 대역과 같은 상표를 쓰지만, **서로 다른 두 무선 시스템**입니다. 하나의 칩이 둘을 모두 지원하는 듀얼 모드가 흔할 뿐, 패킷·채널·연결 방식이 호환되지 않습니다.

    1. **Classic** — 계속 연결된 스트림에 강함: 오디오(A2DP·HFP), 차량, 시리얼 대체.
    2. **LE** — 짧게 깨어나 조금 보내는 데 강함: 센서, 웨어러블, 비콘, 위치, 그리고 이제 오디오(LE Audio)까지.

## 무선·링크 { .l2 }

| 항목 | Classic (BR/EDR) | LE |
|---|---|---|
| 채널 | 79개, 1 MHz 간격 (2402–2480 MHz) | 40개, 2 MHz 간격 (광고 37/38/39 = 2402/2426/2480 MHz, 데이터 0–36) |
| 변조 | GFSK (BR 1 Mbps), π/4-DQPSK (2 Mbps), 8DPSK (3 Mbps) | GFSK: 1M, 2M, Coded S=2 (500 kbps), S=8 (125 kbps) |
| 주파수 도약 | 슬롯(625 µs)마다, 초당 1600 홉, AFH | 연결 이벤트마다 1회 (CSA #1, #2), 채널 맵으로 회피 |
| 시간 단위 | 슬롯 625 µs, 패킷 1·3·5 슬롯 | 연결 간격 7.5 ms–4 s (1.25 ms 단위; 6.2에서 더 짧은 간격 추가), T_IFS 150 µs |
| 최대 처리량 (계산) | DH5 723.2 kbps, 2-DH5 1448.5 kbps, 3-DH5 2178.1 kbps (비대칭) | 1M 약 791 kbps, 2M 약 1402 kbps (251 B PDU, 응용 계층 상한) |
| 송신 전력 | Class 1 최대 20 dBm, Class 2 4 dBm, Class 3 0 dBm | −20 dBm ~ +20 dBm |
| 수신 감도 요구 | −70 dBm (BER 0.1 %) | 1M·2M −70 dBm, Coded S2 −75, S8 −82 dBm |
| 장거리 수단 | Class 1 출력 | Coded PHY (FEC로 감도 향상) |

## 연결·전력·오디오 { .l2 }

| 항목 | Classic (BR/EDR) | LE |
|---|---|---|
| 발견 | 조회(Inquiry) + 조회 응답·EIR | 광고 + 스캔 (응답, 확장 광고) |
| 연결 수립 | 페이징(Paging), 보통 수백 ms–수 초 | `CONNECT_IND` 한 번, 수 ms 수준 |
| 연결 없는 통신 | 거의 없음 (Connectionless Peripheral Broadcast) | 광고·주기적 광고·PAwR·BIS가 핵심 기능 |
| 링크 제어 | LMP | LL 제어 PDU |
| 저전력 수단 | Sniff, Sniff Subrating, Hold | 긴 간격, Peripheral Latency, 서브레이팅 |
| 평균 전류 대략 | 연결 유지 시 수백 µA 이상인 경우가 많음 | µA 단위 가능 ([전류 프로파일](../practice/power-profile.md)) |
| 음성·오디오 | SCO/eSCO (CVSD, mSBC, LC3-SWB), A2DP over ACL (SBC, AAC 등) | ISO (CIS·BIS) + LC3, LE Audio 프로파일, Auracast |
| 서비스 탐색 | SDP | GATT 서비스 탐색 |
| 대표 데이터 프로파일 | SPP(RFCOMM), HID, PAN, OBEX | GATT 서비스, HOGP, L2CAP CoC |

## 보안·토폴로지·용도 { .l2 }

| 항목 | Classic (BR/EDR) | LE |
|---|---|---|
| 페어링 | 레거시 PIN(2.0 이하), SSP (2.1~), Secure Connections (P-256) | 레거시 페어링 (4.0), LE Secure Connections (4.2~, P-256) |
| 암호화 | E0 (레거시), AES-CCM (Secure Connections) | AES-CCM |
| 키 교차 유도 | CTKD로 LE 키 유도 가능 | CTKD로 BR/EDR 링크 키 유도 가능 |
| 프라이버시 | 고정 BD_ADDR | Random 주소, RPA (4.2 Controller 해석) |
| 토폴로지 | 피코넷 (Central 1 + 활성 Peripheral 최대 7), 스캐터넷 | 스타, 다중 연결, 브로드캐스트, Mesh(광고 위) |
| 측위 | — | 방향 탐지(AoA/AoD), Channel Sounding |
| 주 용도 | 헤드셋·스피커, 차량 핸즈프리, 레거시 시리얼 | 센서, 웨어러블, 비콘, 의료, 스마트홈, LE Audio·보청기, 위치 |

??? expert "전문가 노트 — 듀얼 모드에서 헷갈리는 점"
    **같은 주소, 다른 링크.** 듀얼 모드 기기는 BR/EDR과 LE에서 같은 공개 주소를 쓸 수 있지만, 링크와 키는 따로입니다. CTKD를 쓰지 않으면 한쪽에서 본딩해도 다른 쪽은 다시 페어링해야 합니다. → [키 계층과 CTKD](../security/keys.md)

    **안테나·시간 공유.** 듀얼 모드 칩은 하나의 무선을 시분할하므로, A2DP 스트리밍 중에는 LE 스캔·연결 이벤트가 밀리기 쉽습니다. Wi-Fi까지 공존하면 우선순위 설정이 필요합니다. → [Wi-Fi와의 공존](../basics/coexistence.md)

    **이름은 같아도 다른 "채널 37".** Classic의 채널 37은 2439 MHz이고, LE의 채널 37은 2402 MHz(광고 채널)입니다. 로그·시험에서 어느 체계의 번호인지 늘 확인합니다.

## 관련 페이지

- [피코넷과 기저대역](../classic/baseband.md) — Classic 슬롯과 도약
- [LE PHY (1M·2M·Coded)](../le/phy.md) — LE 물리계층
- [LE Audio 개요](../audio/overview.md) — Classic 오디오와의 차이
- [보안 모델의 진화](../security/evolution.md) — 두 보안 체계의 역사
- [Bluetooth vs Wi-Fi vs 5G](bt-vs-wifi-vs-5g.md) — 다른 무선 기술과의 비교
