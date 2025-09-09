from PyQt5 import QtWidgets, QtCore
import sys
from Pages.home import Ui_MainWindow as Ui_Home
from Pages.Mainwindow import Ui_MainWindow as Ui_MainPage
from Pages.cal import Ui_Form as Ui_Cal
from Pages.Graph import GraphWidget, SerialReader
from GetData import GetData
from Middleware.Connect_db import get_connection
from Pages.cal import Ui_Form

class HomeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Home()
        self.ui.setupUi(self)


        if hasattr(self.ui, "textBrowser_2") and self.ui.textBrowser_2 is not None:
            self.ui.textBrowser_2.mousePressEvent = self._on_home_clicked
        elif hasattr(self.ui, "widget_3") and self.ui.widget_3 is not None:
            self.ui.widget_3.mousePressEvent = self._on_home_clicked

        self._main_page = None

    def _on_home_clicked(self, event):
        if self._main_page is None:
            self._main_page = MainPageWindow()
        self._fade_to_window(self._main_page)


    def _fade_to_window(self, next_window: QtWidgets.QMainWindow):
        next_window.setWindowOpacity(0.0)
        next_window.show()
        animation = QtCore.QPropertyAnimation(next_window, b"windowOpacity")
        animation.setDuration(300)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        # Keep a reference to prevent GC
        next_window._fade_animation = animation
        def on_finished():
            self.close()
            next_window._fade_animation = None
        animation.finished.connect(on_finished)
        animation.start()

class MainPageWindow(QtWidgets.QMainWindow):
    def __init__(self, start_with_graph: bool = False, sensitivity_threshold: float = None):
        super().__init__()
        self.ui = Ui_MainPage()
        self.ui.setupUi(self)
        # Make the back arrow clickable to return to Home
        if hasattr(self.ui, "label_5") and self.ui.label_5 is not None:
            self.ui.label_5.mousePressEvent = self._on_back_clicked
        
        # Connect the Start button to open calculation page
        if hasattr(self.ui, "pushButton") and self.ui.pushButton is not None:
            self.ui.pushButton.clicked.connect(self._on_start_clicked)

        self._home_page = None
        self._cal_page = None

        # Prepare embedded graph components (hidden by default)
        self._graph_widget = None
        self._serial_reader = None
        self._graph_visible = False
        self._start_with_graph = start_with_graph
        self._sensitivity_threshold = sensitivity_threshold

        # Connect the Test button to toggle the embedded real-time graph
        if hasattr(self.ui, "pushButton_2") and self.ui.pushButton_2 is not None:
            self.ui.pushButton_2.clicked.connect(self._on_test_clicked)

    def showEvent(self, event):
        super().showEvent(event)
        if self._start_with_graph and not self._graph_visible:
            # auto-show the graph when arriving from review with Test
            QtCore.QTimer.singleShot(0, lambda: self._toggle_graph(True))
            self._start_with_graph = False

    def _ensure_graph_initialized(self):
        if self._graph_widget is not None:
            return
        # Place graph where the control grid is currently located
        target_parent = getattr(self.ui, "widget_2", self)
        geometry_source = getattr(self.ui, "layoutWidget", None)
        self._graph_widget = GraphWidget(target_parent, sensitivity_threshold=self._sensitivity_threshold)
        if geometry_source is not None:
            self._graph_widget.setGeometry(geometry_source.geometry())
        else:
            # Fallback geometry inside the main card
            self._graph_widget.setGeometry(QtCore.QRect(100, 120, 800, 380))
        self._graph_widget.hide()

        # Create reader and wire to graph using a single GetData instance
        self._serial_reader = SerialReader(reader=GetData(), command="RAI01;", delay_seconds=0.1)
        self._serial_reader.new_value.connect(self._graph_widget.update_plot)
        self._serial_reader.error.connect(self._on_serial_error)

    def _toggle_graph(self, show: bool):
        self._ensure_graph_initialized()
        controls_container = getattr(self.ui, "layoutWidget", None)

        if show:
            if controls_container is not None:
                controls_container.hide()
            self._graph_widget.show()
            if self._serial_reader is not None and not self._serial_reader.isRunning():
                self._serial_reader.start()
        else:
            if self._serial_reader is not None and self._serial_reader.isRunning():
                self._serial_reader.stop()
                self._serial_reader.wait(1500)
            self._graph_widget.hide()
            if controls_container is not None:
                controls_container.show()

        self._graph_visible = show

    def _on_serial_error(self, message: str):
        print(f"Serial Error: {message}")

    def _on_back_clicked(self, event):
        # If graph is visible, hide it first and restore controls
        if self._graph_visible:
            self._toggle_graph(False)
        if self._home_page is None:
            self._home_page = HomeWindow()
        self._fade_to_window(self._home_page)

    def _on_start_clicked(self):
        if self._cal_page is None:
            self._cal_page = CalWindow()
        self._fade_to_window(self._cal_page)

    def _on_test_clicked(self):
        # Toggle embedded graph inside the current window
        self._toggle_graph(not self._graph_visible)

    def _fade_to_window(self, next_window: QtWidgets.QMainWindow):
        next_window.setWindowOpacity(0.0)
        next_window.show()
        animation = QtCore.QPropertyAnimation(next_window, b"windowOpacity")
        animation.setDuration(300)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        # Keep a reference to prevent GC
        next_window._fade_animation = animation
        def on_finished():
            self.close()
            next_window._fade_animation = None
        animation.finished.connect(on_finished)
        animation.start()

    def closeEvent(self, event):
        try:
            if self._serial_reader is not None and self._serial_reader.isRunning():
                self._serial_reader.stop()
                self._serial_reader.wait(1500)
        finally:
            super().closeEvent(event)


class CalWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Cal()
        self.ui.setupUi(self)
        
        if hasattr(self.ui, "label_5") and self.ui.label_5 is not None:
            self.ui.label_5.mousePressEvent = self._on_back_clicked

        self._home_page = None

        # Wire Next button: save to DB then go to Review
        if hasattr(self.ui, "pushButton") and self.ui.pushButton is not None:
            self.ui.pushButton.clicked.connect(self._on_next_clicked)

        self._review_window = None

    def _collect_form_data(self):
        return {
            "customer_name": getattr(self.ui, "lineEdit_4", None).text() if hasattr(self.ui, "lineEdit_4") else "",
            "customer_id": getattr(self.ui, "lineEdit_3", None).text() if hasattr(self.ui, "lineEdit_3") else "",
            "batch_no": getattr(self.ui, "lineEdit_2", None).text() if hasattr(self.ui, "lineEdit_2") else "",
            "paper_gsm": getattr(self.ui, "lineEdit_5", None).text() if hasattr(self.ui, "lineEdit_5") else "",
        }

    def _on_next_clicked(self):
        # Save first; if success, proceed
        try:
            saved = False
            if hasattr(self.ui, "save_to_db"):
                saved = self.ui.save_to_db()
            else:
                # Fallback if method defined on this window (older code)
                if hasattr(self, "save_to_db"):
                    saved = self.save_to_db()
            if not saved:
                return
        except Exception:
            return

        data = self._collect_form_data()
        self._review_window = ReviewWindow(data, cal_window=self)
        self._fade_to_window(self._review_window)

    def _on_back_clicked(self, event):
        if self._home_page is None:
            self._home_page = MainPageWindow()
        self._fade_to_window(self._home_page)
        
    def _fade_to_window(self, next_window: QtWidgets.QMainWindow):
        next_window.setWindowOpacity(0.0)
        next_window.show()
        animation = QtCore.QPropertyAnimation(next_window, b"windowOpacity")
        animation.setDuration(300)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        # Keep a reference to prevent GC
        next_window._fade_animation = animation
        def on_finished():
            self.close()
            next_window._fade_animation = None
        animation.finished.connect(on_finished)
        animation.start()
        

