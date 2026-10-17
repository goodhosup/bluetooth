"""본문에 들어가는 Bluetooth 수치를 계산·검산하는 단일 출처.

채널 번호 ↔ 주파수, 패킷 airtime, 연결 처리량, Classic ACL 처리량을 여기서 계산하고
본문 표와 계산기(docs/javascripts/calculators.js)는 이 값과 일치해야 한다.

    python tools/bt_numbers.py            # 주요 표 출력
    python tools/bt_numbers.py --check    # 본문에 적힌 대표 값 검산 (불일치 시 종료 코드 1)
"""
from __future__ import annotations

import argparse
import sys
from fractions import Fraction as F

# ---------------------------------------------------------------- 채널
# LE: RF 채널 k = 0..39, f = 2402 + 2k MHz. 광고 채널 37/38/39 = RF 0/12/39.
ADV_CH = {37: 2402, 38: 2426, 39: 2480}


def le_freq(ch: int) -> int:
    """LE 채널 인덱스(0–39) → 중심 주파수 (MHz)."""
    if ch in ADV_CH:
        return ADV_CH[ch]
    if 0 <= ch <= 10:
        return 2404 + 2 * ch
    if 11 <= ch <= 36:
        return 2428 + 2 * (ch - 11)
    raise ValueError(ch)


def le_channel(freq: int) -> int:
    for ch in range(40):
        if le_freq(ch) == freq:
            return ch
    raise ValueError(freq)


def br_freq(k: int) -> int:
    """BR/EDR 채널 k = 0..78 → 2402 + k MHz."""
    if not 0 <= k <= 78:
        raise ValueError(k)
    return 2402 + k


# ---------------------------------------------------------------- LE 패킷 airtime (µs)
T_IFS = 150  # 연속 패킷 사이 간격 (µs)
CRC = 3      # 바이트
MIC = 4      # 암호화 시 바이트
HEADER = 2   # 데이터 채널 PDU 헤더 (CTE 없음)


def le_airtime(phy: str, payload: int, mic: bool = False) -> F:
    """LE 패킷 한 개의 공중 시간 (µs). payload는 PDU 페이로드 바이트 (0–251).

    1M: 프리앰블 1 B, 2M: 프리앰블 2 B, 비트당 1 / 0.5 µs.
    Coded: 프리앰블 80 µs + AA 256 µs + CI 16 µs + TERM1 24 µs (항상 S=8)
           + (PDU + CRC) 비트 × S + TERM2 3비트 × S.
    """
    pdu = HEADER + payload + (MIC if mic else 0)
    if phy == "1M":
        return F((1 + 4 + pdu + CRC) * 8)
    if phy == "2M":
        return F((2 + 4 + pdu + CRC) * 8, 2)
    if phy in ("S2", "S8"):
        s = 2 if phy == "S2" else 8
        return F(80 + 256 + 16 + 24 + (pdu + CRC) * 8 * s + 3 * s)
    raise ValueError(phy)


def le_throughput(phy: str, payload: int = 251, mic: bool = False, l2cap_att: int = 7) -> F:
    """연결 이벤트 안에서 한쪽만 데이터를 계속 보낼 때의 응용 처리량 (kbps).

    데이터 패킷 → T_IFS → 빈 패킷(응답) → T_IFS 를 반복한다고 가정.
    l2cap_att: L2CAP 헤더 4 B + ATT Notification 헤더 3 B = 7 B 를 뺀 응용 데이터.
    연결 이벤트 사이의 빈 시간은 무시 (이벤트를 꽉 채운 상한).
    """
    cycle = le_airtime(phy, payload, mic) + T_IFS + le_airtime(phy, 0, mic) + T_IFS
    return F((payload - l2cap_att) * 8 * 1000, 1) / cycle


