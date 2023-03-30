from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide2.QtWidgets import (QApplication, QGraphicsView, QGridLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QWidget)

class Ui_SavorSense(object):
    def setupUi(self, SavorSense):
        if not SavorSense.objectName():
            SavorSense.setObjectName(u"SavorSense")
        SavorSense.resize(800, 620)
        self.centralwidget = QWidget(SavorSense)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.image_label = QLabel(self.centralwidget)
        self.image_label.setObjectName(u"image_label")

        self.gridLayout.addWidget(self.image_label, 0, 0, 1, 2)

        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout.addWidget(self.graphicsView, 1, 0, 1, 3)

        self.nir_label = QLabel(self.centralwidget)
        self.nir_label.setObjectName(u"nir_label")

        self.gridLayout.addWidget(self.nir_label, 2, 0, 1, 1)

        self.mmWave_label = QLabel(self.centralwidget)
        self.mmWave_label.setObjectName(u"mmWave_label")

        self.gridLayout.addWidget(self.mmWave_label, 3, 0, 1, 2)

        self.mmwave_v = QLineEdit(self.centralwidget)
        self.mmwave_v.setObjectName(u"mmwave_v")

        self.gridLayout.addWidget(self.mmwave_v, 3, 2, 1, 1)

        self.start = QPushButton(self.centralwidget)
        self.start.setObjectName(u"start")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start.sizePolicy().hasHeightForWidth())
        self.start.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.start, 4, 2, 1, 1, Qt.AlignHCenter)

        self.nir_v = QLineEdit(self.centralwidget)
        self.nir_v.setObjectName(u"nir_v")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.nir_v.sizePolicy().hasHeightForWidth())
        self.nir_v.setSizePolicy(sizePolicy1)
        self.nir_v.setReadOnly(True)

        self.gridLayout.addWidget(self.nir_v, 2, 2, 1, 1)

        SavorSense.setCentralWidget(self.centralwidget)

        self.retranslateUi(SavorSense)

        QMetaObject.connectSlotsByName(SavorSense)
    # setupUi

    def retranslateUi(self, SavorSense):
        SavorSense.setWindowTitle(QCoreApplication.translate("SavorSense", u"SavorSense", None))
        self.image_label.setText(QCoreApplication.translate("SavorSense", u"Image", None))
        self.nir_label.setText(QCoreApplication.translate("SavorSense", u"NIR", None))
        self.mmWave_label.setText(QCoreApplication.translate("SavorSense", u"mmwave", None))
        self.start.setText(QCoreApplication.translate("SavorSense", u"START", None))
    # retranslateUi

