from .ui.ui_main import Ui_MainWindow
from widgets.custom_grips import CustomGrip
from PySide6.QtWidgets import QMainWindow, QGraphicsDropShadowEffect, QSizeGrip, QPushButton
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PySide6.QtGui import QIcon, QColor


class View(QMainWindow):
    ENABLE_CUSTOM_TITLE_BAR = True
    MENU_WIDTH = 240
    LEFT_BOX_WIDTH = 240
    RIGHT_BOX_WIDTH = 240
    TIME_ANIMATION = 500

    # BTNS LEFT AND RIGHT BOX COLORS
    BTN_LEFT_BOX_COLOR = "background-color: #abcdff;"
    BTN_RIGHT_BOX_COLOR = "background-color: #abcdff;"

    # MENU SELECTED STYLESHEET
    MENU_SELECTED_STYLESHEET = """
    border-left: 18px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(121, 135, 255, 255), stop:0.5 rgba(85, 170, 255, 0));
    background-color: #f2f6ff;
    """

    def __init__(self, model) -> None:
        super(View, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = model

        self.setWindowTitle("Scan-X GUI Application")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.uiDefinitions()

    # TOGGLE MENU
    # ///////////////////////////////////////////////////////////////
    def toggleMenu(self):
        # GET WIDTH
        width = self.ui.leftMenuBg.width()
        maxExtend = self.MENU_WIDTH
        standard = 60

        # SET MAX WIDTH
        if width == 60:
            widthExtended = maxExtend
        else:
            widthExtended = standard

        # ANIMATION
        self.animation = QPropertyAnimation(self.ui.leftMenuBg, b"minimumWidth")
        self.animation.setDuration(self.TIME_ANIMATION)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    # TOGGLE LEFT BOX
    # ///////////////////////////////////////////////////////////////
    def toggleLeftBox(self):
        # GET WIDTH
        width = self.ui.extraLeftBox.width()
        widthRightBox = self.ui.extraRightBox.width()
        maxExtend = self.LEFT_BOX_WIDTH
        color = self.BTN_LEFT_BOX_COLOR
        standard = 0

        # GET BTN STYLE
        style = self.ui.toggleLeftBox.styleSheet()

        # SET MAX WIDTH
        if width == 0:
            widthExtended = maxExtend
            # SELECT BTN
            self.ui.toggleLeftBox.setStyleSheet(style + color)
            if widthRightBox != 0:
                style = self.ui.settingsTopBtn.styleSheet()
                self.ui.settingsTopBtn.setStyleSheet(style.replace(self.BTN_RIGHT_BOX_COLOR, ''))
        else:
            widthExtended = standard
            # RESET BTN
            self.ui.toggleLeftBox.setStyleSheet(style.replace(color, ''))

        self.start_box_animation(width, widthRightBox, "left")

    # TOGGLE RIGHT BOX
    # ///////////////////////////////////////////////////////////////
    def toggleRightBox(self):
        # GET WIDTH
        width = self.ui.extraRightBox.width()
        widthLeftBox = self.ui.extraLeftBox.width()
        maxExtend = self.RIGHT_BOX_WIDTH
        color = self.BTN_RIGHT_BOX_COLOR
        standard = 0

        # GET BTN STYLE
        style = self.ui.settingsTopBtn.styleSheet()

        # SET MAX WIDTH
        if width == 0:
            widthExtended = maxExtend
            # SELECT BTN
            self.ui.settingsTopBtn.setStyleSheet(style + color)
            if widthLeftBox != 0:
                style = self.ui.toggleLeftBox.styleSheet()
                self.ui.toggleLeftBox.setStyleSheet(style.replace(self.BTN_LEFT_BOX_COLOR, ''))
        else:
            widthExtended = standard
            # RESET BTN
            self.ui.settingsTopBtn.setStyleSheet(style.replace(color, ''))

        self.start_box_animation(widthLeftBox, width, "right")

    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0

        # Check values
        if left_box_width == 0 and direction == "left":
            left_width = 240
        else:
            left_width = 0
        # Check values
        if right_box_width == 0 and direction == "right":
            right_width = 240
        else:
            right_width = 0

        # ANIMATION LEFT BOX
        self.left_box = QPropertyAnimation(self.ui.extraLeftBox, b"minimumWidth")
        self.left_box.setDuration(self.TIME_ANIMATION)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

        # ANIMATION RIGHT BOX
        self.right_box = QPropertyAnimation(self.ui.extraRightBox, b"minimumWidth")
        self.right_box.setDuration(self.TIME_ANIMATION)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()

    def maximize_restore(self):
        if not self.isMaximized():
            self.showMaximized()
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.maximizeRestoreAppBtn.setToolTip("Restore")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/resources/images/icons/icon_restore_black.png"))
            self.ui.frame_size_grip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
        else:
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.appMargins.setContentsMargins(10, 10, 10, 10)
            self.ui.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/resources/images/icons/icon_maximize_black.png"))
            self.ui.frame_size_grip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()

    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, self.maximize_restore)
        self.ui.titleRightInfo.mouseDoubleClickEvent = dobleClickMaximizeRestore

        #STANDARD TITLE BAR
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # MOVE WINDOW / MAXIMIZE / RESTORE
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if self.isMaximized():
                self.maximize_restore()
            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        self.ui.titleRightInfo.mouseMoveEvent = moveWindow

        # CUSTOM GRIPS
        self.left_grip = CustomGrip(self, Qt.LeftEdge, True)
        self.right_grip = CustomGrip(self, Qt.RightEdge, True)
        self.top_grip = CustomGrip(self, Qt.TopEdge, True)
        self.bottom_grip = CustomGrip(self, Qt.BottomEdge, True)

        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)

        # RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        # MINIMIZE
        self.ui.minimizeAppBtn.clicked.connect(self.showMinimized)

        # MAXIMIZE/RESTORE
        self.ui.maximizeRestoreAppBtn.clicked.connect(self.maximize_restore)

        # CLOSE APPLICATION
        self.ui.closeAppBtn.clicked.connect(self.close)

    def resize_grips(self):
        self.left_grip.setGeometry(0, 10, 10, self.height())
        self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
        self.top_grip.setGeometry(0, 0, self.width(), 10)
        self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def resizeEvent(self, event):
        self.resize_grips()

    def select_topMenu_clicked_style(self, button):
        button.setStyleSheet(button.styleSheet() + self.MENU_SELECTED_STYLESHEET)

    def reset_topMenu_clicked_style(self):
        for button in self.ui.topMenu.findChildren(QPushButton):
            button.setStyleSheet(button.styleSheet().replace(self.MENU_SELECTED_STYLESHEET, ""))
    
    def changePage(self, button):
        idx = self.model.topMenuPageIdx(button)
        self.reset_topMenu_clicked_style()
        self.select_topMenu_clicked_style(button)
        self.ui.stackedWidget.setCurrentIndex(idx)
