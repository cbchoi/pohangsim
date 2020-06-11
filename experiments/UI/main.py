import sys #getopt
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *

from main_window import MSWSsimulator
#from family_dialog import FamilyTypeManager

app = QApplication(sys.argv)

ui_file = QFile("../../PohangSim.ui")
loader = QUiLoader()
window = loader.load(ui_file)
ui_file.close()
pohangMSWS = MSWSsimulator(window)
pohangMSWS.show()
sys.exit(app.exec_())
"""
def main(argv):

    #FILE_NAME     = argv[0] # command line arguments의 첫번째는 파일명
    INSTANCE_NAME = ""      # 인스턴스명 초기화
    CHANNEL_NAME  = ""      # 채널명 초기화

    try:
        # opts: getopt 옵션에 따라 파싱 ex) [('-i', 'myinstancce1')]
        # etc_args: getopt 옵션 이외에 입력된 일반 Argument
        # argv 첫번째(index:0)는 파일명, 두번째(index:1)부터 Arguments
        opts, etc_args = getopt.getopt(argv[1:], \
                                 "hat", ["help","app","telegram"])

    except getopt.GetoptError: # 옵션지정이 올바르지 않은 경우
        print(FILE_NAME, '-i <instance name> -c <channel name>')
        sys.exit(2)

    for opt, arg in opts: # 옵션이 파싱된 경우
        if opt in ("-h", "--help"): # HELP 요청인 경우 사용법 출력
            print(FILE_NAME, '-i <instance name> -c <channel name>')
            sys.exit()

        elif opt in ("-a", "--app"): # 인스턴명 입력인 경우
            app = QApplication(sys.argv)

            ui_file = QFile("../../PohangSim.ui")
            loader = QUiLoader()
            window = loader.load(ui_file)
            ui_file.close()
            pohangMSWS = MSWSsimulator(window)
            pohangMSWS.show()
            sys.exit(app.exec_())

        elif opt in ("-t", "--telegram"): # 채널명 입력인 경우
            telegram_bot.main()

    if len(INSTANCE_NAME) < 1: # 필수항목 값이 비어있다면
        print(FILE_NAME, "-a or -t option is mandatory") # 필수임을 출력
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv)
"""
