"""LE 호스트 그림

1. host_gatt_hierarchy : GATT 서버의 속성 테이블 (서비스 선언 → 특성 선언 → 값 → CCCD)
2. host_l2cap_sdu      : LE CoC에서 SDU → K-frame → LL 데이터 PDU 분할
3. host_adv_budget     : 레거시 광고 31바이트 예산 예 (Flags + UUID 목록 + 이름)
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


def gatt_hierarchy():
    rows = [
        # handle, type, value, perm, color, indent
        ("0x0010", "0x2800 Primary Service", "0x180D (Heart Rate)", "read", s.CTRL, 0),
        ("0x0011", "0x2803 Characteristic", "props=Notify | handle 0x0012 | 0x2A37", "read", s.SYNC, 1),
        ("0x0012", "0x2A37 HR Measurement", "flags, bpm ... (value)", "none (notify only)", s.DL, 2),
        ("0x0013", "0x2902 CCCD", "0x0001 = notifications on", "read / write", s.SPECIAL, 2),
        ("0x0014", "0x2803 Characteristic", "props=Read | handle 0x0015 | 0x2A38", "read", s.SYNC, 1),
        ("0x0015", "0x2A38 Body Sensor Loc.", "0x01 (chest)", "read", s.DL, 2),
        ("0x0016", "0x2800 Primary Service", "0x180F (Battery)", "read", s.CTRL, 0),
        ("0x0017", "0x2803 Characteristic", "props=Read|Notify | handle 0x0018 | 0x2A19", "read", s.SYNC, 1),
        ("0x0018", "0x2A19 Battery Level", "0x5A (90 %)", "read", s.DL, 2),
        ("0x0019", "0x2902 CCCD", "0x0000", "read / write", s.SPECIAL, 2),
    ]
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    s.bare(ax)
    h = 0.42
    cols = [(0, 8, "Handle"), (8, 30, "Type (UUID)"), (38, 42, "Value"), (80, 18, "Permissions")]
    ytop = len(rows) * 0.5
    for x, w, t in cols:
        ax.text(x + 1.2 if x else x + 0.8, ytop + 0.25, t, ha="left", va="center", fontsize=9.5, fontweight="bold")
    for i, (hd, ty, val, perm, c, ind) in enumerate(rows):
        y = ytop - (i + 1) * 0.5
        box(ax, 0, y, 8, h, s.EMPTY, hd, fs=8.5, ec=s.GRID, tc=s.INK)
        box(ax, 8 + ind * 2, y, 30 - ind * 2, h, c, ty, fs=8.5)
        box(ax, 38, y, 42, h, s.EMPTY, val, fs=8.5, ec=s.GRID, tc=s.INK2)
        box(ax, 80, y, 18, h, s.EMPTY, perm, fs=8, ec=s.GRID, tc=s.INK2)
    # 서비스 그룹 괄호
    for (i0, i1, lab) in ((0, 5, "Heart Rate service\n(group 0x0010-0x0015)"), (6, 9, "Battery service\n(group 0x0016-0x0019)")):
        y0 = ytop - (i1 + 1) * 0.5
        y1 = ytop - i0 * 0.5 - 0.08
        ax.plot([99.5, 100.5, 100.5, 99.5], [y1, y1, y0, y0], color=s.INK2, lw=1)
        ax.text(101.3, (y0 + y1) / 2, lab, ha="left", va="center", fontsize=8.5, color=s.INK2)
    ax.text(49, -0.35, "purple = service declaration · green = characteristic declaration · blue = characteristic value "
            "· yellow = descriptor (CCCD)", ha="center", va="top", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-1, 116)
    ax.set_ylim(-0.8, ytop + 0.6)
    s.save(fig, "host_gatt_hierarchy")


def l2cap_sdu():
    fig, ax = plt.subplots(figsize=(13, 4.6))
    s.bare(ax)
    h = 0.55
    # SDU
    ax.text(-1, 3.4 + h / 2, "SDU\n(<= MTU)", ha="right", va="center", fontsize=9.5, fontweight="bold")
    box(ax, 10, 3.4, 80, h, s.ALT, "upper-layer SDU (e.g. 600 B, MTU = 1000)", fs=9)
    # K-frames
    ax.text(-1, 2.1 + h / 2, "K-frames\n(payload <= MPS)", ha="right", va="center", fontsize=9.5, fontweight="bold")
    x = 0
    parts = [("#1", True, 28), ("#2", False, 28), ("#3", False, 16)]
    xs = []
    for name, first, w in parts:
        box(ax, x, 2.1, 4, h, s.CTRL, "Len", fs=7)
        box(ax, x + 4, 2.1, 4, h, s.CTRL, "CID", fs=7)
        off = 8
        if first:
            box(ax, x + 8, 2.1, 4, h, s.SPECIAL, "SDU\nlen", fs=6.5)
            off = 12
        box(ax, x + off, 2.1, w - off + 8, h, s.ALT, f"SDU part {name}", fs=8)
        xs.append((x, x + w + 8))
        x += w + 10
    ax.text(48, 1.95, "each K-frame consumes 1 credit · first K-frame carries 2-octet SDU length",
            ha="center", va="top", fontsize=8, color=s.INK2)
    # LL PDUs (for K-frame #1)
    ax.text(-1, 0.5 + h / 2, "LL data PDUs\n(<= 251 B)", ha="right", va="center", fontsize=9.5, fontweight="bold")
    box(ax, 0, 0.5, 5, h, s.SYNC, "LLID\n=10", fs=6.5)
    box(ax, 5, 0.5, 14, h, s.DL, "start", fs=8)
    box(ax, 20, 0.5, 5, h, s.SYNC, "LLID\n=01", fs=6.5)
    box(ax, 25, 0.5, 13, h, s.DL, "continuation", fs=8)
    ax.plot([xs[0][0], 0], [2.1, 1.05], color=s.GRID, lw=1)
    ax.plot([xs[0][1], 38], [2.1, 1.05], color=s.GRID, lw=1)
    ax.text(42, 0.5 + h / 2, "if a K-frame (4 B header + payload) is larger than the LL payload,\n"
            "the host/HCI splits it: LLID 10 = start, LLID 01 = continuation",
            ha="left", va="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-16, 102)
    ax.set_ylim(0.2, 4.2)
    s.save(fig, "host_l2cap_sdu")


def adv_budget():
    # (label, bytes, color)
    items = [("Flags\n02 01 06", 3, s.CTRL), ("Complete 16-bit UUIDs\n05 03 0D 18 0F 18", 6, s.SYNC),
             ("Tx Power\n02 0A 00", 3, s.SPECIAL), ("Complete Local Name 'HR-Strap-01'\n0C 09 + 11 B", 13, s.DL)]
    fig, ax = plt.subplots(figsize=(13, 2.9))
    s.bare(ax)
    h = 0.8
    x = 0
    for lab, n, c in items:
        box(ax, x, 1.0, n, h, c, lab, fs=7.5)
        ax.text(x + n / 2, 0.88, f"{n} B", ha="center", va="top", fontsize=8, color=s.INK2)
        x += n
    box(ax, x, 1.0, 31 - x, h, s.EMPTY, "free", fs=8, ec=s.GRID, tc=s.INK2)
    ax.text(x + (31 - x) / 2, 0.88, f"{31 - x} B", ha="center", va="top", fontsize=8, color=s.INK2)
    span(ax, 0, 31, 2.15, "")
    ax.text(15.5, 2.25, "AdvData of ADV_IND: 31 bytes (each AD structure = Length + Type + Data)",
            ha="center", va="bottom", fontsize=9, color=s.INK)
    ax.set_xlim(-0.5, 31.5)
    ax.set_ylim(0.4, 2.7)
    s.save(fig, "host_adv_budget")


if __name__ == "__main__":
    s.setup()
    gatt_hierarchy()
    l2cap_sdu()
    adv_budget()
