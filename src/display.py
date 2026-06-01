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

    def nextPage(self):
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

    def showPage(self, page):
        page.render(self)


class Page:
    def __init__(self, title=""):
        self.title = title
        self.lines = []

    def setLines(self, lines):
        self.lines = lines

    def render(self, display):
        display.ssd1306.fill(0)

        display.ssd1306.text(self.title, 0, 0)

        for i, line in enumerate(self.lines):
            display.ssd1306.text(str(line), 0, (i + 2) * 8)

        display.ssd1306.show()

