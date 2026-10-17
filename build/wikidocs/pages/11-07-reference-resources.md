[[TIP("📘 규격 · 버전")]]
공식 규격·Assigned Numbers·인증 도구: Bluetooth SIG (bluetooth.com) · 도구·오픈소스 스택은 각 프로젝트 저장소 기준 (링크는 2026년 기준 주소이며, 바뀌면 프로젝트 이름으로 검색)
규격은 SIG 웹사이트에서 무료로 내려받을 수 있습니다 (일부 시험 규격·도구는 멤버 로그인 필요)
[[/TIP]]

[TOC]


[[TIP("🟢 한눈에 보기")]]
공부와 개발에 필요한 1차 자료는 크게 네 가지입니다.

1. **공식 규격** — Core, 프로파일·서비스, Assigned Numbers
2. **도구** — 패킷을 보고(Wireshark, 스니퍼), 기기를 만지는(nRF Connect, bluetoothctl) 도구
3. **오픈소스 스택** — 실제 구현을 읽으며 규격 문장을 코드로 확인
4. **참고서·강좌** — 전체 그림을 잡는 데 도움
[[/TIP]]

## 공식 규격과 SIG 자료 (🔵 중급)

| 자료 | 주소 | 내용 |
|---|---|---|
| 규격 목록 | <https://www.bluetooth.com/specifications/specs/> | Core, 프로파일·서비스, Mesh, LC3 등 전체 규격 PDF/HTML |
| Assigned Numbers | <https://www.bluetooth.com/specifications/assigned-numbers/> | UUID, AD 타입, Company Identifier, Appearance, 코덱 ID |
| Assigned Numbers 원본(YAML) | <https://bitbucket.org/bluetooth-SIG/public> | 기계가 읽기 좋은 형식의 번호 목록 |
| Qualification Workspace | <https://qualification.bluetooth.com/> | 제품 인증, 설계(DN/QDID) 검색 (**인증**) |
| SIG 기술 블로그·기능 개요 | <https://www.bluetooth.com/> | 새 Core 버전 기능 개요, 기술 문서 |

## 도구 (🔵 중급)

| 도구 | 주소 | 용도 |
|---|---|---|
| Wireshark | <https://www.wireshark.org/> | btsnoop·pcap 해석, 스니퍼 캡처 표시 (**로그 분석**) |
| nRF Connect for Mobile / Desktop | <https://www.nordicsemi.com/> (Development tools) | 스캔, GATT 탐색·쓰기, 광고 확인, DTM·전류 측정 앱 |
| nRF Sniffer for Bluetooth LE | <https://www.nordicsemi.com/> (Development tools) | 저가 LE 스니퍼 + Wireshark 연동 (**무선 스니퍼**) |
| BlueZ 도구 (`bluetoothctl`, `btmgmt`, `btmon`) | <https://www.bluez.org/> | Linux에서 기기 제어·HCI 기록 (**호스트 스택 비교**) |
| Bumble | <https://github.com/google/bumble> | Python으로 쓴 Bluetooth 스택 — 시험 자동화·가상 기기 |
| Android HCI snoop log | 개발자 옵션 | Android HCI 기록 |

## 오픈소스 스택 저장소 (🔵 중급)

| 스택 | 저장소 | 메모 |
|---|---|---|
| BlueZ | <https://github.com/bluez/bluez> (원본: git.kernel.org) | Linux 사용자 공간 스택. 커널 쪽은 Linux 커널 `net/bluetooth` |
| Zephyr | <https://github.com/zephyrproject-rtos/zephyr> | `subsys/bluetooth` 아래 Host·Controller |
| Apache NimBLE | <https://github.com/apache/mynewt-nimble> | LE Host + Controller |
| Android Bluetooth | <https://android.googlesource.com/platform/packages/modules/Bluetooth/> | Fluoride/Gabeldorsche, Floss |
| BTstack | <https://github.com/bluekitchen/btstack> | 임베디드용 듀얼 모드 스택 (상용 라이선스 조건 확인) |
| Apple Core Bluetooth 문서 | <https://developer.apple.com/documentation/corebluetooth> | 소스는 비공개, API 문서 |

## 참고서와 강좌 (🔵 중급)

| 자료 | 저자·출처 | 다루는 범위 |
|---|---|---|
| *Bluetooth Low Energy: The Developer's Handbook* | Robin Heydon (Prentice Hall, 2012) | Core 4.0 LE 설계 의도 — 오래됐지만 기본 개념의 원전 |
| *Getting Started with Bluetooth Low Energy* | Kevin Townsend 외 (O'Reilly, 2014) | GATT 중심 입문 |
| *Introducing Bluetooth LE Audio* | Nick Hunn (2022) | LE Audio 전체 구조와 배경 |
| Nordic DevAcademy 강좌 | <https://academy.nordicsemi.com/> | 실습 위주 LE 기초·중급 강좌 |
| SIG 학습 자료·백서 | bluetooth.com | 기능별 공식 개요 |

[[TIP("🔴 전문가 노트 — 자료를 고르는 기준")]]
**1차 자료 우선.** 블로그·포럼 글은 버전이 오래되었거나 특정 벤더 구현을 규격처럼 쓰는 경우가 많습니다. 숫자와 동작 조건은 반드시 해당 버전의 Core 규격 원문으로 확인하고, 구현 동작은 오픈소스 스택 코드로 교차 확인합니다.

**규격과 구현을 오가며 읽기.** 예를 들어 연결 수립의 0x3E 처리를 알고 싶다면 Core Vol 6 Part B의 연결 수립 절과 Zephyr·NimBLE Controller 코드의 해당 처리부를 함께 보면 이해가 빠릅니다.

**자매 핸드북.** Wi-Fi와 셀룰러를 함께 다뤄야 한다면 [Wi-Fi 핸드북](https://goodhosup.github.io/wifi/)과 [셀룰러 핸드북](https://goodhosup.github.io/cellular/)을 참고하십시오.
[[/TIP]]

## 관련 페이지

- **규격 인덱스** — 규격 구성표
- **규격 문서 읽는 법** — 규격 읽기 요령
- **학습 로드맵** — 무엇부터 읽을지
- **호스트 스택 비교** — 스택 선택
