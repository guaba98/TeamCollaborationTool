import sys
import time

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont


from class_client.class_client2 import ClientApp2
from main_code.front.client_controller import ClientController

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # 폰트
    fontDB = QFontDatabase()
    fontDB.addApplicationFont("../main_code/front/font/NanumSquareNeo-aLt.ttf")
    fontDB.addApplicationFont("../main_code/front/font/NanumSquareNeo-bRg.ttf")
    fontDB.addApplicationFont("../main_code/front/font/NanumSquareNeo-cBd.ttf")
    fontDB.addApplicationFont("../main_code/front/font/NanumSquareNeo-dEb.ttf")
    fontDB.addApplicationFont("../main_code/front/font/NanumSquareNeo-eHv.ttf")

    # 폰트 확인용
    available_families = fontDB.families()
    # for family in available_families:
    #     print(family)

    # 그래프 폰트 설정(한글로)
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False


    client_object = ClientApp2()
    client_controller = ClientController(client_object)
    client_controller.run()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



    # sys.excepthook = lambda exctype, value, traceback: show_error_message(str(value), traceback)
    # def show_error_message(message, traceback):
    #     msg_box = QMessageBox()
    #     msg_box.setIcon(QMessageBox.Critical)
    #     msg_box.setWindowTitle("Error")
    #     msg_box.setText(message)
    #     msg_box.exec_()
    #     traceback.print_exc()
    #
    #
    # sys.excepthook = lambda exctype, value, traceback: show_error_message(str(value), traceback)
    # intro.exec_()




