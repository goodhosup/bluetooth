[[TIP("🟢 이 페이지의 용도")]]
핸드북에서 쓰는 약어를 알파벳순으로 정리했습니다. 이 표는 사이트 전체 **약어 툴팁**의 원본이기도 합니다(`tools/gen_abbreviations.py`가 이 표에서 `includes/abbreviations.md`를 생성). 뜻이 여러 개인 약어(예: CS, CSA, MIC)는 툴팁에서 제외하고 아래 별도 표에만 적었습니다.
[[/TIP]]

| 약어 | 풀네임 | 설명 |
|---|---|---|
| A2DP | Advanced Audio Distribution Profile | Classic 고음질 오디오 스트리밍 프로파일 |
| ACAD | Additional Controller Advertising Data | 확장 광고 헤더 안의 컨트롤러용 추가 데이터(채널 맵 갱신, BIGInfo 등) |
| ACL | Asynchronous Connection-Oriented | 비예약 데이터 논리 전송 |
| AD | Advertising Data | 광고·스캔 응답에 담는 Length-Type-Data 구조 |
| ADI | Advertising Data Info | 확장 광고의 데이터 ID(DID)와 광고 세트 ID(SID)를 담은 2바이트 필드 |
| AES-CCM | AES Counter with CBC-MAC | 인증 암호화 모드 |
| AES-CMAC | AES Cipher-based MAC | AES 기반 메시지 인증 코드 |
| AFH | Adaptive Frequency Hopping | 나쁜 채널을 빼고 도약하는 기법 (1.2) |
| AG | Audio Gateway | HFP에서 폰 쪽 역할 |
| AICS | Audio Input Control Service | 오디오 입력별 게인 제어 서비스 |
| AMP | Alternate MAC/PHY | 802.11을 빌린 고속 전송 (3.0, 5.3에서 제거) |
| AoA | Angle of Arrival | 도래각(수신기가 안테나 배열) |
| AoD | Angle of Departure | 발사각(송신기가 안테나 배열) |
| AppKey | Application Key | Mesh 응용(상위 전송) 계층 암호화 키 |
| APR | Acceptable Power Reduction | 상대가 줄여도 되는 송신 전력 여유 |
| ASCS | Audio Stream Control Service | ASE 상태를 관리하는 GATT 서비스 |
| ASE | Audio Stream Endpoint | 오디오 스트림 끝점 |
| ASHA | Audio Streaming for Hearing Aids | Google 독자 보청기 스트리밍 규격 |
| ATT | Attribute Protocol | 속성 읽기·쓰기·알림 프로토콜 |
| AVCTP | Audio/Video Control Transport Protocol | AV 리모컨 명령 전송 |
| AVDTP | Audio/Video Distribution Transport Protocol | 오디오·비디오 스트림 설정·전송 |
| AVRCP | Audio/Video Remote Control Profile | 재생 제어·메타데이터·절대 볼륨 프로파일 |
| BAP | Basic Audio Profile | LE Audio 스트림 설정 기본 프로파일 |
| BARB | Bluetooth Architecture Review Board | SIG 아키텍처 검토 위원회 |
| BAS | Battery Service | 배터리 잔량 서비스 |
| BASE | Broadcast Audio Source Endpoint | 브로드캐스트 코덱·BIS 구성 정보 구조 |
| BASS | Broadcast Audio Scan Service | 브로드캐스트 스캔을 위임받는 GATT 서비스 |
| BD_ADDR | Bluetooth Device Address | 48비트 Bluetooth 기기 주소 |
| BIAS | Bluetooth Impersonation AttackS | BR/EDR 사칭 공격 (2020) |
| BIG | Broadcast Isochronous Group | BIS의 묶음 |
| BIS | Broadcast Isochronous Stream | 방송 등시성 스트림 |
| BLOB | Binary Large Object | Mesh에서 전송하는 큰 데이터 덩어리 |
| BN | Burst Number | ISO 이벤트당 새 페이로드 수 |
| BNEP | Bluetooth Network Encapsulation Protocol | 이더넷 프레임 캡슐화 프로토콜 |
| BQE | Bluetooth Qualification Expert | 과거 SIG 인증 전문가 제도 |
| BR | Basic Rate | Classic의 기본 1 Mbps GFSK 전송 |
| BTP | Bluetooth Transport Protocol | Matter 커미셔닝용 GATT 위 전송 프로토콜 |
| CAC | Channel Access Code | 피코넷 식별용 접근 코드 |
| CAP | Common Audio Profile | 여러 기기에 공통 오디오 절차를 적용하는 프로파일 |
| CAS | Common Audio Service | CAP Acceptor가 노출하는 서비스 |
| CASE | Certificate Authenticated Session Establishment | Matter 인증서 기반 세션 수립 |
| CCC | Car Connectivity Consortium | 디지털 차량 키 규격 단체 |
| CCCD | Client Characteristic Configuration Descriptor | 알림/지시를 켜는 디스크립터 (0x2902) |
| CCID | Content Control ID | MCS/TBS 인스턴스 식별자 |
| CCP | Call Control Profile | 통화 제어 프로파일 |
| ChM | Channel Map | 연결에서 사용하는 데이터 채널 비트맵 |
| CID | Channel Identifier | L2CAP 논리 채널 번호 |
| CIG | Connected Isochronous Group | CIS의 묶음 |
| CIS | Connected Isochronous Stream | 연결 기반 등시성 스트림 |
| CLKE | Estimated Clock | 페이징 시 추정한 상대 기기 클럭 |
| CLKN | Native Clock | 기기의 자유 실행 28비트 클럭 (312.5 µs 틱) |
| CoC | Connection-oriented Channel | LE 크레딧 기반 동적 L2CAP 채널 |
| CRC | Cyclic Redundancy Check | 오류 검출 부호 (LE는 24비트) |
| CSIP | Coordinated Set Identification Profile | 코디네이트 세트 식별 프로파일 |
| CSIS | Coordinated Set Identification Service | 코디네이트 세트 식별 서비스 |
| CSRK | Connection Signature Resolving Key | 데이터 서명 키 |
| CSS | Core Specification Supplement | AD Type 등 데이터 정의 보충 문서 |
| CTE | Constant Tone Extension | 방향 탐지용 패킷 뒤 연속 톤 (5.1) |
| CTKD | Cross-Transport Key Derivation | LE와 BR/EDR 사이 키 유도 |
| CTL | Network Control | Mesh 네트워크 PDU의 Access/Control 메시지 구분 비트 |
| CTS | Current Time Service | 현재 시각 서비스 |
| CVSD | Continuously Variable Slope Delta modulation | 8 kHz 협대역 음성 코덱 |
| DAC | Device Access Code | 페이징용 접근 코드 |
| DBAF | Decision-Based Advertising Filtering | 광고자의 결정 PDU로 스캐너가 보조 패킷 수신 여부를 정하는 6.0 기능 |
| DevKey | Device Key | Provisioner와 노드 한 쌍만 아는 Mesh 설정용 키 |
| DFU | Device Firmware Update | Mesh 펌웨어 배포·업데이트 기능 |
| DHKey | Diffie-Hellman Key | ECDH 공유 비밀 |
| DID | Advertising Data ID | 광고 데이터가 바뀔 때마다 바뀌는 12비트 식별자 |
| DIS | Device Information Service | 제조사·모델·펌웨어 정보 서비스 |
| DLCI | Data Link Connection Identifier | RFCOMM 채널 식별자 |
| DLE | Data Length Extension | LE 데이터 PDU 길이 확장 (4.2) |
| DPSK | Differential Phase Shift Keying | 차동 위상 편이 변조 (EDR) |
| DQPSK | Differential Quadrature Phase Shift Keying | 차동 4위상 변조 (EDR 2 Mbps) |
| DRBG | Deterministic Random Bit Generator | CS 무작위화용 결정적 난수 생성기 |
| DTM | Direct Test Mode | LE RF 시험용 칩 시험 모드 |
| DTS | Digital Transmission System | FCC 15.247의 디지털 변조 장비 분류 |
| EAD | Encrypted Advertising Data | 암호화된 광고 데이터 (5.4) |
| EATT | Enhanced Attribute Protocol | 여러 L2CAP 채널 위의 ATT (5.2) |
| ECDH | Elliptic Curve Diffie-Hellman | 타원곡선 키 합의 |
| EDIV | Encrypted Diversifier | Legacy LTK 식별 값 |
| EDR | Enhanced Data Rate | Classic의 2/3 Mbps DPSK 전송 (2.0) |
| EIR | Extended Inquiry Response | 확장 조회 응답 (2.1) |
| EIRP | Equivalent Isotropically Radiated Power | 등가 등방 복사 전력 |
| ERTM | Enhanced Retransmission Mode | L2CAP 재전송·흐름 제어 모드 |
| eSCO | extended Synchronous Connection-Oriented | 재전송 창이 있는 음성 링크 |
| ESL | Electronic Shelf Label | 전자 가격표, PAwR을 쓰는 Bluetooth 프로파일 |
| ESR | Errata Service Release | Core 규격 정오 모음 문서 |
| FEC | Forward Error Correction | 수신 측이 재전송 없이 오류를 고치는 순방향 오류 정정 부호 |
| FHS | Frequency Hop Synchronization | 주소·클럭을 전달하는 Classic 제어 패킷 |
| FHSS | Frequency Hopping Spread Spectrum | 주파수 도약 확산 스펙트럼 |
| FRD | Functional Requirements Document | 새 규격의 기능 요구 사항 문서 |
| FT | Flush Timeout | ISO 페이로드를 시도할 수 있는 이벤트 수 |
| GAP | Generic Access Profile | 발견·연결·보안 모드와 역할 규칙 |
| GATT | Generic Attribute Profile | 서비스·특성 기반 데이터 모델 |
| GFSK | Gaussian Frequency Shift Keying | 가우시안 필터를 거친 주파수 편이 변조 |
| GIAC | General Inquiry Access Code | 일반 발견용 조회 접근 코드 |
| GMAP | Gaming Audio Profile | 게이밍 응용 프로파일 |
| GMCS | Generic Media Control Service | 대표 미디어 제어 서비스 인스턴스 |
| GOEP | Generic Object Exchange Profile | OBEX 기반 프로파일 공통 틀 |
| GSS | GATT Specification Supplement | 특성 값 형식을 정의하는 보충 규격 |
| GTBS | Generic Telephone Bearer Service | 대표 통화 서비스 인스턴스 |
| HAP | Hearing Access Profile | 보청기 응용 프로파일 |
| HAS | Hearing Access Service | 보청기 프리셋 서비스 |
| HCI | Host Controller Interface | Host와 Controller 사이 표준 명령·이벤트·데이터 인터페이스 |
| HDT | High Data Throughput | LE 고속 데이터 전송 PHY (논의 중) |
| HFP | Hands-Free Profile | 통화용 핸즈프리 프로파일 |
| HOGP | HID over GATT Profile | LE로 키보드·마우스를 연결하는 프로파일 |
| HSP | Headset Profile | 최소 기능 헤드셋 프로파일 |
| IAC | Inquiry Access Code | 조회용 접근 코드 |
| ICS | Implementation Conformance Statement | 구현 기능 적합성 선언 |
| IOP | Interoperability | 상호 운용성 (시험) |
| IRC | Immediate Repetition Count | BIS 이벤트 안 반복 횟수 |
| IRK | Identity Resolving Key | RPA 생성·해석용 128비트 키 |
| ISM | Industrial, Scientific and Medical | 비면허 공용 주파수 대역 |
| ISO | Isochronous | 등시성 (CIS·BIS 채널) |
| ISOAL | Isochronous Adaptation Layer | SDU와 ISO PDU 사이 분할·조립 계층 |
| IV | Initialization Vector | 논스의 고정 부분 |
| IVI | IV Index Indicator | Mesh 네트워크 PDU의 IV Index 최하위 비트 |
| IXIT | Implementation eXtra Information for Testing | 시험용 구현 추가 정보 |
| KNOB | Key Negotiation of Bluetooth | 키 길이 다운그레이드 공격 (2019) |
| L2CAP | Logical Link Control and Adaptation Protocol | 채널 다중화와 분할·재조립 계층 |
| LAP | Lower Address Part | BD_ADDR 하위 24비트 |
| LC3 | Low Complexity Communication Codec | LE Audio 필수 오디오 코덱 |
| LC3-SWB | LC3 Super Wideband | HFP 1.9의 32 kHz 초광대역 음성 코덱 |
| LE | Low Energy | Bluetooth 4.0에서 도입된 저전력 무선 방식 |
| LIAC | Limited Inquiry Access Code | 제한 발견용 조회 접근 코드 |
| LL | Link Layer | LE 링크 계층 |
| LLID | Logical Link Identifier | LE 데이터 PDU 헤더에서 L2CAP 시작·이어짐·LL 제어를 구분하는 2비트 필드 |
| LMP | Link Manager Protocol | Classic Controller 간 링크 제어 프로토콜 |
| LPN | Low Power Node | Friend에 메시지를 맡기고 대부분 잠자는 Mesh 노드 |
| LT_ADDR | Logical Transport Address | 피코넷 안 Peripheral의 3비트 주소 |
| LTK | Long Term Key | 재연결 암호화에 쓰는 장기 키 |
| LTPF | Long-Term Postfilter | LC3 장기 후처리 필터 |
| MAP | Message Access Profile | 문자 메시지 접근 프로파일 |
| MCP | Media Control Profile | 미디어 제어 프로파일 |
| MCS | Media Control Service | 미디어 플레이어 상태·제어 서비스 |
| MD | More Data | 이벤트 안에 보낼 데이터가 더 있음을 알리는 헤더 비트 |
| MICP | Microphone Control Profile | 마이크 제어 프로파일 |
| MICS | Microphone Control Service | 마이크 음소거 서비스 |
| MITM | Man-In-The-Middle | 중간자 공격 |
| MPS | Maximum PDU Payload Size | K-frame 하나의 최대 페이로드 크기 |
| mSBC | modified SBC | HFP 광대역(16 kHz) 음성 코덱 |
| MTU | Maximum Transmission Unit | 한 번에 보낼 수 있는 최대 SDU 크기 (ATT MTU 등) |
| MWS | Mobile Wireless Standards | 셀룰러 등 인접 무선과의 공존 신호 (Vol 7) |
| NADM | Normalized Attack Detector Metric | CS 공격 탐지 지표 |
| NESN | Next Expected Sequence Number | LE 데이터 PDU 헤더의 다음 기대 순서 번호(ACK 역할) |
| NetKey | Network Key | Mesh 네트워크 계층 암호화 키 |
| NID | Network Identifier | NetKey에서 유도한 7비트 네트워크 PDU 식별값 |
| NLC | Networked Lighting Control | 상업용 조명용 Mesh 프로파일 묶음 |
| NRPA | Non-Resolvable Private Address | 해석 불가능한 비공개 주소 |
| NSE | Number of Subevents | ISO 이벤트당 서브이벤트 수 |
| NWP | New Work Proposal | SIG 새 작업 제안 |
| OBEX | Object Exchange | 객체 교환 프로토콜 |
| OCF | Opcode Command Field | HCI Opcode 하위 10비트 명령 번호 |
| OGF | Opcode Group Field | HCI Opcode 상위 6비트 명령 그룹 |
| OOB | Out-of-Band | Bluetooth 밖의 채널로 인증 값 전달 |
| OPP | Object Push Profile | OBEX 객체 보내기 프로파일 |
| OUI | Organizationally Unique Identifier | IEEE가 회사에 배정하는 24비트 식별자 |
| PAC | Published Audio Capability | 코덱 능력 레코드 |
| PACS | Published Audio Capabilities Service | 오디오 능력(PAC 레코드)을 공개하는 GATT 서비스 |
| PAN | Personal Area Networking Profile | 블루투스 IP 네트워킹 프로파일 |
| PANU | PAN User | PAN 사용자 기기 역할 |
| PASE | Passcode-Authenticated Session Establishment | Matter 설정 코드 기반 세션 수립 |
| PAST | Periodic Advertising Sync Transfer | 주기적 광고 동기 정보를 LE 연결로 넘겨주는 절차 (5.1) |
| PAwR | Periodic Advertising with Responses | 응답 있는 주기적 광고 (5.4) |
| PB-ADV | Provisioning Bearer over Advertising | 광고 패킷으로 프로비저닝 PDU를 나르는 베어러 |
| PB-GATT | Provisioning Bearer over GATT | GATT 연결로 프로비저닝 PDU를 나르는 베어러 |
| PBAP | Phone Book Access Profile | 전화번호부 접근 프로파일 |
| PBP | Public Broadcast Profile | 공공 브로드캐스트 프로파일 |
| PBR | Phase-Based Ranging | 위상 기반 거리 측정 |
| PDU | Protocol Data Unit | 계층이 주고받는 데이터 단위 |
| PHY | Physical Layer | 물리계층 (LE 1M·2M·Coded) |
| PPK | Power Profiler Kit | Nordic 전류 측정 도구 |
| PTA | Packet Traffic Arbitration | Bluetooth·Wi-Fi 송신 시간 중재 |
| PTO | Pre-Transmission Offset | BIS 사전 전송 오프셋 |
| PTS | Profile Tuning Suite | SIG 적합성 시험 도구 |
| QDID | Qualified Design ID | 2024.7 이전 인증 설계 식별자 |
| QPRD | Qualification Program Reference Document | SIG 인증 프로그램 규정 문서 |
| RAP | Ranging Profile | CS 거리 측정 프로파일 |
| RAS | Ranging Service | CS 측정 결과 전달 GATT 서비스 |
| RFCOMM | Radio Frequency Communication | 직렬 포트 에뮬레이션 프로토콜 |
| RPA | Resolvable Private Address | IRK로 해석 가능한 비공개 주소 |
| RPL | Replay Protection List | SRC별 최신 SEQ를 저장해 재전송 공격을 막는 목록 |
| RSI | Resolvable Set Identifier | SIRK로 해석하는 세트 식별 광고 값 |
| RSSI | Received Signal Strength Indicator | 수신 신호 세기 지표 |
| RTN | Retransmission Number | Host가 요청하는 ISO 재전송 횟수 |
| RTT | Round-Trip Time | 왕복 시간 기반 거리 측정 |
| SAR | Segmentation and Reassembly | 긴 메시지를 조각내고 다시 모으는 동작 |
| SBC | Low Complexity Subband Codec | A2DP 필수 코덱 |
| SCA | Sleep Clock Accuracy | 수면 클럭 정확도 (ppm) |
| SCCD | Server Characteristic Configuration Descriptor | 브로드캐스트를 켜는 디스크립터 (0x2903) |
| SCI | Shorter Connection Intervals | Core 6.2의 짧은 연결 간격 기능 |
| SCO | Synchronous Connection-Oriented | 예약 슬롯 음성 링크 (재전송 없음) |
| SDP | Service Discovery Protocol | Classic 서비스 검색 프로토콜 |
| SDU | Service Data Unit | 상위 계층이 넘겨준 데이터 단위 |
| SEP | Stream End Point | AVDTP 스트림 끝점 |
| SID | Advertising Set ID | 확장 광고 세트를 공중에서 구분하는 4비트 식별자 |
| SIG | Bluetooth Special Interest Group | Bluetooth 규격·인증·상표를 관리하는 단체 |
| SIRK | Set Identity Resolving Key | 코디네이트 세트 공통 키 |
| SLC | Service Level Connection | HFP의 RFCOMM 기반 제어 연결 |
| SMP | Security Manager Protocol | LE 페어링·키 분배 프로토콜 |
| SNS | Spectral Noise Shaping | LC3 스펙트럼 노이즈 셰이핑 |
| SPP | Serial Port Profile | 가상 시리얼 포트 프로파일 |
| SPSM | Simplified Protocol/Service Multiplexer | LE 크레딧 기반 채널의 서비스 식별 번호 |
| SSP | Secure Simple Pairing | Classic 간편 보안 페어링 (2.1) |
| STK | Short Term Key | LE Legacy 페어링의 단기 키 |
| T_IFS | Inter Frame Space | LE에서 연속 패킷 사이의 간격 150 µs |
| T_MAFS | Minimum AUX Frame Space | 같은 체인의 연속 보조 광고 패킷 사이 최소 간격 300 µs |
| TBS | Telephone Bearer Service | 통화 상태·제어 서비스 |
| TCRL | Test Case Reference List | 유효 시험 케이스 목록 |
| TGAP | GAP timers and constants | GAP 권장 타이밍 파라미터 묶음 |
| TIS | Total Isotropic Sensitivity | 제품 전체 등방 수신 감도 |
| TK | Temporary Key | LE Legacy 페어링 입력 키 |
| TMAP | Telephony and Media Audio Profile | 전화·미디어 응용 프로파일 |
| TNS | Temporal Noise Shaping | 시간 영역 노이즈 셰이핑 |
| TRP | Total Radiated Power | 제품 전체 방사 전력 |
| TTL | Time To Live | 메시지가 더 전달될 수 있는 홉 수 |
| UAP | Upper Address Part | BD_ADDR 중간 8비트 |
| UTP | Unified Test Protocol | LE RF 시험 프로토콜 (6.2) |
| UUID | Universally Unique Identifier | 서비스·특성을 구분하는 16/32/128비트 식별자 |
| UWB | Ultra-Wideband | 초광대역 무선 측위 기술 |
| VCP | Volume Control Profile | 볼륨 제어 프로파일 |
| VCS | Volume Control Service | 볼륨 상태 서비스 |
| VNA | Vector Network Analyzer | S11 등 임피던스 측정 장비 |
| VOCS | Volume Offset Control Service | 채널별 볼륨 보정 서비스 |
| WCI | Wireless Coexistence Interface | MWS 공존 신호 전송 인터페이스 |

## 여러 뜻이 있는 약어 (🔵 중급)

| 약어 | 뜻 1 | 뜻 2 |
|---|---|---|
| AA | Access Address (LE 접속 주소) | Authentication Algorithm 등 |
| CS | Channel Sounding (6.0 거리 측정) | Carrier Sense, Coordinated Set 등 문맥에 따라 |
| CSA | Channel Selection Algorithm (LE 채널 선택 #1/#2) | Core Specification Addendum (규격 부록) |
| MIC | Message Integrity Check (암호화 시 4 B 무결성 값) | Microphone (MICP 등) |
| NAP | Non-significant Address Part (BD_ADDR 상위 16비트) | Network Access Point (PAN 프로파일 역할) |
| PA | Periodic Advertising (주기적 광고) | Power Amplifier (전력 증폭기) |
| SC | Secure Connections (P-256 기반 페어링) | Sub-Carrier 등 문맥에 따라 |

## 관련 페이지

- **규격 인덱스** — 프로파일·서비스 규격 약어와 이름
- **Core 버전별 기능 인덱스** — 기능 이름으로 찾기
