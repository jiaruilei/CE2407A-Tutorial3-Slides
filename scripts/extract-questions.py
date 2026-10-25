#!/usr/bin/env python3
"""Rebuild the original PDF question snapshots used in Tutorial 3.

Requires Python with Pillow and Poppler's pdftoppm on PATH. The source PDF
is intentionally not bundled; pass the directory containing tutorial
question set 2 with --source-dir. No content is retyped into the snapshots.

Render: 288 dpi = 4 raster pixels per PDF point.
Display: 2 CSS pixels per PDF point (half the PNG's native dimensions).
Crop coordinates are PDF points measured from the top-left of the page.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image


REPO = Path(__file__).resolve().parents[1]
DPI = 288
RASTER_SCALE = DPI / 72
CSS_SCALE = 2

# set, page, crop bbox (left, top, right, bottom), slide position (left, top)
CROPS = [
    {
        "file": "set2-q3-statement.png",
        "set": 2,
        "question": 3,
        "page": 2,
        "slide_id": "question-t2-q3",
        "bbox_pt": [
            92,
            114,
            521,
            168
        ],
        "position_css": [
            98,
            132
        ],
        "alt": "Tutorial Set 2, Question 3. The present air traffic volume at an airport (number of landings and take offs) during the peak hour is a normal variate with a mean of 200 and a standard deviation of 60 airplanes (See figure)."
    },
    {
        "file": "set2-q3-diagram.png",
        "set": 2,
        "question": 3,
        "page": 2,
        "slide_id": "question-t2-q3",
        "bbox_pt": [
            175,
            184,
            452,
            309
        ],
        "position_css": [
            390,
            198
        ],
        "alt": "Question 3 diagram. Vertical axis: Peak Air Traffic. Horizontal axis: Time, years, with 0 and 10 marked. A normal distribution at year 0 is labelled N(200,60). A rising dotted line is labelled Mean Growth Curve."
    },
    {
        "file": "set2-q3-part-a.png",
        "set": 2,
        "question": 3,
        "page": 2,
        "slide_id": "question-t2-q3",
        "bbox_pt": [
            92,
            328,
            521,
            361
        ],
        "position_css": [
            98,
            450
        ],
        "alt": "(a) If the present-runway capacity (for landings and take offs) is 350 planes per hr, what is the current daily probability of air traffic congestion? Assume there is one peak hour daily."
    },
    {
        "file": "set2-q3-part-b.png",
        "set": 2,
        "question": 3,
        "page": 2,
        "slide_id": "question-t2-q3",
        "bbox_pt": [
            92,
            366,
            521,
            421
        ],
        "position_css": [
            98,
            518
        ],
        "alt": "(b) If no additional airports or expansion is built, what would be the probability of congestion 10 years hence? Assume that the mean traffic volume is increasing linearly at 10% of current volume per year, and the coefficient of variation remains the same."
    },
    {
        "file": "set2-q3-part-c.png",
        "set": 2,
        "question": 3,
        "page": 2,
        "slide_id": "question-t2-q3",
        "bbox_pt": [
            92,
            425,
            521,
            460
        ],
        "position_css": [
            98,
            630
        ],
        "alt": "(c) If the projected growth is correct, what airport capacity will be required 10 years from now to maintain the present service condition (i.e. the same probability of congestion as now)?"
    },
    {
        "file": "set2-q4-statement.png",
        "set": 2,
        "question": 4,
        "page": 2,
        "slide_id": "question-t2-q4",
        "bbox_pt": [
            92,
            483,
            521,
            635
        ],
        "position_css": [
            98,
            132
        ],
        "alt": "Tutorial Set 2, Question 4. A system of storm sewers is proposed for a city. In order to evaluate the effectiveness of the sewer system in preventing flooding of the streets, the following information has been gathered. The left figure shows the probability mass function for the number of occurrences of rainstorm each year in the city. The right figure shows the distribution of the maximum runoff rate in each storm, which is log-normal with a median of 7 cfs (cubic feet/sec) and COV of 15%. From hydraulic analysis, the proposed sewer system is shown to be adequate for any storm with runoff rate less than 8 cfs. Assume that the maximum runoff rates between storms are statistically independent."
    },
    {
        "file": "set2-q4-diagrams.png",
        "set": 2,
        "question": 4,
        "page": 3,
        "slide_id": "question-t2-q4-continued",
        "bbox_pt": [
            106,
            73,
            483,
            207
        ],
        "position_css": [
            98,
            132
        ],
        "alt": "Question 4 diagrams. Left figure: rainstorm probability mass function, with vertical axis P_N(n) and horizontal axis n, number of rainstorms in a year. The probabilities for n=0, 1, 2, and 3 are 0.3, 0.4, 0.2, and 0.1 respectively. Right figure: maximum runoff rate distribution, with vertical axis f_R(r) and horizontal axis r, maximum runoff rate in cfs. A right-skewed density curve is labelled Log Normal Median = 7, c.o.v = 15%."
    },
    {
        "file": "set2-q4-parts.png",
        "set": 2,
        "question": 4,
        "page": 3,
        "slide_id": "question-t2-q4-continued",
        "bbox_pt": [
            92,
            227,
            481,
            282
        ],
        "position_css": [
            98,
            420
        ],
        "alt": "(a) What is the mean and variance of the number of rain storms in a year for the city? (b) What is the probability of flooding during a rainstorm? (c) What is the probability of flooding in a year?"
    },
    {
        "file": "set2-q8.png",
        "set": 2,
        "question": 8,
        "page": 5,
        "slide_id": "question-t2-q8",
        "bbox_pt": [
            92,
            67,
            521,
            272
        ],
        "position_css": [
            98,
            132
        ],
        "alt": "Tutorial Set 2, Question 8. The cantilever beam shown below is subjected to a random concentrated load P and a random distributed load W. Assume P is normally distributed with mean 5 and standard deviation 1, in kips, and W is normally distributed with mean 1 and standard deviation 0.2, in kips per foot. (a) Determine the mean and variance of the applied bending moment, M = 50W + 10P. Assume that the correlation between W and P is 0.5. (b) The resisting moment of the beam R is Gaussian, with mean 200 and standard deviation 50, in foot-kips. Determine the probability of failure of the beam, P(R < M), assuming that R and M are independent. Diagram: a 10-foot cantilever fixed at the left end, carrying a downward uniformly distributed load W and a downward concentrated load P at the right end, with bending moment M_a at the fixed support."
    }
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True, type=Path,
                        help="Directory containing CE2407A Tutorial Questions Set 2.pdf")
    parser.add_argument("--output-dir", type=Path, default=REPO / "assets" / "questions")
    parser.add_argument("--work-dir", type=Path, default=REPO / "tmp" / "question-extraction")
    args = parser.parse_args()
    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm is None:
        parser.error("Poppler pdftoppm was not found on PATH")

    sources = {number: args.source_dir / f"CE2407A Tutorial Questions Set {number}.pdf"
               for number in (2,)}
    for source in sources.values():
        if not source.is_file():
            parser.error(f"Missing source PDF: {source}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    work_dir = args.work_dir.resolve()
    work_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "render_dpi": DPI,
        "raster_pixels_per_pdf_point": RASTER_SCALE,
        "css_pixels_per_pdf_point": CSS_SCALE,
        "coordinate_system": "PDF points from page top-left",
        "sources": [{"set": number, "filename": source.name,
                     "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}
                    for number, source in sources.items()],
        "snapshots": [],
    }
    with tempfile.TemporaryDirectory(prefix="render-", dir=work_dir) as temp:
        # Validate the directory before TemporaryDirectory recursively cleans it.
        if not Path(temp).resolve().is_relative_to(work_dir):
            raise ValueError("Temporary directory is outside the selected work directory")
        page_images: dict[tuple[int, int], Image.Image] = {}
        for number, page in sorted({(crop["set"], crop["page"]) for crop in CROPS}):
            prefix = Path(temp) / f"set{number}-page{page}"
            subprocess.run([pdftoppm, "-f", str(page), "-singlefile", "-r", str(DPI),
                            "-png", str(sources[number]), str(prefix)], check=True)
            page_images[(number, page)] = Image.open(prefix.with_suffix(".png")).convert("RGB")
        for crop in CROPS:
            left, top, right, bottom = crop["bbox_pt"]
            pixel_bbox = tuple(round(value * RASTER_SCALE) for value in (left, top, right, bottom))
            snapshot = page_images[(crop["set"], crop["page"])].crop(pixel_bbox)
            snapshot.save(args.output_dir / crop["file"], optimize=True, dpi=(DPI, DPI))
            dimensions = [(right - left) * CSS_SCALE, (bottom - top) * CSS_SCALE]
            x, y = crop["position_css"]
            if x + dimensions[0] > 1259 or y + dimensions[1] > 700:
                raise ValueError(f"Snapshot exceeds slide-safe area: {crop['file']}")
            manifest["snapshots"].append({**crop, "dimensions_css": dimensions,
                                           "dimensions_px": list(snapshot.size)})
            print(f"{crop['file']}: {snapshot.width}x{snapshot.height}px -> "
                  f"{dimensions[0]}x{dimensions[1]} CSS px at ({x}, {y})")
        for page_image in page_images.values():
            page_image.close()

    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
