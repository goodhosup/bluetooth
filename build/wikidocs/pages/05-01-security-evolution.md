[[TIP("📘 규격 · 버전")]]
Core v6.0 Vol 2 Part H (BR/EDR Security Specification) · Vol 3 Part C (GAP — 보안 모드·레벨) · Vol 3 Part H (Security Manager Protocol) · Vol 6 Part E (LE Link Layer Security)
1.x PIN 페어링(SAFER+, E0) → 2.1 SSP(P-192) → 4.0 LE Legacy Pairing(AES-128, TK) → 4.1 BR/EDR Secure Connections(P-256, AES-CCM) → 4.2 LE Secure Connections·CTKD → 5.2 LE Security Mode 3 → 5.3 키 길이 제어 → 5.4 암호화된 광고 데이터 → 6.1 RPA 갱신 시점 무작위화
[[/TIP]]

[TOC]


[[TIP("🟢 한눈에 보기")]]
Bluetooth 보안의 역사는 **"사람이 입력한 짧은 비밀"에 기대던 방식에서 공개 키 교환으로 옮겨 간 역사**입니다.

1. **PIN 시대(1.x–2.0)**: 두 기기에 같은 PIN(흔히 `0000`)을 넣고, 그 PIN에서 키를 만들었습니다. 페어링을 엿들으면 PIN을 맞춰 볼 수 있었습니다.
2. **SSP(2.1)**: 타원곡선 Diffie-Hellman으로 비밀을 만들고, 사람은 6자리 숫자를 **비교만** 하게 했습니다. 엿들어도 키를 알 수 없습니다.
3. **LE Legacy(4.0)**: 저전력을 위해 ECDH 없이 AES만 쓰는 페어링으로 시작했다가 SSP 이전과 비슷한 약점을 다시 안게 됐습니다.
4. **Secure Connections(4.1 Classic / 4.2 LE)**: 두 전송 모두 P-256 ECDH와 AES 기반 함수로 통일했습니다. 지금 새 제품이 써야 할 기준입니다.
[[/TIP]]

## 연대표 (🔵 중급)

| Core | 연도 | 전송 | 보안 변화 | 핵심 알고리즘 |
|---|---|---|---|---|
| 1.0–2.0 | 1999–2004 | BR/EDR | **레거시 PIN 페어링**, 보안 모드 1–3 | 키 생성·인증 SAFER+ 기반(E1, E21, E22, E3), 암호화 **E0** 스트림 암호 |
| 2.1 + EDR | 2007 | BR/EDR | **SSP**(Secure Simple Pairing), 보안 모드 4, 연결 모델 4종 | **P-192 ECDH**, HMAC-SHA-256(f1, f2, f3, g) — 암호화는 여전히 E0 |
| 4.0 | 2010 | LE | **LE Legacy Pairing**, SMP, LTK·IRK·CSRK, RPA 프라이버시 | AES-128(c1, s1), 임시 키 **TK** |
| 4.1 | 2013 | BR/EDR | **Secure Connections**, 보안 모드 4 레벨 4, LMP Ping·LE Ping | **P-256 ECDH**, 상호 인증 h4/h5, 암호화 **AES-CCM** |
| 4.2 | 2014 | LE | **LE Secure Connections**, Numeric Comparison, **CTKD**, 컨트롤러 기반 프라이버시(LL Privacy) | P-256 ECDH, AES-CMAC 기반 f4/f5/f6/g2, h6 |
| 5.1 | 2019 | 공통 | CTKD로 기존 키를 덮어쓰는 상황을 제한(BLURtooth 공개 시 SIG 설명) | — |
| 5.2 | 2019 | LE | **LE Security Mode 3**(BIG의 Broadcast Code) | AES-CCM |
| 5.3 | 2021 | BR/EDR | **암호 키 길이 제어**: 호스트가 최소 키 길이를 컨트롤러에 지정 | — |
| 5.4 | 2023 | LE | **암호화된 광고 데이터**, LE GATT Security Levels 특성 | AES-CCM |
| 6.1 | 2025 | LE | **RPA 갱신 시점 무작위화** | — |

2019년의 **KNOB** 공개 뒤에는 BR/EDR 암호 키 최소 길이를 7옥텟으로 올리는 정오표(erratum)가 나왔습니다. 공격과 대응은 **알려진 공격과 대응**에 모았습니다.

## LE Legacy Pairing의 약점 (🔵 중급)

LE 4.0의 페어링은 양쪽이 공유하는 128비트 **TK**(Temporary Key)에서 단기 키 STK를 만듭니다. 문제는 TK의 실제 엔트로피입니다.

| 연결 모델 | TK 값 | 실제 비밀의 크기 | 결과 |
|---|---|---|---|
| Just Works | 0 | 없음 | 페어링을 엿들은 사람은 STK와 이후 배포되는 LTK를 바로 계산 |
| Passkey Entry | 0–999999 | 약 20비트 | 엿들은 Confirm/Random 값으로 100만 후보를 짧은 시간에 대입 가능 |
| OOB | 128비트 OOB 값 | 128비트 | OOB 채널(NFC 등)이 안전하면 안전 |

