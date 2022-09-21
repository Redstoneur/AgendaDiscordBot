from BOT.importBot import req, os
from PyPDF2 import PdfFileWriter, PdfFileReader


class TimeTable:
    url: str
    nb_pages: int = 4

    def __init__(self, url: str) -> None:
        self.url = url
        # Download image
        self.__download__()
        # Convert pdf to image
        self.__convert__()

    def __download__(self) -> None:
        # self.__defPdf__()
        # Send GET request
        response = req.get(self.url)
        # Save the PDF
        if response.status_code == 200:
            with open('../file.pdf', 'wb') as f:
                f.write(response.content)
        else:
            print(response.status_code)
        f.close()

        inputpdf = PdfFileReader(open("../file.pdf", "rb"))
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(0))
        with open("../TimeTable.pdf", "wb") as outputStream:
            # noinspection PyTypeChecker
            output.write(outputStream)
        outputStream.close()

    def __convert__(self) -> None:
        # Convert pdf to image (png)
        # todo: convert pdf to image (png)
        pass

    def __delFile__(self):
        # Delete pdf
        self.__defPdf__()
        # Delete images
        self.__delImages__()

    # noinspection PyMethodMayBeStatic
    def __defPdf__(self, select: int = 0) -> None:
        if select not in [0, 1, 2]:
            select = 0
        if os.path.exists('../file.pdf') and select in [0, 1]:
            os.remove('../file.pdf')
        if os.path.exists('../TimeTable.pdf') and select in [0, 2]:
            os.remove('../TimeTable.pdf')

    def __delImages__(self) -> None:
        for i in range(self.nb_pages):
            if os.path.exists(f'save_{i}.png'):
                os.remove(f'save_{i}.png')

    def __update__(self) -> None:
        # Delete last
        # self.__delFile__()
        # Download pdf
        self.__download__()
        # Convert pdf to image
        self.__convert__()


if __name__ == "__main__":
    timetable = TimeTable(url="http://chronos.iut-velizy.uvsq.fr/EDT/g37478.pdf")
