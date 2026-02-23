import sys, PyQt6.QtWidgets, PyQt6.QtCore, PyQt6.QtGui
class app(PyQt6.QtWidgets.QMainWindow):
    def __init__(self): super().__init__(); self.initUI()
    def getGem(self, name):
        a = {
            "window_width":self.width(),
            "window_height":self.height(),
            "widthSCR":self.screen().size().width(),
            "heightSCR":self.screen().size().height()
        }
        return a[name]
    def initUI(self):
        # БезРамки, ПоверхВсего, БезИконки
        self.setWindowFlags(PyQt6.QtCore.Qt.WindowType.FramelessWindowHint | PyQt6.QtCore.Qt.WindowType.WindowStaysOnTopHint | PyQt6.QtCore.Qt.WindowType.Tool)
        self.setAttribute(PyQt6.QtCore.Qt.WidgetAttribute.WA_TranslucentBackground); w, h = 600, 400
        self.setGeometry((self.getGem("widthSCR") - w), (self.getGem("heightSCR") // 2 - (h // 2)), w, h)
        self.setWindowTitle('app')
    def newSquare(self, Artist, r, g, b, x, y, w, h):
        Artist.setBrush(
            PyQt6.QtGui.QBrush(
                PyQt6.QtGui.QColor(r, g, b)))
        Artist.drawRect(x, y, w, h)
    def paintEvent(self, event):
        Artist= PyQt6.QtGui.QPainter(self)
        Artist.setRenderHint(PyQt6.QtGui.QPainter.RenderHint.Antialiasing )

        self.newSquare(Artist, 255, 0, 0, 10, 10, 50, 50)

        Artist.setBrush(
            PyQt6.QtGui.QBrush(
                PyQt6.QtGui.QColor(0, 0, 255)))
        Artist.drawRect(
            (self.getGem("window_width") - 60),
            (self.getGem("window_height") - 60),
            50,
            50)

        Artist.end()

if __name__ == "__main__":
    base= PyQt6.QtWidgets.QApplication(sys.argv)
    window= app()
    window.show()
    sys.exit(base.exec())