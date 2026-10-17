"""구현과 실무 그림

1. practice_hci_packets  : H4(UART) HCI 패킷 5종의 헤더 배치 (Command/ACL/SCO/Event/ISO)
2. practice_adv_current  : 레거시 광고 이벤트 1회의 전류 파형 (예시 가정값, 칩마다 다름)
   - 깨어남 0.5 ms @ 2 mA, 채널당 램프 0.18 ms @ 3 mA + TX 376 us @ 5.3 mA + RX 144 us @ 5 mA,
     후처리 0.5 ms @ 2 mA, 수면 1.5 uA  ->  Q = 1.0 + 3 x 3.25 + 1.0 = 11.76 uC
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import style as s


def box(ax, x, y, w, h, fc, label="", fs=8, ec="#ffffff", lw=1.2, tc=None):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=tc or s.text_on(fc))


def hci_packets():
    s.setup()
    fig, ax = plt.subplots(figsize=(10, 4.6))
    s.bare(ax)
    rows = [
        ("Command", "0x01", [("Opcode\nOCF 10b | OGF 6b", 2, s.CTRL), ("Param\nLen 1B", 1, s.SPECIAL), ("Parameters (0-255 B)", 4, s.DL)]),
        ("ACL data", "0x02", [("Handle 12b\nPB 2b | BC 2b", 2, s.CTRL), ("Data Len\n2B", 1.4, s.SPECIAL), ("L2CAP data", 3.6, s.DL)]),
        ("SCO data", "0x03", [("Handle 12b\nflags 4b", 2, s.CTRL), ("Len\n1B", 1, s.SPECIAL), ("Voice data", 4, s.DL)]),
        ("Event", "0x04", [("Event\nCode 1B", 1, s.UL), ("Param\nLen 1B", 1, s.SPECIAL), ("Parameters (0-255 B)", 5, s.UL)]),
        ("ISO data", "0x05", [("Handle 12b\nPB 2b | TS 1b", 2, s.CTRL), ("Load Len\n14b", 1.4, s.SPECIAL), ("(Timestamp, SN) + SDU", 3.6, s.DL)]),
    ]
    h = 0.62
    for i, (name, ind, fields) in enumerate(rows):
        y = (len(rows) - 1 - i) * 0.9
        ax.text(-0.15, y + h / 2, name, ha="right", va="center", fontsize=9.5, color=s.INK)
        box(ax, 0, y, 1, h, s.SYNC, ind, fs=8.5)
        x = 1
        for lab, w, c in fields:
            box(ax, x, y, w, h, c, lab, fs=7.5)
            x += w
    ax.text(0.5, 4 * 0.9 + 0.85, "H4 indicator", ha="center", fontsize=8, color=s.INK2)
    ax.text(4.5, 4 * 0.9 + 0.85, "HCI packet (same format over USB/SDIO, without indicator)", ha="center", fontsize=8, color=s.INK2)
    ax.text(4.0, -0.35, "Host -> Controller: Command, ACL, SCO, ISO    Controller -> Host: Event, ACL, SCO, ISO",
            ha="center", fontsize=8, color=s.MUTED)
    ax.set_xlim(-1.6, 8.2)
    ax.set_ylim(-0.6, 4.9)
    s.save(fig, "practice_hci_packets")


def adv_current():
    s.setup()
    fig, ax = plt.subplots(figsize=(10, 3.8))
    # (start ms, duration ms, current mA, label, color)
    segs = [(0.0, 0.5, 2.0, "wake\nHFXO", s.SPECIAL)]
    t = 0.5
    for ch in (37, 38, 39):
        segs.append((t, 0.18, 3.0, "", s.MUTED))           # ramp-up
        segs.append((t + 0.18, 0.376, 5.3, f"TX\nch{ch}", s.UL))  # ADV_IND 376 us
        segs.append((t + 0.556, 0.144, 5.0, "RX", s.DL))   # listen for SCAN_REQ / CONNECT_IND
        t += 0.7
    segs.append((t, 0.5, 2.0, "CPU\npost", s.CTRL))
    t += 0.5
    for x, w, i, lab, c in segs:
        ax.add_patch(Rectangle((x, 0), w, i, facecolor=c, edgecolor="#ffffff", linewidth=0.8))
        if lab:
            ax.text(x + w / 2, i + 0.15, lab, ha="center", va="bottom", fontsize=7.5, color=s.INK)
    ax.plot([-0.4, 0], [0.02, 0.02], color=s.INK2, lw=2)
    ax.plot([t, t + 0.6], [0.02, 0.02], color=s.INK2, lw=2)
    ax.text(t + 0.3, 0.35, "sleep\n~1.5 uA", ha="center", fontsize=7.5, color=s.INK2)
    ax.annotate("", xy=(t, -0.55), xytext=(0, -0.55), arrowprops=dict(arrowstyle="<->", color=s.INK2, lw=0.9))
    ax.text(t / 2, -0.75, f"active ~{t:.1f} ms  ->  Q = 11.8 uC per event (example values)", ha="center", va="top",
            fontsize=8, color=s.INK2)
    ax.set_xlim(-0.5, t + 0.8)
    ax.set_ylim(-1.3, 7.0)
    ax.set_yticks(range(0, 8))
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("current (mA)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=s.GRID, lw=0.6)
    s.save(fig, "practice_adv_current")


if __name__ == "__main__":
    hci_packets()
    adv_current()
