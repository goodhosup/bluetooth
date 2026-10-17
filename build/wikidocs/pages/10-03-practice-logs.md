[[TIP("📘 규격 · 버전")]]
Core v6.0 Vol 4 Part E (HCI 명령·이벤트), Vol 1 Part F (오류 코드), Vol 3 Part F (ATT 오류 코드), Vol 3 Part H (SMP Pairing Failed 이유 코드) · 파일 형식: btsnoop(BlueZ·Android 공통), pcap/pcapng
도구는 규격 밖의 구현: BlueZ `btmon`(BlueZ 5), Android HCI snoop log(개발자 옵션), Wireshark 해석기(`bthci_*`, `btle`, `btatt`, `btsmp`)
[[/TIP]]

[TOC]


[[TIP("🟢 한눈에 보기")]]
HCI 로그는 Host와 Controller 사이의 **대화 녹취록**입니다. 무선 구간을 직접 보지는 못하지만, "누가 무엇을 요청했고, 칩이 어떤 이유 코드로 답했는가"는 거의 다 남습니다.

1. **수집**: Linux는 `btmon`, Android는 HCI snoop log, 임베디드는 스택의 HCI 추적 출력.
2. **열기**: Wireshark(또는 `btmon -r`)로 열고 필터로 좁힙니다.
3. **읽기**: 실패한 명령의 Status, 연결 종료 Reason, ATT/SMP 오류 코드를 찾고 시간 순서로 원인을 추적합니다.
[[/TIP]]

## 로그 수집 (🔵 중급)

| 환경 | 방법 | 결과 파일 |
|---|---|---|
| Linux (BlueZ) | `sudo btmon -w trace.btsnoop` (실시간 해석은 `btmon`만) | btsnoop |
| Linux 재생 | `btmon -r trace.btsnoop` | 텍스트 해석 출력 |
| Android | 개발자 옵션 → **Bluetooth HCI 스누프 로그 사용**(Enabled 선택) → Bluetooth 끄고 켜기 → 재현 → `adb bugreport` | 버그 리포트 안 `btsnoop_hci.log` |
| Zephyr | `CONFIG_BT_DEBUG_MONITOR_UART`(또는 RTT) 출력 → `btmon --tty` 등으로 수신 | btsnoop 변환 가능 |
| 벤더 SDK | 벤더 전용 추적 도구 또는 HCI UART 미러링 | 벤더 형식 / pcap |
| macOS·iOS | Apple 제공 Bluetooth 로깅 프로파일 + PacketLogger | PacketLogger 형식 |

Android의 snoop log는 최신 버전에서 **Filtered**(개인정보·오디오 페이로드를 잘라낸) 모드와 **Enabled**(전체) 모드가 나뉩니다. 프로토콜 디버깅에는 전체 모드가 필요합니다. 메뉴 이름과 파일 경로는 Android 버전·제조사에 따라 다르므로, 버그 리포트 압축 파일 안에서 `btsnoop` 이름을 찾는 편이 확실합니다.

## Wireshark 필터 (🔵 중급)

| 목적 | 필터 |
|---|---|
| HCI 이벤트만 | `bthci_evt` |
| LE Meta 이벤트 | `bthci_evt.code == 0x3e` |
| LE Connection Complete 계열 | `bthci_evt.le_meta_subevent == 0x01 or bthci_evt.le_meta_subevent == 0x0a` |
| 연결 종료 | `bthci_evt.code == 0x05` |
| 실패한 명령·이벤트 | `bthci_evt.status != 0x00` |
| 특정 명령 (LE Create Connection) | `bthci_cmd.opcode == 0x200d` |
| ATT 전체 / 오류 응답 | `btatt` / `btatt.opcode == 0x01` |
| SMP (페어링) | `btsmp` / 실패 이유 `btsmp.reason` |
| 무선 스니퍼 캡처: 특정 광고 주소 | `btle.advertising_address == aa:bb:cc:dd:ee:ff` |
| 스니퍼: LL 제어 PDU | `btle.control_opcode` |
| 스니퍼: 연결 요청 | `btle.advertising_header.pdu_type == 0x05` |

`btle.*` 필드는 **무선 스니퍼**로 잡은 공중 패킷에만 있고, HCI 로그에는 `bthci_*`, `btl2cap`, `btatt`, `btsmp`만 있습니다. Wireshark의 *Statistics → Conversations*·*Flow Graph*로 연결별 흐름을 보면 수천 줄 로그에서도 길을 잃지 않습니다.

## 실전 해석 예 (🔵 중급)

**① 연결 실패 0x3E**

```text
< HCI Command: LE Create Connection (0x08|0x000d)
> HCI Event: Command Status (0x0f)   Status: Success
> HCI Event: LE Meta Event (0x3e)    LE Enhanced Connection Complete (0x0a)
        Status: Success  Handle: 64  Interval: 30.00 ms  Timeout: 4000 ms
> HCI Event: Disconnect Complete (0x05)
        Handle: 64  Reason: Connection Failed to be Established (0x3e)
```

