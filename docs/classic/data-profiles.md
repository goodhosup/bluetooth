# 데이터 프로파일 (SPP·HID·PAN)

!!! spec "규격 · 버전"
    Serial Port Profile (SPP) 1.2 · Human Interface Device Profile (HID) 1.1.1 · HID over GATT Profile (HOGP) 1.0 · Personal Area Networking Profile (PAN) 1.0 + BNEP 1.0 · OBEX 기반: GOEP, OPP, PBAP, MAP
    Core 1.1 시절 SPP·DUN·FTP 등 → HID·PAN/BNEP → GOEP 2.0에서 OBEX over L2CAP(ERTM) · HID의 LE 대응은 HOGP(Core 4.x 시대)

!!! basic "한눈에 보기"
    오디오 밖에서 Classic이 맡는 일은 크게 네 가지입니다.

    1. **케이블 대신** — **SPP**: RFCOMM으로 가상 시리얼 포트를 열어 바이트 스트림을 그대로 주고받습니다.
    2. **입력 장치** — **HID**: 키보드·마우스·게임패드가 USB HID와 같은 리포트 형식을 L2CAP 채널 두 개로 보냅니다.
    3. **네트워크** — **PAN**: 이더넷 프레임을 **BNEP**로 감싸 블루투스 테더링을 합니다.
    4. **파일·연락처·문자** — **OPP·PBAP·MAP**: OBEX 위에서 객체를 주고받습니다. 차량 핸즈프리의 전화번호부·문자 표시가 대표적입니다.

## 프로파일 개요 { .l2 }

| 프로파일 | 하위 프로토콜 | 역할 | SDP UUID | 주 용도 |
|---|---|---|---|---|
| **SPP** | RFCOMM | DevA / DevB | `0x1101` (SerialPort) | 산업·계측 장비, POS, 레거시 시리얼 |
| **HID** | L2CAP (PSM `0x0011`, `0x0013`) | HID Host / HID Device | `0x1124` | 키보드, 마우스, 게임패드 |
| **PAN** | BNEP (PSM `0x000F`) | PANU / NAP / GN | `0x1115` / `0x1116` / `0x1117` | 테더링, 소규모 IP 망 |
| DUN | RFCOMM (AT 명령) | DT / GW | `0x1103` | 모뎀 다이얼업 (PAN으로 대체됨) |
| **OPP** | OBEX | Push Client / Push Server | `0x1105` | 명함(vCard)·사진 보내기 |
| **PBAP** | OBEX | PCE / PSE (폰) | `0x112E` / `0x112F` | 차량이 폰의 전화번호부·통화 기록 읽기 |
| **MAP** | OBEX | MCE / MSE (폰) | `0x1133`(MNS) / `0x1132`(MAS) | 차량이 문자 읽기·보내기, 새 메시지 알림 |

- **OPP**: 보내는 쪽(클라이언트)이 항상 시작하는 단순 "밀어 넣기". OBEX `PUT`으로 vCard·vCalendar·이미지를 보냅니다.
- **PBAP**: 폰이 서버(PSE)입니다. 차량(PCE)이 `pb.vcf`, `ich.vcf`(수신 기록) 같은 가상 폴더를 vCard로 내려받습니다.
- **MAP**: 폰이 MSE(서버)이고, 차량이 메시지 목록·본문을 읽거나 새 메시지 알림(MNS)을 받습니다.

## SPP { .l2 }

SPP는 RFCOMM 채널 하나를 그대로 앱에 넘겨주는 가장 단순한 프로파일입니다. 상대의 SDP에서 SerialPort UUID(또는 앱 고유 128비트 UUID)를 찾아 RFCOMM 서버 채널 번호를 얻고, DLCI를 열면 바로 바이트 스트림이 됩니다. 메시지 경계가 없으므로 앱이 자체 프레이밍(길이 필드·구분자)을 둬야 합니다.

## HID — Classic HID와 HOGP { .l2 }

Classic HID는 **두 개의 L2CAP 채널**을 씁니다. **Control 채널**(PSM `0x0011`)은 `GET_REPORT`/`SET_REPORT`, 프로토콜 전환 같은 요청에, **Interrupt 채널**(PSM `0x0013`)은 키 입력·마우스 이동 같은 입력 리포트에 씁니다. 리포트 형식은 SDP 레코드의 **HID Descriptor**(USB HID 리포트 디스크립터와 같은 문법)로 알립니다.

