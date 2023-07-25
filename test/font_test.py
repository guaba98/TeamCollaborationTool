from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
class FontLoader:
    def __init__(self, font_path):
        self.font_id = QFontDatabase.addApplicationFont(font_path)
        if self.font_id == -1:
            print(f'폰트 경로를 가져오는데 실패: {font_path}')
        else:
            self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
            print('폰트 페밀리', self.font_family)

    def get_font(self, size=12):
        if self.font_id == -1 or not self.font_family:
            print('폰트가 로드되지 않았습니다.')
            return QFont()
        else:
            return QFont(self.font_family, size)



class FontManager:
    def __init__(self):
        self.fonts = {}

    def load_font(self, name, path):
        self.fonts[name] = FontLoader(path)

    def get_font(self, name, size=12):
        if name in self.fonts:

            print(name, self.fonts[name])
            return self.fonts[name].get_font(size)
        else:
            print(f'{name} 폰트가 로드되지 않았습니다.')
            return QFont()



# PyQt Application 생성
app = QApplication([])


# 폰트 로더 생성
font_manager = FontManager()
font_manager.load_font('nanum_light', '../code/front/font/NanumSquareNeo-aLt.ttf')
font_manager.load_font('nanum_regular', '../code/front/font/NanumSquareNeo-bRg.ttf')
font_manager.load_font('nanum_bold', '../code/front/font/NanumSquareNeo-cBd.ttf')
font_manager.load_font('nanum_extrabold', '../code/front/font/NanumSquareNeo-dEb.ttf')
font_manager.load_font('nanum_heavy', '../code/front/font/NanumSquareNeo-eHv.ttf')


# ... 나머지 폰트들도 동일하게 로드합니다.

# 라벨과 버튼 생성 및 폰트 설정
label = QLabel('Hello, World!')
label.setFont(font_manager.get_font('nanum_bold', size=16))

button = QPushButton('Click me')
button.setFont(font_manager.get_font('nanum_bold', size=20))



# 위젯 배치를 위한 레이아웃 생성
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)

# 위젯 생성 및 레이아웃 설정
widget = QWidget()
widget.setLayout(layout)

widget.show()

# PyQt 이벤트 루프 실행
app.exec_()



# from PyQt5.QtGui import QFontDatabase, QFont
# from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
#
# class FontLoader:
#     def __init__(self, font_path):
#         self.font_id = QFontDatabase.addApplicationFont(font_path)
#         if self.font_id == -1:
#             print(f'Failed to load font at path: {font_path}')
#         else:
#             self.font_families = QFontDatabase.applicationFontFamilies(self.font_id)
#             print(font_path)
#     def get_font(self, family_index=0, size=12):
#         if self.font_id == -1 or not self.font_families:
#             print('No font loaded')
#             return QFont()
#         else:
#             return QFont(self.font_families[family_index], size)
#
#
# # PyQt Application 생성
# app = QApplication([])
#
# # 폰트 로더 생성
# font_loader1 = FontLoader('../code/front/font/NanumSquareNeo-cBd.ttf')
# font_loader = FontLoader('../code/front/font/NanumSquareNeo-eHv.ttf')
#
# # 라벨과 버튼 생성 및 폰트 설정
# label = QLabel('Hello, World!')
# label.setFont(font_loader1.get_font(family_index=0, size=16))
#
# button = QPushButton('Click me')
# button.setFont(font_loader1.get_font(family_index=0, size=14))
#
# # 위젯 배치를 위한 레이아웃 생성
# layout = QVBoxLayout()
# layout.addWidget(label)
# layout.addWidget(button)
#
# # 위젯 생성 및 레이아웃 설정
# widget = QWidget()
# widget.setLayout(layout)
#
# widget.show()
#
# # PyQt 이벤트 루프 실행
# app.exec_()
