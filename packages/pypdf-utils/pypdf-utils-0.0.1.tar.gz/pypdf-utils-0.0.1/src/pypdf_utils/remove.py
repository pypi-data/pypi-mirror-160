from typing import List
from pathlib import Path
import argparse
import sys

from PyPDF2 import PdfReader, PdfWriter

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TODO: add a description")
    parser.add_argument("pdf", type=Path, help="Path to the pdf file")
    parser.add_argument("page_numbers", type=str, help="Pages to delete. Comma separated. Example: '2,3,5-7'")
    parser.add_argument("-o", "--output", type=Path, help="Save output to file")
    args = parser.parse_args()

    if not args.pdf.is_file():
        print(f"Error: could not find file '{args.pdf}'", file=sys.stderr)
        exit(1)

    if args.output is None and sys.stdout.isatty():
        print(f"Error: printing binary data to terminal. Either redirect it or use an output file.", file=sys.stderr)
        exit(1)

    return args

def parse_page_range(page_range: str) -> List[int]:
    page_range_list = page_range.split("-")
    if len(page_range_list) > 2:
        print(f"Error: unable to interpret page range '{page_range}'", file=sys.stderr)

    if len(page_range_list) == 2:
        return list(range(int(page_range_list[0]), int(page_range_list[1])))
    else:
        return [int(page_range)]

def parse_page_numbers(format: str) -> List[int]:
    pages = []
    for page_range in format.split(","):
        pages += parse_page_range(page_range)

    unique_pages = list(set(pages))
    unique_pages.sort()
    return unique_pages
 
def main() -> None:
    args = parse_args()
    pages_to_delete = parse_page_numbers(args.page_numbers)

    reader = PdfReader(args.pdf)
    total_pages = range(len(reader.pages))

    should_keep = lambda i: i not in pages_to_delete
    page_indices = filter(should_keep, total_pages)

    writer = PdfWriter()
    for page_idx in page_indices:
        writer.add_page(reader.pages[page_idx])

    if args.output is not None:
        with open(args.output, "bw") as output:
            writer.write(output)
    else:
        writer.write(sys.stdout.buffer)

if __name__ == "__main__":
    main()
