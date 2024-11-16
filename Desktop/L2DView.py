from PyQt6.QtGui import QMouseEvent
import live2d.v3 as live2d
from PyQt6.QtCore import QTimerEvent
from PyQt6.QtWidgets import QApplication
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSystemTrayIcon
from PyQt6.QtWidgets import QMenu
from PyQt6.QtWidgets import QLabel
import os
import sys


def callback():
    print("motion end")


class Win(QOpenGLWidget):
    model: live2d.LAppModel

    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.a = 0
        self.motion="Idle"
        self.motionChange=True
        self.resize(400, 300)
        self.initPall()

    def initPall(self):
        # 导入准备在托盘化显示上使用的图标
        icons = os.path.join('./Resources/Image/tigerIcon.jpg')
        # 设置右键显示最小化的菜单项
        # 菜单项退出，点击后调用quit函数
        quit_action = QAction('退出', self, triggered=self.quit)
        # 设置这个点击选项的图片
        quit_action.setIcon(QIcon(icons))
        # 菜单项显示，点击后调用showing函数
        showing = QAction(u'显示', self, triggered=self.showwin)
        # 新建一个菜单项控件
        self.tray_icon_menu = QMenu(self)
        # 在菜单栏添加一个无子菜单的菜单项‘退出’
        self.tray_icon_menu.addAction(quit_action)
        # 在菜单栏添加一个无子菜单的菜单项‘显示’
        self.tray_icon_menu.addAction(showing)
        # QSystemTrayIcon类为应用程序在系统托盘中提供一个图标
        self.tray_icon = QSystemTrayIcon(self)
        # 设置托盘化图标
        self.tray_icon.setIcon(QIcon(icons))
        # 设置托盘化菜单项
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        # 展示
        self.tray_icon.show()


    # 退出操作，关闭程序
    def quit(self):
        self.close()
        sys.exit()
    # 显示宠物
    def showwin(self):
        # setWindowOpacity（）设置窗体的透明度，通过调整窗体透明度实现宠物的展示和隐藏
        self.setWindowOpacity(1)

    def onMotionStarted(self):
        self.motionChange=False

    def onMotionFinshed(self):
        self.motionChange=True
        self.model.SetRandomExpression()

    def setTalking(self,txt):
        if self.motion == "Talk":
            self.setLabelText(txt=txt)
            return
        self.motion="Talk"
        # if self.motionChange:
        self.model.StartMotion("Idle", 4, live2d.MotionPriority.FORCE.value, onFinishMotionHandler=self.onMotionFinshed)
        self.setLabelText(txt=txt)
            # 宠物状态设置为正常待机
    
    def setIdling(self,txt="Nooooooo"):
        if self.motion == "Idle":
            self.setLabelText(txt=txt)
            return
        self.motion="Idle"
        self.setLabelText(txt=txt)
        self.model.StartRandomMotion("Idle",live2d.MotionPriority.FORCE.value,onFinishMotionHandler=self.onMotionFinshed)
        self.model.SetRandomExpression()
            # 宠物状态设置为正常待机
        return True
    def setThinking(self):
        if self.motion == "think":
            self.setLabelText(txt="?......")
            return
        self.motion="think"
        self.model.StartMotion("Idle", 5, live2d.MotionPriority.FORCE.value, onFinishMotionHandler=self.onMotionFinshed)
        self.setLabelText(txt="?.....")
        return True
    def setLabelText(self,txt=' '):    
        if len(txt)>10:
            txt=txt[0:9]
            txt+="..."
        self.talkLabel.setText(txt)
        self.talkLabel.adjustSize()









    def initializeGL(self) -> None:
                # 对话框定义
        self.talkLabel = QLabel(self)
        # 对话框样式设计
        self.talkLabel.setStyleSheet(
                "font: bold;"
                "font:25pt '楷体';"
                "color:white;"
                "background-color: white"
                "url(:/)"
        )
        # 将当前窗口作为 OpenGL 的上下文
        # 图形会被绘制到当前窗口
        self.makeCurrent()

        if live2d.LIVE2D_VERSION == 3:
            live2d.glewInit()
            live2d.setGLProperties()

        # 创建模型
        self.model = live2d.LAppModel()

        # 加载模型参数

        # 适用于 3 的模型
        self.model.LoadModelJson("Resources/v3/Hiyori/Hiyori.model3.json")

        # 以 fps = 30 的频率进行绘图
        self.startTimer(int(1000 / 30))

    def resizeGL(self, w: int, h: int) -> None:
        if self.model:
            # 使模型的参数按窗口大小进行更新
            self.model.Resize(w, h)
    
    def paintGL(self) -> None:
        
        live2d.clearBuffer()

        self.model.Update()

        self.model.Draw()
    
    def timerEvent(self, a0: QTimerEvent | None) -> None:

        if self.a == 0: # 测试一次播放动作和回调函数
            self.model.StartMotion("TapBody", 0, live2d.MotionPriority.FORCE.value, onFinishMotionHandler=callback)
            self.a += 1
        
        self.update() 
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.mouse_drag_pos=None
        self.setIdling(txt="Finally...")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if not self.motion=="Click":
            print("do something")
            self.model.StartMotion("Idle", 7, live2d.MotionPriority.FORCE.value, onFinishMotionHandler=self.onMotionFinshed)
        self.motion="Click"
        # 传入鼠标点击位置的窗口坐标
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_follow_mouse = True
        self.setLabelText(txt="Leave Me!")
        self.model.Touch(event.pos().x(), event.pos().y())
        self.mouse_drag_pos = event.position() - QPointF(self.pos())
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # 如果鼠标左键按下，且处于绑定状态
        # self.model.StartRandomMotion("TapBody",5)
        if Qt.MouseButton.LeftButton and self.is_follow_mouse:
            # 宠物随鼠标进行移动
            self.move((event.position() - self.mouse_drag_pos).toPoint())
        # self.model.Drag(event.pos().x(), event.pos().y())
        event.accept()

