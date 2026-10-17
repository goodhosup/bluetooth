# 방향 탐지 (AoA·AoD)

!!! spec "규격 · 버전"
    Core v6.0 Vol 6 Part A (Physical Layer) — 안테나 스위칭·IQ 샘플링 요구 · Vol 6 Part B (Link Layer) — Constant Tone Extension(CTE), `CTEInfo`, Connection CTE Request 절차 · Vol 4 Part E (HCI) CTE·IQ 관련 명령
    Core 5.1 도입(Direction Finding: AoA, AoD) · 이후 큰 구조 변화 없음 · 6.0의 Channel Sounding은 각도가 아니라 거리를 재는 별도 기능

!!! basic "한눈에 보기"
    전파가 비스듬히 들어오면 **나란히 놓인 안테나마다 도착 시간이 아주 조금씩 다르고**, 그 차이는 신호의 **위상차**로 보입니다. 위상차를 재면 신호가 어느 각도에서 왔는지 계산할 수 있습니다.

    - 이를 위해 패킷 끝에 아무 정보 없는 **일정한 톤(CTE)**을 붙여, 수신기가 안정적인 위상을 재게 함
    - **AoA**(도래각): **수신기**가 안테나 배열을 가짐. 태그는 안테나 1개로 CTE만 보냄 → 자산 추적, 실내 측위 인프라
    - **AoD**(발사각): **송신기**가 안테나 배열을 가짐. 수신기는 안테나 1개로 배열 순서를 알고 위상을 비교 → 스마트폰 측위(비콘이 배열)
    - 계산은 **IQ 샘플**을 받은 Host(또는 측위 엔진)가 함. 규격은 측정 방법까지만 정함

## CTE 구조 { .l2 }

| 항목 | 값 |
|---|---|
| 위치 | 패킷의 CRC 뒤(화이트닝 안 함) |
| 내용 | 연속된 1 → GFSK에서 반송파에서 일정하게 편이된 톤 |
| 길이 | 16 – 160 µs, 8 µs 단위 (`CTETime` 2 – 20) |
| 구성 | 보호 구간 4 µs + 기준 구간 8 µs + 나머지는 스위칭 슬롯·샘플 슬롯 교대 |
| 슬롯 길이 | **1 µs 또는 2 µs** (CTE 유형으로 지정) |
| PHY | LE 1M, LE 2M (Coded PHY에서는 불가) |
| 표시 | 헤더의 `CP` 비트 = 1이면 `CTEInfo` 바이트가 붙음 (CTETime, CTEType) |

| CTEType | 의미 |
|---|---|
| 0 | AoA CTE (수신기가 스위칭) |
| 1 | AoD CTE, 1 µs 슬롯 |
| 2 | AoD CTE, 2 µs 슬롯 |

기준 구간 8 µs 동안은 안테나를 바꾸지 않고 1 µs마다 IQ 샘플을 8개 얻어 기준 위상과 주파수 오프셋을 추정합니다. 이후에는 "스위칭 슬롯 → 샘플 슬롯"이 반복되며 매 샘플 슬롯마다 다른 안테나로 IQ 샘플을 하나씩 얻습니다.

| 전달 방식 | 실리는 패킷 | 요청 |
|---|---|---|
| 비연결 (connectionless) | 주기적 광고 `AUX_SYNC_IND` | 송신 측 `HCI_LE_Set_Connectionless_CTE_Transmit_Parameters` / 수신 측 `HCI_LE_Set_Connectionless_IQ_Sampling_Enable` |
| 연결 (connection) | 데이터 채널 `LL_CTE_RSP` | `LL_CTE_REQ`로 요청, HCI `HCI_LE_Connection_CTE_Request_Enable` |

IQ 샘플은 LE Connectionless IQ Report / LE Connection IQ Report 이벤트로 Host에 올라갑니다.

## AoA와 AoD 비교 { .l2 }

