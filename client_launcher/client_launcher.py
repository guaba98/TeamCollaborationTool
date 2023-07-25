import sys
import time

from PyQt5.QtWidgets import QApplication

from class_client.class_client import ClientApp
# from code.front.asdasffsa import ClientController
# from common.common_module import *
from code.front.client_controller import ClientController


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_object = ClientApp()
    client_controller = ClientController(client_object)
    client_controller.run()
    # sys.excepthook = lambda exctype, value, traceback: show_error_message(str(value), traceback)
    sys.exit(app.exec_())

