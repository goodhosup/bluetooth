"""LE 컨트롤러 그림 (물리계층·광고)

1. le_channel_map   : 40개 LE 채널과 Wi-Fi 1/6/11 (광고 채널 37/38/39 위치)
2. le_packet_format : 1M / 2M / Coded 패킷 필드 배치 비교
3. le_adv_event     : 레거시 광고 이벤트 (37→38→39, advInterval + advDelay)
4. le_ext_adv       : 확장 광고 (주 채널 ADV_EXT_IND → AuxPtr → 보조 채널 AUX_ADV_IND → AUX_CHAIN_IND)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import style as s

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from bt_numbers import le_freq  # noqa: E402


def box(ax, x, y, w, h, fc, label="", fs=8, ec="#ffffff", lw=1.2, tc=None, hatch=None, rot=0):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, hatch=hatch))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=tc or s.text_on(fc),
                rotation=rot)


def span(ax, x0, x1, y, text, color=None, fs=7.5):
    color = color or s.INK2
    ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="<->", color=color, lw=0.9))
    ax.text((x0 + x1) / 2, y - 0.08, text, ha="center", va="top", fontsize=fs, color=color)


def le_channel_map():
    fig, ax = plt.subplots(figsize=(13.5, 4.2))
    s.bare(ax)
    # Wi-Fi 1/6/11 (20 MHz occupied, centre 2412/2437/2462)
    for ch, fc in ((1, 2412), (6, 2437), (11, 2462)):
        ax.add_patch(Rectangle((fc - 10, 0), 20, 1.55, facecolor=s.UL, alpha=0.16, edgecolor=s.UL, lw=1.0))
        ax.text(fc, 1.65, f"Wi-Fi ch {ch} ({fc} MHz)", ha="center", fontsize=8.5, color=s.UL)
    for idx in range(40):
        f = le_freq(idx)
        adv = idx >= 37
        c = s.CTRL if adv else s.DL
        box(ax, f - 0.85, 0.15 if adv else 0.25, 1.7, 1.1 if adv else 0.9, c, "", ec=s.SURFACE, lw=0.6)
        ax.text(f, -0.08, str(idx), ha="center", va="top", fontsize=6.8 if not adv else 8,
                color=s.CTRL if adv else s.INK2, fontweight="bold" if adv else "normal")
    for f in (2402, 2426, 2480):
        ax.text(f, -0.48, f"{f}", ha="center", va="top", fontsize=7.5, color=s.CTRL)
    ax.text(2399, -0.08, "index", ha="right", va="top", fontsize=7.5, color=s.INK2)
    ax.text(2399, -0.48, "MHz", ha="right", va="top", fontsize=7.5, color=s.CTRL)
    box(ax, 2402, 2.2, 3, 0.3, s.CTRL)
    ax.text(2406, 2.35, "advertising (primary) channels 37 / 38 / 39", va="center", fontsize=8.5)
    box(ax, 2445, 2.2, 3, 0.3, s.DL)
    ax.text(2449, 2.35, "data / secondary channels 0-36", va="center", fontsize=8.5)
    ax.text(2441, -1.0, "40 channels x 2 MHz spacing, 2402-2480 MHz (RF channel k: f = 2402 + 2k MHz); "
            "advertising channels sit outside / between the three common Wi-Fi channels",
            ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(2392, 2484)
    ax.set_ylim(-1.3, 2.7)
    s.save(fig, "le_channel_map")


def le_packet_format():
    fig, ax = plt.subplots(figsize=(13.5, 4.8))
    s.bare(ax)
    h = 0.6
    rows = [
        ("LE 1M\n(1 Msym/s)", 3.4, [("Pre-\namble 1 B", 10, s.SYNC), ("Access Address\n4 B", 32, s.CTRL),
                                    ("PDU\n2-257 B (header + payload + MIC)", 60, s.DL), ("CRC\n3 B", 24, s.ALT),
                                    ("CTE\n(opt.)", 12, s.SPECIAL)]),
        ("LE 2M\n(2 Msym/s)", 2.2, [("Pre-\namble 2 B", 10, s.SYNC), ("Access Address\n4 B", 16, s.CTRL),
                                    ("PDU\n2-257 B", 30, s.DL), ("CRC\n3 B", 12, s.ALT),
                                    ("CTE\n(opt.)", 12, s.SPECIAL)]),
    ]
    for name, y, fields in rows:
        ax.text(-1.5, y + h / 2, name, ha="right", va="center", fontsize=9, fontweight="bold")
        x = 0
        for lab, w, c in fields:
            box(ax, x, y, w, h, c, lab, fs=7.5, hatch="//" if "CTE" in lab else None)
            x += w
    # Coded
    y = 0.8
    ax.text(-1.5, y + h / 2, "LE Coded\n(S=2 / S=8)", ha="right", va="center", fontsize=9, fontweight="bold")
    coded = [("Preamble\n80 µs", 20, s.SYNC), ("Access Address\n256 µs", 36, s.CTRL), ("CI\n16 µs", 8, s.MUTED),
             ("TERM1\n24 µs", 10, s.SPECIAL), ("PDU (S=2 or S=8)", 40, s.DL), ("CRC", 14, s.ALT),
             ("TERM2", 8, s.SPECIAL)]
    x = 0
    for lab, w, c in coded:
        box(ax, x, y, w, h, c, lab, fs=7.5)
        x += w
    ax.annotate("", xy=(0, y - 0.15), xytext=(74, y - 0.15), arrowprops=dict(arrowstyle="-", color=s.INK2))
    ax.text(37, y - 0.22, "not coded (preamble) + FEC block 1: always S=8", ha="center", va="top", fontsize=8,
            color=s.INK2)
    ax.annotate("", xy=(74, y - 0.15), xytext=(136, y - 0.15), arrowprops=dict(arrowstyle="-", color=s.DL))
    ax.text(105, y - 0.22, "FEC block 2: S=2 or S=8 (CI tells which)", ha="center", va="top", fontsize=8,
            color=s.DL)
    ax.text(68, -0.25, "widths are schematic, not to scale  |  CTE = Constant Tone Extension (direction finding, "
            "not on Coded PHY)  |  CI = Coding Indicator", ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-16, 140)
    ax.set_ylim(-0.5, 4.2)
    s.save(fig, "le_packet_format")


def le_adv_event():
    fig, ax = plt.subplots(figsize=(13.5, 4.0))
    s.bare(ax)
    h = 0.55
    rows = {"ch 37": 2.4, "ch 38": 1.6, "ch 39": 0.8}
    for lab, y in rows.items():
        ax.text(-1.5, y + h / 2, lab, ha="right", va="center", fontsize=9, fontweight="bold")
        ax.plot([-1, 121], [y, y], color=s.GRID, lw=0.8, zorder=0)

    def event(x0, tag):
        box(ax, x0, rows["ch 37"], 4, h, s.CTRL, "ADV", fs=7.5)
        box(ax, x0 + 6, rows["ch 38"], 4, h, s.CTRL, "ADV", fs=7.5)
        box(ax, x0 + 12, rows["ch 39"], 4, h, s.CTRL, "ADV", fs=7.5)
        ax.add_patch(Rectangle((x0 - 0.3, 0.6), 16.6, 2.55, facecolor="none", edgecolor=s.MUTED, lw=0.8,
                               linestyle="--"))
        ax.text(x0 + 8, 3.25, tag, ha="center", fontsize=8, color=s.INK2)

    event(0, "advertising event n")
    event(48, "advertising event n+1")
    event(103, "event n+2")
    span(ax, 0, 40, 0.45, "advInterval (20 ms - 10.24 s)")
    span(ax, 40, 48, 0.45, "advDelay\n(0-10 ms random)")
    span(ax, 48, 95, 0.45, "advInterval")
    span(ax, 95, 103, 0.45, "advDelay")
    ax.text(60, -0.45, "within one event the same PDU is sent on 37, 38, 39 (order may be randomized since 5.1); "
            "PDUs within an event are <= 10 ms apart; time axis not to scale", ha="center", fontsize=8.5,
            color=s.INK2)
    ax.set_xlim(-8, 122)
    ax.set_ylim(-0.7, 3.5)
    s.save(fig, "le_adv_event")


def le_ext_adv():
    fig, ax = plt.subplots(figsize=(13.5, 4.4))
    s.bare(ax)
    h = 0.55
    rows = {"primary 37": 3.0, "primary 38": 2.3, "primary 39": 1.6, "secondary k": 0.6, "secondary m": -0.3}
    for lab, y in rows.items():
        ax.text(-1.5, y + h / 2, lab, ha="right", va="center", fontsize=9, fontweight="bold")
        ax.plot([-1, 112], [y, y], color=s.GRID, lw=0.8, zorder=0)
    for i, ch in enumerate(("primary 37", "primary 38", "primary 39")):
        x = i * 11
        box(ax, x, rows[ch], 10, h, s.CTRL, "ADV_EXT_IND", fs=7)
        ax.annotate("", xy=(36, rows["secondary k"] + h), xytext=(x + 10, rows[ch] + h / 2), zorder=0,
                    arrowprops=dict(arrowstyle="->", color=s.MUTED, lw=0.8, linestyle="--",
                                    connectionstyle="arc3,rad=-0.15"))
    ax.text(16, 3.75, "header only: ADI + AuxPtr (channel, offset, PHY)", ha="center", fontsize=8, color=s.INK2)
    box(ax, 36, rows["secondary k"], 36, h, s.DL, "AUX_ADV_IND  (ADI, AuxPtr, AdvData up to 254 B)", fs=7.5)
    ax.annotate("", xy=(78, rows["secondary m"] + h), xytext=(71, rows["secondary k"]),
                arrowprops=dict(arrowstyle="->", color=s.INK2, lw=0.9))
    box(ax, 78, rows["secondary m"], 32, h, s.DL, "AUX_CHAIN_IND  (more AdvData)", fs=7.5)
    ax.text(76, 0.45, "AuxPtr", fontsize=7.5, color=s.INK2)
    ax.text(55, -0.95, "primary channels (1M or Coded) carry only a short pointer; the payload goes on a data channel "
            "0-36 (1M, 2M or Coded) - host data up to 1650 B in total", ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-12, 113)
    ax.set_ylim(-1.2, 4.0)
    s.save(fig, "le_ext_adv")


if __name__ == "__main__":
    s.setup()
    le_channel_map()
    le_packet_format()
    le_adv_event()
    le_ext_adv()
