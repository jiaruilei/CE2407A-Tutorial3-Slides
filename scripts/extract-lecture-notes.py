#!/usr/bin/env python3
"""Extract original lecture-note snapshots and lossless panels from the source PPTX.

The original image bytes are copied unchanged. Panel images crop and, for the
normal table, concatenate source pixels without resampling. PowerPoint's
separate handwriting images are deliberately excluded.
Requires Pillow and lxml. Example:
  python scripts/extract-lecture-notes.py --source "path/to/Tutorial 3_Recorded.pptx"
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import posixpath
from zipfile import ZipFile

from lxml import etree as ET
from PIL import Image

REPO = Path(__file__).resolve().parents[1]
SPECS = [
    {
        "question": 3,
        "slide_number": 3,
        "media_member": "ppt/media/image5.png",
        "source_dimensions_px": [
            565,
            677
        ],
        "description": "Standard normal distribution function table",
        "panels": [
            {
                "side": "left",
                "components": [
                    [
                        56,
                        0,
                        565,
                        386
                    ]
                ],
                "alt": "Standard normal distribution function table, original header and rows z=0.0 through z=1.8. The table gives cumulative probabilities for column offsets 0.00 through 0.09. Original red and blue guide marks are retained."
            },
            {
                "side": "right",
                "components": [
                    [
                        56,
                        0,
                        565,
                        109
                    ],
                    [
                        56,
                        386,
                        565,
                        677
                    ]
                ],
                "alt": "Standard normal distribution function table, repeated original header and remaining rows z=1.9 through z=3.5, plus the original z=4.0 and z=5.0 entries. The table gives cumulative probabilities for column offsets 0.00 through 0.09."
            }
        ],
        "split_note": "Split at source y=386 between z=1.8 and z=1.9. The right panel repeats the original header y=0..109. Crop x=56 removes the blank left margin while retaining all table text and baked guide marks. The untouched full image is retained."
    },
    {
        "question": 4,
        "slide_number": 8,
        "media_member": "ppt/media/image15.png",
        "source_dimensions_px": [
            488,
            725
        ],
        "description": "Lognormal distribution parameters and cumulative distribution function",
        "panels": [
            {
                "side": "left",
                "components": [
                    [
                        0,
                        0,
                        488,
                        370
                    ]
                ],
                "alt": "Lecture notes on the lognormal distribution: probability density, parameters lambda and zeta, relationship between mean, variance, coefficient of variation and median, and density curves for several zeta values."
            },
            {
                "side": "right",
                "components": [
                    [
                        0,
                        370,
                        488,
                        725
                    ]
                ],
                "alt": "Lecture notes deriving the lognormal cumulative distribution function through standard normal transformation S=(ln X-lambda)/zeta, with the equivalence between lognormal X and normally distributed ln X."
            }
        ],
        "split_note": "Split immediately below the original horizontal divider at y=370. All source pixels are retained across the two panels."
    },
    {
        "question": 5,
        "slide_number": 13,
        "media_member": "ppt/media/image25.png",
        "source_dimensions_px": [
            476,
            730
        ],
        "description": "Poisson process assumptions and distribution derivation",
        "panels": [
            {
                "side": "left",
                "components": [
                    [
                        0,
                        0,
                        476,
                        368
                    ]
                ],
                "alt": "Lecture notes on Poisson process assumptions: random occurrence in time or space, independence between intervals, rate nu, event probability nu times delta t in a short interval, and negligible probability of multiple events in an infinitesimal interval."
            },
            {
                "side": "right",
                "components": [
                    [
                        0,
                        368,
                        476,
                        730
                    ]
                ],
                "alt": "Lecture notes deriving the Poisson distribution as a limit of binomial probabilities. The result is P(X=x)=(nu t)^x exp(-nu t)/x!, for x=0,1,2,..., with the same interpretation for distance in place of time."
            }
        ],
        "split_note": "Split immediately below the original separator at y=368. All source pixels are retained across the two panels."
    },
    {
        "question": 6,
        "slide_number": 18,
        "media_member": "ppt/media/image35.png",
        "source_dimensions_px": [
            500,
            712
        ],
        "description": "Exponential distribution from Poisson recurrence times",
        "panels": [
            {
                "side": "left",
                "components": [
                    [
                        0,
                        0,
                        500,
                        378
                    ]
                ],
                "alt": "Lecture notes deriving the exponential distribution from the waiting time to the first event in a Poisson process. Zero occurrences during time t is equivalent to the first occurrence time T being greater than t."
            },
            {
                "side": "right",
                "components": [
                    [
                        0,
                        378,
                        500,
                        712
                    ]
                ],
                "alt": "Lecture notes on the exponential distribution: P(T>t)=exp(-nu t), cumulative distribution F_T(t)=1-exp(-nu t), density f_T(t)=nu exp(-nu t) for t at least zero, and mean return period E(T)=1/nu."
            }
        ],
        "split_note": "Split immediately below the original separator at y=378. All source pixels are retained across the two panels."
    }
]
NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output-dir", default=REPO / "assets" / "lecture-notes", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source": {"filename": args.source.name,
                   "sha256": hashlib.sha256(args.source.read_bytes()).hexdigest()},
        "panel_method": "Original PNG bytes preserved. Derived panels copy source pixels without resampling.",
        "coordinate_system": "Source image pixels, left/top inclusive and right/bottom exclusive",
        "originals": [],
        "snapshots": [],
    }
    with ZipFile(args.source) as archive:
        for spec in SPECS:
            number = spec["slide_number"]
            slide = ET.fromstring(archive.read(f"ppt/slides/slide{number}.xml"))
            rels = ET.fromstring(archive.read(f"ppt/slides/_rels/slide{number}.xml.rels"))
            targets = {rel.get("Id"): posixpath.normpath(posixpath.join("ppt/slides", rel.get("Target")))
                       for rel in rels}
            matches = []
            for pic in slide.findall(".//p:pic", NS):
                blip = pic.find("p:blipFill/a:blip", NS)
                if blip is not None and targets.get(blip.get("{" + NS["r"] + "}embed")) == spec["media_member"]:
                    matches.append(pic)
            if len(matches) != 1:
                raise ValueError(f"Expected exactly one source picture on slide {number}")
            rect = matches[0].find("p:blipFill/a:srcRect", NS)
            crop = {} if rect is None else dict(rect.attrib)
            if any(int(value) != 0 for value in crop.values()):
                raise ValueError(f"Unexpected PowerPoint crop for question {spec['question']}: {crop}")
            original_file = f"set2-q{spec['question']}.png"
            data = archive.read(spec["media_member"])
            destination = args.output_dir / original_file
            destination.write_bytes(data)
            original_sha = hashlib.sha256(data).hexdigest()
            with Image.open(destination) as original:
                if list(original.size) != spec["source_dimensions_px"]:
                    raise ValueError(f"Unexpected source dimensions for {original_file}")
                manifest["originals"].append({
                    "file": original_file, "set": 2, "question": spec["question"],
                    "source_slide": number, "media_member": spec["media_member"],
                    "source_picture_name": matches[0].find("p:nvPicPr/p:cNvPr", NS).get("name"),
                    "source_crop": crop, "dimensions_px": list(original.size),
                    "sha256": original_sha, "description": spec["description"],
                    "split_note": spec["split_note"],
                })
                for panel in spec["panels"]:
                    pieces = [original.crop(box) for box in panel["components"]]
                    width = pieces[0].width
                    if not all(piece.width == width for piece in pieces):
                        raise ValueError("Panel components must have equal widths")
                    height = sum(piece.height for piece in pieces)
                    result = Image.new(original.mode, (width, height))
                    y = 0
                    for piece in pieces:
                        result.paste(piece, (0, y))
                        y += piece.height
                    filename = f"set2-q{spec['question']}-{panel['side']}.png"
                    result.save(args.output_dir / filename, optimize=True)
                    css_height = round(height * 530 / width, 6)
                    position = [98 if panel["side"] == "left" else 652, 132]
                    if position[0] + 530 > 1182 or 132 + css_height > 700:
                        raise ValueError(f"Panel exceeds designated slide area: {filename}")
                    manifest["snapshots"].append({
                        "file": filename, "set": 2, "question": spec["question"],
                        "slide_id": f"notes-t2-q{spec['question']}", "source_slide": number,
                        "media_member": spec["media_member"], "original_file": original_file,
                        "source_components_px": panel["components"],
                        "dimensions_px": [width, height],
                        "dimensions_css": [530, css_height],
                        "position_css": position, "alt": panel["alt"],
                        "sha256": hashlib.sha256((args.output_dir / filename).read_bytes()).hexdigest(),
                    })
                    print(f"{filename}: {width}x{height}px, CSS 530x{css_height} at {position}")
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
