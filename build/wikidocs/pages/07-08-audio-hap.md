[[TIP("📘 규격 · 버전")]]
Hearing Access Profile (HAP) v1.0, v1.0.1 · Hearing Access Service (HAS) v1.0, v1.0.1 · Telephony and Media Audio Profile (TMAP) v1.0, v1.0.1 · Gaming Audio Profile (GMAP) v1.0, v1.0.1 · 하위: CAP, BAP, CSIP, VCP(+AICS·VOCS), MICP, Immediate Alert Service
HAP·TMAP은 2022년 LE Audio 규격 완성과 함께 제공 → GMAP은 그 뒤 2024년 무렵 완성(v1.0.1이 이어짐) · ASHA는 SIG 규격이 아닌 Google 독자 규격
[[/TIP]]

[TOC]


[[TIP("🟢 한눈에 보기")]]
BAP·CAP·VCP 같은 규격은 "부품"입니다. 부품이 많으면 제조사마다 고르는 조합이 달라 서로 안 맞을 수 있습니다. 그래서 SIG는 **응용 프로파일**로 "이런 제품이라면 최소한 이 부품, 이 설정을 갖춰라"를 정했습니다.

- **HAP**: 보청기. 좌우 한 쌍을 하나로 묶고, 청취 프로그램(**프리셋**)을 휴대폰에서 바꿀 수 있게 합니다.
- **TMAP**: 전화·음악용 일반 이어버드·헤드셋·스피커.
- **GMAP**: 게임 콘솔·PC와 게이밍 헤드셋의 저지연 조합.

보청기가 Bluetooth 표준 프로파일을 처음으로 얻었다는 점이 LE Audio의 큰 의미 중 하나입니다. 이전에는 제조사·OS의 독자 방식(Apple의 MFi 보청기, Google의 ASHA)뿐이었습니다.
[[/TIP]]

## HAP 역할과 구성 (🔵 중급)

| HAP 역할 | 하는 일 | 대표 기기 | 필요한 하위 역할 |
|---|---|---|---|
| **Hearing Aid** (HA) | 오디오 수신, HAS 노출, 프리셋 보유 | 보청기 | BAP Unicast Server, CAP Acceptor, VCP Volume Renderer, (양이형이면) CSIP Set Member |
| **Hearing Aid Unicast Client** (HAUC) | 보청기로 통화·미디어 스트리밍 | 휴대폰, TV 동글 | BAP Unicast Client, CAP Initiator |
| **Hearing Aid Remote Controller** (HARC) | 프리셋·볼륨 원격 조작 | 휴대폰 앱, 워치, 리모컨 | HAS 클라이언트, VCP Volume Controller, MICP Controller |
| **Immediate Alert Client** (IAC) | 보청기에 즉각 알림 전달(예: 찾기) | 휴대폰 | Immediate Alert Service 클라이언트 |

| 보청기 유형 (Hearing Aid Features) | 구성 |
|---|---|
| **Binaural** (양이) | 좌우 두 기기, CSIP 코디네이트 세트로 묶음 |
| **Monaural** (단이) | 한쪽 귀만 |
| **Banded** | 한 기기가 양쪽 귀를 담당(넥밴드 형태 등) — 하나의 기기에 좌우 채널 |

보청기는 대부분 **양방향** 스트림이 필요합니다. 통화 시 휴대폰 → 보청기(Sink ASE)와 보청기 마이크 → 휴대폰(Source ASE)을 동시에 열고, 저비트율 음성 설정(`16_2`, `24_2`)이 주로 쓰입니다. 또한 Auracast 수신(Broadcast Sink)이 되면 공공장소의 보조 청취 시스템(텔레코일 루프)을 대체할 수 있어, 보청기 생태계에서 브로드캐스트의 중요성이 큽니다. → **Auracast 브로드캐스트**

## HAS: 프리셋 (🔵 중급)

**프리셋**은 "식당 모드", "음악 모드", "조용한 실내"처럼 보청기의 증폭·잡음 억제 설정 묶음입니다. 내용 자체(주파수별 이득)는 청능사가 피팅 소프트웨어로 넣고, Bluetooth로는 **목록 조회·선택·이름 변경**만 합니다.

| HAS 특성 | 내용 |
|---|---|
| Hearing Aid Features | 보청기 유형, 프리셋 동기화 지원, 좌우 독립 프리셋 여부, 동적 프리셋, 이름 쓰기 가능 여부 |
| Hearing Aid Preset Control Point | Read Presets Request, Read Preset Response, Preset Changed, Write Preset Name, Set Active Preset, Set Next/Previous Preset (+ "Synchronized Locally" 변형) |
| Active Preset Index | 현재 프리셋 번호 (알림) |

