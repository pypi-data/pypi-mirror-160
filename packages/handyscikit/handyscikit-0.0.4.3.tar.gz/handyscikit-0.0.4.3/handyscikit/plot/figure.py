from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import os


def hasChinese(input_str):
    for char in input_str:
        if "\u4e00" <= char <= u"\u9fff": return True


class FigureBase:
    def __init__(self):
        self._base_data = None
        self._font_size = 10
        file_path = os.path.abspath(__file__)[:-9] + "simsun.ttc"
        self._font_dict = {"SongTi" : FontProperties(fname=file_path, size=self._font_size),
                           "TimesNewRoman" : FontProperties(family="Times New Roman", size=self._font_size)}
        # Make plt canvas.
        plt.figure()

    def _choose_font(self, text):
        if hasChinese(text):
            return self._font_dict["SongTi"]
        else:
            return self._font_dict["TimesNewRoman"]


class Figure(FigureBase):
    def __init__(self):
        FigureBase.__init__(self)

    def add_line_data(self, data):
        """
        One line each time.
        :param data:
        :return:
        """
        plt.plot(self._base_data, data)

    def save(self, filename="unknown", dpi=1000):
        self._mpl_figure.saveFig(filename, dpi=dpi)

    def set_base_data(self, base_data):
        self._base_data = base_data

    def set_title(self, title):
        plt.title(title, fontproperties=self._choose_font(title))

    def set_x_label(self, text):
        plt.xlabel(text, fontproperties=self._choose_font(text))

    def set_x_limit(self, range):
        # todo: Waiting...
        pass

    def set_y_label(self, text):
        plt.ylabel(text, fontproperties=self._choose_font(text))

    def set_y_limit(self, range):
        # todo: Waiting...
        pass

    def show(self):
        plt.show()