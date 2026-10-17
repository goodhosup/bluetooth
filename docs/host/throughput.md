# 처리량 최적화

!!! spec "규격 · 버전"
    LL 타이밍·DLE: Core v6.0 Vol 6 Part B · PHY: Vol 6 Part A · L2CAP: Vol 3 Part A · ATT: Vol 3 Part F · 플랫폼 제약: Apple Accessory Design Guidelines(QA1931), Android `BluetoothGatt` API 문서
    Core 4.0 (LL 페이로드 27 B, 1M) → 4.2 DLE (251 B) → 5.0 LE 2M PHY → 5.2 EATT (병렬 ATT)

!!! basic "한눈에 보기"
    LE의 "1 Mbps"나 "2 Mbps"는 무선 심볼 속도일 뿐, 앱이 실제로 얻는 속도는 훨씬 낮습니다. 처리량은 다음 곱셈으로 생각하면 됩니다.

    **처리량 ≈ (패킷당 앱 데이터) × (연결 이벤트당 패킷 수) ÷ (연결 간격)**

    1. **패킷당 앱 데이터**를 키우려면: DLE(251 B) + 큰 ATT MTU(247 이상)
    2. **이벤트당 패킷 수**를 키우려면: 2M PHY(패킷이 짧아짐) + 컨트롤러가 이벤트를 길게 쓰도록 허용
    3. **응답을 기다리지 않는 전송**: Notification, Write Without Response
    4. **연결 간격**: 짧을수록 지연이 줄지만, 이벤트를 꽉 채울 수 있으면 간격 자체보다 "이벤트 안에서 쉬지 않는 것"이 더 중요

## 처리량을 결정하는 요소 { .l2 }

| 요소 | 기본(4.0) | 최적화 | 효과 |
|---|---|---|---|
| **PHY** | 1M | 2M (5.0) | 같은 바이트의 airtime이 약 절반 → 이벤트당 패킷 수 증가 |
| **LL 페이로드 (DLE)** | 27 B | 251 B (4.2) | 패킷당 헤더·T_IFS·빈 응답 오버헤드 비율 감소 |
| **ATT MTU** | 23 | 247 (LL 251 B에 맞춤) 또는 더 크게 | ATT/L2CAP 헤더 7 B 비율 감소. MTU > 247이면 L2CAP 조각이 여러 LL 패킷으로 나뉨 |
| **ATT 동작** | Write Request / Indication (왕복마다 대기) | Write Without Response / Notification | 응답 대기 제거. 요청-응답은 연결 이벤트당 1회 수준으로 묶임 |
| **연결 간격** | 플랫폼 기본 (보통 30–50 ms) | 짧게 요청 (7.5–15 ms) | 이벤트가 꽉 차지 않을 때 효과 큼 |
| **이벤트당 패킷 수** | 컨트롤러·OS 구현 | 이벤트 길이 확장(Connection Event Length) 허용 | 스케줄러가 이벤트를 일찍 닫으면 상한에 못 미침 |
| **암호화** | — | — | MIC 4 B 추가로 airtime 약간 증가 (아래 계산은 MIC 없음) |

## 계산 예 { .l2 }

한쪽만 데이터를 보내고 상대는 빈 패킷으로 응답하는 구간을 **데이터 패킷 → T_IFS(150 µs) → 빈 패킷 → T_IFS**의 반복으로 보면, 한 사이클에 앱 데이터 (LL 페이로드 − 7) 바이트를 보냅니다(7 B = L2CAP 헤더 4 B + ATT Notification 헤더 3 B). airtime과 상한값은 `tools/bt_numbers.py` 출력입니다.

| PHY | 251 B 패킷 airtime | 빈 패킷 | 사이클 | 이벤트를 꽉 채운 상한 (251 B) | 27 B 패킷일 때 상한 |
|---|---|---|---|---|---|
| 1M | 2088 µs | 80 µs | 2468 µs | **≈ 791 kbps** | ≈ 237 kbps |
| 2M | 1048 µs | 44 µs | 1392 µs | **≈ 1402 kbps** | ≈ 323 kbps |
| Coded S=2 | 4478 µs | 462 µs | 5240 µs | ≈ 373 kbps | ≈ 97 kbps |
| Coded S=8 | 16784 µs | 720 µs | 17804 µs | ≈ 110 kbps | ≈ 46 kbps |

예를 들어 1M 상한은 \( 244 \times 8 \text{ bit} / 2468\ \mu s \approx 790.9\ \text{kbps} \)입니다. DLE 없이(27 B, 앱 데이터 20 B) 같은 방식으로 계산하면 1M에서 약 237 kbps로, **DLE 하나만으로 3배 이상** 차이가 납니다.

실제로는 연결 간격 안에 사이클이 정수 개만 들어갑니다. 연결 간격 15 ms라면

- 1M: \( 15000 / 2468 \approx 6.08 \) → 이벤트당 최대 6 패킷 → \( 6 \times 244 \times 8 / 15\ \text{ms} \approx 780.8\ \text{kbps} \)
- 2M: \( 15000 / 1392 \approx 10.78 \) → 최대 10 패킷 → \( 10 \times 244 \times 8 / 15\ \text{ms} \approx 1301.3\ \text{kbps} \)

