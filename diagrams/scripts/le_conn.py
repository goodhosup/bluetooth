"""LE 연결·등시성 그림 (시간 축은 개략, 축척 아님)

1. le_conn_window : CONNECT_IND → transmitWindowDelay → WinOffset → 전송 창 → 첫 앵커 포인트
2. le_conn_event  : 연결 이벤트 안 패킷 교환 (T_IFS 150 µs, MD 비트, 이벤트 종료), 다음 앵커
3. le_iso_cis     : CIS 이벤트와 서브이벤트 (NSE = 3, BN = 2 예, ISO_Interval, Sub_Interval)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import style as s


def box(ax, x, y, w, h, fc, label="", fs=8, ec="#ffffff", lw=1.2, tc=None, hatch=None):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, hatch=hatch))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=tc or s.text_on(fc))


def span(ax, x0, x1, y, text, color=None, fs=7.5, above=False):
    color = color or s.INK2
    ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="<->", color=color, lw=0.9))
    if above:
        ax.text((x0 + x1) / 2, y + 0.08, text, ha="center", va="bottom", fontsize=fs, color=color)
    else:
        ax.text((x0 + x1) / 2, y - 0.08, text, ha="center", va="top", fontsize=fs, color=color)


def lanes(ax, rows, x0, x1, h):
    for y, lab in rows:
        ax.text(x0 - 1, y + h / 2, lab, ha="right", va="center", fontsize=9.5, fontweight="bold")
        ax.plot([x0, x1], [y, y], color=s.GRID, lw=0.8, zorder=0)


def anchor(ax, x, y0, y1, label):
    ax.plot([x, x], [y0, y1], color=s.RS, lw=1.1, ls="--")
    ax.text(x, y1 + 0.05, label, ha="center", va="bottom", fontsize=7.5, color=s.RS)


def le_conn_window():
    fig, ax = plt.subplots(figsize=(13, 4.2))
    s.bare(ax)
    h = 0.5
    ya, yb = 1.9, 0.8  # Central(initiator), Peripheral(advertiser)
    lanes(ax, ((ya, "Central"), (yb, "Peripheral")), 0, 112, h)
    # 광고 + CONNECT_IND
    box(ax, 2, yb, 8, h, s.CTRL, "ADV_IND", fs=7.5)
    box(ax, 12, ya, 11, h, s.CTRL, "CONNECT_IND", fs=7.5)
    span(ax, 10, 12, yb - 0.12, "T_IFS")
    # transmitWindowDelay, WinOffset
    box(ax, 23, ya + 0.62, 8, 0.28, s.SPECIAL, "1.25 ms", fs=7)
    box(ax, 31, ya + 0.62, 24, 0.28, s.EMPTY, "WinOffset x 1.25 ms", fs=7, ec=s.GRID, tc=s.INK2)
    # transmit window
    box(ax, 55, ya + 0.62, 26, 0.28, s.SYNC, "transmit window (WinSize x 1.25 ms)", fs=7)
    ax.add_patch(Rectangle((55, yb - 0.05), 26, h + 0.1, facecolor="none", edgecolor=s.SYNC, lw=1.2, ls="--"))
    ax.text(68, yb - 0.25, "Peripheral listens for whole window", ha="center", va="top", fontsize=7.5, color=s.INK2)
    # 첫 패킷 (앵커)
    box(ax, 63, ya, 6, h, s.DL, "C->P", fs=7.5)
    box(ax, 70, yb, 6, h, s.UL, "P->C", fs=7.5)
    anchor(ax, 63, yb - 0.1, ya + 1.0, "first anchor point")
    # 다음 앵커 = connInterval 뒤
    box(ax, 103, ya, 6, h, s.DL, "C->P", fs=7.5)
    anchor(ax, 103, yb - 0.1, ya + 1.0, "anchor +1")
    span(ax, 63, 103, 0.15, "connInterval", above=False)
    ax.text(56, -0.65, "transmitWindowDelay: 1.25 ms (CONNECT_IND) · 2.5 ms (AUX_CONNECT_REQ, 1M/2M) · 3.75 ms (AUX_CONNECT_REQ, Coded)"
            "   (not to scale)", ha="center", fontsize=8.2, color=s.INK2)
    ax.set_xlim(-12, 114)
    ax.set_ylim(-0.95, 3.2)
    s.save(fig, "le_conn_window")


def le_conn_event():
    fig, ax = plt.subplots(figsize=(13, 4.0))
    s.bare(ax)
    h = 0.5
    ya, yb = 1.8, 0.8
    lanes(ax, ((ya, "Central"), (yb, "Peripheral")), 0, 116, h)
    x = 4
    pkts = [("C->P MD=1", "D", 11), ("P->C MD=1", "U", 11), ("C->P MD=1", "D", 11), ("P->C MD=0", "U", 11),
            ("C->P MD=0", "D", 11), ("P->C empty", "U", 11)]
    starts = []
    for i, (lab, d, w) in enumerate(pkts):
        y = ya if d == "D" else yb
        c = s.DL if d == "D" else s.UL
        if "empty" in lab:
            box(ax, x, y, w, h, s.EMPTY, lab, fs=7, ec=s.GRID, tc=s.INK2)
        else:
            box(ax, x, y, w, h, c, lab, fs=6.8)
        starts.append(x)
        if i < len(pkts) - 1:
            x2 = x + w
            x = x2 + 2
    end = x + 5
    ax.text(starts[1] + 10, yb - 0.3, "T_IFS = 150 us between packets", ha="center", va="top", fontsize=7.5, color=s.INK2)
    ax.text(end + 2, ya + 0.65, "both MD=0 -> event closes", ha="left", va="bottom", fontsize=7.5, color=s.INK2)
    # sleep
    box(ax, end + 2, 0.15, 16, 0.32, s.EMPTY, "radio idle / sleep", fs=7.5, ec=s.GRID, tc=s.INK2)
    anchor(ax, 4, yb - 0.1, ya + 0.95, "anchor point (n)")
    nxt = 104
    box(ax, nxt, ya, 9, h, s.DL, "C->P", fs=7.5)
    anchor(ax, nxt, yb - 0.1, ya + 0.95, "anchor point (n+1)")
    # 윈도 확장
    ax.add_patch(Rectangle((nxt - 4, yb - 0.04), 8, h + 0.08, facecolor="none", edgecolor=s.SPECIAL, lw=1.4, ls="--"))
    ax.text(nxt + 1, yb - 0.25, "rx window\n+/- windowWidening", ha="center", va="top", fontsize=7, color=s.INK2)
    span(ax, 4, nxt, ya + 1.35, "connInterval (7.5 ms - 4 s, 1.25 ms steps)", above=True)
    ax.set_xlim(-12, 118)
    ax.set_ylim(-0.6, 3.6)
    s.save(fig, "le_conn_event")


def le_iso_cis():
    fig, ax = plt.subplots(figsize=(13, 4.4))
    s.bare(ax)
    h = 0.5
    ya, yb = 1.9, 0.9
    lanes(ax, ((ya, "Central"), (yb, "Peripheral")), 0, 118, h)
    sub_int = 17
    labels = [("C->P PDU0", "P->C PDU0"), ("C->P PDU1", "P->C PDU1"), ("spare/retx", "spare/retx")]
    for k in range(3):
        x = 4 + k * sub_int
        c1 = s.DL if k < 2 else s.ALT
        c2 = s.UL if k < 2 else s.ALT
        box(ax, x, ya, 7.6, h, c1, labels[k][0], fs=6.3)
        box(ax, x + 8.2, yb, 7.6, h, c2, labels[k][1], fs=6.3)
        ax.text(x + 7.9, ya + 1.2, f"subevent {k + 1}", ha="center", va="bottom", fontsize=7.5, color=s.INK2)
    span(ax, 4, 4 + sub_int, ya + 0.75, "Sub_Interval", above=True, fs=7)
    # CIS event end
    ax.add_patch(Rectangle((2.5, yb - 0.25), 3 * sub_int, 2.0, facecolor="none", edgecolor=s.CTRL, lw=1.0, ls=":"))
    ax.text(2.5 + 3 * sub_int / 2, yb - 0.32, "CIS event (NSE = 3, BN = 2: 2 new PDUs + 1 spare subevent)",
            ha="center", va="top", fontsize=7.5, color=s.CTRL)
    anchor(ax, 4, yb - 0.6, ya + 1.45, "CIS anchor point")
    nxt = 100
    box(ax, nxt, ya, 7.6, h, s.DL, "C->P PDU2", fs=6.3)
    anchor(ax, nxt, yb - 0.6, ya + 1.45, "next CIS anchor")
    span(ax, 4, nxt, 0.05, "ISO_Interval (5 ms - 4 s, 1.25 ms steps)")
    ax.text(77, 1.35, "radio free for\nother links", ha="center", va="center", fontsize=8, color=s.MUTED)
    ax.set_xlim(-12, 120)
    ax.set_ylim(-0.55, 3.75)
    s.save(fig, "le_iso_cis")


if __name__ == "__main__":
    s.setup()
    le_conn_window()
    le_conn_event()
    le_iso_cis()
