from PySide6.QtGui import QIcon, QAction, QFont
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QColorDialog
from yeelight import Bulb

# set your bulb's local ipv4 address
bulb = Bulb("10.0.0.165")

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

tray = QSystemTrayIcon()
tray.setToolTip("Yeelight")
tray.setIcon(QIcon("resources/icon.png"))
tray.setVisible(True)

font_size = 12
font_style = "Consolas"

menu = QMenu()
menu.setFont(QFont(font_style, font_size))
menu.setStyleSheet(
    """QMenu {background-color: #2e2e2e; color: #ffffff; border: 1px solid #757575; border-radius: 5px; padding: 6px; text-align: center;}
    QMenu::item:selected {background-color: #ebebeb; color: #000000;}
    QMenu::indicator { width: 14px; height: 14px;}
    QMenu::indicator:checked { image: url(resources/checked.png);}
    QMenu::item { border-radius: 4px; padding: 6px 14px 6px 6px;}
    QMenu::item:disabled { border-radius: 4px; padding: 10px 14px 6px 6px; color: #999999;}
    """)
menu.setEnabled(True)

rgb_clipboard = QApplication.clipboard()
dialog = QColorDialog()

turn_on_off_action = QAction()
turn_on_off_action.setCheckable(False)
turn_on_off_action.setFont(QFont(font_style, font_size, QFont.Bold))
turn_on_off_action.setChecked(bulb.get_properties()['power'] == "on")

temp4700_action = QAction("4700K")
temp4700_action.setCheckable(True)

temp3200_action = QAction("3200K")
temp3200_action.setCheckable(True)

temp1900_action = QAction("1900K")
temp1900_action.setCheckable(True)

rgb_action = QAction("RGB")
rgb_action.setCheckable(True)

quit_action = QAction("Exit")
quit_action.setCheckable(False)
quit_action.setFont(QFont(font_style, font_size, QFont.Bold))


def set_dependent_actions_enabled(enabled):
    temp4700_action.setEnabled(enabled)
    temp3200_action.setEnabled(enabled)
    temp1900_action.setEnabled(enabled)
    rgb_action.setEnabled(enabled)


def set_all_actions_unchecked():
    temp4700_action.setChecked(False)
    temp3200_action.setChecked(False)
    temp1900_action.setChecked(False)
    rgb_action.setChecked(False)


if (bulb.get_properties()['power'] == "on"):
    turn_on_off_action.setText("Off")
else:
    turn_on_off_action.setText("On")
    set_dependent_actions_enabled(False)


def turn_on_off():
    if bulb.get_properties()['power'] == "on":
        bulb.turn_off()
        turn_on_off_action.setText("On")
        set_dependent_actions_enabled(False)
    else:
        bulb.turn_on()
        set_temp_4700()
        turn_on_off_action.setText("Off")
        set_dependent_actions_enabled(True)


def set_temp_4700():
    bulb.set_color_temp(4700)
    set_all_actions_unchecked()
    temp4700_action.setChecked(True)


def set_temp_3200():
    bulb.set_color_temp(3200)
    set_all_actions_unchecked()
    temp3200_action.setChecked(True)


def set_temp_1900():
    bulb.set_color_temp(1900)
    set_all_actions_unchecked()
    temp1900_action.setChecked(True)


def set_rgb():
    if dialog.exec():
        color = dialog.currentColor()
        bulb.set_rgb(color.red(), color.green(), color.blue())
        set_all_actions_unchecked()
        rgb_action.setChecked(True)
    else:
        rgb_action.setChecked(False)


turn_on_off_action.triggered.connect(turn_on_off)
temp4700_action.triggered.connect(set_temp_4700)
temp3200_action.triggered.connect(set_temp_3200)
temp1900_action.triggered.connect(set_temp_1900)
rgb_action.triggered.connect(set_rgb)
quit_action.triggered.connect(app.quit)

menu.addAction(turn_on_off_action)
menu.addAction(temp4700_action)
menu.addAction(temp3200_action)
menu.addAction(temp1900_action)
menu.addAction(rgb_action)
menu.addAction(quit_action)

tray.setContextMenu(menu)

app.exec()
