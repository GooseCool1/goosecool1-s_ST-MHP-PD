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
        self.setAttribute(PyQt6.QtCore.Qt.WidgetAttribute.WA_TranslucentBackground); w, h = 300, 150
        self.setGeometry((self.getGem("widthSCR") - w - 50), (self.getGem("heightSCR") // 2 - (h // 2)), w, h)
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
    def addBlurredRect(self, Artist, r, g, b, r2, g2, b2, x, y, w, h, a=255, blur=10):
        tt = PyQt6.QtWidgets.QWidget()
        tt.resize(w + blur * 4, h + blur * 4)
        tt.setAttribute(PyQt6.QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        temp_scene = PyQt6.QtWidgets.QGraphicsScene(0, 0, w + blur * 4, h + blur * 4)
        temp_view = PyQt6.QtWidgets.QGraphicsView(temp_scene)
        temp_view.setParent(tt)
        temp_view.setGeometry(0, 0, w + blur * 4, h + blur * 4)
        temp_view.setStyleSheet("background: transparent; border: none;")
        rect_item = PyQt6.QtWidgets.QGraphicsRectItem(blur * 2, blur * 2, w, h)
        gradient = PyQt6.QtGui.QLinearGradient(blur * 2, blur * 2, blur * 2 + w, blur * 2 + h)
        gradient.setColorAt(0.0, PyQt6.QtGui.QColor(r, g, b, a))
        gradient.setColorAt(1.0, PyQt6.QtGui.QColor(r2, g2, b2, a))
        rect_item.setBrush(PyQt6.QtGui.QBrush(gradient))
        rect_item.setPen(PyQt6.QtGui.QPen(PyQt6.QtCore.Qt.PenStyle.NoPen))
        if blur > 0:
            blur_effect = PyQt6.QtWidgets.QGraphicsBlurEffect()
            blur_effect.setBlurRadius(blur)
            rect_item.setGraphicsEffect(blur_effect)
        temp_scene.addItem(rect_item)
        temp_pixmap = PyQt6.QtGui.QPixmap(tt.size())
        temp_pixmap.fill(PyQt6.QtCore.Qt.GlobalColor.transparent)
        tt.render(temp_pixmap, PyQt6.QtCore.QPoint(0, 0))
        Artist.drawPixmap(x - blur * 2, y - blur * 2, temp_pixmap)

    def addBlurredImage(self, Artist, image_path, x, y, width=None, height=None, opacity=255, blur=0):
        original_pixmap = PyQt6.QtGui.QPixmap(image_path)
        if original_pixmap.isNull(): print(f"Я...извини, но я не могу загрузить эту картинку.. {image_path} [original_pixmap.isNull]"); return
        if width and height:
            pixmap = original_pixmap.scaled(width, height,
                                            PyQt6.QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                                            PyQt6.QtCore.Qt.TransformationMode.SmoothTransformation)
        else:
            pixmap = original_pixmap
            width, height = pixmap.width(), pixmap.height()
        if blur > 0:
            tt = PyQt6.QtWidgets.QWidget()
            tt.resize(width + blur * 4, height + blur * 4)
            tt.setAttribute(PyQt6.QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
            temp_scene = PyQt6.QtWidgets.QGraphicsScene(0, 0, width + blur * 4, height + blur * 4)
            tw = PyQt6.QtWidgets.QGraphicsView(temp_scene)
            tw.setParent(tt)
            tw.setGeometry(0, 0, width + blur * 4, height + blur * 4)
            tw.setStyleSheet("background: transparent; border: none;")
            pixmap_item = PyQt6.QtWidgets.QGraphicsPixmapItem(pixmap)
            pixmap_item.setPos(blur * 2, blur * 2)
            if opacity < 255: pixmap_item.setOpacity(opacity / 255)
            if blur > 0:
                blur_effect = PyQt6.QtWidgets.QGraphicsBlurEffect()
                blur_effect.setBlurRadius(blur)
                pixmap_item.setGraphicsEffect(blur_effect)
            temp_scene.addItem(pixmap_item)
            temp_pixmap = PyQt6.QtGui.QPixmap(tt.size())
            temp_pixmap.fill(PyQt6.QtCore.Qt.GlobalColor.transparent)
            tt.render(temp_pixmap, PyQt6.QtCore.QPoint(0, 0))
            Artist.drawPixmap(x - blur * 2, y - blur * 2, temp_pixmap)
        else:
            if opacity < 255: Artist.setOpacity(opacity / 255)
            Artist.drawPixmap(x, y, pixmap)
            if opacity < 255: Artist.setOpacity(1.0)

    def addPixelImage(self, Artist, image_path, x, y, w, h, opacity=255):
        pixmap = PyQt6.QtGui.QPixmap(image_path)
        if pixmap.isNull(): print(f"Я...извини, но я не могу загрузить эту картинку.. {image_path} [original_pixmap.isNull]"); return
        orig_width, orig_height = pixmap.width(), pixmap.height()
        result = PyQt6.QtGui.QPixmap(w, h)
        result.fill(PyQt6.QtCore.Qt.GlobalColor.transparent)
        tempArtist = PyQt6.QtGui.QPainter(result)
        tempArtist.setRenderHint(PyQt6.QtGui.QPainter.RenderHint.Antialiasing, False)
        tempArtist.setRenderHint(PyQt6.QtGui.QPainter.RenderHint.SmoothPixmapTransform, False)
        pixel_w = w / orig_width
        pixel_h = h / orig_height
        for y_orig in range(orig_height):
            for x_orig in range(orig_width):
                color = pixmap.toImage().pixelColor(x_orig, y_orig)
                if color.alpha() == 0: continue
                x1 = int(x_orig * pixel_w)
                y1 = int(y_orig * pixel_h)
                x2 = int((x_orig + 1) * pixel_w)
                y2 = int((y_orig + 1) * pixel_h)
                tempArtist.fillRect(x1, y1, x2 - x1, y2 - y1, color)
        tempArtist.end()
        if opacity < 255: Artist.setOpacity(opacity / 255)
        Artist.drawPixmap(x, y, result)
        if opacity < 255: Artist.setOpacity(1.0)
    def paintEvent(self, event):
        Artist= PyQt6.QtGui.QPainter(self)
        Artist.setRenderHint(PyQt6.QtGui.QPainter.RenderHint.Antialiasing )

        self.newSquare(Artist, 0, 0, 0, 0, 0, 300, 150, 75)
        self.addBlurredRect(Artist, 255, 0, 0, 255, 0, 0, 25, 25, 50, 50, 255, 15)
        self.newSquare(Artist, 0, 0, 255, (self.getGem("window_width") - 75), (self.getGem("window_height") - 75), 50, 50)
        self.newText(Artist, 'lorem ipsum', 30, 30, 255, 255, 255)
        self.addBlurredImage(Artist, r"Z:\PROJECT ZHOPA\goosecool1-s_ST-MHP-PD\ProtoOnYourScreen!\src\environment\images\unnamed.jpg", 35, 25, 100, 100, 250, 15)
        self.addPixelImage(Artist, r"Z:\PROJECT ZHOPA\goosecool1-s_ST-MHP-PD\ProtoOnYourScreen!\src\environment\images\unnamed.jpg", 35, 25, 100, 100, 255)

        Artist.end()

if __name__ == "__main__":
    base= PyQt6.QtWidgets.QApplication(sys.argv)
    window= app()
    window.show()
    sys.exit(base.exec())