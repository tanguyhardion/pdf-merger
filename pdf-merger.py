"""
This script defines a simple PDF merger application using PyQt5 and pypdf.

Written by Tanguy Hardion.
"""

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QListWidget,
    QMessageBox,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from pypdf import PdfWriter


class PdfMergerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initializes the GUI of the app by creating the layout and widgets.
        """

        self.setWindowTitle("PDF Merger")
        self.setWindowIcon(QIcon("assets/favicon.ico"))
        self.setGeometry(100, 100, 600, 500)
        self.move(
            QApplication.desktop().screen().rect().center() - self.rect().center()
        )

        layout = QVBoxLayout()

        self.drop_label = QLabel("Drop PDF files here", self)
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet(
            "QLabel { border: 2px dashed #aaa; padding: 20px; font-size: 16px; }"
        )
        layout.addWidget(self.drop_label)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet("QListWidget { padding: 10px; font-size: 14px; }")
        layout.addWidget(self.file_list)

        self.upload_button = QPushButton("Upload Files", self)
        self.upload_button.setStyleSheet(
            """
            QPushButton {
                border: 2px solid #202020;
                border-radius: 20px;
                padding: 10px;
                font-size: 14px;
                background-color: #eee;
            }
            QPushButton:hover {
                background-color: #ddd;
            }
        """
        )
        self.upload_button.clicked.connect(self.upload_files)
        layout.addWidget(self.upload_button)

        self.remove_button = QPushButton("Remove Selected File", self)
        self.remove_button.setStyleSheet(
            """
            QPushButton {
                border: 2px solid #202020;
                border-radius: 20px;
                padding: 10px;
                font-size: 14px;
                background-color: #eee;
            }
            QPushButton:hover {
                background-color: #ddd;
            }
        """
        )
        self.remove_button.clicked.connect(self.remove_selected_file)
        layout.addWidget(self.remove_button)

        self.merge_button = QPushButton("Merge PDFs", self)
        self.merge_button.setStyleSheet(
            """
            QPushButton {
                border: 2px solid #202020;
                border-radius: 20px;
                padding: 10px;
                font-size: 14px;
                background-color: #eee;
            }
            QPushButton:hover {
                background-color: #ddd;
            }
        """
        )
        self.merge_button.clicked.connect(self.merge_pdfs)
        self.merge_button.setEnabled(False)
        layout.addWidget(self.merge_button)

        self.setLayout(layout)

        self.setAcceptDrops(True)
        self.pdf_files = []

    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        Accepts the drag event if the data contains a path to a PDF file.
        """

        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """
        Handles the drop event by extracting the paths of the PDF files and adding them to the list.
        """

        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()
            if file_path.endswith(".pdf"):
                self.pdf_files.append(file_path)
                self.file_list.addItem(file_path)
        self.update_merge_button_state()

    def upload_files(self):
        """
        Opens a file dialog to select PDF files to merge.
        """

        files, _ = QFileDialog.getOpenFileNames(
            self, "Open PDF Files", "", "PDF Files (*.pdf)"
        )
        if files:
            self.pdf_files.extend(files)
            for file in files:
                self.file_list.addItem(file)
        self.update_merge_button_state()

    def remove_selected_file(self):
        """
        Removes the selected file from the list of uploaded PDF files.
        """

        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "No file selected to remove.")
            return

        for item in selected_items:
            file_path = item.text()
            self.pdf_files.remove(file_path)
            self.file_list.takeItem(self.file_list.row(item))
        self.update_merge_button_state()

    def merge_pdfs(self):
        """
        Merges the uploaded PDF files into a single PDF file and saves it to the specified location.
        """

        if len(self.pdf_files) < 2:
            QMessageBox.warning(
                self,
                "Not Enough Files",
                "You need to add at least two PDF files to merge.",
            )
            return

        merger = PdfWriter()
        for pdf in self.pdf_files:
            merger.append(pdf)

        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Merged PDF", "", "PDF Files (*.pdf)"
        )
        if output_path:
            try:
                merger.write(output_path)
                merger.close()
                QMessageBox.information(
                    self, "Success", f"Merged PDF saved to: {output_path}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save merged PDF: {e}")

    def update_merge_button_state(self):
        """
        Enables or disables the merge button based on the number of uploaded PDF files.
        """

        self.merge_button.setEnabled(len(self.pdf_files) > 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PdfMergerApp()
    ex.show()
    sys.exit(app.exec_())
