// 레퍼런스 > 계산기 페이지 전용 스크립트
// 공식과 표는 tools/bt_numbers.py와 같은 값을 쓴다 (본문 수치의 단일 출처).
(function () {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const num = (id) => parseFloat($(id).value);
  const fmt = (x, d = 1) => Number.isFinite(x) ? x.toLocaleString("ko-KR", { maximumFractionDigits: d, minimumFractionDigits: d }) : "—";

  // ---------- 1. LE airtime과 처리량 ----------
  const T_IFS = 150;
  const HEADER = 2, CRC = 3, MIC = 4, L2CAP_ATT = 7;

  function airtime(phy, payload, mic) {
    const pdu = HEADER + payload + (mic ? MIC : 0);
    if (phy === "1M") return (1 + 4 + pdu + CRC) * 8;
    if (phy === "2M") return (2 + 4 + pdu + CRC) * 4;
    const s = phy === "S2" ? 2 : 8;
    return 80 + 256 + 16 + 24 + (pdu + CRC) * 8 * s + 3 * s;
  }

  function throughput() {
    const phy = $("tp-phy").value;
    const len = Math.max(0, Math.min(251, Math.round(num("tp-len"))));
    const mic = $("tp-mic").value === "1";
    const ci = num("tp-ci");
    const maxPairs = Math.max(0, Math.round(num("tp-max")));
    const air = airtime(phy, len, mic);
    const empty = airtime(phy, 0, mic);
    const cycle = air + T_IFS + empty + T_IFS;
    let pairs = Math.floor((ci * 1000 + T_IFS) / cycle);
    if (maxPairs > 0) pairs = Math.min(pairs, maxPairs);
    const app = Math.max(0, len - L2CAP_ATT);
    const kbps = pairs * app * 8 / ci;
    $("tp-air").textContent = fmt(air, 0);
    $("tp-empty").textContent = fmt(empty, 0);
    $("tp-cycle").textContent = fmt(cycle, 0);
    $("tp-pairs").textContent = pairs;
    $("tp-out").textContent = fmt(kbps, 1);
    let note = `상한(간격 무시): ${fmt(app * 8 * 1000 / cycle, 1)} kbps`;
    if (ci < 7.5) note += " · ⚠ 일반 연결 간격 최소값은 7.5 ms";
    if (len > 27) note += " · 27 B 초과 페이로드는 DLE(데이터 길이 확장) 필요";
    $("tp-note").textContent = note;
  }

  // ---------- 2. Classic ACL ----------
  const SLOT = 625;
  const ACL = {
    DM1: [1, 17], DH1: [1, 27], DM3: [3, 121], DH3: [3, 183], DM5: [5, 224], DH5: [5, 339],
    "2-DH1": [1, 54], "2-DH3": [3, 367], "2-DH5": [5, 679],
    "3-DH1": [1, 83], "3-DH3": [3, 552], "3-DH5": [5, 1021],
  };

  function acl() {
    const [slots, size] = ACL[$("acl-pkt").value];
    $("acl-slots").textContent = slots;
    $("acl-size").textContent = size;
    $("acl-asym").textContent = fmt(size * 8 * 1000 / ((slots + 1) * SLOT), 1);
    $("acl-sym").textContent = fmt(size * 8 * 1000 / (2 * slots * SLOT), 1);
  }

  // ---------- 3. 채널 ↔ 주파수 ----------
  const ADV = { 37: 2402, 38: 2426, 39: 2480 };
  function leFreq(ch) {
    if (ch in ADV) return ADV[ch];
    if (ch >= 0 && ch <= 10) return 2404 + 2 * ch;
    if (ch >= 11 && ch <= 36) return 2428 + 2 * (ch - 11);
    return NaN;
  }

  function chToF() {
    const mode = $("ch-mode").value;
    const ch = Math.round(num("ch-n"));
    if (mode === "le") {
      const f = leFreq(ch);
      if (!Number.isFinite(f)) { $("ch-note").textContent = "LE 채널 인덱스는 0–39"; return; }
      $("ch-f").value = f;
      const kind = ch >= 37 ? "주 광고 채널" : "데이터(보조 광고) 채널";
      $("ch-note").textContent = `채널 ${ch} · ${f} MHz · RF 채널 ${(f - 2402) / 2} · ${kind} · 점유 ${f - 1}–${f + 1} MHz`;
    } else {
      if (!(ch >= 0 && ch <= 78)) { $("ch-note").textContent = "BR/EDR 채널은 0–78"; return; }
      const f = 2402 + ch;
      $("ch-f").value = f;
      $("ch-note").textContent = `채널 ${ch} · ${f} MHz · 점유 ${f - 0.5}–${f + 0.5} MHz`;
    }
  }

  function fToCh() {
    const mode = $("ch-mode").value;
    const f = Math.round(num("ch-f"));
    if (mode === "le") {
      for (let ch = 0; ch < 40; ch++) {
        if (leFreq(ch) === f) { $("ch-n").value = ch; chToF(); return; }
      }
      $("ch-note").textContent = "LE 채널은 2402–2480 MHz의 짝수 MHz";
    } else {
      if (f >= 2402 && f <= 2480) { $("ch-n").value = f - 2402; chToF(); return; }
      $("ch-note").textContent = "BR/EDR 채널은 2402–2480 MHz";
    }
  }

  // ---------- 4. 배터리 수명 ----------
  function battery() {
    const q = num("bt-ie") * num("bt-te"); // mA × ms = µC
    const avg = q / (num("bt-int") / 1000) + num("bt-sleep"); // µA
    const hours = num("bt-cap") * (num("bt-derate") / 100) * 1000 / avg;
    $("bt-q").textContent = fmt(q, 2);
    $("bt-avg").textContent = fmt(avg, 2);
    const days = hours / 24;
    $("bt-life").textContent = days >= 365 ? `${fmt(days / 365, 1)}년` : `${fmt(days, 0)}일`;
  }

  // ---------- 5. 링크 버짓 ----------
  function link() {
    const pt = num("lb-pt"), g = num("lb-g"), d = num("lb-d");
    const loss = num("lb-walls") * num("lb-wl");
    const sens = num("lb-sens");
    const fspl = 20 * Math.log10(d) + 20 * Math.log10(2440) - 27.55;
    const pr = pt + g - fspl - loss;
    const budget = pt + g - loss - sens; // 허용 경로 손실
    const range = Math.pow(10, (budget - 20 * Math.log10(2440) + 27.55) / 20);
    $("lb-fspl").textContent = fmt(fspl, 1);
    $("lb-pr").textContent = fmt(pr, 1);
    $("lb-margin").textContent = fmt(pr - sens, 1);
    $("lb-range").textContent = range >= 1000 ? `${fmt(range / 1000, 2)} km` : `${fmt(range, 0)} m`;
  }

  function init() {
    if (!$("tp-phy")) return;
    ["tp-phy", "tp-len", "tp-mic", "tp-ci", "tp-max"].forEach((id) => $(id).addEventListener("input", throughput));
    throughput();

    $("acl-pkt").innerHTML = Object.keys(ACL).map((k) => `<option value="${k}">${k}</option>`).join("");
    $("acl-pkt").value = "3-DH5";
    $("acl-pkt").addEventListener("change", acl);
    acl();

    $("ch-mode").addEventListener("change", () => {
      $("ch-n").value = $("ch-mode").value === "le" ? 37 : 0;
      chToF();
    });
    $("ch-n").addEventListener("input", chToF);
    $("ch-f").addEventListener("change", fToCh);
    chToF();

    ["bt-ie", "bt-te", "bt-int", "bt-sleep", "bt-cap", "bt-derate"].forEach((id) => $(id).addEventListener("input", battery));
    battery();

    $("lb-phy").addEventListener("change", () => { $("lb-sens").value = $("lb-phy").value; link(); });
    ["lb-pt", "lb-g", "lb-d", "lb-walls", "lb-wl", "lb-sens"].forEach((id) => $(id).addEventListener("input", link));
    link();
  }

  // Material의 instant navigation에도 대응
  if (window.document$) window.document$.subscribe(init);
  else document.addEventListener("DOMContentLoaded", init);
})();
