import sys

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import *


def make_row(*widgets):
    row = QHBoxLayout()
    for widget in widgets:
        row.addWidget(widget)
    return row


class MainWindow(QMainWindow):
    task_created = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.title_edit = QLineEdit()
        self.chars_label = QLabel("Название: 0 символов")
        self.description_edit = QTextEdit()
        self.priority_box = QComboBox()
        self.priority_box.addItems(["Low", "Medium", "High"])
        self.priority_box.setCurrentIndex(1)
        self.checkboxes = [QCheckBox("Send notification"), QCheckBox("Add to favorites")]
        self.task_list = QListWidget()
        self.status_label = QLabel("Задач: 0")
        add_button, delete_button, clear_button, about_button = (
            QPushButton(text) for text in ("Добавить задачу", "Удалить выбранную", "Очистить список", "О программе")
        )

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(QLabel("Задача"))
        layout.addWidget(self.title_edit)
        layout.addWidget(self.chars_label)
        layout.addWidget(QLabel("Описание"))
        layout.addWidget(self.description_edit)
        layout.addWidget(self.priority_box)
        layout.addLayout(make_row(*self.checkboxes))
        layout.addWidget(add_button)
        layout.addWidget(self.task_list)
        layout.addWidget(self.status_label)
        layout.addLayout(make_row(delete_button, clear_button, about_button))
        self.setCentralWidget(central)

        add_button.clicked.connect(self.add_task)
        delete_button.clicked.connect(self.delete_task)
        clear_button.clicked.connect(self.clear_tasks)
        about_button.clicked.connect(self.show_about)
        self.title_edit.textChanged.connect(self.update_chars)
        self.task_created.connect(self.update_status)

    def update_chars(self, text):
        self.chars_label.setText(f"Название: {len(text)} символов")

    def update_status(self):
        self.status_label.setText(f"Задач: {self.task_list.count()}")

    def add_task(self):
        title = self.title_edit.text().strip()
        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите название задачи")
            return
        priority = self.priority_box.currentText()
        flags = [c.text() for c in self.checkboxes if c.isChecked()]
        description = self.description_edit.toPlainText().strip()

        text = f"{title} [{priority}]"
        if flags:
            text += " " + ", ".join(flags)
        if description:
            text += "\n" + description
        self.task_list.addItem(text)

        self.title_edit.clear()
        self.description_edit.clear()
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)
        self.task_created.emit()

    def delete_task(self):
        row = self.task_list.currentRow()
        if row < 0:
            QMessageBox.information(self, "Удаление", "Выберите задачу")
        elif QMessageBox.question(self, "Удаление", "Удалить выбранную задачу?") == QMessageBox.StandardButton.Yes:
            self.task_list.takeItem(row)
            self.update_status()

    def clear_tasks(self):
        if QMessageBox.question(self, "Очистка", "Очистить весь список?") == QMessageBox.StandardButton.Yes:
            self.task_list.clear()
            self.update_status()

    def show_about(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("О программе")
        QVBoxLayout(dialog).addWidget(QLabel("Task Manager 2.0"))
        dialog.exec()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
