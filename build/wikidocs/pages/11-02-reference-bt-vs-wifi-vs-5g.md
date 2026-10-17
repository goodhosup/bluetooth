[[TIP("📘 규격 · 버전")]]
Bluetooth: Bluetooth SIG Core v6.0 (2024.9) · Wi-Fi: IEEE 802.11-2024, 802.11be(Wi-Fi 7) · 5G NR: 3GPP TS 38 시리즈 (Rel-15 이후)
자매 핸드북: [Wi-Fi 핸드북](https://goodhosup.github.io/wifi/), [셀룰러 핸드북 (LTE·5G NR)](https://goodhosup.github.io/cellular/)
[[/TIP]]

[[TIP("🟢 한눈에 보기")]]
세 기술은 경쟁 관계라기보다 **거리와 역할이 다른 층**입니다.

1. **Bluetooth** — 몸 주변·방 안(수 m–수십 m)의 개인 기기를 아주 적은 전력으로 잇습니다. 이어폰, 시계, 센서.
2. **Wi-Fi** — 건물 안(수십 m)에서 인터넷 접속을 빠르게 나눠 씁니다. 노트북, TV, 공유기.
3. **5G NR** — 사업자 기지국을 통해 km 단위로 이동 중에도 연결을 유지합니다. 스마트폰, 차량, 산업망.

스마트폰은 셋을 모두 갖고 있고, 같은 2.4 GHz를 쓰는 Bluetooth와 Wi-Fi는 칩 안에서 시간을 나눠 씁니다.
[[/TIP]]

## 기본 특성 (🔵 중급)

| 항목 | Bluetooth (LE / Classic) | Wi-Fi (802.11) | 5G NR |
|---|---|---|---|
| 표준화 | Bluetooth SIG | IEEE 802.11 + Wi-Fi Alliance(인증) | 3GPP |
| 주파수 | 2.4 GHz ISM (2402–2480 MHz) | 2.4 / 5 / 6 GHz (비면허) | FR1 (7.125 GHz 이하), FR2 (mmWave), 주로 면허 대역 |
| 채널 폭 | LE 2 MHz, Classic 1 MHz | 20–320 MHz (Wi-Fi 7) | FR1 최대 100 MHz, FR2 최대 400 MHz (반송파당) |
| 변조 | GFSK (EDR: DPSK) | OFDM/OFDMA, 최대 4096-QAM (Wi-Fi 7) | OFDM(+DFT-s-OFDM 상향), 최대 256-QAM(일부 1024-QAM) |
| 다중 접속 | 연결 이벤트 스케줄(Central 주도), 주파수 도약 | CSMA/CA 경쟁 + OFDMA/트리거 | 기지국 스케줄링 (OFDMA) |
| 간섭 회피 | 도약, AFH, 채널 맵 | LBT, 채널 선택, DFS | 면허 대역, 셀 계획, 빔포밍 |
| 전형적 거리 | 수 m–수십 m (Coded PHY는 더 멀리) | 수십 m | 수백 m–수 km |

## 성능·전력·용도 (🔵 중급)

| 항목 | Bluetooth | Wi-Fi | 5G NR |
|---|---|---|---|
| 데이터율 | LE 응용 처리량 상한 약 791 kbps (1M)·1402 kbps (2M), Classic 3-DH5 2178.1 kbps | 수백 Mbps–수 Gbps (실사용) | 수백 Mbps–수 Gbps (망·대역에 따라) |
| 지연 | 연결 간격에 따라 ms–수 s, ISO로 결정적 지연 | 경쟁에 따라 변동, ms 단위 | 스케줄 기반, URLLC 목표 1 ms 수준 |
| 송신 전력 | −20 ~ +20 dBm (대개 0–10 dBm) | 대개 15–23 dBm 급 | 단말 23 dBm 급 (전력 등급 3) |
| 평균 전력 | µA 단위 가능 (코인셀 수년) | 수십–수백 mW (TWT로 절감) | 수백 mW–W (DRX·PSM·RedCap으로 절감) |
| 망 구조 | 기기 간 직접 (P2P, 브로드캐스트, Mesh) | AP 중심 BSS (+ Wi-Fi Direct, 메시) | 사업자 코어망 + 기지국 |
| 보안 | 페어링 (LE SC, ECDH P-256), AES-CCM | WPA3 (SAE), AES-CCMP/GCMP | SIM 기반 5G-AKA, 128비트 NEA/NIA |
| 측위 | AoA/AoD, Channel Sounding (위상·RTT) | 802.11mc/az FTM (RTT) | PRS 기반 측위 (Rel-16~) |
| 대표 용도 | 오디오, 웨어러블, 센서, 비콘, 디지털 키 | 인터넷 접속, 영상, 대용량 전송 | 이동통신, FWA, 산업 IoT, V2X |

[[TIP("🔴 전문가 노트 — 함께 쓰는 지점")]]
**2.4 GHz 공존.** Bluetooth와 Wi-Fi 콤보 칩은 PTA(Packet Traffic Arbitration) 같은 공존 인터페이스로 순간순간 무선 사용권을 나눕니다. 5G/LTE의 일부 대역(예: 2.3 GHz, 2.5–2.6 GHz 대역)은 ISM 대역 가장자리에 붙어 있어 단말 내부 간섭 문제가 생기며, Core 규격의 MWS 공존 인터페이스(Vol 7)가 이를 다룹니다. → **Wi-Fi와의 공존**

**역할 분담의 예.** Matter 기기는 Bluetooth LE로 초기 설정(커미셔닝)을 한 뒤 Wi-Fi나 Thread로 운용합니다. 차량 디지털 키는 LE로 접근을 감지하고 UWB나 Channel Sounding으로 거리를 잽니다. → **Matter·Thread와 Bluetooth**

**비교 수치의 주의점.** 표의 Wi-Fi·5G 데이터율은 구성(대역폭, MIMO 계층, 망 부하)에 따라 수십 배까지 달라집니다. 자세한 수치는 자매 핸드북을 참고하십시오.
[[/TIP]]

## 관련 페이지

- **Classic vs LE 비교** — Bluetooth 안의 두 시스템
- **2.4 GHz ISM 대역과 규제** — 공유 대역 규칙
- **Wi-Fi와의 공존** — 같은 대역 공존
- [Wi-Fi 핸드북](https://goodhosup.github.io/wifi/) — 802.11 상세 (외부)
- [셀룰러 핸드북](https://goodhosup.github.io/cellular/) — LTE·5G NR 상세 (외부)
