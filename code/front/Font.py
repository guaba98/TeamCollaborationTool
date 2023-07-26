from PyQt5.QtGui import QFont

class Font:
    @staticmethod
    def title(t_size=1):
        font = QFont()
        #
        if t_size == 1:
            font.setPointSize(35)
        elif t_size == 2:
            font.setPointSize(25)
        elif t_size == 3:
            font.setPointSize(15)
        elif t_size == 5:
            font.setPointSize(10)

        font.setFamily("나눔스퀘어 네오 ExtraBold")
        return font

    @staticmethod
    def button(t_size=1):
        font = QFont()
        if t_size == 1:
            font.setPointSize(12)
        elif t_size == 2:
            font.setPointSize(11)
        elif t_size == 3:
            font.setPointSize(10)
        elif t_size == 4:
            font.setPointSize(9)
        elif t_size == 5:
            font.setPointSize(8)
        elif t_size == 6:
            font.setPointSize(15)

        font.setFamily("나눔스퀘어 네오 Bold")
        return font

    @staticmethod
    def text(t_size=1, t_blod=True):
        font = QFont()
        if t_size == 1:
            font.setPointSize(12)
        elif t_size == 2:
            font.setPointSize(11)
        elif t_size == 3:
            font.setPointSize(10)
        elif t_size == 4:
            font.setPointSize(9)
        elif t_size == 5:
            font.setPointSize(8)

        if t_blod:
            font.setFamily("나눔스퀘어 네오 Bold")
        else:
            font.setFamily("나눔스퀘어 네오 Regular")

        return font
    @staticmethod
    def contents(t_size=1, t_blod=True):
        font = QFont()
        if t_size == 1:
            font.setPointSize(12)
        elif t_size == 2:
            font.setPointSize(11)
        elif t_size == 3:
            font.setPointSize(10)
        elif t_size == 4:
            font.setPointSize(9)
        elif t_size == 5:
            font.setPointSize(8)

        if t_blod:
            font.setFamily("나눔스퀘어 네오 Regular")
        else:
            font.setFamily("나눔스퀘어 네오 Light")

        return font