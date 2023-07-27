import os
import sys

if __name__ == '__main__':
    os.system(f"pyrcc5 ../src_img/my_qrc.qrc -o my_qrc_rc.py")

    uis = ['notice_board', 'todo_list', 'admin_todo_check', 'admin_todo_edit_dialog',
           'category_list', 'message_label_left', 'message_label_right',
           'notice_widget', 'profile_dialog', 'Warning_dialog', 'notice_dialog']
    for ui in uis:
        os.system(f'python  -m PyQt5.uic.pyuic --import-from=main_code.front.ui -x {ui}.ui -o ui_class_{ui}.py')
    print('컴파일 완료!')