from smartMirrorManager import *
# Constants
small_fontsize = 12
med_fontsize = 18
large_fontsize = 28
xlarge_fontsize = 48

class Weather(QWidget):
    def __init__(self):
        super(Weather, self).__init__()
        self.initUI()

    def initUI(self):
        font3 = QFont('Helvetica', large_fontsize)

        self.vbox = QVBoxLayout()
        self.tempLabel = QLabel()
        self.tempLabel.setFont(font3)
        self.tempLabel.setText("<font color='white'>Temperature</font>")
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.tempLabel)
        self.hbox.setAlignment(Qt.AlignLeft)
        self.setLayout(self.hbox)