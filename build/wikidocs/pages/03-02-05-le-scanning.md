[[TIP("📘 규격 · 버전")]]
Core v6.0 Vol 6 Part B (스캔 상태, 스캐너 필터 정책, 결정 기반 광고 필터링, Monitoring Advertisers) · Vol 4 Part E (HCI: `HCI_LE_Set_Extended_Scan_Parameters` 등)
Core 4.0 수동·능동 스캔, White List → 4.2 RPA 대상 directed 광고 필터 정책 → 5.0 확장 스캔(PHY별 파라미터, Duration/Period) → 5.3 용어 변경(White List → Filter Accept List) → 6.0 결정 기반 광고 필터링, Monitoring Advertisers
[[/TIP]]

[TOC]


[[TIP("🟢 한눈에 보기")]]
스캐너는 라디오처럼 광고 채널 하나에 귀를 대고 있다가 일정 시간마다 채널을 바꿉니다.

1. **얼마나 오래 들을까** — scan window / scan interval 비율(듀티 사이클)이 클수록 빨리 찾지만 전류가 늘어납니다.
2. **듣기만 할까, 물어볼까** — 수동 스캔은 듣기만, 능동 스캔은 `SCAN_REQ`로 추가 정보(`SCAN_RSP`)를 요청합니다.
3. **누구 말만 들을까** — Filter Accept List로 아는 기기만 받거나, 중복 필터로 같은 보고를 줄입니다.
4. **6.0** — 광고자가 "판단용 요약"을 먼저 보내 스캐너가 쓸모없는 패킷을 건너뛰고(결정 기반 필터링), 컨트롤러가 기기의 "들어옴/나감"만 알려 줍니다(Monitoring Advertisers).
[[/TIP]]

## 수동 스캔과 능동 스캔 (🔵 중급)

| 항목 | 수동 스캔 (passive) | 능동 스캔 (active) |
|---|---|---|
| 송신 | 없음 | `SCAN_REQ` / `AUX_SCAN_REQ` |
| 얻는 데이터 | AdvData | AdvData + 스캔 응답 데이터 |
| 광고자에게 보이는가 | 아니오 | 예 (ScanA 주소가 노출, 프라이버시 고려) |
| 전력 | 낮음 | 송신과 응답 대기만큼 높음 |
| 쓰임 | 비컨 수집, 백그라운드 탐색 | 기기 목록 화면(이름 표시) |

능동 스캔에서는 여러 스캐너의 `SCAN_REQ`가 같은 광고에 몰려 충돌하지 않도록 스캐너가 **백오프**를 씁니다. 응답을 받지 못할 때마다 다음 요청까지 건너뛸 광고 수의 상한을 늘리고(최대 256), 성공하면 줄입니다.

## scan interval·window와 발견 확률 (🔵 중급)

| 파라미터 | 범위 | 의미 |
|---|---|---|
| `LE_Scan_Interval` | 2.5 ms – 10.24 s (0.625 ms 단위) | 한 채널에서 다음 채널로 넘어가는 주기 |
| `LE_Scan_Window` | 2.5 ms – interval 이하 | 각 interval 안에서 실제로 듣는 시간 |
| 듀티 사이클 | window / interval | 100 %면 연속 스캔 |
| `Duration`·`Period` (5.0 확장 스캔) | 10 ms 단위 / 1.28 s 단위 | 정해진 시간만 스캔, 주기적으로 반복 |

간단한 모델로 보면, 광고자는 한 이벤트에 세 채널 모두 보내므로 스캐너가 어느 채널을 듣고 있든 이벤트마다 한 번은 기회가 옵니다. 그 PDU가 window 안에 떨어질 확률을 듀티 사이클 $D = W/I$로 근사하면, 이벤트 $k$번 안에 발견할 확률과 평균 발견 시간은

$$
P(k) \approx 1 - (1 - D)^{k}, \qquad \bar{T} \approx \frac{T\_{adv}}{D}
$$

입니다($T\_{adv}$ = advInterval + 평균 advDelay 5 ms). 계산 예는 다음과 같습니다.

| 광고 간격 | 스캔 window / interval | $D$ | 평균 발견 시간 (근사) | 10 이벤트 안 발견 확률 |
|---|---|---|---|---|
| 100 ms | 30 / 100 ms | 0.3 | 105 / 0.3 ≈ 350 ms | 1 − 0.7¹⁰ ≈ 97 % |
| 100 ms | 100 / 100 ms | 1.0 | ≈ 105 ms (첫 이벤트) | ≈ 100 % |
| 1000 ms | 30 / 300 ms | 0.1 | 1005 / 0.1 ≈ 10 s | 1 − 0.9¹⁰ ≈ 65 % |

이 모델은 광고와 스캔 일정이 서로 독립이라고 가정합니다. 실제로 두 간격이 정수배에 가까우면 한동안 계속 엇갈릴 수 있는데, advDelay의 무작위성이 이런 동기화된 엇갈림을 깨는 역할을 합니다. 또한 스캐너가 연결 이벤트와 시간을 나눠 쓰면 실제 듀티 사이클은 설정값보다 낮아집니다.

