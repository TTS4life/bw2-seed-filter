# BW/BW2 Seed Filter - Executable Build Guide

This guide explains how to convert the BW/BW2 Seed Filter application into an executable file for users who don't have Python installed.

## Prerequisites

- Python 3.7 or higher installed
- Internet connection (for PyInstaller download)

## Steps

### 1. Run the Build Script

```bash
python build_exe.py
```

This script automatically performs the following:
- Installs PyInstaller (if needed)
- Creates the application executable
- Automatically detects and includes dependencies

### 2. Generated Files

After a successful build, the following files will be created:
- `dist/BW2_Seed_Filter.exe` - Distribution executable file

### 3. Distribution Methods

The created executable can be distributed in the following ways:

#### Single File Distribution
- Distribute `dist/BW2_Seed_Filter.exe` as-is
- Users can run it by double-clicking

#### Folder Distribution (Recommended)
- Distribute the entire `dist/` folder
- More stable operation expected

## Troubleshooting

### Common Issues

1. **"PyInstaller not found" Error**
   - Check internet connection
   - Run command prompt as administrator

2. **"Module not found" Error**
   - Ensure all Python files are in the same folder
   - Check for import errors in dependencies

3. **Executable won't start**
   - Check Windows Defender or antivirus settings
   - Try running as administrator

### Manual Build

If the automatic script doesn't work, run the following commands manually:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name=BW2_Seed_Filter main.py
```

## Distribution Notes

1. **File Size**
   - The executable is typically 50-100MB
   - This includes Python runtime and libraries

2. **Security**
   - Some antivirus software may give false positives
   - Add exceptions as needed

3. **Compatibility**
   - Works on Windows 7 and later
   - Supports both 32-bit and 64-bit

## Support

If problems occur, check the following:
- Python version (3.7+ recommended)
- All required files exist
- File paths don't contain Japanese or special characters

## Updates

To update the application, follow these steps:

1. Update source code
2. Re-run `python build_exe.py`
3. Distribute the new executable

This allows users without Python to use the BW/BW2 Seed Filter application! 