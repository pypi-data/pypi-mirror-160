from pathlib import Path
import argparse
import sys
import logging

from PyPDF2 import PdfReader, PdfWriter

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TODO: add a description")
    parser.add_argument("pdf", type=Path, help="Path to the pdf file")
    parser.add_argument("-o", "--output", type=Path, help="Save output to file")
    parser.add_argument("-b", "--add-blank", type=int, action="append", help="Add blank page. Format <pos,qty>. example: --blank 0,2")
    parser.add_argument("--pages", type=int, default=4, help="Number of pages in a booklet (also known as signature)")
    args = parser.parse_args()

    if args.pages == 0 or (args.pages % 4) != 0:
        print("Error: number of pages in a booklet must be divisible by 4, since there are 4 pages in a sheet (front and back)")
        exit(1)

    if args.output is None and sys.stdout.isatty():
        print(f"Error: printing binary data to terminal. Either redirect it or use an output file.", file=sys.stderr)
        exit(1)

    return args
 
def main() -> None:
    args = parse_args()

    logging.info(f"input file: '{args.pdf}'")
    logging.info(f"output file: '{args.output if args.output is not None else 'sys.stdout.buffer'}'")

    # Read input pdf
    input_pdf = PdfReader(args.pdf)
    logging.info(f"pages: {len(input_pdf.pages)}")

    with_blank = PdfWriter()
    for page in input_pdf.pages:
        with_blank.add_page(page)

    # Add blank pages
    blank_page_indices = [idx + val for idx, val in enumerate(args.add_blank)]
    logging.info(f"blank page indices: {blank_page_indices}")
    for idx in blank_page_indices:
        with_blank.insert_blank_page(index=idx)

    # Check number of pages are correct
    num_pages = len(with_blank.pages)
    pages_per_booklet = args.pages
    num_booklets = num_pages / pages_per_booklet
    if not num_booklets.is_integer():
        print(f"Error: the number of pages is not a multiple of the number of pages in a booklet")
        print(f"num_pages/pages_in_booklet = {len(with_blank.pages) / args.pages}")
        exit(1)

    # Reorganize pages into booklet order
    booklet_pages_idx = list(range(pages_per_booklet))
    lower_indices = booklet_pages_idx[0:pages_per_booklet//2]
    upper_indices = booklet_pages_idx[-1:pages_per_booklet//2-1:-1]
    output_pdf = PdfWriter()
    for i in range(int(num_booklets)):
        logging.debug("booklet: ", i)
        for page_1, page_2 in zip(upper_indices, lower_indices):
            # logging.debug("page: ", i*pages_per_booklet + page_1, i*pages_per_booklet + page_2)
            print("page: ", i*pages_per_booklet + page_1, i*pages_per_booklet + page_2)
            output_pdf.add_page(with_blank.pages[i*pages_per_booklet + page_1])
            output_pdf.add_page(with_blank.pages[i*pages_per_booklet + page_2])
        logging.debug("---")


    # Save output pdf
    if args.output is not None:
        with open(args.output, "bw") as output:
            output_pdf.write(output)
    # else:
    #     output_pdf.write(sys.stdout.buffer)


if __name__ == "__main__":
    main()
