from PyQt6.QtWidgets import QMessageBox, QTextEdit
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtCore import QTimer
from PyQt6 import QtWidgets, QtGui, QtCore
import os, logging, requests
from threading import Thread

flag = 1#全局变量，用来判断是否执行排队

#程序的log配置和开始log
logging.basicConfig(filename='data/log.txt',
                     format = '%(asctime)s - %(message)s',
                     encoding="utf-8",
                     level=logging.INFO) 

def readlog(): #读取log函数
    with open("data/log.txt","r", encoding="utf-8") as f_read:
        #读取数据
        f_read.seek(0)#把读取光标放在文件首
        file = f_read.read()
        return file       

class Ui_Form(object):#主窗体

    def setupUi(self, Form):
        # 步骤1：加载字体文件
        QFontDatabase.addApplicationFont("data/胡晓波男神体.otf")

        # 步骤2：设置样式表
        stylesheet = '''
            QListWidget {
                font-family: 胡晓波男神体;
                font-size: 30px;
                background-image: url('data/BGP.jpg');
                background-position: center;

            }
            
        '''

        # 步骤3：创建应用程序窗口
        Form.setObjectName("AutoQueue")
        Form.resize(260,600)
        Form.setWindowTitle("排队列表v2.8")

        # 步骤4：应用样式表
        Form.setStyleSheet(stylesheet)

        #创建表单标签，设置布局
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.resize(240,400)
        self.listWidget.move(10,10)
        self.listWidget.setSpacing(0)
    
        #创建pushButton标签，设置布局
        self.finish = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.finish.setFont(font)
        self.finish.move(22,420)
        self.finish.resize(100,50)
        self.finish.setText("完成")

        #创建pushButton标签，设置布局
        self.delete = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.delete.setFont(font)
        self.delete.move(138,420)
        self.delete.resize(100,50)
        self.delete.setText("删除")

        #创建pushButton标签，设置布局
        self.trans = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.trans.setFont(font)
        self.trans.move(22,480)
        self.trans.resize(100,50)
        self.trans.setText("移至队尾")

        #创建pushButton标签，设置布局
        self.openlog = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.openlog.setFont(font)
        self.openlog.move(138,480)
        self.openlog.resize(100,50)
        self.openlog.setText("查看log")

        #创建定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_list)
        self.timer.start(2000)

        #暂停排队开关
        self.stopbtn = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.stopbtn.setFont(font)
        self.stopbtn.move(22,540)
        self.stopbtn.resize(100,50)
        self.stopbtn.setText("停止排队")

        #继续排队开关
        self.resumebtn = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.resumebtn.setFont(font)
        self.resumebtn.move(138,540)
        self.resumebtn.resize(100,50)
        self.resumebtn.setText("继续排队")

        #排队状态提示label
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.resize(270,100)
        self.label.move(1,345)
        self.label.setWordWrap(True)
        self.label.setText("要打请发【深渊排队+层数】")

    def update_list(self): #更新list
        current_row = self.listWidget.currentRow()
        self.listWidget.clear()
        with open("data/data.txt","r", encoding="utf-8") as f_read:
            #读取数据
            f_read.seek(0)#把读取光标放在文件首
            files = f_read.readlines()
            line_count = len(files)
            str = [0 for i in range(line_count)]
            i = 0
            while i < line_count:
                    str[i] = files[i].strip('\n')
                    self.listWidget.insertItem(i,str[i])
                    i = i + 1
            self.listWidget.setCurrentRow(current_row)#避免选中的选项在更新后被改变

    def finish_func(self): #完成函数，记录log
        if not os.path.getsize("data/data.txt"):#读取文件的size，若为0则是空文件
            QMessageBox.warning(self.listWidget,"提示","排队列表为空！") #改成弹窗
        else:
            current_row = self.listWidget.currentRow()
            if current_row >= 0:
                self.listWidget.takeItem(current_row)

            with open("data/data.txt", encoding="utf-8") as f:
                lines = f.readlines()
                str = lines[current_row].strip('\n')
                logging.info('完成：' + str)

                del lines[current_row]
            with open("data/data.txt","w", encoding="utf-8") as f_new:
                    f_new.writelines(lines) # 将删除行后的数据写入文件
            self.update_list()

    def delete_func(self): #删除函数，不记录log
        if not os.path.getsize("data/data.txt"):#读取文件的size，若为0则是空文件
            QMessageBox.warning(self.listWidget,"提示","排队列表为空！") #改成弹窗
        else:
            current_row = self.listWidget.currentRow()
            if current_row >= 0:
                self.listWidget.takeItem(current_row)

            with open("data/data.txt", encoding="utf-8") as f:
                lines = f.readlines()
                #str = lines[current_row].strip('\n')
                del lines[current_row]

            with open("data/data.txt","w", encoding="utf-8") as f_new:
                    f_new.writelines(lines) # 将删除行后的数据写入文件
            self.update_list()

    def transfer_func(self):
        if not os.path.getsize("data/data.txt"):#读取文件的size，若为0则是空文件
            QMessageBox.warning(self.listWidget,"提示","排队列表为空！") #改成弹窗
        else:
            current_row = self.listWidget.currentRow()
            with open("data/data.txt","r+", encoding="utf-8") as f:
                lines = f.readlines()
                if lines[-1].strip('\n') != lines[current_row].strip('\n'):
                    str = lines[current_row].strip('\n')
                    del lines[current_row]

                    with open("data/data.txt","w", encoding="utf-8") as f_new:
                        f_new.writelines(lines) # 将删除行后的数据写入文件

                    with open("data/data.txt","a", encoding="utf-8") as f_w:
                        if lines[-1] == '\n':
                            f_w.write(str)
                        else:
                            f_w.write('\n' + str)
                else:
                    pass
            self.listWidget.clear()
            self.update_list()

    def stop_queue(self):
        global flag
        flag = 0
        font = QtGui.QFont()
        font.setPointSize(90)
        self.label.setFont(font)
        self.label.resize(270,300)
        self.label.move(-5,120)
        self.label.setText("暂停排队")

        
    def resume_queue(self):
        global flag
        flag = 1
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.move(1,345)
        self.label.resize(270,100)
        self.label.setText("要打请发【深渊排队+层数】")

