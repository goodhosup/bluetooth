---
hide:
  - navigation
---

# Bluetooth Handbook

**Bluetooth Classic(BR/EDR)부터 Low Energy, LE Audio, Mesh, 그리고 Core 6.x Channel Sounding까지.**
처음 공부하는 사람은 개념부터, 현업 엔지니어는 규격 디테일까지 한 페이지 안에서 단계적으로 읽을 수 있도록 만든 한글 블루투스 핸드북입니다.

## 이 핸드북을 읽는 법

모든 페이지는 같은 틀을 따르고, 난이도를 신호 막대 아이콘으로 구분합니다.

| 표시 | 대상 | 내용 |
|---|---|---|
| <span class="lv lv1">기초</span> | 처음 공부하는 사람, 비전공자 | 개념, 비유, "왜 이렇게 만들었나" — 수식 없이 |
| <span class="lv lv2">중급</span> | 전공자, 신입 엔지니어, 앱 개발자 | 구조, 파라미터 표, 그림, 동작 순서 |
| <span class="lv lv3">전문가</span> | 펌웨어·드라이버·RF 엔지니어 | 규격 수식, 예외 처리, 버전별 변화, 실무 팁 (접힌 상자) |

!!! spec "스펙 박스"
    각 페이지 맨 위의 이 상자에는 관련 Bluetooth Core Specification의 Vol/Part와 기능이 들어온 Core 버전, 해당하면 프로파일·서비스 규격 이름이 적혀 있습니다.

    본문을 읽다가 원문을 확인하고 싶을 때 바로 찾아갈 수 있습니다.

약어 위에 마우스를 올리면 풀네임이 툴팁으로 나옵니다. 예: GATT, PAwR, CIS

## 섹션

<div class="grid cards" markdown>

-   :material-flag-checkered: **시작하기**

    ---

    Core 1.0에서 6.x까지의 변천, Bluetooth SIG와 규격 체계, 규격 문서 읽는 법, 학습 로드맵

    [:octicons-arrow-right-24: 시작하기](getting-started/index.md)

-   :material-sine-wave: **공통 기초**

    ---

    2.4 GHz ISM 대역, 링크 버짓, GFSK, 주파수 도약과 AFH, 저전력 원리, HCI, 주소, Wi-Fi 공존

    [:octicons-arrow-right-24: 공통 기초](basics/index.md)

-   :material-chip: **LE 컨트롤러**

    ---

    1M·2M·Coded PHY, 광고·스캔, 연결 이벤트, 채널 선택, DLE, 등시성 채널, 방향 탐지, Channel Sounding

    [:octicons-arrow-right-24: LE 컨트롤러](le/index.md)

-   :material-layers-triple: **LE 호스트**

    ---

    L2CAP, ATT·GATT·EATT, GAP, 광고 데이터 형식, 대표 GATT 서비스, 처리량 최적화

    [:octicons-arrow-right-24: LE 호스트](host/index.md)

-   :material-shield-lock: **보안**

    ---

    페어링과 본딩, LE Secure Connections, 키 계층과 CTKD, RPA 프라이버시, 알려진 공격과 대응

    [:octicons-arrow-right-24: 보안](security/index.md)

-   :material-headphones: **Classic (BR/EDR)**

    ---

    피코넷과 기저대역, 조회·페이징, LMP, ACL·SCO/eSCO, RFCOMM, A2DP·HFP, SPP·HID

    [:octicons-arrow-right-24: Classic](classic/index.md)

-   :material-ear-hearing: **LE Audio**

    ---

    LC3, BAP, PACS·ASCS, CAP·CSIP, Auracast 브로드캐스트, 볼륨·통화 제어, 보청기

    [:octicons-arrow-right-24: LE Audio](audio/index.md)

-   :material-lan: **Mesh**

    ---

    관리형 플러딩, 프로비저닝, 네트워크·전송·접근 계층, 모델, 키 관리, Mesh 1.1

    [:octicons-arrow-right-24: Mesh](mesh/index.md)

-   :material-rocket-launch: **최신 동향**

    ---

    Core 6.0–6.3, Channel Sounding 활용, HDT와 상위 대역 확장, Matter·Thread

    [:octicons-arrow-right-24: 최신 동향](next/index.md)

-   :material-tools: **구현과 실무**

    ---

    호스트 스택 비교, HCI, btmon·Wireshark 로그 분석, 스니퍼, 전류 프로파일, RF 시험, 인증

    [:octicons-arrow-right-24: 구현과 실무](practice/index.md)

-   :material-bookshelf: **레퍼런스**

    ---

    Classic vs LE, Bluetooth vs Wi-Fi vs 5G, 버전별 기능, 규격 인덱스, 약어 사전, 계산기

    [:octicons-arrow-right-24: 레퍼런스](reference/index.md)

</div>

## 자매 핸드북

- [Cellular Handbook](https://goodhosup.github.io/cellular/) — LTE · 5G NR · 6G
- [Wi-Fi Handbook](https://goodhosup.github.io/wifi/) — IEEE 802.11 · Wi-Fi 6/7/8

!!! note "출처와 저작권"
    본문과 그림은 직접 작성했습니다. Bluetooth SIG 규격(Core Specification, 프로파일·서비스 규격)은 문서 이름과 Vol/Part/절만 출처로 인용하며, 규격 원문의 그림이나 표를 복제하지 않습니다.
    정확한 값은 항상 최신 버전 규격으로 확인하세요.