class ReviewWindow(QtWidgets.QMainWindow):
    def __init__(self, data: dict, cal_window: CalWindow):
        super().__init__()
        self.setObjectName("ReviewWindow")
        self.resize(1024, 600)
        self._cal_window = cal_window
        self._data = dict(data)

        central = QtWidgets.QWidget(self)
        central.setObjectName("central_widget")
        self.setCentralWidget(central)

        # Background container to visually match other pages
        root = QtWidgets.QWidget(central)
        root.setGeometry(QtCore.QRect(0, 0, 1024, 600))
        root.setMinimumSize(QtCore.QSize(1024, 600))
        root.setStyleSheet("background-color: #17AEAA;")

        card = QtWidgets.QWidget(root)
        card.setGeometry(QtCore.QRect(45, 32, 931, 532))
        card.setMinimumSize(QtCore.QSize(931, 532))
        card.setStyleSheet("background-color: #FFF6ED;\nborder-radius: 40px;")

        # Simple form layout for review/edit
        form = QtWidgets.QFormLayout()
        form.setHorizontalSpacing(40)
        form.setVerticalSpacing(18)

        container = QtWidgets.QWidget(card)
        container.setGeometry(QtCore.QRect(160, 120, 611, 260))
        container.setLayout(form)

        self.name_edit = QtWidgets.QLineEdit(container)
        self.id_edit = QtWidgets.QLineEdit(container)
        self.batch_edit = QtWidgets.QLineEdit(container)
        self.gsm_edit = QtWidgets.QLineEdit(container)

        self.name_edit.setText(self._data.get("customer_name", ""))
        self.id_edit.setText(self._data.get("customer_id", ""))
        self.batch_edit.setText(self._data.get("batch_no", ""))
        self.gsm_edit.setText(self._data.get("paper_gsm", ""))

        for edit in (self.name_edit, self.id_edit, self.batch_edit, self.gsm_edit):
            edit.setMinimumHeight(44)
            edit.setStyleSheet("background-color: #D9D9D9;\nborder-radius: 12px;\nfont-size: 16px;")

        form.addRow("Customer Name", self.name_edit)
        form.addRow("Customer ID", self.id_edit)
        form.addRow("Batch No", self.batch_edit)
        form.addRow("Paper GSM", self.gsm_edit)

        # Action buttons: Edit (back), Test (proceed)
        buttons = QtWidgets.QWidget(card)
        buttons.setGeometry(QtCore.QRect(160, 400, 611, 50))
        h = QtWidgets.QHBoxLayout(buttons)
        h.setSpacing(20)

        self.edit_btn = QtWidgets.QPushButton("Edit", buttons)
        self.edit_btn.setMinimumSize(QtCore.QSize(120, 40))
        self.edit_btn.setStyleSheet("background-color: #FEC04D;\nborder-radius: 18px;\nfont-size: 20px;")

        self.test_btn = QtWidgets.QPushButton("Test", buttons)
        self.test_btn.setMinimumSize(QtCore.QSize(120, 40))
        self.test_btn.setStyleSheet("background-color: #17AEAA;\ncolor: white;\nborder-radius: 18px;\nfont-size: 20px;")

        h.addStretch(1)
        h.addWidget(self.edit_btn)
        h.addWidget(self.test_btn)
        h.addStretch(1)

        # Top-right icons to match style
        icon_user = QtWidgets.QLabel(card)
        icon_user.setGeometry(QtCore.QRect(750, 40, 31, 31))
        icon_user.setPixmap(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DirHomeIcon).pixmap(31,31))
        icon_user.setScaledContents(True)

        # Wire actions
        self.edit_btn.clicked.connect(self._on_edit_clicked)
        self.test_btn.clicked.connect(self._on_test_clicked)

    def _on_edit_clicked(self):
        # Send updated values back to the CalWindow inputs
        try:
            if hasattr(self._cal_window, "ui") and self._cal_window.ui is not None:
                if hasattr(self._cal_window.ui, "lineEdit_4"):
                    self._cal_window.ui.lineEdit_4.setText(self.name_edit.text())
                if hasattr(self._cal_window.ui, "lineEdit_3"):
                    self._cal_window.ui.lineEdit_3.setText(self.id_edit.text())
                if hasattr(self._cal_window.ui, "lineEdit_2"):
                    self._cal_window.ui.lineEdit_2.setText(self.batch_edit.text())
                if hasattr(self._cal_window.ui, "lineEdit_5"):
                    self._cal_window.ui.lineEdit_5.setText(self.gsm_edit.text())
        finally:
            self._fade_to_window(self._cal_window)

    def _on_test_clicked(self):
        # Get sensitivity value from the calculation window
        sensitivity = None
        try:
            if hasattr(self._cal_window, "ui") and hasattr(self._cal_window.ui, "lineEdit_3"):
                sensitivity_text = self._cal_window.ui.lineEdit_3.text().strip()
                if sensitivity_text:
                    sensitivity = float(sensitivity_text)
        except (ValueError, AttributeError):
            pass
        
        # Proceed to Main page and auto-show graph
        next_main = MainPageWindow(start_with_graph=True, sensitivity_threshold=sensitivity)
        self._fade_to_window(next_main)

    def _fade_to_window(self, next_window: QtWidgets.QMainWindow):
        next_window.setWindowOpacity(0.0)
        next_window.show()
        animation = QtCore.QPropertyAnimation(next_window, b"windowOpacity")
        animation.setDuration(300)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        # Keep a reference to prevent GC
        next_window._fade_animation = animation
        def on_finished():
            self.close()
            next_window._fade_animation = None
        animation.finished.connect(on_finished)
        animation.start()


def main():
    try:
        conn = get_connection()
        print("connected")
    except Exception as e:
        print(e)    
        
    app = QtWidgets.QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

