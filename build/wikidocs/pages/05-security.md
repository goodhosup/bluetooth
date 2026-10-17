이 섹션은 Bluetooth가 "누구와 연결하는지 확인하고(인증), 오가는 데이터를 숨기고(암호화), 내가 누구인지 드러내지 않는(프라이버시)" 방법을 다룹니다. Classic(BR/EDR)과 LE는 서로 다른 시기에 따로 보안을 쌓아 왔기 때문에 이름과 함수가 다르지만, 지금은 둘 다 **P-256 타원곡선 Diffie-Hellman + AES** 조합으로 수렴했습니다. 먼저 **보안 모델의 진화**로 큰 줄기를 잡고, LE 페어링 → 키 → 프라이버시 순서로 읽기를 권합니다.

| 페이지 | 핵심 질문 |
|---|---|
| **보안 모델의 진화** | PIN 페어링에서 Secure Connections까지 무엇이 왜 바뀌었나? 보안 모드·레벨은 무엇을 뜻하나? |
| **LE 페어링과 본딩** | SMP의 세 페이즈에서 무엇이 오가고, Just Works·Passkey·Numeric Comparison·OOB 중 무엇이 왜 선택되나? |
| **키 계층과 CTKD** | LTK·IRK·CSRK·Link Key는 각각 무슨 일을 하고, 한 번 페어링으로 Classic과 LE 키를 모두 얻는 원리는? |
| **프라이버시와 RPA** | 주소를 계속 바꾸면서도 아는 기기끼리는 서로를 알아보는 방법은? 추적은 어디서 새나? |
| **Classic 보안 (SSP)** | BR/EDR의 SSP 단계, Link Key 종류, 보안 모드 4와 Secure Connections Only 모드는? |
| **알려진 공격과 대응** | KNOB·BIAS·BLURtooth·BrakTooth 등은 어떤 약점을 노렸고, 규격과 구현은 어떻게 대응했나? |
| **암호화된 광고 데이터** | 연결 없이 광고 데이터 일부만 아는 기기에게 보여 주는 방법은? (Core 5.4) |

[[TIP("🟢 보안 모드·레벨 미리 보기")]]
Bluetooth는 "얼마나 안전한 링크인가"를 **보안 모드(Security Mode)**와 **보안 레벨(Security Level)**이라는 등급으로 표현합니다. 서비스(예: GATT 특성)는 "레벨 N 이상의 링크에서만 접근 가능"처럼 요구 조건을 걸고, 링크가 그보다 약하면 페어링이나 재암호화를 요구합니다.

1. **LE Security Mode 1** — 암호화 기반. 레벨 1(보안 없음) → 2(인증 없는 페어링 + 암호화) → 3(인증된 페어링 + 암호화) → 4(인증된 **LE Secure Connections** + 128비트 키)
2. **LE Security Mode 2** — 암호화 없이 **데이터 서명**만 쓰는 모드(레벨 1·2)
3. **LE Security Mode 3** — Core 5.2의 **브로드캐스트 등시성 그룹(BIG)**용, Broadcast Code 사용 여부로 레벨 1–3
4. **BR/EDR Security Mode 4** — SSP 기반 서비스 수준 보안, 레벨 0–4 (레벨 4 = Secure Connections)

"인증됨(authenticated)"은 사용자가 숫자를 비교하거나 입력하는 등 **중간자(MITM) 보호**가 있는 연결 모델로 페어링했다는 뜻입니다. Just Works로 만든 키는 암호화는 되지만 "인증되지 않은" 키입니다.
[[/TIP]]

[[TIP("💡 다른 섹션과의 연결")]]
주소 종류(공개·랜덤 정적·RPA)는 **디바이스 주소**, 링크 계층의 암호화 시작 절차(`LL_ENC_REQ` 등)는 **LL 제어 절차**, 메시 네트워크의 별도 키 체계는 **Mesh 보안**에서 다룹니다.
[[/TIP]]

## 이 장의 페이지

[[SubPages]]
