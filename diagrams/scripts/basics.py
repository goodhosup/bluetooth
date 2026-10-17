"""공통 기초 그림

1. basics_stack        : Classic(BR/EDR) 스택과 LE 스택, Host/Controller 경계와 HCI
2. basics_ism_channels : 2.4 GHz ISM 대역 위의 Classic 79채널, LE 40채널(광고 37/38/39), Wi-Fi 1/6/11
3. basics_duty_cycle   : 연결 이벤트 기반 저전력 동작의 전류 프로파일 (개념도)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import style as s


def box(ax, x, y, w, h, fc, label="", fs=9, ec="#ffffff", lw=1.2, tc=None, bold=False, alpha=1.0):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, alpha=alpha))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs,
                color=tc or s.text_on(fc), fontweight="bold" if bold else "normal")


# ---------------------------------------------------------------- 1. 스택
def stack():
    fig, ax = plt.subplots(figsize=(12, 6.4))
    s.bare(ax)
    H = 0.62
    # (x0, 폭) 열 정의
    cx, cw = 0.0, 5.0     # Classic
    lx, lw = 6.0, 5.0     # LE

    def col(x0, w, rows):
        for y, parts in rows:
            tot = sum(p[1] for p in parts)
            xx = x0
            for lab, frac, color in parts:
                ww = w * frac / tot
                box(ax, xx, y, ww, H, color, lab, fs=8.5)
                xx += ww

    ctrl, host, app = s.CTRL, s.DL, s.ALT
    classic = [
        (0.0, [("Radio (BR/EDR PHY)  GFSK / pi/4-DQPSK / 8DPSK", 1, ctrl)]),
        (0.7, [("Baseband / Link Controller", 1, ctrl)]),
        (1.4, [("Link Manager (LMP)", 1, ctrl)]),
        (2.9, [("L2CAP", 1, host)]),
        (3.6, [("SDP", 1, host), ("RFCOMM", 1, host), ("AVDTP / AVCTP", 1.3, host)]),
        (4.3, [("GAP", 0.8, host), ("HFP · A2DP · AVRCP · SPP · HID ...", 3, app)]),
    ]
    le = [
        (0.0, [("PHY  LE 1M / 2M / Coded", 1, ctrl)]),
        (0.7, [("Link Layer (+ ISOAL)", 1, ctrl)]),
        (1.4, [("", 1, s.EMPTY)]),
        (2.9, [("L2CAP", 1, host)]),
        (3.6, [("ATT / EATT", 1, host), ("SMP", 0.7, host)]),
        (4.3, [("GAP", 0.8, host), ("GATT", 1, host), ("Profiles / Services", 1.6, app)]),
    ]
    col(cx, cw, classic)
    col(lx, lw, le)
    # LE의 빈 칸 정리
    ax.add_patch(Rectangle((lx, 1.4), lw, H, facecolor=s.EMPTY, edgecolor=s.GRID, lw=1.0))
    ax.text(lx + lw / 2, 1.4 + H / 2, "(no separate LMP: control PDUs live in the Link Layer)",
            ha="center", va="center", fontsize=8, color=s.INK2)
    # HCI 띠
    for x0, w in ((cx, cw), (lx, lw)):
        box(ax, x0, 2.15, w, 0.6, s.SPECIAL, "HCI  (UART H4 / H5, USB, SDIO, or in-chip API)", fs=8.5)
    # 경계선과 라벨
    ax.plot([-1.6, 11.2], [2.08, 2.08], color=s.INK2, lw=0.9, ls="--")
    ax.plot([-1.6, 11.2], [2.82, 2.82], color=s.INK2, lw=0.9, ls="--")
    ax.text(-0.25, 1.05, "Controller", rotation=90, ha="center", va="center", fontsize=10, fontweight="bold", color=s.CTRL)
    ax.text(-0.25, 3.95, "Host", rotation=90, ha="center", va="center", fontsize=10, fontweight="bold", color=s.DL)
    ax.text(cx + cw / 2, 5.2, "Classic (BR/EDR)", ha="center", fontsize=11, fontweight="bold")
    ax.text(lx + lw / 2, 5.2, "Low Energy (LE)", ha="center", fontsize=11, fontweight="bold")
    ax.text(5.5, -0.45, "Dual-mode devices share one Host stack (L2CAP, GAP, security) over one HCI; "
            "the two Controllers share one 2.4 GHz radio.", ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-0.6, 11.2)
    ax.set_ylim(-0.7, 5.5)
    s.save(fig, "basics_stack")


# ---------------------------------------------------------------- 2. ISM 대역 채널
def ism_channels():
    fig, ax = plt.subplots(figsize=(13, 4.4))
    ax.set_yticks([])
    for sp in ("left", "right", "top"):
        ax.spines[sp].set_visible(False)
    # ISM 대역
    ax.add_patch(Rectangle((2400, -0.15), 83.5, 3.55, facecolor=s.EMPTY, edgecolor="none", zorder=0))
    ax.text(2441.75, 3.48, "2.4 GHz ISM band  2400 - 2483.5 MHz", ha="center", fontsize=9, color=s.INK2)
    # Wi-Fi 1/6/11 (20 MHz 근사)
    for ch, fc in ((1, 2412), (6, 2437), (11, 2462)):
        ax.add_patch(Rectangle((fc - 10, 2.3), 20, 0.8, facecolor=s.UL, alpha=0.85, edgecolor="#ffffff"))
        ax.text(fc, 2.7, f"Wi-Fi ch {ch}\n{fc} MHz", ha="center", va="center", fontsize=8, color="#ffffff")
    # LE 40채널
    le = {37: 2402, 38: 2426, 39: 2480}
    for k in range(37):
        f = 2404 + 2 * k if k <= 10 else 2428 + 2 * (k - 11)
        le[k] = f
    for k, f in le.items():
        adv = k >= 37
        ax.add_patch(Rectangle((f - 0.8, 1.15 if not adv else 1.0), 1.6, 0.7 if not adv else 1.0,
                               facecolor=s.RS if adv else s.DL, edgecolor="none"))
    for k in (37, 38, 39):
        ax.text(le[k], 0.78, f"{k}\n{le[k]}", ha="center", va="top", fontsize=7.5, color=s.RS, fontweight="bold")
    ax.text(2399, 1.5, "LE 40 ch\n(2 MHz)", ha="right", va="center", fontsize=8.5, color=s.INK)
    # Classic 79채널
    for k in range(79):
        f = 2402 + k
        ax.plot([f, f], [0.05, 0.35], color=s.CTRL, lw=1.1)
    ax.text(2399, 0.2, "Classic 79 ch\n(1 MHz)", ha="right", va="center", fontsize=8.5, color=s.INK)
    ax.text(2399, 2.7, "Wi-Fi 1/6/11\n(~20 MHz)", ha="right", va="center", fontsize=8.5, color=s.INK)
    ax.set_xlim(2384, 2486)
    ax.set_ylim(-0.25, 3.7)
    ax.set_xticks([2400, 2412, 2437, 2450, 2462, 2483.5])
    ax.set_xticklabels(["2400", "2412", "2437", "2450", "2462", "2483.5"], fontsize=8)
    ax.set_xlabel("frequency (MHz)", fontsize=9)
    s.save(fig, "basics_ism_channels")


# ---------------------------------------------------------------- 3. 듀티 사이클 전류
def duty_cycle():
    fig, ax = plt.subplots(figsize=(12.5, 3.8))
    s.bare(ax)
    base = 0.25
    xs = [0]
    ys = [base]
    events = [6, 46, 86]
    for e in events:
        # 깨어남(램프) → RX → TX → 처리 → 수면
        seg = [(e, base), (e, 1.2), (e + 2.0, 1.2), (e + 2.0, 3.0), (e + 4.4, 3.0), (e + 4.4, 3.4),
               (e + 6.8, 3.4), (e + 6.8, 1.0), (e + 8.8, 1.0), (e + 8.8, base)]
        for x, y in seg:
            xs.append(x)
            ys.append(y)
    xs.append(120)
    ys.append(base)
    ax.fill_between(xs, 0, ys, color=s.DL, alpha=0.18, step=None)
    ax.plot(xs, ys, color=s.DL, lw=1.6)
    ax.plot([-2, 121], [0, 0], color=s.GRID, lw=0.8)
    e = events[1]
    ax.text(e + 1.0, 1.35, "wake", ha="center", fontsize=7.5, color=s.INK2)
    ax.text(e + 3.2, 3.15, "RX", ha="center", fontsize=8, color=s.INK)
    ax.text(e + 5.6, 3.55, "TX", ha="center", fontsize=8, color=s.INK)
    ax.text(e + 7.8, 1.15, "CPU", ha="center", fontsize=7.5, color=s.INK2)
    ax.text(28, base + 0.25, "sleep: RTC + RAM retention (µA range)", ha="center", fontsize=8.5, color=s.INK2)
    ax.annotate("", xy=(events[1], 4.05), xytext=(events[0], 4.05),
                arrowprops=dict(arrowstyle="<->", color=s.INK2, lw=0.9))
    ax.text((events[0] + events[1]) / 2, 4.15, "connection interval (one event per interval)", ha="center", fontsize=8.5, color=s.INK2)
    ax.annotate("", xy=(events[1] + 8.8, -0.3), xytext=(events[1], -0.3),
                arrowprops=dict(arrowstyle="<->", color=s.INK2, lw=0.9))
    ax.text(events[1] + 4.4, -0.45, "active (ms range, mA)", ha="center", va="top", fontsize=8.5, color=s.INK2)
    ax.text(-3, 1.7, "current", rotation=90, ha="center", va="center", fontsize=9, color=s.INK2)
    ax.text(60, -1.15, "I_avg = (I_active x t_active + I_sleep x t_sleep) / interval   (time and current not to scale)",
            ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-5, 122)
    ax.set_ylim(-1.4, 4.5)
    s.save(fig, "basics_duty_cycle")


if __name__ == "__main__":
    s.setup()
    stack()
    ism_channels()
    duty_cycle()
