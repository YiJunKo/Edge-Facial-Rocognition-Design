import os

from PyQt5 import QtCore, QtWidgets
import cv2
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)
from deepface import DeepFace
from pyModbusTCP.client import ModbusClient
import numpy as np

# Load the cascade
face_cascade_path = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(face_cascade_path)

class Model:
    def __init__(self):
        # 初始化攝像頭捕捉物件、畫面變數和返回值變數
        self.capture = cv2.VideoCapture(0)
        self.frame = None
        self.ret = None

    def get_frame(self):
        # 讀取攝像頭畫面
        self.ret, self.frame = self.capture.read()

    def get_recognition_result(self, image, db_path):
        # 執行人臉辨識
        df = DeepFace.find(
            img_path=image,
            db_path=db_path,
            detector_backend="mtcnn",
            model_name="Facenet",
            distance_metric="euclidean_l2",
            align=True,
            enforce_detection=False,
        )[0]
        return df

    def read_and_convert_image(self, image_path):
        # 讀取圖片並將其轉換為QPixmap
        image = cv2.imread(image_path)
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        qt_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qt_image)


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 680)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser_1 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_1.setGeometry(QtCore.QRect(0, 0, 400, 40))
        self.textBrowser_1.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.textBrowser_1.setObjectName("textBrowser_1")

        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(400, 0, 400, 40))
        self.textBrowser_2.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.textBrowser_2.setObjectName("textBrowser_2")

        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(0, 340, 400, 40))
        self.textBrowser_3.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.textBrowser_3.setObjectName("textBrowser_3")

        self.textBrowser_4 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_4.setGeometry(QtCore.QRect(400, 340, 400, 40))
        self.textBrowser_4.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.textBrowser_4.setObjectName("textBrowser_4")

        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(0, 40, 400, 300))
        self.label_1.setObjectName("label_1")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(400, 40, 400, 300))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 380, 400, 300))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(400, 380, 400, 300))
        self.label_4.setObjectName("label_4")
        self.label_4.setWordWrap(True)

        # Set font size and align the text to center
        font = QFont()
        font.setPointSize(18)
        self.label_4.setFont(font)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textBrowser_1.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">畫面顯示</span></p></body></html>"))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">畫面擷取</span></p></body></html>"))
        self.textBrowser_3.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">相似照片</span></p></body></html>"))
        self.textBrowser_4.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">辨識結果</span></p></body></html>"))

class Controller:
    def __init__(self, model, view, ui):
        self.model = model
        self.view = view
        self.ui = ui

        # 原始影像
        self.original_frame = None

        # ModbusTCP
        self.client = ModbusClient(host="192.168.1.20", port=502, auto_open=True)

        # 使用 QTimer 定時更新畫面
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

        # 使用 QTimer 定時擷取
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.capture_frame)
        self.timer2.start(1000)

    def update_frame(self):
        # 更新攝像頭畫面
        self.model.get_frame()

        self.original_frame = self.model.frame.copy()

        # 將攝像頭畫面轉換為 QImage 格式並顯示在左區域的 QLabel 上
        rgb_image = cv2.cvtColor(self.model.frame, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_image.shape
        bytes_per_line = channel * width
        img = QImage(
            rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888
        )
        self.ui.label_1.setPixmap(QPixmap.fromImage(img))

    def send_person_name_to_server(self, personName):
        # Convert person name to ASCII and then to decimal.
        data_to_send = [int(c) for c in personName]
        # Write to holding registers. You may need to modify this line depending on your server configuration.
        self.client.write_multiple_registers(0, data_to_send)

    def capture_frame(self):
        # 擷取左區域的畫面並執行人臉辨識
        pixmap = self.ui.label_1.grab()
        # scaled 影響長寬比會影響圖像辨識率
        self.ui.label_2.setPixmap(
            pixmap.scaled(
                self.ui.label_2.size(), Qt.AspectRatioMode.KeepAspectRatio
            )
        )

        try:
            image = self.original_frame
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # image = "person7/1.jpg"
        except Exception as e:
            print("Error converting image:", e)

        db_path = "database_2"

        # recognition = self.model.get_recognition_result(image, db_path)
        # if recognition.empty:
        #     print("No matches found in the database.")
        #     # 讀取照片並將其設置到 label_3
        #     pixmap = self.model.read_and_convert_image("none.jpg")
        #     self.ui.label_3.setPixmap(
        #         pixmap.scaled(
        #             self.ui.label_3.size(), Qt.AspectRatioMode.IgnoreAspectRatio
        #         )
        #     )
        #     self.ui.label_4.setText("No matches found in the database.\n\nRecognition result: Failure")
        # else:
        #     print(recognition)
        #     most_similar_face = recognition.iloc[recognition['Facenet_euclidean_l2'].idxmin()]  # 找到最小的 cosine
        #     print(most_similar_face)
        #     # 讀取照片並將其設置到 label_3
        #     pixmap = self.model.read_and_convert_image(most_similar_face['identity'])
        #     self.ui.label_3.setPixmap(
        #         pixmap.scaled(
        #             self.ui.label_3.size(), Qt.AspectRatioMode.IgnoreAspectRatio
        #         )
        #     )
        #     # 設定辨識結果到 label_4
        #     personName = os.path.splitext(os.path.basename(most_similar_face['identity']))[0]  # 只獲取照片名稱
        #     personName = personName.split('_')[0]
        #     self.ui.label_4.setText(f"Most similar photo: {personName}\n\nRecognition result: Successful")
        # Execute face detection first
        faces = face_cascade.detectMultiScale(image, 1.1, 4)

        # If faces are detected, proceed with face recognition
        if len(faces) > 0:
            # 執行人臉辨識並輸出結果
            recognition = self.model.get_recognition_result(image, db_path)
            if recognition.empty:
                print("No matches found in the database.")
                # 讀取照片並將其設置到 label_3
                pixmap = self.model.read_and_convert_image("none.jpg")
                self.ui.label_3.setPixmap(
                    pixmap.scaled(
                        self.ui.label_3.size(), Qt.AspectRatioMode.IgnoreAspectRatio
                    )
                )
                self.ui.label_4.setText("No matches found in the database.\n\nRecognition result: Failure")
            else:
                print(recognition)
                most_similar_face = recognition.iloc[recognition['Facenet_euclidean_l2'].idxmin()]  # 找到最小的 cosine
                print(most_similar_face)
                # 讀取照片並將其設置到 label_3
                pixmap = self.model.read_and_convert_image(most_similar_face['identity'])
                self.ui.label_3.setPixmap(
                    pixmap.scaled(
                        self.ui.label_3.size(), Qt.AspectRatioMode.IgnoreAspectRatio
                    )
                )
                # 設定辨識結果到 label_4
                personName = os.path.splitext(os.path.basename(most_similar_face['identity']))[0]  # 只獲取照片名稱
                # Remove the _1, _2 etc. part
                personName = personName.split('_')[0]
                self.send_person_name_to_server(personName)
                self.ui.label_4.setText(f"Most similar photo: {personName}\n\nRecognition result: Successful")
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    view = QMainWindow()
    model = Model()
    ui = Ui_MainWindow()
    ui.setupUi(view)

    controller = Controller(model, view, ui)

    view.show()
    sys.exit(app.exec_())