연결 완료 직후 수십 ms 안에 0x3E로 끊겼습니다. 첫 6개 연결 이벤트 안에 상대가 응답하지 않았다는 뜻입니다. 의심할 것: 상대가 `CONNECT_IND`를 못 받음(광고 채널 혼잡), Peripheral의 RF·클럭 문제, 지나치게 짧은 연결 간격과 큰 Peripheral 쪽 처리 지연. 반복된다면 스니퍼로 첫 연결 이벤트를 확인합니다.

**② 감독 타임아웃 0x08**

정상 데이터가 오가다 `Disconnect Complete Reason: Connection Timeout (0x08)`이 오면 링크가 **감독 타임아웃**(예: 4000 ms) 동안 한 패킷도 성공하지 못한 것입니다. 직전의 `Number Of Completed Packets`가 멈춘 시점, `LE Connection Update Complete`로 바뀐 간격·타임아웃, 주변 Wi-Fi 상황을 함께 봅니다.

**③ 페어링 실패**

```text
> ACL Data RX: SMP: Pairing Response   IO capability: NoInputNoOutput  Auth: Bonding, SC
< ACL Data TX: SMP: Pairing Public Key
> ACL Data RX: SMP: Pairing Failed     Reason: DHKey Check Failed (0x0b)
```

SMP의 Pairing Failed 이유 코드는 HCI 오류 코드와 **다른 표**입니다(예: 0x03 Authentication Requirements, 0x05 Pairing Not Supported, 0x0B DHKey Check Failed). 이미 본딩된 기기에서 `Encryption Change` 대신 Status 0x06 (PIN or Key Missing)이 보이면, 한쪽이 키를 지운 것이므로 본딩을 지우고 다시 페어링합니다.

[[TIP("🔴 전문가 노트 — 타임스탬프, 누락, 프라이버시")]]
**타임스탬프의 의미.** HCI 로그의 시각은 Host가 패킷을 주고받은 시각이지 공중 송신 시각이 아닙니다. UART 지연·Host 스케줄링 때문에 수 ms 오차가 생기므로, 연결 이벤트 타이밍 분석에는 **스니퍼**를 씁니다.

**로그가 비어 보일 때.** Android snoop log는 Bluetooth 스택이 다시 시작된 뒤부터 기록됩니다. 설정 직후 Bluetooth를 끄고 켜지 않으면 아무것도 남지 않습니다. 또한 Controller 내부에서 끝나는 동작(LL 재전송, 채널 맵 갱신, 자동 PHY 협상)은 HCI에 나타나지 않습니다.

**주소 해석.** RPA를 쓰는 상대는 연결마다 주소가 바뀌어 보입니다. `LE Enhanced Connection Complete`의 Peer RPA와 Peer Identity Address 필드를 같이 확인하고, Host가 Controller 주소 해석 목록에 IRK를 넣었는지(`HCI_LE_Add_Device_To_Resolving_List`) 봅니다.

**공유 시 주의.** 전체 모드 snoop log에는 링크 키 교환, 기기 이름, 주소, 오디오·파일 페이로드가 그대로 들어갑니다. 외부에 보낼 때는 필요한 구간만 잘라 냅니다.
[[/TIP]]

## 로그 읽기 체크리스트 (🔵 중급)

- ⬜ 시작 시점: `HCI_Reset` 이후 `HCI_Read_Local_Version_Information`으로 Controller 버전·제조사 확인
- ⬜ `HCI_LE_Set_Event_Mask`에서 필요한 서브이벤트가 켜져 있는지
- ⬜ 모든 Command Status / Complete의 Status가 0x00인지 (`bthci_evt.status != 0`)
- ⬜ 연결 완료 이벤트의 간격·Peripheral 지연·감독 타임아웃 값
- ⬜ PHY·DLE 협상 결과 (`LE PHY Update Complete`, `LE Data Length Change`)
- ⬜ 암호화: `Encryption Change` Status, SMP 실패 이유
- ⬜ ATT 오류 응답(Insufficient Authentication 0x05, Insufficient Encryption 0x0F 등)과 그 뒤의 페어링 시도
- ⬜ 연결 종료 Reason과 직전 수 초간의 트래픽
- ⬜ 예상 밖의 `HCI_Reset`, Hardware Error(0x10) → Controller 재시작 의심

## 관련 페이지

- **HCI 명령과 이벤트** — Opcode·이벤트·오류 코드 표
- **무선 스니퍼** — HCI에 안 보이는 공중 패킷 보기
- **LE 페어링과 본딩** — SMP 메시지 흐름
- **ATT** — ATT 오류 코드
- **연결 이벤트와 파라미터** — 감독 타임아웃