| 항목 | Classic HID | HOGP (HID over GATT) |
|---|---|---|
| 전송 | L2CAP 채널 2개 (Control, Interrupt) | GATT의 HID Service (`0x1812`) |
| 리포트 디스크립터 | SDP 속성 (HIDDescriptorList) | Report Map 특성 |
| 입력 리포트 | Interrupt 채널의 `DATA` | Report 특성의 Notification |
| 부트 프로토콜 | 지원 (BIOS·간단한 호스트용) | Boot Keyboard/Mouse Input Report 특성 |
| 재연결 | HID Device가 페이징 (`HIDReconnectInitiate`) 또는 호스트가 페이징 | 디바이스가 광고 → 호스트가 연결 (화이트리스트·RPA) |
| 지연·전력 | Sniff 간격으로 조절, 대기 전력이 비교적 큼 | 연결 간격·Peripheral Latency로 조절, 대기 전력이 작음 |
| 보안 | 키보드는 암호화 필수 | 암호화된 연결 필수 (LE 보안 모드 1 레벨 2 이상) |

신규 키보드·마우스는 대부분 HOGP를 쓰지만, BIOS·구형 OS·게임 콘솔 호환을 위해 Classic HID를 함께 넣는 듀얼 모드 제품이 많습니다.

## PAN과 BNEP { .l2 }

**BNEP**(Bluetooth Network Encapsulation Protocol)는 이더넷 프레임의 헤더를 압축해 L2CAP 채널(PSM `0x000F`)에 실어 보냅니다. **NAP**(Network Access Point)는 외부 망으로 연결해 주는 브리지(테더링하는 폰), **PANU**는 사용자 기기, **GN**(Group ad-hoc Network)은 외부 망 없이 PANU끼리 묶는 역할입니다. 링크 처리량이 수백 kbps–2 Mbps급이라 Wi-Fi 핫스팟에 대부분 자리를 내주었지만, 일부 차량·임베디드 장비가 여전히 씁니다.

??? expert "전문가 노트 — HID 지연, SPP 처리량, OBEX over L2CAP"
    **HID 지연.** Classic HID의 입력 지연은 Sniff 간격이 지배합니다. 게이밍 기기는 활성 중 Sniff를 끄거나 짧게 두고, 유휴 시간이 지나면 긴 Sniff나 연결 해제로 전력을 아낍니다. 키를 누르는 순간 Sniff를 빠져나오는(`LMP_unsniff_req`) 데에도 Sniff 간격만큼 기다려야 할 수 있습니다.

    **SPP 처리량.** RFCOMM 프레임 크기(`PN`의 N1)를 L2CAP MTU에 맞게 키우고, 크레딧을 충분히 주고, EDR 5슬롯 패킷이 허용되어 있어야 링크 상한(3-DH5 기준 약 2178 kbps, 실제 응용은 이보다 낮음)에 가까워집니다. 작은 쓰기를 자주 하면 1슬롯 패킷만 나가 처리량이 크게 떨어집니다.

    **OBEX over L2CAP.** GOEP 2.0부터 OBEX를 RFCOMM 대신 ERTM 모드 L2CAP 채널로 직접 실을 수 있습니다(SDP의 `GoepL2capPsm` 속성). 큰 전화번호부·사진 전송에서 RFCOMM 오버헤드를 줄입니다.

## Classic ↔ LE 비교

| 용도 | Classic | LE |
|---|---|---|
| 시리얼 스트림 | SPP (RFCOMM) | 표준 없음 — 벤더 GATT 서비스 또는 L2CAP CoC |
| 입력 장치 | HID | HOGP |
| IP 네트워크 | PAN/BNEP | IPSP(6LoWPAN) — 실사용 드묾 |
| 파일·객체 전송 | OPP·FTP (OBEX) | Object Transfer Service (OTS) |
| 전화번호부·문자 | PBAP·MAP | 표준 프로파일 없음 (차량은 Classic 사용) |

## 관련 페이지

- [L2CAP·SDP·RFCOMM](l2cap-sdp-rfcomm.md) — 이 프로파일들이 쓰는 채널과 서비스 발견
- [대표 GATT 서비스](../host/gatt-services.md) — HID Service 등 LE 대응
- [처리량 최적화](../host/throughput.md) — LE 쪽 처리량 조정
- [피코넷과 기저대역](baseband.md) — Sniff와 패킷 타입
