# Medical Reports Organizer

A desktop application for organizing scanned medical reports by specialty.

## Features

- Import scanned medical reports (PDF, images, etc.)
- Organize reports by medical specialty
- View reports listed in a table with metadata
- Open reports with the default application
- Delete reports
- Add new specialties as needed

## Requirements

- Python 3.6+
- PyQt6
- PyPDF2
- Pillow

## Installation and Basic Usage

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python medical_reports_organizer.py
```

3. The application will create a folder structure at `~/MedicalReports` with subfolders for each medical specialty.

4. To import reports:
   - Select the appropriate specialty from the dropdown
   - Click the "Import Report" button
   - Choose the file(s) you want to import

5. To view reports for a specific specialty, select it from the dropdown.

6. To open a report, click the "Open" button next to the report in the table.

7. To delete a report, click the "Delete" button next to the report in the table.

8. To add a new specialty:
   - Click the "Add Specialty" button
   - Enter the name of the new specialty

## Development Setup (Optional)

If you're planning to develop or modify the application, you may want to use a virtual environment:

### Windows
```cmd
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Build Instructions

### Building for Windows

1. Install PyInstaller:
```cmd
pip install pyinstaller
```

2. Create standalone executable:
```cmd
pyinstaller --name MedicalReportsOrganizer --windowed --onefile medical_reports_organizer.py
```

The executable will be created in the `dist` directory.

### Building for macOS

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Create macOS application:
```bash
pyinstaller --name MedicalReportsOrganizer --windowed --onefile medical_reports_organizer.py
```

3. The application bundle will be created in the `dist` directory.

(Optional) Code signing on macOS - This verification step ensures the application is properly signed and ready for distribution to users:
```bash
codesign --force --deep --sign "Developer ID Application: Your Name" dist/MedicalReportsOrganizer.app
```