"Synchronized Locally" 명령은 휴대폰이 한쪽 보청기에만 명령을 써도, 보청기끼리의 자체 링크로 반대쪽도 같은 프리셋으로 바꾸게 합니다. 이 기능이 없으면 HARC가 양쪽에 각각 써야 합니다.

## TMAP과 GMAP (🔵 중급)

**TMAP**(Telephony and Media Audio Profile)은 일반 소비자 오디오 제품의 기준선입니다. 역할은 **Call Gateway**(CG)·**Call Terminal**(CT)(통화), **Unicast Media Sender**(UMS)·**Unicast Media Receiver**(UMR)(유니캐스트 음악), **Broadcast Media Sender**(BMS)·**Broadcast Media Receiver**(BMR)(브로드캐스트 음악)입니다. BAP의 기본 필수 설정(`16_2`, `24_2`) 위에 48 kHz 음악 품질 설정과 CCP·MCP·VCP 지원을 역할별로 추가로 요구해, "TMAP 이어버드"라면 음악·통화·볼륨이 휴대폰과 기본적으로 맞물리게 합니다.

**GMAP**(Gaming Audio Profile)은 게이밍용 응용 프로파일로, 2024년 무렵 완성되어 2025–2026년에 콘솔·헤드셋 제품 지원이 나오기 시작했습니다. 역할은 **Unicast Game Gateway**(UGG)·**Unicast Game Terminal**(UGT)·**Broadcast Game Sender**(BGS)·**Broadcast Game Receiver**(BGR)입니다. 게임 소리와 음성 채팅을 동시에 주고받는 양방향 스트림과 저지연 QoS 조합을 정해, 서로 다른 제조사의 콘솔·동글과 헤드셋이 저지연 모드로 바로 맞물리게 하는 것이 목적입니다.

| 응용 프로파일 | 대상 | 역할 | 핵심 요구 |
|---|---|---|---|
| HAP | 보청기 | HA, HAUC, HARC, IAC | 프리셋(HAS), 양이 세트, 양방향 음성 |
| TMAP | 이어버드·헤드셋·스피커 | CG, CT, UMS, UMR, BMS, BMR | 48 kHz 음악, 통화·미디어·볼륨 제어 |
| PBP | 공공 브로드캐스트 | Source, Sink, Assistant | SQ/HQ 등급, Broadcast_Name → **Auracast** |
| GMAP | 게임 콘솔·PC·게이밍 헤드셋 | UGG, UGT, BGS, BGR | 저지연 양방향 게임 오디오 + 채팅 |

[[TIP("🔴 전문가 노트 — 보청기 생태계와 ASHA, 전환기의 현실")]]
**ASHA는 SIG 규격이 아닙니다.** ASHA(Audio Streaming for Hearing Aids)는 Google이 Android 10(2019)에 넣은 독자 규격입니다. LE 연결 위의 L2CAP CoC(Connection-oriented Channel)로 G.722(16 kHz) 오디오를 보내며, 등시성 채널이나 LC3를 쓰지 않습니다. Apple의 MFi 보청기도 Apple 독자 방식입니다. LE Audio 이전에 보청기를 휴대폰에 직접 연결하는 현실적 방법은 이 두 가지였고, 그래서 보청기 칩은 오랫동안 독자 프로토콜·ASHA·MFi를 함께 지원해 왔습니다.

**전환기.** HAP는 OS·휴대폰 칩셋이 LE Audio(CIS, LC3)를 지원해야 동작합니다. 그래서 같은 보청기가 휴대폰에 따라 ASHA/MFi 또는 HAP로 연결되는 상황이 한동안 이어지고 있습니다. 보청기 제조사 입장에서 HAP의 가장 큰 이점은 OS와 무관한 하나의 표준과 Auracast 수신입니다.

**전력.** 보청기는 아연-공기 전지나 작은 충전 전지로 하루 종일 동작해야 합니다. 저비트율 LC3 설정(`16_2` 32 kbps)과 짧은 airtime, 그리고 보청기 간 자체 링크(규격 범위 밖, 근거리 자기 유도 등 제조사 고유)가 함께 쓰입니다.

**GMAP 지연.** GMAP이 요구하는 정확한 지연 수치와 필수 코덱 설정 목록은 GMAP 규격 원문 확인이 필요합니다. 제품 발표에서는 30 ms 이하 수준의 저지연을 내세우는 경우가 많습니다.
[[/TIP]]

## 관련 페이지

- **CAP과 CSIP** — 양이 보청기를 한 세트로
- **볼륨·통화·미디어 제어** — VCS·AICS·MICS
- **Auracast 브로드캐스트** — 보조 청취와 PBP
- **LC3 코덱** — `16_2`·`24_2` 설정
- **L2CAP** — ASHA가 쓰는 LE CoC
