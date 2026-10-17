[[TIP("📘 규격 · 버전")]]
Core v6.0 Vol 2 Part B (Baseband) — 논리 전송(ACL, SCO, eSCO), 패킷 타입 · Vol 4 Part E (HCI) — 동기 연결 명령 · 음성 코덱 사용: Hands-Free Profile 1.9
Core 1.1 ACL·SCO → 1.2 eSCO(재전송 가능 음성 링크) → 2.0 + EDR 2-EV/3-EV 패킷 · HFP 1.6 mSBC 광대역 → HFP 1.9 LC3-SWB 초광대역
[[/TIP]]

[TOC]


[[TIP("🟢 한눈에 보기")]]
피코넷의 슬롯 위에는 성격이 다른 두 종류의 "차선"이 있습니다.

1. **ACL**(Asynchronous Connection-Oriented) — 일반 차선. 빈 슬롯이 있을 때 데이터를 보내고, 틀리면 될 때까지 다시 보냅니다. 파일, 제어 명령, 그리고 **A2DP 음악**이 여기로 갑니다.
2. **SCO**(Synchronous Connection-Oriented) — 버스 전용 차선. 일정한 간격의 슬롯을 미리 예약해 두고 64 kbps 음성을 정확한 박자로 보냅니다. 틀려도 다시 보내지 않습니다.
3. **eSCO**(extended SCO) — 전용 차선 + 짧은 재시도 구간. 예약 슬롯 뒤에 **재전송 창**을 두어 깨진 음성 패킷을 한두 번 다시 보낼 수 있습니다. 오늘날 **통화(HFP)**는 거의 모두 eSCO를 씁니다.

음악은 버퍼링으로 지연을 감출 수 있어 ACL이 맞고, 통화는 왕복 지연이 체감되므로 예약 슬롯을 쓰는 eSCO가 맞습니다.
[[/TIP]]

## ACL vs SCO vs eSCO (🔵 중급)

| 항목 | ACL | SCO | eSCO |
|---|---|---|---|
| 슬롯 할당 | 비예약 — Central이 폴링으로 배분 | 예약 — $T\_{SCO}$ = 2·4·6 슬롯마다 | 예약 — $T\_{eSCO}$마다 + 재전송 창 $W\_{eSCO}$ |
| 재전송 | 성공할 때까지 (Flush Timeout 전까지) | 없음 | 재전송 창 안에서만 |
| 오류 검출 | CRC | 없음 (HV는 FEC만) | CRC |
| 패킷 | DM/DH, 2-DH/3-DH | HV1·HV2·HV3 (+ DV) | EV3·EV4·EV5, 2-EV3·2-EV5, 3-EV3·3-EV5 |
| 속도 | 비대칭 최대 723.2(DH5) / 2178.1(3-DH5) kbps | 64 kbps 고정 | 설정에 따라 (대칭·비대칭 가능) |
| 링크 수 | 피코넷의 각 Peripheral과 1개 | 최대 3개 | 여러 개 (슬롯 여유 내) |
| 수립 | 페이징으로 생성 | `LMP_SCO_link_req` | `LMP_eSCO_link_req` |
| 대표 용도 | 데이터, LMP, L2CAP, A2DP | 초기 헤드셋 | HFP 통화 (CVSD·mSBC·LC3-SWB) |

HV3는 30바이트를 6슬롯(3.75 ms)마다 보내므로 $30 \times 8 / 3.75\ \text{ms} = 64$ kbps입니다. 6슬롯 중 2슬롯(왕복)만 쓰고 나머지 4슬롯은 ACL에 남습니다. HV1(FEC 1/3)은 2슬롯마다 보내야 해서 피코넷 전체를 차지합니다.

## eSCO 재전송 창 (🔵 중급)

| 파라미터 | 의미 |
|---|---|
| $T\_{eSCO}$ | 예약 주기(슬롯). 이 주기마다 새 음성 프레임 |
| $D\_{eSCO}$ | 주기 안에서 예약 슬롯의 위치(오프셋) |
| $W\_{eSCO}$ | 예약 슬롯 다음의 재전송 창(슬롯). 0이면 재전송 없음 |
| Max_Latency | 호스트가 허용하는 최대 지연(ms) — 컨트롤러가 $T\_{eSCO}$와 $W\_{eSCO}$를 고르는 상한 |
| Retransmission_Effort | 0 없음 · 1 전력 우선 · 2 품질 우선 · 0xFF 상관없음 |

HFP는 자주 쓰는 조합을 **파라미터 세트**로 정해 두었습니다. 예를 들어 광대역 통화의 **T2** 설정은 `2-EV3` 패킷 하나(60바이트)를 $T\_{eSCO}$ = 12슬롯(7.5 ms)마다 보내며, 60 B × 8 / 7.5 ms = 64 kbps가 됩니다. 남는 슬롯 일부가 재전송 창으로 쓰입니다. 정확한 세트별 값(S1–S4, T1–T2)은 HFP 규격의 표를 참고합니다.

