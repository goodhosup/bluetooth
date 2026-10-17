"""Mesh 그림

1. mesh_flooding    : 관리형 플러딩 — Relay/Proxy/Friend/LPN 노드 배치와 TTL 감소
2. mesh_network_pdu : 네트워크 PDU 필드 배치 (IVI, NID, CTL, TTL, SEQ, SRC, DST, Transport PDU, NetMIC)
3. mesh_stack       : Mesh 계층 구조 (Bearer → Model)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

import style as s


def box(ax, x, y, w, h, fc, label="", fs=8.5, ec="#ffffff", lw=1.2, tc=None):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs,
                color=tc or s.text_on(fc))


def mesh_flooding():
    fig, ax = plt.subplots(figsize=(11, 5.4))
    s.bare(ax)
    # (이름, x, y, 역할, 색)
    nodes = {
        "SW": (0.5, 2.5, "Switch\n(src)", s.UL),
        "R1": (3.0, 3.6, "Relay", s.DL),
        "R2": (3.0, 1.3, "Relay", s.DL),
        "N1": (5.6, 4.4, "Node", s.MUTED),
        "R3": (5.6, 2.4, "Relay", s.DL),
        "P": (5.6, 0.4, "Proxy", s.CTRL),
        "L1": (8.4, 3.6, "Light\n(sub)", s.SYNC),
        "F": (8.4, 1.5, "Friend", s.SPECIAL),
        "LPN": (10.6, 1.5, "LPN", s.ALT),
        "PH": (8.4, -0.6, "Phone\n(GATT)", s.MUTED),
    }
    links = [("SW", "R1", "TTL 4"), ("SW", "R2", "TTL 4"), ("R1", "N1", "3"), ("R1", "R3", "3"),
             ("R2", "R3", "3"), ("R2", "P", "3"), ("R3", "L1", "2"), ("R3", "F", "2"),
             ("R1", "L1", "3")]
    for a, b, lab in links:
        xa, ya = nodes[a][:2]
        xb, yb = nodes[b][:2]
        ax.add_patch(FancyArrowPatch((xa, ya), (xb, yb), arrowstyle="-|>", mutation_scale=12,
                                     color=s.INK2, lw=1.0, shrinkA=22, shrinkB=22))
        ax.text((xa + xb) / 2, (ya + yb) / 2 + 0.12, lab, fontsize=7.5, color=s.INK2, ha="center")
    # Friend - LPN (poll), Proxy - phone (GATT)
    for a, b, lab, st in (("F", "LPN", "Friend Poll /\nqueued msgs", "--"), ("P", "PH", "GATT bearer", ":")):
        xa, ya = nodes[a][:2]
        xb, yb = nodes[b][:2]
        ax.plot([xa, xb], [ya, yb], ls=st, color=s.RS, lw=1.4, zorder=0)
        ax.text((xa + xb) / 2 + 0.15, (ya + yb) / 2 + 0.45, lab, fontsize=7.5, color=s.RS, ha="center")
    for name, (x, y, lab, c) in nodes.items():
        ax.add_patch(Circle((x, y), 0.55, facecolor=c, edgecolor="#ffffff", lw=1.5))
        ax.text(x, y, lab, ha="center", va="center", fontsize=8, color=s.text_on(c))
    ax.text(5.6, -1.75, "ADV bearer broadcast on ch 37/38/39 · each relay decrements TTL and drops "
            "messages already in its message cache", ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-0.4, 11.5)
    ax.set_ylim(-2.0, 5.2)
    ax.set_aspect("equal")
    s.save(fig, "mesh_flooding")


def mesh_network_pdu():
    fig, ax = plt.subplots(figsize=(13, 3.4))
    s.bare(ax)
    # (라벨, 비트 길이, 색, 보호)
    fields = [("IVI", 1, s.SYNC), ("NID", 7, s.SYNC), ("CTL", 1, s.CTRL), ("TTL", 7, s.CTRL),
              ("SEQ", 24, s.CTRL), ("SRC", 16, s.CTRL), ("DST", 16, s.DL),
              ("TransportPDU\n1-16 octets", 64, s.DL), ("NetMIC\n32 / 64 bit", 24, s.RS)]
    scale = 0.075
    x = 0
    h = 0.9
    pos = {}
    for lab, bits, c in fields:
        w = max(bits * scale, 0.42)
        box(ax, x, 1.0, w, h, c, lab, fs=8)
        bl = f"{bits} bit" if lab in ("IVI", "NID", "CTL", "TTL", "SEQ", "SRC", "DST") else ""
        if bl:
            ax.text(x + w / 2, 0.85, bl, ha="center", va="top", fontsize=7, color=s.INK2)
        pos[lab.split("\n")[0]] = (x, x + w)
        x += w

    def bracket(x0, x1, y, text, color):
        ax.plot([x0, x0, x1, x1], [y - 0.1, y, y, y - 0.1], color=color, lw=1.1)
        ax.text((x0 + x1) / 2, y + 0.08, text, ha="center", va="bottom", fontsize=8, color=color)

    bracket(pos["CTL"][0], pos["SRC"][1], 2.1, "obfuscated (PrivacyKey, AES-ECB)", s.CTRL)
    bracket(pos["DST"][0], pos["NetMIC"][0], 2.1, "encrypted (EncryptionKey, AES-CCM)", s.DL)
    bracket(pos["IVI"][0], pos["NID"][1], 2.1, "clear", s.SYNC)
    ax.text(x / 2, 0.25, "max 29 octets in one Mesh Message AD · CTL=0: access msg, NetMIC 32 bit · "
            "CTL=1: control msg, NetMIC 64 bit", ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-0.2, x + 0.2)
    ax.set_ylim(0, 2.7)
    s.save(fig, "mesh_network_pdu")


def mesh_stack():
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    s.bare(ax)
    layers = [
        ("Model layer  (Generic OnOff, Light Lightness, Sensor ...)", s.SYNC),
        ("Foundation Model layer  (Configuration, Health)", s.SYNC),
        ("Access layer  (opcode, AppKey/DevKey selection)", s.DL),
        ("Upper Transport layer  (AppKey encryption, TransMIC)", s.DL),
        ("Lower Transport layer  (segmentation & reassembly)", s.CTRL),
        ("Network layer  (NetKey, relay, address, TTL)", s.CTRL),
    ]
    y = 5.0
    for lab, c in layers:
        box(ax, 0, y, 8, 0.7, c, lab, fs=9.5)
        y -= 0.78
    box(ax, 0, y, 3.95, 0.7, s.UL, "ADV bearer (AD 0x2A)", fs=9.5)
    box(ax, 4.05, y, 3.95, 0.7, s.UL, "GATT bearer (Proxy 0x1828)", fs=9.5)
    y -= 0.78
    box(ax, 0, y, 8, 0.7, s.MUTED, "Bluetooth LE Core (Link Layer, GAP, GATT)", fs=9.5)
    ax.set_xlim(-0.2, 8.2)
    ax.set_ylim(y - 0.2, 5.9)
    s.save(fig, "mesh_stack")


if __name__ == "__main__":
    s.setup()
    mesh_flooding()
    mesh_network_pdu()
    mesh_stack()
