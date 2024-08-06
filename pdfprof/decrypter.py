import os

from pdfprof.gui_utils import GuiUitils
from pdfprof.pdf_processor import PdfProcessor


class Decrypter:
    def __init__(self, filename):
        self.filename = filename
        self.doc = PdfProcessor(filename).get_doc()

    def decrypt_protected_pdf(self, password, decrypt_filename):
        auth: int = self.doc.authenticate(password)
        if auth == 0:
            raise ValueError("Authentication failed")

        target_path = os.path.dirname(self.doc.name)

        # decrypt_filename = (decrypt_filename or "decrypted.pdf").rstrip(".pdf") + ".pdf"
        suffix = ".pdf"
        decrypt_filename = (decrypt_filename or f"decrypted{suffix}")
        modified_filename = (
            decrypt_filename[: -len(suffix)]
            if decrypt_filename.endswith(suffix)
            else decrypt_filename
        ) + suffix

        self.doc.save(os.path.join(target_path, modified_filename))

        GuiUitils().popup("Decrypted Successfully")