class NewWin(object): #新建子窗口
    def setupUi(self,newWin):
        newWin.setObjectName("log查看")
        newWin.resize(400,800)
        newWin.move(1200,50)

        self.btn = QtWidgets.QPushButton(newWin)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btn.setFont(font)
        self.btn.move(10,730)
        self.btn.resize(100,50)
        self.btn.setText("更新log")

        self.logtext = QTextEdit(newWin)
        self.logtext.resize(380,700)
        self.logtext.move(10,10)
        self.logtext.setReadOnly(True)
        self.logtext.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
    
    def update_log(self):#更新log函数
        str = readlog()
        self.logtext.setText(str)

#readtxt():判断排队人是否重复，未重复则写入排队人
def readtxt(str, Abyss_text):   
    with open("data/data.txt","a+", encoding="utf-8") as f_read:
        #读取数据
        f_read.seek(0)#把读取光标放在文件首
        file = f_read.read()
        if str in file:
            pass
        else:
            logging.info('排队：' + str)
            if os.path.getsize("data/data.txt") != 0:
                last_lines = file[-1]
                if last_lines != '\n':#如果文件最后一行不为换行符，则输入前的字符串前加换行符
                    if Abyss_text == "2": 
                        f_read.write('\n' + "12 " + str)
                    if Abyss_text == "9":
                        f_read.write('\n' + "9-12 " + str)
                    if Abyss_text == "0" or Abyss_text == "1":
                        f_read.write('\n' + "1" + Abyss_text + "-12" + str)
                    else:
                        pass
                else:
                    if Abyss_text == "2":
                        f_read.write("12 " + str)
                    if Abyss_text == "9":
                        f_read.write("9-12 " + str)
                    if Abyss_text == "0" or Abyss_text == "1":
                        f_read.write("1" + Abyss_text + "-12" + str)
                    else:
                        pass
            else:
                if Abyss_text == "2":
                        f_read.write("12 " + str + '\n')
                if Abyss_text == "9":
                    f_read.write("9-12 " + str + '\n')
                if Abyss_text == "0" or Abyss_text == "1":
                    f_read.write("1" + Abyss_text + "-12" + str + '\n')
                else:
                    pass

