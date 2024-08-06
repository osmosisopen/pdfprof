
import pymupdf


class PdfProcessor:
    def __init__(self, filename):
        self.doc = pymupdf.open(filename)

    def get_doc(self):
        return self.doc

    def is_encrypted(self):
        return self.doc.is_encrypted