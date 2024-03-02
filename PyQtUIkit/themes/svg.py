import bs4


class SVG:
    def __init__(self, data):
        self._data = bs4.BeautifulSoup(data, 'xml')

    def change_color(self, color):
        for tag in self._data.find_all(['path', 'circle', 'polygon', 'rect', 'ellipse']):
            tag['fill'] = color
            tag['stroke'] = color

    def set_width(self, width):
        for tag in self._data.find_all('svg'):
            tag['width'] = str(width)

    def set_height(self, height):
        for tag in self._data.find_all('svg'):
            tag['height'] = str(height)

    def resize(self, width, height):
        for tag in self._data.find_all('svg'):
            tag['width'] = str(width)
            tag['height'] = str(height)

    def bytes(self):
        return self._data.encode()
