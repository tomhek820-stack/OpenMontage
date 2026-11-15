"""Generate the Arabic narration track for the world-in-numbers demo."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


TEXT = (
    "تَخَيَّلْ كَوْكَبًا يَضُمُّ أَكْثَرَ مِنْ ثَمَانِيَةِ مِلْيَارَاتِ إِنْسَانٍ. "
    "تَتَجَمَّعُ الْحَيَاةُ فِي مُدُنٍ كَبِيرَةٍ، وَتَتَغَيَّرُ طَرِيقَةُ إِنْتَاجِ الطَّاقَةِ حَوْلَ الْعَالَمِ. "
    "الأَرْقَامُ لَيْسَتْ مُجَرَّدَ إِحْصَائِيَّاتٍ؛ إِنَّهَا قِصَصٌ عَنْ قَرَارَاتِنَا وَمُسْتَقْبَلِنَا."
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if not args.model.is_file() or not args.config.is_file():
        raise SystemExit("Piper Arabic model or config is missing.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "piper",
            "--model", str(args.model),
            "--config", str(args.config),
            "--output_file", str(args.output),
        ],
        input=TEXT,
        text=True,
        check=True,
    )

    if not args.output.is_file() or args.output.stat().st_size < 10_000:
        raise SystemExit("Piper did not create a valid narration WAV file.")

    print(f"Generated narration: {args.output} ({args.output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