# ---------------------------------------------------------------- BR/EDR ACL
SLOT = 625  # µs
# 패킷 종류 → (슬롯 수, 최대 페이로드 바이트)
ACL = {
    "DM1": (1, 17), "DH1": (1, 27), "DM3": (3, 121), "DH3": (3, 183), "DM5": (5, 224), "DH5": (5, 339),
    "2-DH1": (1, 54), "2-DH3": (3, 367), "2-DH5": (5, 679),
    "3-DH1": (1, 83), "3-DH3": (3, 552), "3-DH5": (5, 1021),
}


def acl_max_rate(pkt: str) -> F:
    """비대칭 최대 처리량 (kbps): 한 방향은 pkt, 반대 방향은 1슬롯 패킷."""
    slots, size = ACL[pkt]
    return F(size * 8 * 1000, (slots + 1) * SLOT)


# ---------------------------------------------------------------- 평균 전류
def avg_current_ua(event_charge_uc: float, interval_ms: float, sleep_ua: float) -> float:
    """이벤트 한 번의 전하(µC)와 주기(ms), 대기 전류(µA) → 평균 전류(µA)."""
    return event_charge_uc / (interval_ms / 1000) + sleep_ua


# ---------------------------------------------------------------- 출력·검산
def show() -> None:
    print("LE 채널 → 주파수")
    print("  " + ", ".join(f"{c}:{le_freq(c)}" for c in range(40)))
    print("\nLE 패킷 airtime (µs) — 페이로드 0 / 27 / 251 B, MIC 없음 / 있음")
    for phy in ("1M", "2M", "S2", "S8"):
        row = [le_airtime(phy, n, m) for n in (0, 27, 251) for m in (False, True)]
        print(f"  {phy:>2}: " + "  ".join(f"{float(x):7.0f}" for x in row))
    print("\nLE 응용 처리량 상한 (kbps, 251 B PDU, ATT Notification)")
    for phy in ("1M", "2M", "S2", "S8"):
        print(f"  {phy:>2}: {float(le_throughput(phy)):7.1f}  (27 B PDU: {float(le_throughput(phy, 27)):6.1f})")
    print("\nBR/EDR ACL 비대칭 최대 처리량 (kbps)")
    for pkt in ACL:
        print(f"  {pkt:>5}: {float(acl_max_rate(pkt)):7.1f}")


# (설명, 계산값, 본문에 쓰는 값, 허용 오차)
def checks():
    return [
        ("광고 채널 38 주파수", le_freq(38), 2426, 0),
        ("데이터 채널 10 주파수", le_freq(10), 2424, 0),
        ("데이터 채널 11 주파수", le_freq(11), 2428, 0),
        ("데이터 채널 36 주파수", le_freq(36), 2478, 0),
        ("1M 빈 패킷", le_airtime("1M", 0), 80, 0),
        ("1M 27 B + MIC", le_airtime("1M", 27, True), 328, 0),
        ("1M 251 B + MIC (최대)", le_airtime("1M", 251, True), 2120, 0),
        ("2M 251 B + MIC", le_airtime("2M", 251, True), 1064, 0),
        ("Coded S8 27 B + MIC (DLE 이전 최대)", le_airtime("S8", 27, True), 2704, 0),
        ("Coded S8 251 B + MIC (최대)", le_airtime("S8", 251, True), 17040, 0),
        ("1M 처리량 상한 (kbps)", le_throughput("1M"), 791, 1),
        ("2M 처리량 상한 (kbps)", le_throughput("2M"), 1402, 1),
        ("DH5 비대칭 (kbps)", acl_max_rate("DH5"), F(7232, 10), F(1, 10)),
        ("2-DH5 비대칭 (kbps)", acl_max_rate("2-DH5"), F(14485, 10), F(1, 10)),
        ("3-DH5 비대칭 (kbps)", acl_max_rate("3-DH5"), F(21781, 10), F(1, 10)),
    ]


def check() -> int:
    bad = 0
    for desc, got, want, tol in checks():
        ok = abs(F(got) - F(want)) <= tol
        bad += not ok
        print(f"  {'✓' if ok else '✗'} {desc}: {float(got):.1f} (본문 {float(want):g})")
    print("불일치", bad, "건" if bad else "— 모두 일치")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        return check()
    show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
