# 계산기

!!! spec "계산식 출처"
    LE 패킷 길이와 airtime: Core Vol 6 Part B (Link Layer) 패킷 형식, Coded PHY 필드 길이 · T_IFS 150 µs: Core Vol 6 Part B · BR/EDR 패킷 종류와 페이로드: Core Vol 2 Part B (Baseband) · 채널 주파수: Core Vol 6 Part A (LE PHY), Vol 2 Part A (BR/EDR Radio) · 최소 수신 감도: Core Vol 6 Part A · 경로 손실: Friis 자유 공간 식

!!! basic "사용법"
    값을 바꾸면 결과가 바로 갱신됩니다. 모든 계산은 브라우저에서만 이루어집니다. 공식과 표는 `tools/bt_numbers.py`와 같은 값을 씁니다.

## LE 패킷 airtime과 연결 처리량 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>PHY
      <select id="tp-phy">
        <option value="1M">LE 1M</option>
        <option value="2M" selected>LE 2M</option>
        <option value="S2">LE Coded S=2</option>
        <option value="S8">LE Coded S=8</option>
      </select>
    </label>
    <label>PDU 페이로드 (바이트, 0–251)
      <input id="tp-len" type="number" min="0" max="251" value="251">
    </label>
    <label>암호화 (MIC 4 B)
      <select id="tp-mic">
        <option value="0">없음</option>
        <option value="1" selected>있음</option>
      </select>
    </label>
    <label>연결 간격 (ms)
      <input id="tp-ci" type="number" min="7.5" step="1.25" value="30">
    </label>
    <label>이벤트당 최대 패킷 쌍 (0 = 제한 없음)
      <input id="tp-max" type="number" min="0" value="0">
    </label>
  </div>
  <div class="calc-result">
    <div>데이터 패킷 <b id="tp-air">—</b> µs · 빈 응답 패킷 <b id="tp-empty">—</b> µs · 한 쌍 주기 <b id="tp-cycle">—</b> µs · 이벤트당 <b id="tp-pairs">—</b>쌍</div>
    <div class="calc-big"><span id="tp-out">—</span> kbps <small>(응용 데이터, ATT Notification 기준)</small></div>
    <div><small id="tp-note"></small></div>
  </div>
</div>

## Classic ACL 최대 처리량 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>패킷 종류
      <select id="acl-pkt"></select>
    </label>
  </div>
  <div class="calc-result">
    <div>슬롯 <b id="acl-slots">—</b> · 최대 페이로드 <b id="acl-size">—</b> 바이트</div>
    <div class="calc-big">비대칭 <span id="acl-asym">—</span> kbps · 대칭 <span id="acl-sym">—</span> kbps</div>
  </div>
</div>

## 채널 번호 ↔ 중심 주파수 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>방식
      <select id="ch-mode">
        <option value="le" selected>LE (채널 인덱스 0–39)</option>
        <option value="br">BR/EDR (채널 0–78)</option>
      </select>
    </label>
    <label>채널 번호
      <input id="ch-n" type="number" min="0" max="78" value="37">
    </label>
    <label>중심 주파수 (MHz)
      <input id="ch-f" type="number" min="2402" max="2480" value="2402">
    </label>
  </div>
  <div class="calc-result"><span id="ch-note"></span></div>
</div>

## 평균 전류와 배터리 수명 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>이벤트 평균 전류 (mA)
      <input id="bt-ie" type="number" step="0.1" value="5">
    </label>
    <label>이벤트 길이 (ms)
      <input id="bt-te" type="number" step="0.1" value="2.5">
    </label>
    <label>이벤트 주기 (ms) — 광고 간격 또는 연결 간격
      <input id="bt-int" type="number" value="1000">
    </label>
    <label>대기 전류 (µA)
      <input id="bt-sleep" type="number" step="0.1" value="2">
    </label>
    <label>배터리 용량 (mAh)
      <input id="bt-cap" type="number" value="220">
    </label>
    <label>사용 가능 비율 (%)
      <input id="bt-derate" type="number" min="1" max="100" value="80">
    </label>
  </div>
  <div class="calc-result">
    <div>이벤트당 전하 <b id="bt-q">—</b> µC</div>
    <div class="calc-big">평균 <span id="bt-avg">—</span> µA · 수명 약 <span id="bt-life">—</span></div>
  </div>
</div>

## 경로 손실과 링크 버짓 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>송신 출력 (dBm)
      <input id="lb-pt" type="number" value="0">
    </label>
    <label>안테나 이득 합 (dBi)
      <input id="lb-g" type="number" value="0">
    </label>
    <label>거리 (m)
      <input id="lb-d" type="number" min="0.1" value="20">
    </label>
    <label>벽 개수
      <input id="lb-walls" type="number" min="0" value="1">
    </label>
    <label>벽당 손실 (dB)
      <input id="lb-wl" type="number" value="6">
    </label>
    <label>PHY (규격 최소 감도)
      <select id="lb-phy">
        <option value="-70">LE 1M (−70 dBm)</option>
        <option value="-70">LE 2M (−70 dBm)</option>
        <option value="-75">LE Coded S=2 (−75 dBm)</option>
        <option value="-82">LE Coded S=8 (−82 dBm)</option>
      </select>
    </label>
    <label>수신 감도 (dBm) — 칩 데이터시트 값으로 바꿔 쓰기
      <input id="lb-sens" type="number" value="-70">
    </label>
  </div>
  <div class="calc-result">
    <div>자유 공간 손실 (2440 MHz) <b id="lb-fspl">—</b> dB</div>
    <div class="calc-big">수신 전력 <span id="lb-pr">—</span> dBm · 여유 <span id="lb-margin">—</span> dB</div>
    <div>자유 공간에서 감도까지의 거리 (벽 손실 반영): <b id="lb-range">—</b></div>
  </div>
</div>

??? expert "계산기 사용 시 주의"
    - **처리량**은 한쪽만 데이터를 보내고 반대쪽은 빈 패킷으로 응답하는 경우의 상한입니다. 연결 이벤트를 연결 간격 끝까지 채울 수 있다고 가정했으므로, 실제 처리량은 컨트롤러가 허용하는 이벤트 길이와 이벤트당 패킷 수(플랫폼 제약)에 따라 크게 줄어듭니다. 이 값을 "이벤트당 최대 패킷 쌍"에 넣어 보세요([처리량 최적화](../host/throughput.md)).
    - 응용 데이터는 PDU 페이로드에서 L2CAP 헤더 4 B와 ATT Notification 헤더 3 B를 뺀 값입니다.
    - **Classic ACL**의 비대칭 값은 한 방향이 다중 슬롯 패킷, 반대 방향이 1슬롯 패킷일 때, 대칭 값은 양방향 모두 같은 패킷일 때의 값입니다.
    - **배터리 수명**은 이벤트 전류를 평균값 하나로 본 단순 모델입니다. 실제로는 깨어남·RX·TX 구간 전류가 다르므로 전류 분석기로 측정한 이벤트당 전하를 쓰는 편이 정확합니다([저전력 설계와 전류 프로파일](../practice/power-profile.md)). 코인셀은 펄스 전류와 온도에 따라 쓸 수 있는 용량이 줄어듭니다.
    - **링크 버짓**의 규격 최소 감도는 요구 하한이라 실제 칩은 대개 20 dB 이상 좋습니다. 실내에서는 다중 경로·인체 손실로 수–10 dB 이상 차이 날 수 있습니다([무선 전파와 링크 버짓](../basics/radio-channel.md)).

<script src="../../javascripts/calculators.js"></script>
