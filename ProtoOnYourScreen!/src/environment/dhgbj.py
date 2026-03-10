import sys
import PyQt6.QtWidgets
import PyQt6.QtCore
import PyQt6.QtGui


class app(PyQt6.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def getGem(self, name):
        a = {
            "window_width": self.width(),
            "window_height": self.height(),
            "widthSCR": self.screen().size().width(),
            "heightSCR": self.screen().size().height()
        }
        return a[name]

    def initUI(self):
        # БезРамки, ПоверхВсего, БезИконки
        self.setWindowFlags(PyQt6.QtCore.Qt.WindowType.FramelessWindowHint |
                            PyQt6.QtCore.Qt.WindowType.WindowStaysOnTopHint |
                            PyQt6.QtCore.Qt.WindowType.Tool)
        self.setAttribute(PyQt6.QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        w, h = 600, 400
        self.setGeometry((self.getGem("widthSCR") - w),
                         (self.getGem("heightSCR") // 2 - (h // 2)), w, h)
        self.setWindowTitle('app')

    def newSquare(self, Artist, r, g, b, x, y, w, h, a=255):
        Artist.setPen(PyQt6.QtCore.Qt.PenStyle.NoPen)
        Artist.setBrush(
            PyQt6.QtGui.QBrush(
                PyQt6.QtGui.QColor(r, g, b, a)))
        Artist.drawRect(x, y, w, h)

    def newText(self, Artist, text, x, y, r=0, g=0, b=0, font_size=12,
                font_family="Arial", italic=False, underline=False, bold=False):
        Artist.setPen(PyQt6.QtGui.QColor(r, g, b))
        font = PyQt6.QtGui.QFont(font_family, font_size)
        font.setItalic(italic)
        font.setUnderline(underline)
        font.setBold(bold)
        Artist.setFont(font)
        Artist.drawText(x, y, text)

    def addBlurredRect(self, painter, r, g, b, x, y, w, h, a=255, blur=10):
        # Создаем временный виджет для применения эффекта размытия
        temp_widget = PyQt6.QtWidgets.QWidget()
        temp_widget.resize(w + blur * 4, h + blur * 4)
        temp_widget.setAttribute(PyQt6.QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # Создаем сцену и виджет для рендеринга
        temp_scene = PyQt6.QtWidgets.QGraphicsScene(0, 0, w + blur * 4, h + blur * 4)
        temp_view = PyQt6.QtWidgets.QGraphicsView(temp_scene)
        temp_view.setParent(temp_widget)
        temp_view.setGeometry(0, 0, w + blur * 4, h + blur * 4)
        temp_view.setStyleSheet("background: transparent; border: none;")

        # Создаем прямоугольник с размытием
        rect_item = PyQt6.QtWidgets.QGraphicsRectItem(blur * 2, blur * 2, w, h)
        rect_item.setBrush(PyQt6.QtGui.QBrush(PyQt6.QtGui.QColor(r, g, b, a)))
        rect_item.setPen(PyQt6.QtGui.QPen(PyQt6.QtCore.Qt.PenStyle.NoPen))

        # Применяем эффект размытия
        if blur > 0:
            blur_effect = PyQt6.QtWidgets.QGraphicsBlurEffect()
            blur_effect.setBlurRadius(blur)
            rect_item.setGraphicsEffect(blur_effect)

        temp_scene.addItem(rect_item)

        # Рендерим виджет в pixmap
        temp_pixmap = PyQt6.QtGui.QPixmap(temp_widget.size())
        temp_pixmap.fill(PyQt6.QtCore.Qt.GlobalColor.transparent)

        temp_widget.render(temp_pixmap, PyQt6.QtCore.QPoint(0, 0))

        # Рисуем размытый прямоугольник
        painter.drawPixmap(x - blur * 2, y - blur * 2, temp_pixmap)

    def paintEvent(self, event):
        Artist = PyQt6.QtGui.QPainter(self)
        Artist.setRenderHint(PyQt6.QtGui.QPainter.RenderHint.Antialiasing)

        self.newSquare(Artist, 255, 0, 0, 10, 10, 50, 50)
        self.newSquare(Artist, 0, 0, 255, (self.getGem("window_width") - 60),
                       (self.getGem("window_height") - 60), 50, 50)
        self.newText(Artist, 'lorem ipsum', 30, 30, 255, 255, 255)
        self.newSquare(Artist, 0, 0, 0, 0, 0, 600, 400, 100)

        # Тестируем размытый прямоугольник
        self.addBlurredRect(Artist, 255, 0, 0, 10, 10, 50, 50, 255, 15)

        Artist.end()


if __name__ == "__main__":
    base = PyQt6.QtWidgets.QApplication(sys.argv)
    window = app()
    window.show()
    sys.exit(base.exec())