즉 Legacy Pairing은 **수동 도청자**를 막지 못합니다(OOB 제외). 2013년 무렵 이 점을 이용해 캡처한 LE 페어링에서 LTK를 복구하는 도구가 공개되었습니다. LE Secure Connections는 공개 키를 교환한 뒤 ECDH로 **DHKey**를 만들기 때문에, 도청만으로는 Just Works에서도 키를 알 수 없습니다. Just Works에 남는 약점은 **능동적 중간자(MITM)**뿐이고, 이를 막는 것이 Numeric Comparison·Passkey·OOB입니다.

## 보안 모드와 레벨 (🔵 중급)

GAP는 링크가 제공하는 보호 수준을 아래 등급으로 정의합니다. 서비스는 필요한 레벨을 요구하고, 링크가 미달이면 ATT는 `Insufficient Authentication`·`Insufficient Encryption`·`Insufficient Encryption Key Size` 같은 오류를 돌려줍니다.

| 모드 | 레벨 | 의미 |
|---|---|---|
| LE Security Mode 1 | 1 | 보안 없음(인증·암호화 없음) |
| | 2 | 인증 없는 페어링 + 암호화 (예: Just Works) |
| | 3 | 인증된 페어링 + 암호화 (Legacy Passkey/OOB 포함) |
| | 4 | 인증된 **LE Secure Connections** 페어링 + 128비트 키 |
| LE Security Mode 2 | 1 | 인증 없는 페어링 + 데이터 서명(CSRK) |
| | 2 | 인증된 페어링 + 데이터 서명 |
| LE Security Mode 3 (5.2) | 1 | 보안 없음 (암호화되지 않은 BIG) |
| | 2 | 인증되지 않은 Broadcast Code 사용 |
| | 3 | 인증된 Broadcast Code 사용 |
| BR/EDR Security Mode 4 | 0–4 | 0: SDP 등 예외용 무보안 · 1: 최소 · 2: 인증 없는 키 + 암호화 · 3: 인증된 키 + 암호화 · 4: 인증된 **Secure Connections** 키 + AES-CCM |

GAP는 이 밖에 Mode 1과 Mode 2 요구가 섞인 **Mixed Security Mode**, 모든 서비스에 Mode 1 Level 4만 허용하는 **Secure Connections Only Mode**를 정의합니다. BR/EDR 쪽 Secure Connections Only 모드는 **Classic 보안 (SSP)**에서 다룹니다.

[[TIP("🔴 전문가 노트 — 레벨 판정, 키 길이, 5.4의 GATT Security Levels")]]
**레벨 판정의 함정.** "레벨 3"은 인증된 키라는 뜻이지 알고리즘이 안전하다는 뜻이 아닙니다. LE Legacy Passkey로 만든 키는 Mode 1 Level 3이지만 도청에 약합니다. 신규 설계에서 민감한 특성은 Level 4를 요구하는 것이 안전합니다.

**키 길이.** 레벨과 별개로 암호 키 길이(7–16옥텟)가 협상됩니다. Level 4는 16옥텟(128비트) 키를 전제로 합니다. 서비스는 필요하면 최소 키 길이를 따로 요구하고, 부족하면 `Insufficient Encryption Key Size` 오류가 납니다.

**LE GATT Security Levels 특성(5.4).** GAP 서비스에 서버가 요구하는 최고 보안 모드·레벨을 미리 알려 주는 특성이 추가되었습니다. 클라이언트는 오류를 받아 보고 나서 재페어링하는 대신, 처음부터 필요한 수준으로 페어링을 시작할 수 있습니다.

**E0의 처지.** E0은 BR/EDR 레거시 암호화로 여전히 호환을 위해 남아 있습니다. Secure Connections를 양쪽이 지원할 때만 AES-CCM이 쓰이므로, 한쪽이라도 구형이면 E0과 SAFER+ 기반 인증으로 떨어집니다.
[[/TIP]]

## Classic ↔ LE 비교

| 항목 | Classic (BR/EDR) | LE |
|---|---|---|
| 첫 공개 키 페어링 | 2.1 SSP (P-192) | 4.2 LE SC (P-256) |
| P-256 도입 | 4.1 Secure Connections | 4.2 LE Secure Connections |
| 페어링 프로토콜 | LMP (컨트롤러가 수행) | SMP (호스트가 수행) |
| 레거시 암호화 | E0 스트림 암호 | AES-CCM (처음부터) |
| 장기 키 | Link Key | LTK (+ IRK, CSRK) |
| 보안 모드 | Mode 1–4 (현재는 4) | LE Mode 1–3 |

## 관련 페이지
- **LE 페어링과 본딩** — SMP 절차와 연결 모델 선택
- **Classic 보안 (SSP)** — BR/EDR의 SSP와 보안 모드 4
- **알려진 공격과 대응** — 진화를 이끈 실제 공격들
- **Bluetooth 세대와 Core 버전** — 버전별 전체 기능
