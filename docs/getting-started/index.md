# 시작하기

Bluetooth를 처음 공부한다면 이 섹션부터 읽으세요. 프로토콜 디테일로 들어가기 전에 큰 그림 네 가지를 잡습니다. 이 책은 **Classic(BR/EDR)**과 **LE(Low Energy)**를 함께 다루지만, 최근 기능 대부분이 LE 쪽에서 나오기 때문에 LE 비중이 더 큽니다.

| 페이지 | 얻는 것 |
|---|---|
| [Bluetooth 세대와 Core 버전](generations.md) | Core 1.x부터 6.x까지 무엇이 바뀌었는지, "Bluetooth 5 지원"이 정확히 무슨 뜻인지 |
| [Bluetooth SIG와 규격 체계](sig-specs.md) | Core Specification, 프로파일·서비스, Assigned Numbers, 테스트 규격, 인증이 어떻게 맞물리는지 |
| [규격 문서 읽는 법](reading-specs.md) | Core Specification의 Vol/Part 구조, 정오표(Errata), 원문 구하는 법과 읽는 요령 |
| [학습 로드맵](roadmap.md) | 입문자·앱/임베디드 개발자·프로토콜 전문가별 추천 읽기 순서 |

## 페이지 구성

모든 기술 페이지는 다음 순서로 구성됩니다.

!!! spec "규격 · 버전"
    관련 Core Specification의 Volume/Part(확실할 때는 절 번호까지)와 프로파일·서비스 규격 이름, 기능이 도입되고 확장된 Core 버전

!!! basic "한눈에 보기"
    <span class="lv lv1">기초</span> 개념과 비유. 수식 없이 "무엇이고 왜 필요한가"만 설명합니다.

**본문** <span class="lv lv2">중급</span> 구조, 파라미터, 표, 그림, 동작 순서. 헤딩 옆 배지로 난이도를 표시합니다.

??? expert "전문가 노트"
    <span class="lv lv3">전문가</span> 규격 디테일, 경계 조건, 버전별 차이, 실무에서 자주 헷갈리는 점, HCI 명령·이벤트 이름 같은 구현 팁.
    기본으로 접혀 있으니 필요할 때 펼쳐 보세요.

해당하는 페이지에는 끝에 **Classic ↔ LE 비교** 표가 붙고, 마지막은 항상 **관련 페이지** 목록입니다. 규격의 필드·PDU·HCI 명령 이름은 `ADV_IND`, `LL_CONNECTION_UPDATE_IND`, `HCI_LE_Set_Scan_Parameters`처럼 코드 글꼴로 씁니다.

## 용어 몇 가지 먼저

| 용어 | 뜻 |
|---|---|
| Host | 운영체제나 MCU 펌웨어에서 돌아가는 상위 스택. L2CAP, ATT/GATT, SMP, GAP, 프로파일이 여기에 있습니다 |
| Controller | 무선부와 링크 계층을 담당하는 칩(또는 칩의 일부). Classic은 Radio·Baseband·LMP, LE는 PHY·Link Layer |
| HCI (Host Controller Interface) | Host와 Controller 사이의 표준 명령·이벤트·데이터 인터페이스. UART, USB 등으로 실어 나릅니다 |
| PDU (Protocol Data Unit) | 한 계층이 주고받는 데이터 단위. 예: 링크 계층의 광고 PDU, 데이터 PDU, L2CAP의 K-frame |
| 광고 (advertising) | LE 기기가 연결 없이 정해진 채널로 자기 존재와 데이터를 알리는 방송 |
| 연결 (connection) | 두 기기가 시간과 채널 도약 순서를 맞춰 주기적으로 만나는 상태. LE에서는 연결 이벤트마다 데이터를 교환 |
| Central / Peripheral | LE 연결에서 연결을 시작하고 타이밍을 주도하는 쪽(Central)과 광고하다가 연결을 받아들인 쪽(Peripheral). Core 5.3부터 이전의 master/slave 용어를 이렇게 바꿨습니다 |
| GATT 서버 / 클라이언트 | 데이터(속성, attribute)를 가진 쪽이 서버, 그것을 읽고 쓰는 쪽이 클라이언트. Central/Peripheral 역할과는 독립입니다 |

!!! tip "역할은 서로 독립"
    스마트폰(Central)이 심박계(Peripheral)에 연결해 심박수를 읽으면 심박계가 GATT 서버입니다. 그러나 같은 연결에서 심박계가 스마트폰의 현재 시각을 읽으면 그때는 스마트폰이 GATT 서버입니다. 링크 계층 역할(Central/Peripheral)과 GAP 역할, GATT 역할은 각각 따로 정해집니다.

자세한 구조는 [Host·Controller·HCI](../basics/architecture.md)와 [프로토콜 스택 개요](../basics/stack.md)에서 다룹니다.
