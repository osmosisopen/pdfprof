from pypdf import PdfReader, PdfWriter


class Converter:
    def __init__(self, filename):
        self.reader = PdfReader(filename)

    def is_encrypted(self):
        return self.reader.is_encrypted

    def convert_protected_pdf(self, enc_pdf_filename, password):
        try:
            self.reader.decrypt(str(password))
            # else:
            #     page = reader.pages[0]
            #     count = 0

            #     for image_file_object in page.images:
            #         with open(str(count) + image_file_object.name, "wb") as fp:
            #             fp.write(image_file_object.data)
            #             count += 1

                # if extracted_text := page.extract_text():
                #     print(extracted_text)
                # else:
                #     message = "No extracted text"
                #     message_and_raise(message)

        except Exception as e:
            raise e

        try:
            writer = PdfWriter(clone_from=self.reader)
            # Save the new PDF to a file
            with open("decrypted-pdf.pdf", "wb") as f:
                writer.write(f)

            sg.popup("Decryption successful.")
        except Exception as e:
            print(f"Failed to decrypt {enc_pdf_filename}")
            raise e