## 음성 코덱 (🔵 중급)

| 코덱 | 샘플링 / 대역 | 링크 위 속도 | 도입 | 비고 |
|---|---|---|---|---|
| **CVSD** | 8 kHz / 협대역(전화 음질) | 64 kbps | Core 1.0부터 | 컨트롤러가 인코딩 가능(air coding), 비트 오류에 강하지만 음질 한계 |
| μ-law / A-law | 8 kHz | 64 kbps | Core | 실제 제품에서 거의 쓰이지 않음 |
| **mSBC** | 16 kHz / 광대역(**HD Voice**) | 64 kbps | **HFP 1.6** | SBC의 변형. 7.5 ms마다 57바이트 프레임 + 헤더, 호스트에서 인코딩 후 투명(transparent) 모드로 전송 |
| **LC3-SWB** | 32 kHz / 초광대역 | 약 64 kbps 수준 | **HFP 1.9** | LE Audio의 LC3를 Classic 통화에 재사용. mSBC의 후속 |

코덱은 HFP의 **코덱 협상**(`AT+BAC`, `+BCS`)으로 결정되고, 결정된 코덱에 맞춰 호스트가 eSCO 링크의 air coding(CVSD 또는 transparent)과 파라미터를 고릅니다. → **오디오 프로파일 (A2DP·AVRCP·HFP)**

[[TIP("🔴 전문가 노트 — HCI 음성 경로, A2DP와의 공존")]]
**음성 데이터 경로.** eSCO 데이터는 HCI를 통해 호스트로 올라올 수도(`HCI_Write_Voice_Setting`, HCI SCO 데이터 패킷), 칩의 PCM/I²S 핀으로 바로 나갈 수도 있습니다. 후자가 일반적이며 `HCI_Enhanced_Setup_Synchronous_Connection`의 `Input_Data_Path`/`Output_Data_Path`, 코딩 포맷(CVSD·transparent·mSBC) 필드로 지정합니다. 호스트에서 mSBC/LC3를 인코딩하는 구현은 HCI SCO 패킷 타이밍(7.5 ms마다 60바이트)을 정확히 맞춰야 합니다.

**Erroneous Data Reporting.** 재전송 창 안에서도 못 받은 프레임은 `HCI_Write_Default_Erroneous_Data_Reporting`을 켜면 "깨진 프레임" 표시와 함께 올라옵니다. 호스트는 이를 **PLC**(Packet Loss Concealment)로 감춥니다. mSBC의 H2 헤더 시퀀스 번호도 손실 검출에 쓰입니다.

**ACL 처리량과의 공존.** eSCO는 예약 슬롯을 먹으므로, 통화 중 같은 피코넷의 ACL(A2DP, 파일 전송)은 남은 슬롯만 쓸 수 있습니다. T2 설정(12슬롯 주기 안에 왕복 슬롯과 재전송 창이 함께 들어감)에서는 남은 연속 구간이 짧아 5슬롯 패킷이 들어가지 못할 때가 있습니다. 통화 중 A2DP를 멈추는(HFP가 오디오 우선권을 가져가는) 구현이 일반적인 이유입니다.

**Flush Timeout.** ACL 오디오(A2DP)는 무한 재전송이면 지연이 쌓이므로 `HCI_Write_Automatic_Flush_Timeout`으로 오래된 패킷을 버리게 하고, 이를 위해 L2CAP 패킷은 "flushable"로 표시합니다.
[[/TIP]]

## Classic ↔ LE 비교

| 항목 | Classic | LE |
|---|---|---|
| 데이터 링크 | ACL | ACL (연결 이벤트) |
| 실시간 음성·오디오 | SCO/eSCO (음성만, 대칭) | **CIS/BIS** 등시성 채널 (음성·음악, 브로드캐스트 가능) |
| 음악 | A2DP over ACL | BAP over CIS/BIS |
| 코덱 | CVSD, mSBC, LC3-SWB (통화) / SBC·AAC (음악) | LC3 (필수), LC3plus 등 선택 |
| 재전송 구조 | 재전송 창 $W\_{eSCO}$ | Flush Timeout, BN·FT·NSE 파라미터 |

## 관련 페이지

- **피코넷과 기저대역** — 패킷 타입과 슬롯
- **오디오 프로파일 (A2DP·AVRCP·HFP)** — 코덱 협상과 프로파일
- **등시성 채널 (CIS·BIS)** — LE의 실시간 오디오 링크
- **LC3 코덱** — LC3-SWB의 바탕이 된 코덱