이 값은 컨트롤러가 이벤트를 다음 앵커 직전까지 계속 쓴다는 가정이며, 이벤트당 패킷 수를 4–6개 등으로 제한하는 구현에서는 훨씬 낮아집니다(예: 2M에서 4 패킷이면 \( 4 \times 1952 / 15\ \text{ms} \approx 520.5\ \text{kbps} \)).

## 플랫폼 제약 { .l2 }

| 항목 | iOS / iPadOS | Android |
|---|---|---|
| 연결 간격 | Apple 가이드(QA1931): 최소 15 ms(15 ms 배수), BLE HID는 11.25 ms까지 허용될 수 있음. Min = Max = 15 ms 요청 시 30 ms로 조정될 수 있음 | `requestConnectionPriority()`: HIGH는 기기에 따라 대략 11.25–15 ms, BALANCED는 30–50 ms 수준. 정확한 값은 제조사·버전마다 다름 |
| ATT MTU | OS가 연결 후 자동으로 교환. 앱은 `maximumWriteValueLength`로 확인 | `requestMtu()`로 요청(최대 517). Android 14부터 첫 요청 시 517로 요청하고 이후 요청은 무시 |
| PHY | 앱에서 직접 선택하는 API 없음. 기기·OS가 2M을 자동 사용 | `setPreferredPhy()`(API 26+)로 2M·Coded 요청 |
| 이벤트당 패킷 수 | 기기 세대·OS 버전에 따라 다름, 공개 수치 없음 | 칩셋·스택 구현에 따라 다름 |
| 쓰기 흐름 제어 | `canSendWriteWithoutResponse` / `peripheralIsReady(toSendWriteWithoutResponse:)` | `onCharacteristicWrite` 콜백 후 다음 쓰기 (Write Without Response도 동일) |

??? expert "전문가 노트 — 측정 방법과 함정"
    **양방향이 동시에 차면 절반.** 위 계산은 한 방향만 데이터를 보내는 경우입니다. 양쪽이 동시에 251 B를 보내면 사이클당 airtime이 늘어 한 방향 처리량은 줄어듭니다.

    **MTU 247 vs 512.** ATT MTU를 LL 페이로드보다 크게 잡으면 ATT 헤더 비율은 더 줄지만, 하나의 Notification이 LL 패킷 여러 개로 나뉘어 하나라도 다음 이벤트로 밀리면 지연이 커집니다. 처리량 차이는 몇 % 수준이라 247(=251 − 4)이 흔한 선택입니다.

    **연결 간격을 무조건 줄이지 말 것.** 이벤트를 꽉 채울 수 있다면 간격이 길수록 이벤트 사이 빈틈(다음 앵커 전 남는 시간, 다른 링크·Wi-Fi 공존 슬롯) 비율이 줄어듭니다. 짧은 간격은 지연 시간과 "이벤트를 일찍 닫는 구현"에 대한 대응책입니다.

    **측정은 앱 계층에서, 원인은 무선에서.** 처리량은 앱에서 바이트/초로 재고, 병목은 btsnoop/스니퍼로 이벤트당 패킷 수·NACK 비율·연결 간격·PHY·DLE 협상(`LL_LENGTH_REQ`/`LL_LENGTH_RSP`, `LL_PHY_REQ`) 결과를 확인합니다. NACK가 많으면 처리량 문제가 아니라 RF 문제입니다. → [로그 분석](../practice/logs.md)

    **EATT는 처리량보다 지연.** EATT는 링크 용량을 늘리지 않습니다. 여러 트랜잭션을 겹쳐 왕복 대기를 줄일 뿐이므로, 요청-응답 위주(읽기 많은 앱)일 때 효과가 있습니다.

## 체크리스트 { .l2 }

1. 양쪽 컨트롤러가 **DLE(251 B)**를 지원하고 실제로 협상되었는가 (`HCI_LE_Data_Length_Change` 이벤트)
2. **2M PHY**로 전환되었는가 (`HCI_LE_PHY_Update_Complete`)
3. **ATT MTU ≥ 247**로 교환되었는가, 앱이 MTU − 3 크기로 보내고 있는가
4. 대량 전송에 **Notification / Write Without Response**를 쓰는가 (Write Request·Indication은 왕복 대기)
5. 송신 큐를 비우지 않게 **흐름 제어 콜백에 맞춰 연속으로** 밀어 넣는가
6. 연결 간격을 플랫폼 허용 범위에서 적절히 요청했는가 (Peripheral 쪽에서는 Central이 최종 결정)
7. 스니퍼로 **이벤트당 패킷 수**와 재전송 비율을 확인했는가
8. 페어링·암호화 후의 값(MIC 4 B 포함)으로 다시 측정했는가

## 관련 페이지
- [데이터 길이 확장 (DLE)](../le/data-length.md) — 27 → 251 B 협상
- [LE PHY (1M·2M·Coded)](../le/phy.md) — PHY별 airtime
- [연결 이벤트와 파라미터](../le/connection-events.md) — 연결 간격·이벤트 길이
- [ATT](att.md) — MTU 교환과 Write/Notify PDU
- [계산기](../reference/calculators.md) — airtime·처리량 계산
