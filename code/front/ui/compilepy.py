import os
import sys

if __name__ == '__main__':
    os.system(f"pyrcc5 ../src_img/my_qrc.qrc -o my_qrc_rc.py")

    uis = ['notice_board', 'todo_list']
    for ui in uis:
        os.system(f'python  -m PyQt5.uic.pyuic --import-from=code.front.ui -x {ui}.ui -o ui_class_{ui}.py')
