import sys
import time

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont


from class_client.class_client import ClientApp
from code.front.client_controller import ClientController

def main():
    app = QApplication(sys.argv)
    # app.setStyle("Fusion")

    # 폰트
    fontDB = QFontDatabase()
    fontDB.addApplicationFont("../code/front/font/NanumSquareNeo-aLt.ttf")
    fontDB.addApplicationFont("../code/front/font/NanumSquareNeo-bRg.ttf")
    fontDB.addApplicationFont("../code/front/font/NanumSquareNeo-cBd.ttf")
    fontDB.addApplicationFont("../code/front/font/NanumSquareNeo-dEb.ttf")
    fontDB.addApplicationFont("../code/front/font/NanumSquareNeo-eHv.ttf")

    client_object = ClientApp()
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