| 항목 | AoA | AoD |
|---|---|---|
| 안테나 배열 | **수신기** | **송신기** |
| 스위칭하는 쪽 | 수신기 (샘플링하며 바꿈) | 송신기 (보내며 바꿈) |
| 각도 계산 위치 | 고정 로케이터(인프라) | 이동 기기(휴대폰 등) |
| 이동 기기 요구 | 안테나 1개, CTE 송신만 | 안테나 1개, IQ 샘플링 + 배열 정보 |
| 프라이버시 | 인프라가 태그 위치를 앎 | 기기가 스스로 위치를 계산 (GPS와 비슷) |
| 대표 응용 | 자산·사람 추적 RTLS | 실내 길 찾기 |

## 위상차에서 각도로 { .l2 }

간격 \(d\)인 두 안테나에 평면파가 각도 \(\theta\)(배열 법선 기준)로 들어오면 경로 차이는 \(d \sin\theta\)이고, 위상차는

\[
\Delta\varphi = \frac{2\pi d \sin\theta}{\lambda} \quad\Rightarrow\quad \theta = \arcsin\!\left(\frac{\lambda\,\Delta\varphi}{2\pi d}\right)
\]

2.44 GHz에서 \(\lambda = c/f \approx 3\times10^8 / 2.44\times10^9 \approx 12.3\) cm입니다. 위상차가 ±π 안에서만 유일하게 해석되려면 \(d \le \lambda/2 \approx 6.1\) cm여야 합니다(모호성 없는 조건). 실제로는 2차원 배열(예: 4×4)과 MUSIC·ESPRIT 같은 고분해능 알고리즘으로 방위각·고도각을 함께 추정합니다.

| 오차 요인 | 영향 | 대응 |
|---|---|---|
| 다중 경로 | 반사파가 섞여 위상이 왜곡 | 여러 채널·여러 패킷 평균, 고분해능 알고리즘 |
| 주파수 오프셋 | 시간에 따라 위상이 회전 | 기준 구간 8 µs로 추정·보정 |
| 안테나 간 결합·배선 차 | 고정 위상 오차 | 배열 교정(calibration) |
| 넓은 입사각 | \(\sin\theta\) 기울기가 작아져 분해능 저하 | 법선 근처에서 사용, 배열 여러 개 |
| 편파 | 태그 방향에 따라 수신 세기 변화 | 이중 편파 안테나 |

??? expert "전문가 노트 — 정확도 한계, 스위칭 패턴, 구현 팁"
    **정확도.** 규격은 정확도를 정하지 않습니다. 업계 시연은 좋은 조건에서 각도 수 도, 여러 로케이터를 삼각 측량해 서브미터 위치를 보고하지만, 사람·금속이 많은 실내에서는 다중 경로 때문에 크게 나빠질 수 있습니다. 결과는 배열 설계·교정·알고리즘 품질에 좌우됩니다.

    **스위칭 패턴.** Host가 `Antenna_IDs` 배열로 스위칭 순서를 정합니다(AoA는 수신 쪽, AoD는 송신 쪽). AoD 수신기는 송신기의 배열 형태와 스위칭 순서를 알아야 하므로, 이를 GATT 서비스나 광고 데이터로 전달하는 상위 규약이 필요합니다.

    **1 µs vs 2 µs 슬롯.** 1 µs 슬롯은 같은 CTE 길이에서 더 많은 샘플을 주지만 RF 스위치가 빠르고 과도 응답이 짧아야 합니다. Controller가 1 µs 스위칭·샘플링을 지원하는지는 `HCI_LE_Read_Antenna_Information`(지원 스위칭·샘플링 속도, 안테나 수, 스위칭 패턴 최대 길이)으로 확인합니다.

    **IQ 샘플 형식.** 샘플은 8비트 I·Q 쌍으로 보고되고, 보고 이벤트에는 채널 인덱스·RSSI·패킷 상태가 함께 실립니다. 채널마다 파장이 다르므로 각도 계산에는 채널 인덱스로 구한 \(\lambda\)를 써야 합니다.

## 관련 페이지
- [Channel Sounding](channel-sounding.md) — 각도 대신 거리를 재는 6.0 기능
- [주기적 광고와 PAwR](periodic-advertising.md) — 비연결 CTE의 운반체
- [패킷 구조](packet.md) — `CP` 비트와 `CTEInfo`
- [LE PHY (1M·2M·Coded)](phy.md) — CTE가 가능한 PHY
- [무선 전파와 링크 버짓](../basics/radio-channel.md) — 다중 경로