def getname():
    #无限循环
    while True:
        if flag == 1:
            #发送请求，返回值为响应对象
            response = requests.get(url=urltxt, headers=headers)

            #获取相应的json数据
            json_data = response.json()

            #取值：根据冒号左边内容，提取冒号右边内容
            #json字典数据取值只能一层一层取值，不能跨层

            try:#读取弹幕发送人id和弹幕内容，若不存在则抛出异常
                for index1 in json_data['data']['room']:
                    dit1 = {
                        'nickname':index1['nickname']
                    }
                for values in dit1.values():
                    nickname_str = values

                for index2 in json_data['data']['room']:
                    dit2 = {
                        'text':index2['text'],
                    }
                for values in dit2.values():
                    text = values
            except AttributeError:
                pass
            
            main_text = text.replace(" ","")#去掉弹幕中的所有空格
            sub_text = main_text[0:4]
            if sub_text == trigger:#如果弹幕口令与trigger中的内容一致，则调用readtxt函数
                Abyss_text1 = main_text[4]
                if Abyss_text1 == "9":
                    readtxt(nickname_str, Abyss_text1)
                else:
                    Abyss_text2 = main_text[5]
                    readtxt(nickname_str, Abyss_text2)
        else:
            pass

def front_window():
    #窗口组件
    app = QtWidgets.QApplication(sys.argv)
    Form =  QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    
    newWin = QtWidgets.QWidget()
    new_ui = NewWin()
    new_ui.setupUi(newWin)

    ui.finish.clicked.connect(ui.finish_func)
    ui.delete.clicked.connect(ui.delete_func)
    ui.trans.clicked.connect(ui.transfer_func)
    ui.openlog.clicked.connect(newWin.show)
    ui.stopbtn.clicked.connect(ui.stop_queue)
    ui.resumebtn.clicked.connect(ui.resume_queue)
    new_ui.btn.clicked.connect(new_ui.update_log)

    ui.update_list()
    Form.show()
    app.exec()
    os._exit(0) #关闭窗口的同时关闭进程

if __name__ == "__main__": #主函数
    import sys

    #读取直播间的弹幕api
    with open("data/url.txt", "r", encoding='utf-8') as f_url:
        urltxt = f_url.read()

    #模拟浏览器
    headers = {
        'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        'Cookie':"i-wanna-go-back=-1; buvid4=91B06761-31B1-A41C-3B04-AAAB1CF8CDA769412-022123118-EmA0kTcprsj6ZWXuK2Wv0A%3D%3D; rpdid=|(umRYkRJk)Y0J'uY~kR)~|uJ; buvid_fp_plain=undefined; LIVE_BUVID=AUTO8616727502288434; CURRENT_PID=99e6d3f0-cd76-11ed-b276-2b90878e5ca1; FEED_LIVE_VERSION=V8; hit-new-style-dyn=1; header_theme_version=CLOSE; CURRENT_BLACKGAP=0; is-2022-channel=1; enable_web_push=DISABLE; DedeUserID=76763587; DedeUserID__ckMd5=055e8879a4922ba0; CURRENT_QUALITY=80; fingerprint=115213008ff99f892b82568b70fb7b2a; CURRENT_FNVAL=4048; home_feed_column=5; buvid3=9AFCC58D-87CC-F17D-5DFD-8C9D6FF9C98901508infoc; b_nut=1704019103; _uuid=C5B7D5D4-3106B-EDA8-98810-1791C1B156F144946infoc; browser_resolution=1888-1050; hit-dyn-v2=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDQ3MDk5NjIsImlhdCI6MTcwNDQ1MDcwMiwicGx0IjotMX0.O34wNwvhFF6wTmogQiQOWAGCiMAUsIrsXdWzojC60T8; bili_ticket_expires=1704709902; SESSDATA=e4508341%2C1720015758%2C124b2%2A12CjDfKDuvSMJOGrJmkDvdn5Rp8fyWA6YW5ZjjBw8K_hOBYcSwRAag_xM8Bk5BtJYLZ4QSVjFrSm9IUFpoVENIcW5sSlBDaWwwUlBHWnpnUWRfbldMaE5yR1BHQ19NdFVFd2FfenBtSzlhMTdtWWgxS1N0eXkyUV9RWURXXzFWeWlsVHlXU2cydU53IIEC; bili_jct=f790949bab5622fd9c2dae0035d20112; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1703161696,1703769968,1704198750,1704469631; buvid_fp=115213008ff99f892b82568b70fb7b2a; bp_video_offset_76763587=883352898834006057; b_lsid=5471975C_18CDCCCF376; PVID=2; sid=79devmbl; bsource=search_bing"
    }

    #识别弹幕口令
    with open("data/trigger.txt","r", encoding='utf-8') as f_trigger:
        trigger = f_trigger.read()

    #开始运行的log
    logging.info('开始运行')
    t1 = Thread(target=getname)
    t2 = Thread(target=front_window)

    # 启动线程运行
    t2.start()
    t1.start()
    t1.join()
    # 等待所有线程执行完毕
    t2.join()
