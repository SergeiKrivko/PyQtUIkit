import bs4


class SVG:
    def __init__(self, data):
        self._data = bs4.BeautifulSoup(data, 'xml')

    def change_color(self, color):
        for tag in self._data.find_all(['path', 'circle', 'polygon', 'rect', 'ellipse']):
            fill, stroke = tag.get('fill'), tag.get('stroke')
            if fill or not stroke:
                tag['fill'] = color
            if stroke:
                tag['stroke'] = color

    def set_width(self, width):
        for tag in self._data.find_all('svg'):
            tag['width'] = str(width)

    def set_height(self, height):
        for tag in self._data.find_all('svg'):
            tag['height'] = str(height)

    def resize(self, width, height, keep_aspect=True):
        view_box = self._data.find('svg').get('viewBox')
        x1, y1, x2, y2 = map(int, view_box.split())
        cur_width = x2 - x1
        cur_height = y2 - y1
        aspect = cur_width / cur_height

        if keep_aspect:
            if width > height * aspect:
                width = int(height * aspect)
            else:
                height = int(width / aspect)

        tag = self._data.find('svg')
        tag['width'] = str(width)
        tag['height'] = str(height)
        return width, height

    def bytes(self):
        return self._data.encode()
