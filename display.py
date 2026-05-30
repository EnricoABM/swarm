from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
import framebuf 

class Display:
    def __init__(self, sda, scl):
        self.ssd1306 = display = SSD1306_I2C(128, 64, I2C(0, sda=Pin(sda), scl=Pin(scl)))
        self.pages = []
        self.pagesIndex = 0

    def addPage(self, page):
        if page not in self.pages:
            self.pages.append(page)

    def removePage(self, page):
        if page in self.pages:
            self.pages.remove(page)

    def nextPage(self, _):
        pagesSize = len(self.pages)

        if self.pagesIndex < pagesSize - 1:
            self.pagesIndex += 1
        elif self.pagesIndex >= pagesSize - 1:
            self.pagesIndex = 0

        return self.pages[self.pagesIndex]

    def previousPage(self):
        pagesSize = len(self.pages)

        if self.pagesIndex <= 0:
            self.pagesIndex = pagesSize - 1
        else:
            self.pagesIndex -= 1
        
        return self.pages[self.pagesIndex]

    def getCurrentPage(self):
        return self.pages[self.pagesIndex]

    def show(self, page):
        self.ssd1306.fill(0)
        self.ssd1306.text(page.message(), 0, 0, 1)
        self.ssd1306.show()

    def showImage(self):
        
        buffer = bytearray(b'\xff\xff\xff\xff\xff\xff\xff\x7f\xbf\x9f\xe7\xf9~\xb79\xf0\xf8\xf8\xfc\xfe\xdf\xa7y\xfe\xff\xff\xff\xff\xff?\xdf\xdff\xf9\xff\xff?\xdf\xecq\xf9\xfe}~\xbf\xbf\xbf\xdf\xefoo\x7f\xff\xff\xfe\xf9\x87\x7f\xff\xff\xff\x1f\xfe\xf9\xf8\xe7\xdf\xdf\xdf\xbe\xbdxyv\xf4\xf6\xfb\xfd\xfd\xfe\xfe\xfc\x00\xff\xff\xff\xff\xff\xff\xf8\x87wy\xbe\xd1\xef\xff\xff\xff\x7f\x9f\xef\xef\xef\xdf\xdf\xde\xed\xeb\xf3\xf1\xe1\xe00\xfc\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xf8\xe7\xdf?')        
        self.ssd1306.fill(0)
        self.showBufferImage(buffer, 32, 32, 32, 0)
        self.ssd1306.show()


class Page:
    def __init__(self, label="", value=0, prefix="", sufix=""):
        self.label = label
        self.value = value
        self.prefix = prefix
        self.sufix = sufix

    def updateValue(self, value):
        self.value = value

    def message(self):
        return f"{self.label}: {self.prefix} {self.value:.2f} {self.sufix}"


