import os
import sys
import shutil
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QFileDialog, 
                            QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
                            QMessageBox, QInputDialog, QLineEdit)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QIcon

class MedicalReportsOrganizer(QMainWindow):
    """
    Desktop application for organizing scanned medical reports by specialty.
    """
    
    def __init__(self):
        super().__init__()
        self.specialties = [
            "Cardiology",
            "Dermatology",
            "Endocrinology",
            "Gastroenterology",
            "Hematology",
            "Immunology",
            "Nephrology",
            "Neurology",
            "Oncology",
            "Ophthalmology",
            "Orthopedics",
            "Otolaryngology",
            "Pediatrics",
            "Psychiatry",
            "Pulmonology",
            "Radiology",
            "Rheumatology",
            "Urology",
            "General Medicine",
            "Other"
        ]
        self.base_directory = os.path.join(os.path.expanduser("~"), "MedicalReports")
        self.init_ui()
        self.setup_folder_structure()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Medical Reports Organizer")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize search state
        self.current_search_text = ""
        
        # Setup search timer
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(500)  # 500ms delay
        self.search_timer.timeout.connect(self.filter_reports)
        
        # Main widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Top controls
        top_controls = QHBoxLayout()
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search reports...")
        self.search_box.textChanged.connect(self.on_search_text_changed)
        top_controls.addWidget(self.search_box)
        
        # Import button
        self.import_btn = QPushButton("Import Report")
        self.import_btn.clicked.connect(self.import_report)
        top_controls.addWidget(self.import_btn)
        
        # Specialty selector
        specialty_label = QLabel("Specialty:")
        top_controls.addWidget(specialty_label)
        self.specialty_combo = QComboBox()
        self.specialty_combo.addItem("All")
        self.specialty_combo.addItems(self.specialties)
        self.specialty_combo.currentIndexChanged.connect(self.on_specialty_changed)
        top_controls.addWidget(self.specialty_combo)

        # Add specialty button
        self.add_specialty_btn = QPushButton("Add Specialty")
        self.add_specialty_btn.clicked.connect(self.add_specialty)
        top_controls.addWidget(self.add_specialty_btn)
        
        # Add top controls to main layout
        main_layout.addLayout(top_controls)
        
        # Reports table
        self.reports_table = QTableWidget(0, 4)  # 0 rows, 4 columns
        self.reports_table.setHorizontalHeaderLabels(["Filename", "Date Added", "Specialty", "Actions"])
        
        # Set resize modes using the correct enum
        self.reports_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.reports_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.reports_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.reports_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        main_layout.addWidget(self.reports_table)
        
        # Initial refresh of table contents
        self.refresh_reports_table()
    
    def setup_folder_structure(self):
        """Create the base directory and specialty folders if they don't exist."""
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)
        
        for specialty in self.specialties:
            specialty_dir = os.path.join(self.base_directory, specialty)
            if not os.path.exists(specialty_dir):
                os.makedirs(specialty_dir)
    
    def import_report(self):
        """Import a scanned medical report and copy it to the selected specialty folder."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, 
            "Select Medical Reports", 
            "", 
            "PDF Files (*.pdf);;Image Files (*.png *.jpg *.jpeg);;All Files (*.*)"
        )
        
        if not file_paths:
            return
            
        selected_specialty = self.specialty_combo.currentText()
        
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            destination = os.path.join(self.base_directory, selected_specialty, file_name)
            
            if os.path.exists(destination):
                reply = QMessageBox.question(
                    self, 
                    'File Exists', 
                    f'The file {file_name} already exists in {selected_specialty}. Overwrite?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                    QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.No:
                    continue
            
            shutil.copy2(file_path, destination)
            self.refresh_reports_table()
    
    def on_specialty_changed(self, index):
        """Handle specialty combo box changes."""
        self.filter_reports()
    
    def on_search_text_changed(self, text):
        """Handle search text changes."""
        self.current_search_text = text.strip()
        if self.search_timer.isActive():
            self.search_timer.stop()
        self.search_timer.start()
    
    def filter_reports(self):
        """Filter reports based on search text and selected specialty."""
        self.refresh_reports_table()
    
    def refresh_reports_table(self):
        """Refresh the reports table with current filters."""
        self.reports_table.clearContents()
        self.reports_table.setRowCount(0)
        
        selected_specialty = self.specialty_combo.currentText()
        search_text = self.current_search_text.lower()
        
        all_files = []
        specialties_to_check = self.specialties if selected_specialty == "All" else [selected_specialty]
        
        for specialty in specialties_to_check:
            specialty_dir = os.path.join(self.base_directory, specialty)
            if os.path.exists(specialty_dir):
                files = os.listdir(specialty_dir)
                for file_name in files:
                    if os.path.isfile(os.path.join(specialty_dir, file_name)):
                        if not search_text or search_text in file_name.lower():
                            all_files.append((file_name, specialty))
        
        self.reports_table.setRowCount(len(all_files))
        for row, (file_name, specialty) in enumerate(all_files):
            file_path = os.path.join(self.base_directory, specialty, file_name)
            
            # File name
            self.reports_table.setItem(row, 0, QTableWidgetItem(file_name))
            
            # Date added
            timestamp = os.path.getctime(file_path)
            date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            self.reports_table.setItem(row, 1, QTableWidgetItem(date_str))
            
            # Specialty
            self.reports_table.setItem(row, 2, QTableWidgetItem(specialty))
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            
            open_btn = QPushButton("Open")
            open_btn.clicked.connect(lambda checked=False, f=file_path: self.open_file(f))
            actions_layout.addWidget(open_btn)
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked=False, f=file_path: self.delete_report(f))
            actions_layout.addWidget(delete_btn)
            
            actions_widget.setLayout(actions_layout)
            self.reports_table.setCellWidget(row, 3, actions_widget)
    
    def open_file(self, file_path):
        """Open the report file with the default application."""
        if sys.platform == 'win32':
            os.startfile(file_path)
        elif sys.platform == 'darwin':  # macOS
            os.system(f'open "{file_path}"')
        else:  # Linux
            os.system(f'xdg-open "{file_path}"')
    
    def delete_report(self, file_path):
        """Delete a report after confirmation."""
        file_name = os.path.basename(file_path)
        reply = QMessageBox.question(
            self, 
            'Delete Report', 
            f'Are you sure you want to delete {file_name}?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(file_path)
                self.refresh_reports_table()
                QMessageBox.information(self, 'Success', 'Report deleted successfully.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete report: {str(e)}')
    
    def add_specialty(self):
        """Add a new medical specialty to the list."""
        new_specialty, ok = QInputDialog.getText(
            self, 
            'Add Specialty', 
            'Enter new medical specialty name:'
        )
        
        if ok and new_specialty:
            if new_specialty in self.specialties:
                QMessageBox.warning(self, 'Warning', 'This specialty already exists!')
                return
                
            self.specialties.append(new_specialty)
            self.specialty_combo.addItem(new_specialty)
            
            specialty_dir = os.path.join(self.base_directory, new_specialty)
            if not os.path.exists(specialty_dir):
                os.makedirs(specialty_dir)
                
            self.specialty_combo.setCurrentText(new_specialty)

def main():
    app = QApplication(sys.argv)
    window = MedicalReportsOrganizer()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
