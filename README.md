# extract-info-from-pdf-paper
This Python script uses pdfminer.six, PyPDF2, pdf2image to extract information (text, image) from pdf paper. 


### Install dependencies
```
pip3 install -r requirementx.txt
```

### How to Run
```plaintext
python3 extract-text-image.py
```
Check out output folder for the result of extraction of this script.

### Note
Change the input and output file path in the Python script.
```python
pdf_path = "2305.02301.pdf"
out_text_path = "output/2305.02301.txt" 
```

### TODO: extract latex
- [ ] 1. extract latex formula image
- [ ] 2. use LaTeX-OCR for convert latex formula image to latex
- [ ] 3. replace the plaintext formula in result with $$ latex $$

### TODO: extract table

