import PyPDF2

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTFigure

from pdf2image import convert_from_path

""" input and output file paths"""
pdf_path = "2305.02301.pdf"
out_text_path = "output/2305.02301.txt"


def simple_text_extraction(element):
    line_text = element.get_text()
    return line_text


def crop_image(element, pageObj):
    [image_left, image_top, image_right, image_bottom] = [
        element.x0,
        element.y0,
        element.x1,
        element.y1,
    ]
    pageObj.mediabox.lower_left = (image_left, image_bottom)
    pageObj.mediabox.upper_right = (image_right, image_top)
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(pageObj)
    with open("output/cropped_image.pdf", "wb") as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)


def convert_to_images(input_file, output_file):
    images = convert_from_path(input_file)
    image = images[0]
    image.save(output_file, "PNG")


if __name__ == "__main__":
    with open(pdf_path, "rb") as pdf_file_obj:
        pdf_file_reader = PyPDF2.PdfReader(pdf_file_obj)
        total_pages = len(pdf_file_reader.pages)
        print(f"Total pages in {pdf_path}: {total_pages}")

        text_per_page = {}
        image_index = 0

        for page_num, page in enumerate(extract_pages(pdf_path)):
            page_obj = pdf_file_reader.pages[page_num]
            page_content = []

            table_num = 0

            page_elements = [(element.y1, element) for element in page._objs]

            for i, component in enumerate(page_elements):
                element = component[1]

                if isinstance(element, LTTextContainer):
                    line_text = simple_text_extraction(element)
                    page_content.append(line_text)

                if isinstance(element, LTFigure):
                    crop_image(element, page_obj)
                    convert_to_images(
                        "output/cropped_image.pdf", f"output/image-{image_index}-page{page_num+1}.png"
                    )
                    # page_content.append(f'\nimage-{image_index}.png\n')
                    image_index += 1

            dctkey = "Page_" + str(page_num + 1)
            text_per_page[dctkey] = [page_content]

    for i in range(total_pages):
        with open(out_text_path, "a", encoding='utf-8') as f:
            f.write("".join(text_per_page[f"Page_{i+1}"][0]))
