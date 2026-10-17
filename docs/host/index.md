# LE 호스트

이 섹션은 LE 컨트롤러(PHY·링크 계층) 위에서 동작하는 **호스트(Host)** 쪽 프로토콜을 다룹니다. 앱 개발자가 실제로 만지는 "서비스", "특성", "알림(Notify)", "MTU", "광고 데이터"가 모두 여기에 속합니다. 컨트롤러가 무선 패킷을 정확한 시각에 주고받는 일을 맡는다면, 호스트는 **그 패킷에 무엇을 담고 어떤 순서로 주고받을지**를 정합니다.

| 페이지 | 핵심 질문 |
|---|---|
| [L2CAP](l2cap.md) | ATT·SMP·시그널링 데이터는 하나의 LE 링크 위에서 어떻게 구분되고, 큰 데이터는 어떻게 쪼개지나? |
| [ATT](att.md) | "핸들 + 타입 + 값" 표 하나로 어떻게 읽기·쓰기·알림을 모두 표현하나? |
| [GATT](gatt.md) | 서비스·특성·디스크립터 계층은 ATT 표 위에 어떻게 쌓이고, 클라이언트는 그것을 어떻게 찾나? |
| [EATT](eatt.md) | 왜 5.2에서 ATT를 여러 채널로 동시에 돌리게 되었나? |
| [GAP](gap.md) | 광고·스캔·연결·본딩을 "역할·모드·절차"로 어떻게 묶어 정의하나? |
| [광고 데이터 형식 (AD Type)](ad-types.md) | 31바이트 광고 안에 이름·UUID·제조사 데이터를 어떻게 채우나? |
| [대표 GATT 서비스](gatt-services.md) | Battery, Device Information, Heart Rate, HID over GATT는 어떤 UUID와 특성을 쓰나? |
| [처리량 최적화](throughput.md) | PHY, DLE, MTU, 연결 간격 중 무엇을 바꿔야 실제 kbps가 늘어나나? |

!!! basic "미리 보기 — 컨트롤러와 호스트의 경계"
    Bluetooth 스택은 **HCI**(Host Controller Interface)를 경계로 둘로 나뉩니다.

    1. **컨트롤러** — PHY와 링크 계층. 광고 이벤트·연결 이벤트 타이밍, 채널 도약, 재전송(ACK/NACK), 암호화(AES-CCM)를 하드웨어에 가까운 곳에서 처리합니다. 최대 251바이트 LL 페이로드 단위로 일합니다.
    2. **호스트** — L2CAP, ATT/GATT, SMP, GAP. "어떤 서비스가 있나", "이 값을 읽어도 되나", "페어링을 어떻게 하나"를 결정합니다. 보통 휴대폰 OS나 MCU 펌웨어의 소프트웨어 스택(BlueZ, Android Bluetooth, Zephyr 등)입니다.
    3. 둘 사이에는 HCI 명령(`HCI_LE_Set_Advertising_Data` 등), 이벤트(`HCI_LE_Connection_Complete` 등), ACL 데이터 패킷이 오갑니다. 호스트의 데이터는 결국 **L2CAP PDU → ACL 데이터 → LL 데이터 PDU** 순서로 내려갑니다.

    그래서 "알림이 느리다"는 문제는 호스트(MTU, 쓰기 방식)와 컨트롤러(PHY, DLE, 연결 간격) 양쪽을 함께 봐야 풀립니다. 컨트롤러 쪽 내용은 [LE 컨트롤러](../le/index.md), 경계 자체는 [Host·Controller·HCI](../basics/architecture.md)에서 다룹니다.
