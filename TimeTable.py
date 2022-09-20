from importBot import req, p2i, os, t


class TimeTable:
    url: str
    nb_pages: int = 0
    expentionImage: t.List[str] = ['jpg', 'JPEG']

    def __init__(self, url: str) -> None:
        self.url = url
        # Download image
        self.__download__()
        # Convert pdf to image
        self.__convert__()

    def __download__(self) -> None:
        # Send GET request
        response = req.get(self.url)
        # Save the PDF
        if response.status_code == 200:
            with open('file.pdf', 'wb') as f:
                f.write(response.content)
        else:
            print(response.status_code)

    def __convert__(self) -> None:
        # Convert PDF to PNG
        pages = p2i.convert_from_path('file.pdf')
        # Save the image
        self.nb_pages = len(pages)
        for page in pages:
            pageName = 'file' + str(pages.index(page)) + self.expentionImage[0]
            page.save(pageName, self.expentionImage[1])

    def __del__(self):
        # Delete image
        os.remove('file.pdf')
        for i in range(self.nb_pages):
            os.remove('file' + str(i) + self.expentionImage[0])

    def __update__(self) -> None:
        # Delete last
        self.__del__()
        # Download pdf
        self.__download__()
        # Convert pdf to image
        self.__convert__()


if __name__ == "__main__":
    timetable = TimeTable(url="http://chronos.iut-velizy.uvsq.fr/EDT/g37478.pdf")
