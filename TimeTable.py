from importBot import req, p2i, os, t
import time


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
        self.__defPdf__()
        # Send GET request
        response = req.get(self.url)
        # Save the PDF
        if response.status_code == 200:
            with open('file.pdf', 'wb') as f:
                f.write(response.content)
        else:
            print(response.status_code)

    def __convert__(self) -> None:
        pass

    def __del__(self):
        # Delete pdf
        self.__defPdf__()
        # Delete images
        self.__delImages__()

    # noinspection PyMethodMayBeStatic
    def __defPdf__(self) -> None:
        if os.path.exists('file.pdf'):
            os.remove('file.pdf')

    def __delImages__(self) -> None:
        for i in range(self.nb_pages):
            if os.path.exists(f'save_{i}.png'):
                os.remove(f'save_{i}.png')

    def __update__(self) -> None:
        # Delete last
        self.__del__()
        # Download pdf
        self.__download__()
        # Convert pdf to image
        self.__convert__()


if __name__ == "__main__":
    timetable = TimeTable(url="http://chronos.iut-velizy.uvsq.fr/EDT/g37478.pdf")
