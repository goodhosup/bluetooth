"""Classic (BR/EDR) 그림

1. classic_slots  : 625 µs 슬롯 TDD — 1/3/5 슬롯 패킷과 도약 주파수 (Central 짝수 슬롯 시작)
2. classic_packet : BR 패킷과 EDR 패킷의 필드 배치 (Access Code · Header · Guard · Sync · Payload · Trailer)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import style as s


def box(ax, x, y, w, h, fc, label="", fs=8, ec="#ffffff", lw=1.2, tc=None):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=tc or s.text_on(fc))


def span(ax, x0, x1, y, text, color=None, fs=7.5):
    color = color or s.INK2
    ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="<->", color=color, lw=0.9))
    ax.text((x0 + x1) / 2, y - 0.08, text, ha="center", va="top", fontsize=fs, color=color)


def classic_slots():
    """슬롯 k = 0..13. 1 슬롯 = 1 단위. 패킷은 슬롯 경계에서 시작, 다중 슬롯 패킷 동안 주파수 고정."""
    fig, ax = plt.subplots(figsize=(13, 4.4))
    s.bare(ax)
    n = 14
    h = 0.55
    yc, yp = 1.9, 0.9
    # 슬롯 경계와 번호
    for k in range(n + 1):
        ax.plot([k, k], [0.6, 2.75], color=s.GRID, lw=0.8, zorder=0)
    for k in range(n):
        ax.text(k + 0.5, 2.85, str(k), ha="center", va="bottom", fontsize=8, color=s.INK2)
    ax.text(-0.2, 2.95, "slot k", ha="right", va="bottom", fontsize=8, color=s.INK2)
    for y, lab in ((yc, "Central"), (yp, "Peripheral")):
        ax.text(-0.2, y + h / 2, lab, ha="right", va="center", fontsize=9.5, fontweight="bold")
    # 패킷 열: (시작 슬롯, 길이, 행, 라벨)
    pk = [
        (0, 1, "C", "DH1"), (1, 1, "P", "DH1"),
        (2, 3, "C", "DH3"), (5, 1, "P", "NULL"),
        (6, 5, "C", "DH5"), (11, 1, "P", "NULL"),
        (12, 1, "C", "POLL"), (13, 1, "P", "NULL"),
    ]
    for st, ln, who, lab in pk:
        y = yc if who == "C" else yp
        col = s.DL if who == "C" else s.UL
        if lab in ("NULL", "POLL"):
            col = s.CTRL
        # 1 슬롯 패킷은 슬롯의 일부만 점유 (BR DH1 ≈ 366 µs / 625 µs)
        w = ln - 0.4 if ln > 1 else 0.6
        box(ax, st + 0.02, y, w, h, col, lab, fs=8)
        ax.text(st + 0.02, y - 0.12, f"f({st})", ha="left", va="top", fontsize=7, color=s.INK2)
    # 다중 슬롯 패킷 동안 건너뛴 홉 표시
    for st, ln in ((2, 3), (6, 5)):
        ax.text(st + ln - 0.2, yc + h + 0.08, f"hops f({st + 1})..f({st + ln - 1}) skipped",
                ha="right", va="bottom", fontsize=6.8, color=s.MUTED)
    span(ax, 0, 1, 0.45, "625 µs")
    span(ax, 0, 2, 0.05, "1250 µs = 1 TX/RX pair (1600 hops/s)")
    ax.text(7, -0.55, "Central transmits in even slots, Peripheral replies in odd slots. A 3- or 5-slot packet keeps "
            "one frequency; the next packet uses the hop for its current slot.", ha="center", fontsize=8.3,
            color=s.INK2)
    ax.set_xlim(-1.8, n + 0.2)
    ax.set_ylim(-0.8, 3.2)
    s.save(fig, "classic_slots")


def classic_packet():
    fig, ax = plt.subplots(figsize=(13, 3.6))
    s.bare(ax)
    h = 0.6
    # BR: Access Code 72 | Header 54 | Payload 0-2745
    y1, y2 = 1.9, 0.6
    ax.text(-0.3, y1 + h / 2, "BR (GFSK)", ha="right", va="center", fontsize=9.5, fontweight="bold")
    ax.text(-0.3, y2 + h / 2, "EDR (2/3 Mbps)", ha="right", va="center", fontsize=9.5, fontweight="bold")
    box(ax, 0, y1, 2.4, h, s.SYNC, "Access Code\n72 b", fs=8)
    box(ax, 2.4, y1, 2.0, h, s.CTRL, "Header\n54 b (FEC 1/3)", fs=7.5)
    box(ax, 4.4, y1, 6.6, h, s.DL, "Payload  0-2745 b  (payload header + data + CRC)", fs=8)
    # EDR
    box(ax, 0, y2, 2.4, h, s.SYNC, "Access Code\n72 b", fs=8)
    box(ax, 2.4, y2, 2.0, h, s.CTRL, "Header\n54 b", fs=8)
    box(ax, 4.4, y2, 0.5, h, s.SPECIAL, "G", fs=8)
    box(ax, 4.9, y2, 0.7, h, s.SYNC, "Sync", fs=7.5)
    box(ax, 5.6, y2, 4.8, h, s.DL, "EDR Payload (pi/4-DQPSK or 8DPSK)", fs=8)
    box(ax, 10.4, y2, 0.6, h, s.SPECIAL, "Trl", fs=7.5)
    ax.annotate("", xy=(4.4, y2 - 0.15), xytext=(0, y2 - 0.15), arrowprops=dict(arrowstyle="<->", color=s.INK2, lw=0.9))
    ax.text(2.2, y2 - 0.22, "GFSK 1 Mbps", ha="center", va="top", fontsize=7.5, color=s.INK2)
    ax.annotate("", xy=(11.0, y2 - 0.15), xytext=(4.9, y2 - 0.15), arrowprops=dict(arrowstyle="<->", color=s.INK2, lw=0.9))
    ax.text(7.95, y2 - 0.22, "DPSK 1 Msym/s (2 or 3 bit/sym)", ha="center", va="top", fontsize=7.5, color=s.INK2)
    # 헤더 세부
    xs = 11.6
    ax.text(xs, y1 + h + 0.05, "Header (18 b before FEC)", fontsize=8.5, fontweight="bold", color=s.INK)
    fields = [("LT_ADDR", 3), ("TYPE", 4), ("FLOW", 1), ("ARQN", 1), ("SEQN", 1), ("HEC", 8)]
    x = xs
    for name, b in fields:
        w = 0.12 * b + 0.55
        box(ax, x, y1, w, h, s.CTRL if name != "HEC" else s.MUTED, f"{name}\n{b}", fs=6.5)
        x += w
    ax.text(xs, y2 + 0.3, "Access Code = preamble 4 + sync word 64 + trailer 4\n"
            "sync word from LAP (CAC: Central, DAC: device, IAC: inquiry)", fontsize=7.6, color=s.INK2, va="center")
    ax.set_xlim(-2.6, 18.6)
    ax.set_ylim(-0.3, 2.9)
    s.save(fig, "classic_packet")


if __name__ == "__main__":
    s.setup()
    classic_slots()
    classic_packet()
