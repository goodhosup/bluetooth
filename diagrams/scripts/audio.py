"""LE Audio 그림

1. audio_cig_timing : 하나의 CIG 안에 좌/우 이어버드용 CIS 두 개 (Sequential 배치, ISO interval 10 ms)
2. audio_base_levels: BASE 3단계 구조 (Level 1 그룹 → Level 2 서브그룹 → Level 3 BIS)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

import style as s


def box(ax, x, y, w, h, fc, label="", fs=8, ec="#ffffff", lw=1.2, tc=None):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=tc or s.text_on(fc))


def span(ax, x0, x1, y, text, color=None, fs=7.5):
    color = color or s.INK2
    ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="<->", color=color, lw=0.9))
    ax.text((x0 + x1) / 2, y - 0.08, text, ha="center", va="top", fontsize=fs, color=color)


def cig_timing():
    fig, ax = plt.subplots(figsize=(13, 4.4))
    s.bare(ax)
    h = 0.5
    rows = {"Phone (Central)": 2.4, "Left earbud": 1.4, "Right earbud": 0.4}
    for lab, y in rows.items():
        ax.text(-2, y + h / 2, lab, ha="right", va="center", fontsize=9.5, fontweight="bold")
        ax.plot([-1, 104], [y, y], color=s.GRID, lw=0.8, zorder=0)
    yP, yL, yR = rows["Phone (Central)"], rows["Left earbud"], rows["Right earbud"]
    for ev in range(2):
        x0 = ev * 50
        ax.plot([x0, x0], [0.1, 3.55], color=s.MUTED, lw=0.8, ls="--")
        ax.text(x0, 3.6, "CIG anchor", ha="center", fontsize=7.5, color=s.INK2)
        # CIS 1 (left): 2 subevents, CIS 2 (right): 2 subevents
        x = x0 + 1
        for cis, y_dev, col in ((1, yL, s.DL), (2, yR, s.ALT)):
            for se in range(2):
                box(ax, x, yP, 4.2, h, col, f"C>P {'L' if cis == 1 else 'R'}", fs=7)
                box(ax, x + 4.8, y_dev, 3.0, h, s.UL, "P>C", fs=7)
                x += 9.2
        box(ax, x + 1, yP, 49 - (x - x0) - 2, h, s.EMPTY, "idle: ACL,\nWi-Fi, sleep", fs=6.5, ec=s.GRID, tc=s.INK2)
    span(ax, 0, 50, -0.15, "ISO_Interval = 10 ms (= SDU interval for a 10 ms LC3 frame)")
    span(ax, 1, 19.4, 3.35, "CIS 1 (Left): NSE = 2", fs=7)
    span(ax, 19.4, 37.8, 3.35, "CIS 2 (Right): NSE = 2", fs=7)
    ax.text(52, -0.75, "Sequential CIS placement · second subevent = retransmission opportunity · not to scale",
            ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-14, 104)
    ax.set_ylim(-1.0, 3.9)
    s.save(fig, "audio_cig_timing")


def base_levels():
    fig, ax = plt.subplots(figsize=(12, 4.6))
    s.bare(ax)

    def rbox(x, y, w, hh, fc, lines, fs=8):
        ax.add_patch(FancyBboxPatch((x, y), w, hh, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    facecolor=fc, edgecolor="#ffffff", linewidth=1.2))
        ax.text(x + w / 2, y + hh / 2, "\n".join(lines), ha="center", va="center", fontsize=fs,
                color=s.text_on(fc), linespacing=1.4)

    rbox(3.0, 3.2, 6.0, 0.9, s.CTRL, ["Level 1: BIG / group", "Presentation_Delay · Num_Subgroups"], fs=8.5)
    subs = [(0.2, "Subgroup 0 (English)", ["Codec_ID = LC3", "Codec config: 48 kHz, 10 ms", "Metadata: Language = eng"]),
            (6.2, "Subgroup 1 (Korean)", ["Codec_ID = LC3", "Codec config: 48 kHz, 10 ms", "Metadata: Language = kor"])]
    for x, title, lines in subs:
        rbox(x, 1.65, 5.6, 1.15, s.DL, ["Level 2: " + title] + lines, fs=7.5)
        ax.annotate("", xy=(x + 2.8, 2.8), xytext=(6.0, 3.2), arrowprops=dict(arrowstyle="->", color=s.INK2, lw=0.9))
    bis = [(0.2, 1, "Front Left"), (3.0, 2, "Front Right"), (6.2, 3, "Front Left"), (9.0, 4, "Front Right")]
    for x, idx, loc in bis:
        rbox(x, 0.2, 2.6, 0.95, s.SYNC, [f"Level 3: BIS {idx}", f"Allocation = {loc}"], fs=7.5)
        parent = 3.0 if x < 6 else 9.0
        ax.annotate("", xy=(x + 1.3, 1.15), xytext=(parent, 1.65), arrowprops=dict(arrowstyle="->", color=s.INK2, lw=0.9))
    ax.text(6.0, -0.3, "BASE is carried in the periodic advertising (AUX_SYNC_IND) as Service Data, UUID 0x1851",
            ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-0.2, 12.2)
    ax.set_ylim(-0.6, 4.3)
    s.save(fig, "audio_base_levels")


if __name__ == "__main__":
    s.setup()
    cig_timing()
    base_levels()