## 필터: Filter Accept List와 중복 필터 (🔵 중급)

**Filter Accept List**(5.3 이전 이름 White List)는 컨트롤러가 가진 주소 목록입니다. `HCI_LE_Add_Device_To_Filter_Accept_List` 등으로 관리하며, 스캐너·광고자·개시자의 필터 정책이 이 목록을 참조합니다.

| `Scanning_Filter_Policy` | 받는 광고 |
|---|---|
| 0x00 | 모두 (단, 나를 대상으로 하지 않은 directed 광고 제외) |
| 0x01 | Filter Accept List에 있는 광고자만 |
| 0x02 | 0x00 + TargetA가 해석 가능한 RPA인 directed 광고 (4.2) |
| 0x03 | 0x01 + 위 RPA directed 광고 (4.2) |

**중복 필터**(`Filter_Duplicates`)는 같은 광고자의 같은 보고를 호스트에 한 번만 올립니다. 확장 스캔에서는 0(끔), 1(켬), 2(켬, `Period`마다 초기화)를 고릅니다. 확장 광고에서는 ADI의 DID가 바뀌면 새 데이터로 보고 다시 올립니다.

## 6.0의 새 필터 (🔵 중급)

| 기능 | 풀려는 문제 | 동작 | HCI |
|---|---|---|---|
| **결정 기반 광고 필터링** | 스캐너가 쓸모없는 보조 패킷을 따라가느라 주 채널을 놓침 | 광고자가 주 채널에 `ADV_DECISION_IND`(결정 데이터 + AuxPtr)를 보냄. 스캐너는 호스트가 준 검사 규칙을 통과할 때만 보조 채널로 이동 | `HCI_LE_Set_Decision_Data`(광고자), `HCI_LE_Set_Decision_Instructions`(스캐너) |
| **Monitoring Advertisers** | 중복 필터를 켜면 기기가 아직 근처에 있는지 알 수 없고, 끄면 보고가 폭주 | 컨트롤러가 목록의 기기별 RSSI 임계값·시간으로 "신호 상실"과 "복귀"만 보고 | LE Monitored Advertisers List / Enable 명령, LE Monitored Advertisers Report 이벤트 |

결정 데이터에는 공유 키로 만든 **Resolvable Tag**나 임의 데이터를 넣을 수 있고, 스캐너 규칙은 Resolvable Tag, AdvMode, RSSI, 경로 손실, 광고자 주소, 마스크 비교한 임의 데이터 등을 검사합니다. 규칙은 그룹 안에서는 AND, 그룹끼리는 OR로 묶입니다. 스캔 필터 정책에는 결정 PDU를 무시 / 함께 검사 / 결정 PDU만 받기 모드가 추가되었습니다. 결정 PDU는 LE 1M 또는 LE Coded PHY로 보냅니다.

Monitoring Advertisers는 목록 항목마다 주소, RSSI 하한·상한, 시간 초과를 둡니다. RSSI가 하한 이하로 시간 초과만큼 이어지면 신호 상실을 보고하고, 이후 상한 이상으로 받으면 복귀를 보고합니다. Filter Accept List와 독립이라 본딩 기기 필터와 함께 쓸 수 있으며, LE Audio에서 주변 이어버드가 범위 안에 있는지 지켜보는 용도가 대표 사례입니다.

[[TIP("🔴 전문가 노트 — 스캔 보고 이벤트, OS 정책, Resolvable Tag 키")]]
**보고 이벤트.** 레거시 스캔은 `HCI_LE_Advertising_Report`, 확장 스캔은 `HCI_LE_Extended_Advertising_Report`를 씁니다. 확장 보고에는 이벤트 종류 비트(연결 가능, 스캔 가능, directed, 스캔 응답, legacy), 주·보조 PHY, SID, TxPower, RSSI, 주기적 광고 간격, `Data_Status`(완료/이어짐/불완전)가 들어 있습니다. 체인이 길면 한 광고가 보고 이벤트 여러 개로 나뉘어 올라옵니다.

**모바일 OS의 스캔 정책.** 스마트폰 OS는 백그라운드 앱의 스캔 듀티를 크게 낮추거나 필터 없는 스캔을 막는 경우가 많습니다. 앱에서 설정한 "저지연 모드"가 그대로 컨트롤러 파라미터가 된다고 가정하면 안 되며, 발견 시간이 길면 광고 간격을 줄이는 쪽이 더 확실한 해결책인 경우가 많습니다.

**Resolvable Tag의 키 공유.** 6.0 Core는 태그를 만들고 검사하는 방법을 정했지만, 광고자와 스캐너가 키를 어떻게 나눠 갖는지는 앞으로 GATT 서비스·프로파일 규격에서 정한다고 설명합니다.
[[/TIP]]

## 관련 페이지
- **레거시 광고** — `SCAN_REQ`/`SCAN_RSP` 교환
- **확장 광고** — ADI와 보조 채널
- **링크 계층 상태 기계** — Scanning 상태와 다른 상태의 공존
- **프라이버시와 RPA** — Resolving List와 필터 정책 0x02/0x03
- **Core 6.0–6.3** — 6.0 신기능 전체
