from util import Doc
import argparse


def main():
    doc = Doc(doc_id="5dcaff517ee6318db01361a6ef548291", filename="HarryPotter.pdf")
    doc.extract_pdf()
    doc.build_index()


if __name__ == "__main__":
    main()