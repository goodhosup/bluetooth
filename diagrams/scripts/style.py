"""모든 그림이 같은 시각 언어를 쓰도록 하는 공통 스타일.

- 색은 '역할'로 고정한다: 하향(DL)·데이터=파랑, 상향(UL)=주황, 가드/대기=노랑,
  프리앰블(레거시 필드)=초록, 제어·신호 필드=보라, 파일럿·경합=빨강 …
  그림이 달라도 같은 의미는 같은 색이 되도록 이 모듈의 상수만 쓴다.
- 색만으로 의미를 전달하지 않는다: 칸 안에 D/U/S 같은 글자 라벨을 함께 넣는다.
- 결과물은 docs/assets/figures/<name>.svg (텍스트는 path로 변환 → 어느 환경에서나 동일)
"""
from __future__ import annotations

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "docs" / "assets" / "figures"

# 역할별 색 (dataviz 기준 팔레트의 categorical 슬롯을 의미에 고정)
DL = "#2a78d6"        # 하향(AP→STA) / 데이터 필드
UL = "#eb6834"        # 상향(STA→AP)
SPECIAL = "#eda100"   # 가드, IFS, 대기
SYNC = "#1baf7a"      # 프리앰블 학습 필드 (L-STF/L-LTF, xx-STF/LTF)
CTRL = "#4a3aa7"      # 신호 필드 (L-SIG, HT/VHT/HE/EHT-SIG, U-SIG) · 제어 프레임
RS = "#e34948"        # 파일럿·충돌·경합
ALT = "#e87ba4"       # 보조 강조 (두 번째 링크·STA 등)

INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8985"
GRID = "#d9d8d4"
EMPTY = "#f4f3f0"
SURFACE = "#ffffff"


def setup() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.edgecolor": GRID,
        "axes.labelcolor": INK2,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "text.color": INK,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "svg.fonttype": "path",
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.15,
    })


def bare(ax) -> None:
    """축 눈금·테두리를 모두 끈다 (다이어그램용)."""
    ax.set_axis_off()


def save(fig, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.svg"
    fig.savefig(path, format="svg")
    preview = os.environ.get("FIG_PREVIEW_DIR")  # PNG 사본 (검토용·위키독스 내보내기용, 선택)
    if preview:
        dpi = int(os.environ.get("FIG_PNG_DPI", "110"))
        fig.savefig(Path(preview) / f"{name}.png", format="png", dpi=dpi)
    plt.close(fig)
    print(f"  ✓ {path.relative_to(OUT.parents[2])}")
    return path


def text_on(color: str) -> str:
    """배경색 위에서 읽히는 글자색 (밝은 노랑/분홍 위에는 검정)."""
    return INK if color in (SPECIAL, ALT, EMPTY, SURFACE) else "#ffffff"
