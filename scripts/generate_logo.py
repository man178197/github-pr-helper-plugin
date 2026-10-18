#!/usr/bin/env python3
"""Generate the raster logo used by the plugin listing."""

from pathlib import Path

from PIL import Image, ImageDraw


SCALE = 4
SIZE = 512
OUTPUT = Path(__file__).resolve().parents[1] / "plugins" / "github-pr-helper" / "assets" / "logo.png"


def scaled(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return [(x * SCALE, y * SCALE) for x, y in points]


def main() -> None:
    image = Image.new("RGBA", (SIZE * SCALE, SIZE * SCALE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((0, 0, 511 * SCALE, 511 * SCALE), radius=104 * SCALE, fill="#0d1117")
    draw.rounded_rectangle(
        (14 * SCALE, 14 * SCALE, 498 * SCALE, 498 * SCALE),
        radius=92 * SCALE,
        outline="#30363d",
        width=12 * SCALE,
    )

    line_width = 30 * SCALE
    draw.line(
        scaled([(166, 356), (166, 184), (217, 134), (300, 134)]),
        fill="#f0f6fc",
        width=line_width,
        joint="curve",
    )
    draw.line(
        scaled([(269, 92), (331, 134), (269, 176)]),
        fill="#f0f6fc",
        width=line_width,
        joint="curve",
    )

    draw.ellipse(scaled([(121, 331), (211, 421)]), fill="#58a6ff")
    for center in ((166, 156), (330, 156)):
        x, y = center
        draw.ellipse(
            scaled([(x - 45, y - 45), (x + 45, y + 45)]),
            fill="#0d1117",
            outline="#f0f6fc",
            width=20 * SCALE,
        )

    draw.line(
        scaled([(292, 330), (330, 368), (405, 278)]),
        fill="#3fb950",
        width=34 * SCALE,
        joint="curve",
    )

    image = image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
