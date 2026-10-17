# Classic (BR/EDR)

이 섹션은 Bluetooth **BR/EDR**(Basic Rate / Enhanced Data Rate, 흔히 "Classic")을 다룹니다. 이 책의 중심은 LE이므로, Classic은 **오디오와 실무에 필요한 만큼**만 정리합니다. 무선 구간의 시간 구조(슬롯·피코넷)에서 시작해 연결 수립(조회·페이징), 링크 관리(LMP), 논리 링크(ACL·SCO), 상위 프로토콜(L2CAP·SDP·RFCOMM), 그리고 프로파일 순서로 올라갑니다.

| 페이지 | 핵심 질문 |
|---|---|
| [피코넷과 기저대역](baseband.md) | 625 µs 슬롯과 초당 1600 홉 위에서 Central과 Peripheral은 어떻게 번갈아 말하나? DH5와 3-DH5의 처리량은? |
| [조회와 페이징](inquiry-paging.md) | 광고 채널이 없는 Classic은 주변 기기를 어떻게 찾고, 연결까지 몇 초가 걸리나? |
| [링크 관리자 (LMP)](lmp.md) | 두 컨트롤러는 기능·버전·역할·암호화·Sniff를 어떤 메시지로 협상하나? |
| [ACL과 SCO/eSCO](acl-sco.md) | 데이터 링크와 음성 링크는 무엇이 다르고, 통화 음질(CVSD·mSBC·LC3-SWB)은 어떻게 정해지나? |
| [L2CAP·SDP·RFCOMM](l2cap-sdp-rfcomm.md) | PSM·서비스 레코드·DLCI는 각각 무엇을 찾아가는 주소인가? |
| [오디오 프로파일 (A2DP·AVRCP·HFP)](audio-profiles.md) | 음악 스트리밍과 통화는 어떤 프로파일·코덱·명령으로 동작하나? |
| [데이터 프로파일 (SPP·HID·PAN)](data-profiles.md) | 시리얼, 키보드, 테더링, 파일·전화번호부 전송은 어떤 프로파일이 맡나? |

!!! basic "Classic이 여전히 쓰이는 곳"
    LE가 대부분의 새 기기를 가져갔지만, Classic은 다음 영역에서 여전히 기본값입니다.

    1. **무선 이어폰·스피커의 음악 재생** — A2DP + AVRCP. LE Audio가 확산 중이지만 대부분의 기기는 아직 A2DP를 함께 지원합니다.
    2. **차량 핸즈프리와 헤드셋 통화** — HFP. 차량 인포테인먼트는 PBAP(전화번호부)·MAP(문자)까지 Classic으로 묶여 있습니다.
    3. **키보드·마우스·게임패드** — Classic HID. 새 제품은 HOGP(LE)로 옮겨 가는 중이지만 구형 호스트 호환 때문에 듀얼 모드가 많습니다.
    4. **산업·계측 장비의 시리얼 대체** — SPP. "케이블 대신 무선"이 필요한 레거시 장비와 POS·바코드 스캐너.
    5. **듀얼 모드 칩** — 스마트폰·PC·차량의 칩은 BR/EDR과 LE를 함께 지원하며, 같은 안테나와 2.4 GHz 대역을 시분할로 나눠 씁니다.

!!! tip "먼저 읽으면 좋은 페이지"
    주파수 도약과 AFH는 [주파수 도약과 AFH](../basics/fhss-afh.md), GFSK·DPSK 변조는 [디지털 변조 (GFSK·DPSK)](../basics/modulation.md), 페어링(SSP)은 [Classic 보안 (SSP)](../security/classic-security.md), 두 기술의 전체 비교는 [Classic vs LE 비교](../reference/classic-vs-le.md)에서 다룹니다.
