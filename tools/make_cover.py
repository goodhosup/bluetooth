"""위키독스 책 표지 (1200 × 1600 PNG)를 만든다.

    python tools/make_cover.py            # → docs/assets/cover.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import Arc, FancyBboxPatch, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "cover.png"

KO = next((f for f in ("NanumSquare", "NanumBarunGothic", "NanumGothic", "Noto Sans CJK KR")
           if any(f in x.name for x in font_manager.fontManager.ttflist)), "DejaVu Sans")

BG_TOP = np.array([0x0b, 0x2a, 0x6f]) / 255     # 짙은 파랑
BG_BOT = np.array([0x0a, 0x1a, 0x2e]) / 255     # 남색
TEAL = "#2dd4bf"
WHITE = "#ffffff"
SOFT = "#cfe9e5"
CH = ["#2a78d6", "#1baf7a", "#eda100", "#eb6834", "#4a3aa7", "#e87ba4"]


def main() -> None:
    W, H = 12, 16
    fig = plt.figure(figsize=(W, H), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_axis_off()

    # 배경 그라데이션
    grad = np.linspace(0, 1, 512)[:, None, None]
    img = BG_BOT * grad + BG_TOP * (1 - grad)
    ax.imshow(np.repeat(img, 2, axis=1), extent=[0, W, 0, H], aspect="auto", zorder=0)

    # Bluetooth 룬 심볼 (둥근 방패 + 하갈·베르카노 룬 선)
    cx, cy = W / 2, 8.2
    ax.add_patch(FancyBboxPatch((cx - 1.75, cy - 2.6), 3.5, 5.2, boxstyle="round,pad=0,rounding_size=1.65",
                                facecolor="#1d4ed8", edgecolor=TEAL, lw=4, zorder=3))
    k = 0.92
    rune = [(-1, -1), (1, 1), (0, 2), (0, -2), (1, -1), (-1, 1)]
    ax.plot([cx + x * k for x, _ in rune], [cy + y * k for _, y in rune], color=WHITE, lw=16,
            solid_capstyle="round", solid_joinstyle="miter", zorder=4)

    # 주변으로 퍼지는 옅은 파면
    for r in np.arange(3.6, 9.5, 0.75):
        ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, theta1=20, theta2=160, lw=1.2,
                         color=TEAL, alpha=max(0.05, 0.35 - (r - 3.6) * 0.06), zorder=2))

    # LE 40채널 띠 (광고 채널 37·38·39 강조, 주파수 순서)
    x0, x1 = 0.9, W - 0.9
    n = 40
    w = (x1 - x0) / n
    for j in range(n):  # j = RF 채널 (2402 + 2j MHz)
        adv = j in (0, 12, 39)
        ax.add_patch(Rectangle((x0 + j * w + 0.02, 4.6), w - 0.04, 0.42,
                               color=TEAL if adv else "#3b82f6", alpha=0.95 if adv else 0.55, zorder=2))

    # 제목
    ax.text(cx, 13.55, "Bluetooth Handbook", ha="center", va="center", color=WHITE, fontsize=72,
            fontweight="bold", family="DejaVu Sans", zorder=4)
    ax.text(cx, 12.45, "Classic  ·  Low Energy  ·  LE Audio", ha="center", va="center", color=TEAL,
            fontsize=40, family="DejaVu Sans", zorder=4)
    ax.text(cx, 3.05, "블루투스 핸드북", ha="center", va="center", color=WHITE, fontsize=66,
            fontweight="bold", family=KO, zorder=4)
    ax.text(cx, 2.05, "기초부터 전문가까지 · 한글 블루투스 규격 해설", ha="center", va="center", color=SOFT,
            fontsize=30, family=KO, zorder=4)

    # 개정판 칩
    chips = ["4.0", "4.2", "5.0", "5.4", "6.0"]
    cw, gap = 1.5, 0.3
    total = len(chips) * cw + (len(chips) - 1) * gap
    for i, c in enumerate(chips):
        x = cx - total / 2 + i * (cw + gap)
        ax.add_patch(FancyBboxPatch((x, 0.75), cw, 0.62, boxstyle="round,pad=0,rounding_size=0.31",
                                    facecolor="none", edgecolor=TEAL, lw=2.5, zorder=4))
        ax.text(x + cw / 2, 1.06, c, ha="center", va="center", color=WHITE, fontsize=24,
                family="DejaVu Sans", zorder=5)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=100)
    plt.close(fig)
    print(f"→ {OUT.relative_to(ROOT)} ({KO})")


if __name__ == "__main__":
    main()
