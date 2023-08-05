from pathlib import Path
from typing import List, Optional
import argparse
import sys

from PyPDF2 import PdfMerger

def join(pdfs: List[Path]) -> PdfMerger:
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(str(pdf))
    return merger

def output(pdf: PdfMerger, out: Optional[Path]) -> None:
    if out is not None:
        with open(out, "bw") as output:
            pdf.write(output)
    else:
        pdf.write(sys.stdout.buffer)
    pdf.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Join multiple PDFs")
    parser.add_argument("pdf", type=Path, nargs="+", help="Path to the pdf file")
    parser.add_argument("-o", "--output", type=Path, help="Save output to file")
    args = parser.parse_args()

    for pdf in args.pdf:
        if not pdf.is_file():
            print(f"Error: could not find file '{pdf}'", file=sys.stderr)
            exit(1)

    if args.output is None and sys.stdout.isatty():
        print(f"Error: printing binary data to terminal. Either redirect it or use an output file.", file=sys.stderr)
        exit(1)

    return args
 
def main() -> None:
    args = parse_args()
    output(join(args.pdf), args.output)

if __name__ == "__main__":
    main()
