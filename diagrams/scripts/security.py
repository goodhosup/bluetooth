"""보안 섹션 그림

1. sec_rpa_format    : 48비트 RPA = prand(24, 최상위 2비트 01) || hash(24) 와 ah() 계산
2. sec_key_hierarchy : LE Secure Connections 키 유도 (DHKey → f5 → MacKey/LTK) 와 CTKD(h6/h7)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

import style as s


def box(ax, x, y, w, h, fc, label="", fs=9, ec="#ffffff", lw=1.2, tc=None):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=tc or s.text_on(fc))


def rbox(ax, x, y, w, h, fc, label, fs=9, tc=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor=fc, edgecolor="#ffffff", linewidth=1.2))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=tc or s.text_on(fc))


def arrow(ax, x0, y0, x1, y1, text="", fs=8, color=None, off=(0.1, 0)):
    color = color or s.INK2
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="->", color=color, lw=1.1))
    if text:
        ax.text((x0 + x1) / 2 + off[0], (y0 + y1) / 2 + off[1], text, fontsize=fs, color=color,
                ha="left" if off[0] >= 0 else "right", va="center")


def rpa_format():
    fig, ax = plt.subplots(figsize=(11, 4.0))
    s.bare(ax)
    y, h = 2.2, 0.8
    # MSB (bit 47) on the left
    box(ax, 0, y, 1.2, h, s.CTRL, "0 1", fs=9)
    box(ax, 1.2, y, 10.8, h, s.DL, "prand: random part (22 bits)", fs=9.5)
    box(ax, 12, y, 12, h, s.SYNC, "hash = ah(IRK, prand)  (24 bits)", fs=9.5)
    for x, t in ((0, "bit 47"), (12, "bit 23"), (24, "bit 0")):
        ax.text(x, y + h + 0.15, t, ha="center", fontsize=8, color=s.INK2)
    ax.annotate("", xy=(12, y - 0.25), xytext=(0, y - 0.25), arrowprops=dict(arrowstyle="<->", color=s.INK2, lw=0.9))
    ax.text(6, y - 0.4, "prand (24 bits, two MSBs = 0b01 marks RPA)", ha="center", va="top", fontsize=8.5, color=s.INK2)
    ax.annotate("", xy=(24, y - 0.25), xytext=(12, y - 0.25), arrowprops=dict(arrowstyle="<->", color=s.INK2, lw=0.9))
    ax.text(18, y - 0.4, "hash (24 bits)", ha="center", va="top", fontsize=8.5, color=s.INK2)
    # ah()
    yb = 0.0
    rbox(ax, 1.0, yb, 6.0, 0.7, s.EMPTY, "r' = 104 zero bits || prand", fs=8.5, tc=s.INK)
    rbox(ax, 8.5, yb, 6.5, 0.7, s.SPECIAL, "e(IRK, r')  AES-128", fs=9)
    rbox(ax, 16.5, yb, 6.5, 0.7, s.EMPTY, "lowest 24 bits -> hash", fs=8.5, tc=s.INK)
    arrow(ax, 7.0, yb + 0.35, 8.5, yb + 0.35)
    arrow(ax, 15.0, yb + 0.35, 16.5, yb + 0.35)
    ax.text(12, -0.55, "resolver: for each IRK in resolving list, recompute ah(IRK, prand) and compare with hash",
            ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-0.5, 24.5)
    ax.set_ylim(-0.9, 3.4)
    s.save(fig, "sec_rpa_format")


def key_hierarchy():
    fig, ax = plt.subplots(figsize=(12, 5.2))
    s.bare(ax)
    w, h = 3.0, 0.75
    # LE SC pairing chain
    rbox(ax, 0.0, 4.0, w, h, s.DL, "P-256 key pair A")
    rbox(ax, 0.0, 2.8, w, h, s.UL, "P-256 key pair B")
    rbox(ax, 4.2, 3.4, w, h, s.CTRL, "DHKey (ECDH)")
    arrow(ax, 3.0, 4.35, 4.2, 3.9)
    arrow(ax, 3.0, 3.15, 4.2, 3.6)
    rbox(ax, 8.4, 3.4, 3.4, h, s.SPECIAL, "f5(DHKey, Na, Nb, A, B)", fs=8.5)
    arrow(ax, 7.2, 3.775, 8.4, 3.775)
    rbox(ax, 13.0, 4.3, w, h, s.EMPTY, "MacKey", tc=s.INK)
    rbox(ax, 13.0, 2.6, w, h, s.SYNC, "LTK (128 bits)")
    arrow(ax, 11.8, 3.9, 13.0, 4.6)
    arrow(ax, 11.8, 3.6, 13.0, 3.0)
    ax.text(14.5, 5.3, "f6 -> DHKey Check (Ea, Eb)", ha="center", fontsize=8, color=s.INK2)
    # LTK uses
    rbox(ax, 13.0, 0.6, w, h, s.EMPTY, "LE session key SK", tc=s.INK)
    arrow(ax, 14.5, 2.6, 14.5, 1.35, "e(LTK, SKD)", off=(0.12, 0))
    # CTKD
    rbox(ax, 8.4, 0.6, 3.4, h, s.ALT, "BR/EDR Link Key")
    ax.annotate("", xy=(11.8, 1.15), xytext=(13.0, 2.75),
                arrowprops=dict(arrowstyle="<->", color=s.RS, lw=1.3))
    ax.text(10.0, 2.25, "CTKD: h6 / h7\n'tmp1','lebr' (LE -> BR)\n'tmp2','brle' (BR -> LE)",
            ha="center", fontsize=8, color=s.RS)
    # distributed keys
    rbox(ax, 0.0, 0.9, w, h, s.EMPTY, "IRK (privacy)", tc=s.INK)
    rbox(ax, 0.0, -0.1, w, h, s.EMPTY, "CSRK (signing)", tc=s.INK)
    ax.text(1.5, 1.95, "phase 3: distributed,\nnot derived from DHKey", ha="center", fontsize=8, color=s.INK2)
    ax.set_xlim(-0.3, 16.3)
    ax.set_ylim(-0.4, 5.6)
    s.save(fig, "sec_key_hierarchy")


if __name__ == "__main__":
    s.setup()
    rpa_format()
    key_hierarchy()
