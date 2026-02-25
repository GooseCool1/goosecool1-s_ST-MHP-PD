import sys, asyncio, PyQt6.QtWidgets, PyQt6.QtCore, PyQt6.QtGui
class app(PyQt6.QtWidgets.QWidget):
    def __init__(self): super().__init__(); self.initUI()
    def getGem(self, name):
        a = {
            "window_width":self.width(),
            "window_height":self.height(),
            "widthSCR":self.screen().size().width(),
            "heightSCR":self.screen().size().height()
        };return a[name]
    def initUI(self):
        # БезРамки, ПоверхВсего, БезИконки
        self.setWindowFlags(PyQt6.QtCore.Qt.WindowType.FramelessWindowHint | PyQt6.QtCore.Qt.WindowType.WindowStaysOnTopHint | PyQt6.QtCore.Qt.WindowType.Tool)
        self.setAttribute(PyQt6.QtCore.Qt.WidgetAttribute.WA_TranslucentBackground); w, h = 600, 400
        self.setGeometry((self.getGem("widthSCR") - w), (self.getGem("heightSCR") // 2 - (h // 2)), w, h)
        self.scene = PyQt6.QtWidgets.QGraphicsScene()
        self.view = PyQt6.QtWidgets.QGraphicsView(self.scene)
        self.view.setStyleSheet("background: transparent; border: none;")
        self.view.setGeometry(0, 0, w, h)
        layout = PyQt6.QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.setWindowTitle('app')
    def newSquare(self, Artist, r, g, b, x, y, w, h, a=255):
        Artist.setPen(PyQt6.QtCore.Qt.PenStyle.NoPen)
        Artist.setBrush(
            PyQt6.QtGui.QBrush(
                PyQt6.QtGui.QColor(r, g, b, a)))
        Artist.drawRect(x, y, w, h)
    def newText(self, Artist, text, x, y, r=0, g=0, b=0, font_size=12, font_family="Arial", italic=False, underline=False, bold=False):
        Artist.setPen(PyQt6.QtGui.QColor(r, g, b))
        font = PyQt6.QtGui.QFont(font_family, font_size)
        font.setItalic(italic)
        font.setUnderline(underline)
        font.setBold(bold)
        Artist.setFont(font)
        Artist.drawText(x, y, text)
    def blurForPix(self, pixmap, radius):
        s=PyQt6.QtWidgets.QGraphicsScene()
        s.addItem(PyQt6.QtWidgets.QGraphicsPixmapItem(
            pixmap ).setGraphicsEffect(PyQt6.QtWidgets.QGraphicsBlurEffect().setBlurRadius(
            radius ) ))
        s.renderQPainter(PyQt6.QtGui.QPixmap(pixmap.size()).fill(PyQt6.QtCore.Qt.GlobalColor.transparent))
    def blurSquare(self, x, y, w, h, blur=15):
        self.scene.addItem(square:= PyQt6.QtWidgets.QGraphicsPixmapItem(
            self.blurForPix(
                self.grab(
                    PyQt6.QtCore.QRect(x, y, w, h)),
                    blur
                )).setPos(x, y)); return square
    def paintEvent(self, event):
        Artist= PyQt6.QtGui.QPainter(self)
        Artist.setRenderHint(PyQt6.QtGui.QPainter.RenderHint.Antialiasing )

        #self.newSquare(Artist, 0, 0, 0, 0, 0, 600, 400, 127, 10)
        self.newSquare(Artist, 255, 0, 0, 10, 10, 50, 50)
        self.newSquare(Artist, 0, 0, 255, (self.getGem("window_width") - 60), (self.getGem("window_height") - 60), 50, 50)
        self.newText(Artist, 'lorem ipsum', 30, 30, 255, 255, 255)
        self.newSquare(Artist, 0, 0, 0, 0, 0, 600, 400, 100)
        self.blurSquare(0, 0, 0,0, 0, 600, 400)

        Artist.end()

if __name__ == "__main__":
    base= PyQt6.QtWidgets.QApplication(sys.argv)
    window= app()
    window.show()
    sys.exit(base.exec())