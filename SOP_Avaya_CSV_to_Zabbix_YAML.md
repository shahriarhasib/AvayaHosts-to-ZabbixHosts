# 📋 Standard Operating Procedure
## Avaya IP Office CSV to Zabbix YAML Converter
### Bulk Host Upload Tool for Zabbix Network Monitoring

---

| Field | Details |
|---|---|
| **Document Version** | 1.0 |
| **Status** | Active |
| **Platform** | Windows (All Versions) |
| **Python Version** | 3.8 or later |
| **Target Application** | Zabbix 7.0 |
| **Data Source** | Avaya IP Office Extension List |
| **GitHub Ready** | ✅ Yes |

---

## Table of Contents

1. [Overview & Purpose](#1-overview--purpose)
2. [Prerequisites](#2-prerequisites)
3. [Installing Python on Windows](#3-installing-python-on-windows)
4. [Source File: CSV from Avaya IP Office](#4-source-file-csv-from-avaya-ip-office)
5. [Setting Up File Paths](#5-setting-up-file-paths)
6. [Using the Conversion Script](#6-using-the-conversion-script)
7. [Importing the YAML File into Zabbix](#7-importing-the-yaml-file-into-zabbix)
8. [Publishing to GitHub](#8-publishing-to-github)
9. [Quick Reference Card](#9-quick-reference-card)

---

## 1. Overview & Purpose

This Standard Operating Procedure (SOP) provides step-by-step instructions for using the **CSV to Zabbix YAML Converter** Python script on a Windows computer. This tool is designed for **network/IT administrators** who manage Avaya IP Office phone systems and want to import phone extensions in bulk into the **Zabbix network monitoring platform** — even if they have no prior programming experience.

The script reads an Avaya IP Office extension export file (`InceptaExt.csv`), automatically categorizes each device as Avaya or Grandstream, and outputs a `.yaml` file that can be directly imported into Zabbix.

### 1.1 What This Script Does

- 📥 **Reads** the Avaya IP Office exported CSV extension list
- 🔍 **Identifies** phone type: Avaya (ICMP monitoring) or Grandstream/Other (SNMP monitoring)
- 🏗️ **Generates** Zabbix-compatible YAML with correct host groups, templates, and interfaces
- 📤 **Outputs** a single YAML file ready for Zabbix bulk import

### 1.2 Use Case

This is ideal when you have tens or hundreds of IP phones registered in Avaya IP Office and want to add all of them to Zabbix monitoring in one operation — instead of adding them one by one through the Zabbix web interface.

---

## 2. Prerequisites

### 2.1 System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| Operating System | Windows 7 (64-bit) | Windows 10/11 (64-bit) |
| Python Version | Python 3.8 | Python 3.11 or 3.12 |
| Disk Space | 200 MB (for Python) | 500 MB |
| Internet Access | Required (for Python install) | Required |
| Permissions | Standard user | Administrator (for install) |

### 2.2 Accounts & Access

- Administrator access to the Windows computer (for Python installation)
- Access to Avaya IP Office Manager or System Status to export extension data
- Access to Zabbix web interface (for the final import step)

---

## 3. Installing Python on Windows

Python is a free programming language that runs the conversion script. If Python is already installed on your computer, skip to [Section 3.4](#34-verify-python-installation) to verify the installation.

### 3.1 Download Python

1. Open your web browser (Chrome, Edge, or Firefox)
2. Go to: **https://www.python.org/downloads/**
3. Click the yellow button: **"Download Python 3.x.x"** (the latest version is shown automatically)
4. Save the installer file to your `Downloads` folder

> 📝 **NOTE:** The file will be named something like `python-3.12.4-amd64.exe`. The exact version number may differ — this is fine.

### 3.2 Run the Installer

1. **Double-click** the downloaded file (`python-3.12.x-amd64.exe`) to launch the installer
2. ⚠️ **IMPORTANT:** On the first installer screen, check the box at the bottom that says:
   ```
   ✅ Add Python to PATH
   ```
   **This is critical — do not skip this step!**
3. Click **"Install Now"** (recommended option)
4. Wait for the installation to complete (approximately 1–3 minutes)
5. When finished, click **"Close"**

> ⚠️ **WARNING:** If you see a User Account Control (UAC) pop-up asking *"Do you want to allow this app to make changes?"*, click **Yes**.

### 3.3 Install Required Python Libraries

The script uses two Python libraries: `csv` and `yaml`. The `csv` module is built into Python. However, `PyYAML` must be installed separately.

1. **Open Command Prompt:**
   Press **Windows Key + R**, type `cmd`, and press **Enter**

2. In the black Command Prompt window, type the following command and press **Enter**:
   ```
   pip install pyyaml
   ```

3. You will see text scrolling — this is normal. Wait until you see:
   ```
   Successfully installed PyYAML-x.x.x
   ```

> ⚠️ **WARNING:** If you get an error like `'pip' is not recognized`, this means Python was not added to PATH correctly. Uninstall Python and reinstall it, making sure to check the **"Add Python to PATH"** checkbox.

### 3.4 Verify Python Installation

To confirm Python is installed correctly:

1. Open Command Prompt: Press **Windows Key + R**, type `cmd`, press **Enter**
2. Type the following and press **Enter**:
   ```
   python --version
   ```
3. You should see output like:
   ```
   Python 3.12.4
   ```

If you see a version number, Python is correctly installed. If you see an error, repeat [Section 3.1–3.2](#31-download-python).

---

## 4. Source File: CSV from Avaya IP Office

### 4.1 Required File Name

> ⚠️ **The CSV file must be named exactly:** `InceptaExt.csv`

The script is pre-configured to look for this exact filename. If your file has a different name, you must either:
- Rename it to `InceptaExt.csv`, **or**
- Change the filename inside the script (covered in [Section 6.3](#63-using-custom-file-paths))

### 4.2 How to Export from Avaya IP Office

1. **Open Avaya IP Office Manager** on your computer
2. Connect to the IP Office system
3. Navigate to: **File → Export** or **Reports → Extension List**
4. Choose **CSV format** when prompted for the export format
5. **Save the file** as `InceptaExt.csv`

> 📝 **NOTE:** Avaya IP Office Manager export steps may vary slightly depending on your IP Office version (9.x, 10.x, 11.x). Consult your Avaya documentation if you cannot find the export option.

### 4.3 Required CSV Structure

The script reads specific columns by their **position (index)**. Your CSV file must have columns in the following order:

| Column | Index | Field Name | Example Value / Description |
|---|---|---|---|
| Column A | 0 (col1) | Extension Number | `4036` — phone extension ID |
| Column B | 1 (col2) | *(Unused)* | Any value — not used by script |
| Column C | 2 (col3) | Person Name | `Md. Saiful Islam` |
| Column D | 3 (col4) | IP Address | `192.168.21.149` |
| Column E | 4 (col5) | *(Unused)* | Any value — not used by script |
| Column F | 5 (col6) | Device Type | `Avaya`, `9608`, `J179`, `VPN`, `Grandstream`, etc. |

#### 4.3.1 Sample CSV Content

Your CSV file should look like this when opened in Notepad or Excel:

```csv
4036,,Md. Saiful Islam,192.168.21.149,,Avaya 9608
4037,,Karim Ahmed,192.168.21.150,,J179
4038,,Rahim Uddin,192.168.21.151,,Grandstream GXP2135
4039,,Sara Begum,192.168.21.152,,VPN User 9611
4040,,Jalal Khan,192.168.21.153,,9621
```

> 💡 **TIP:** Rows with a missing IP address, missing person name, or invalid IP addresses (such as `0.0.0.0` or `?`) are automatically skipped by the script.

### 4.4 Device Classification Rules

The script automatically determines the device category based on keywords found in **Column F (Device Type)**:

| Keyword(s) in Column F | Category | Zabbix Template | Zabbix Group |
|---|---|---|---|
| `avaya`, `9608`, `J179`, `VPN`, `9611`, `9621`, `9641` | Avaya Phone | `ICMP Ping` | `Avaya-Phones` |
| Anything else (e.g., `Grandstream`, `GXP`) | Non-Avaya Phone | `Grandstream IP Phone` | `Grandstream-Phones` + `Non-Avaya-Phones` |

---

## 5. Setting Up File Paths

### 5.1 Understanding File Paths on Windows

A **file path** is the full location of a file on your computer. For example, if you save a file called `InceptaExt.csv` to your Desktop, its path would be:

```
C:\Users\YourName\Desktop\InceptaExt.csv
```

Replace `YourName` with your actual Windows username.

### 5.2 Recommended Folder Structure

For this tool, we recommend creating a dedicated folder to keep all files organized:

```
C:\ZabbixConverter\
    ├── convert.py          ← the Python script
    ├── InceptaExt.csv      ← your Avaya export file
    └── InceptaExt.yaml     ← output (created automatically)
```

#### 5.2.1 How to Create the Folder

1. Open **File Explorer** (Windows Key + E)
2. Navigate to **Local Disk (C:)**
3. Right-click in an empty area → **New → Folder**
4. Name it `ZabbixConverter`
5. Press **Enter**

### 5.3 How to Find Your Windows Username

If you are unsure of your Windows username:

1. Open Command Prompt (Windows Key + R → type `cmd` → Enter)
2. Type the following and press Enter:
   ```
   echo %USERNAME%
   ```
3. Your username will be displayed

### 5.4 Copying Files to the Folder

1. Save the Python script file (`convert.py`) into `C:\ZabbixConverter\`
2. Copy your `InceptaExt.csv` from Avaya into `C:\ZabbixConverter\`

> 💡 **TIP:** Both the Python script and the CSV file must be in the **same folder** for the default setup to work.

---

## 6. Using the Conversion Script

### 6.1 Saving the Python Script

1. Open **Notepad** (Start Menu → search "Notepad")
2. Copy the entire Python script code
3. Paste it into Notepad
4. Click **File → Save As**
5. Navigate to `C:\ZabbixConverter\`
6. In the **File name** field, type: `convert.py`
7. In the **Save as type** dropdown, select: **"All Files (*.*)"**
8. Click **Save**

> ⚠️ **WARNING:** Make sure the filename ends in `.py` and **not** `.py.txt`. If you see `convert.py.txt` in the folder, rename it by removing the `.txt` part.

### 6.2 Running the Script (Default Setup)

If your files are in `C:\ZabbixConverter\` and the CSV is named `InceptaExt.csv`:

1. Open Command Prompt: **Windows Key + R** → type `cmd` → Enter
2. Navigate to the folder:
   ```
   cd C:\ZabbixConverter
   ```
3. Run the script:
   ```
   python convert.py
   ```
4. Press **Enter**
5. When complete, you will see:
   ```
   ✓ Conversion complete!
   ✓ Processed 87 hosts
   ✓ Output saved to: InceptaExt.yaml

   Summary:
     - Avaya phones: 72
     - Non-Avaya phones: 15
   ```
6. Your output file `InceptaExt.yaml` is now in `C:\ZabbixConverter\`

### 6.3 Using Custom File Paths

If your CSV file is in a different location (e.g., your Desktop or Downloads folder), you need to update the file paths inside the script.

#### 6.3.1 Opening the Script for Editing

1. Navigate to `C:\ZabbixConverter\` in File Explorer
2. Right-click on `convert.py`
3. Click **Open with → Notepad**

#### 6.3.2 Locating the Configuration Section

Scroll to the **bottom** of the script. You will find this section:

```python
if __name__ == "__main__":
    # Configuration
    csv_file = 'InceptaExt.csv'  # Change this to your CSV file path
    output_yaml = 'InceptaExt.yaml'
```

#### 6.3.3 Updating File Paths

Replace the path values with your actual file locations. Use **forward slashes** (`/`) in the paths:

```python
# Example: CSV file is on the Desktop
csv_file = 'C:/Users/YourName/Desktop/InceptaExt.csv'

# Example: CSV file is in Downloads folder
csv_file = 'C:/Users/YourName/Downloads/MyPhones.csv'

# Example: Custom output location
output_yaml = 'C:/Users/YourName/Desktop/zabbix_hosts.yaml'
```

> ⚠️ **WARNING:** Always use **forward slashes** (`/`) in file paths inside the Python script, even on Windows. Alternatively, use **double backslashes** (`C:\\Users\\YourName\\...`) — but **NEVER** single backslashes.

#### 6.3.4 Changing the CSV File Name

If your Avaya export file has a different name (e.g., `phones_export.csv`), update the `csv_file` line:

```python
csv_file = 'phones_export.csv'   # Or full path if not in same folder
```

### 6.4 Troubleshooting Common Errors

| Error Message | Likely Cause | Solution |
|---|---|---|
| `'python' is not recognized...` | Python not installed or not in PATH | Reinstall Python with "Add to PATH" checked |
| `FileNotFoundError: InceptaExt.csv not found` | CSV file not in the same folder as script | Copy CSV to `C:\ZabbixConverter\` or update `csv_file` path |
| `ModuleNotFoundError: No module named 'yaml'` | PyYAML not installed | Run: `pip install pyyaml` |
| No output / 0 hosts processed | CSV columns in wrong order or wrong delimiter | Check CSV structure matches [Section 4.3](#43-required-csv-structure) |
| `UnicodeDecodeError` | CSV file has special characters with wrong encoding | Re-export from Avaya with UTF-8 or save CSV as UTF-8 from Excel |

---

## 7. Importing the YAML File into Zabbix

### 7.1 Prerequisites for Import

- Zabbix version **7.0** or later
- The host groups `Avaya-Phones`, `Grandstream-Phones`, and `Non-Avaya-Phones` must exist in Zabbix (or will be created automatically on import)
- Templates `ICMP Ping` and `Grandstream IP Phone` must exist in Zabbix

### 7.2 Import Steps

1. Log into your **Zabbix web interface**
2. Navigate to: **Configuration → Hosts**
3. Click the **Import** button in the top-right corner
4. Click **Browse** and select your `InceptaExt.yaml` file
5. Review the import options — ensure **"Create new hosts"** is checked
6. Click **Import**
7. Zabbix will display a summary of imported hosts

> ⚠️ **WARNING:** If Zabbix shows errors about missing templates or host groups, create them first in Zabbix before re-importing.

---

## 8. Publishing to GitHub

### 8.1 Recommended Repository Structure

```
avaya-to-zabbix-converter/
├── convert.py               # Main conversion script
├── README.md                # Documentation
├── SOP.md                   # This SOP file
├── sample/
│   ├── sample_input.csv     # Example CSV (with dummy data only)
│   └── sample_output.yaml   # Example YAML output
├── .gitignore               # Exclude real CSV/YAML files
└── LICENSE                  # e.g., MIT License
```

### 8.2 .gitignore File

Create a `.gitignore` file to prevent accidentally uploading real phone data:

```gitignore
# Ignore real data files — never commit actual phone/IP data
*.csv
*.yaml

# Allow sample files only
!sample/*.csv
!sample/*.yaml

# Python cache
__pycache__/
*.pyc
*.pyo
.env
```

### 8.3 README.md Template

Use the following as your GitHub repository `README.md`:

````markdown
# Avaya IP Office → Zabbix YAML Converter

Converts Avaya IP Office extension export (CSV) to Zabbix bulk-import
format (YAML) for Zabbix 7.0.

## Features

- Reads Avaya IP Office extension list CSV
- Auto-detects Avaya vs Grandstream/Other phones
- Outputs Zabbix 7.0 compatible YAML
- Assigns ICMP Ping (Avaya) or Grandstream IP Phone template automatically

## Requirements

- Python 3.8+
- PyYAML: `pip install pyyaml`

## Quick Start

1. Export extension list from Avaya IP Office as CSV
2. Save as `InceptaExt.csv` in the same folder as `convert.py`
3. Run: `python convert.py`
4. Import `InceptaExt.yaml` into Zabbix via Configuration → Hosts → Import

## CSV Format

| Column | Field |
|---|---|
| Column A (index 0) | Extension Number |
| Column C (index 2) | Person Name |
| Column D (index 3) | IP Address |
| Column F (index 5) | Device Type |

## Output Host Groups

| Group | Monitoring Type |
|---|---|
| `Avaya-Phones` | ICMP Ping |
| `Grandstream-Phones` | SNMP (port 161) |
| `Non-Avaya-Phones` | SNMP (port 161) |

## Full SOP

See [SOP.md](SOP.md) for complete beginner-friendly instructions.
````

### 8.4 Uploading to GitHub (Step by Step)

1. Create a free account at **https://github.com** if you don't have one
2. Click **"New Repository"** → name it `avaya-to-zabbix-converter`
3. Choose **Public** or **Private** as appropriate for your organization
4. Check **"Add a README file"** → click **"Create repository"**
5. Click **"Add file → Upload files"**
6. Drag all your files into the upload area (script, SOP.md, sample files, .gitignore)
7. Add a commit message like: `Initial upload: CSV to Zabbix converter with SOP`
8. Click **"Commit changes"**

> ⚠️ **WARNING:** Never upload real CSV files containing actual extension numbers, names, and IP addresses. Use only the `sample/` folder with **dummy data** for public repositories.

---

## 9. Quick Reference Card

### 9.1 Step-by-Step Summary

| Step | Action | Details | Expected Result |
|---|---|---|---|
| 1 | Install Python | python.org → Download → Run installer → Check "Add to PATH" | Python available in Command Prompt |
| 2 | Install PyYAML | `pip install pyyaml` | "Successfully installed" message |
| 3 | Export CSV | Avaya IP Office Manager → Export → CSV | `InceptaExt.csv` file created |
| 4 | Arrange Files | Script + CSV in `C:\ZabbixConverter\` | Both files in same folder |
| 5 | Run Script | `cd C:\ZabbixConverter` → `python convert.py` | `InceptaExt.yaml` created |
| 6 | Import YAML | Zabbix → Configuration → Hosts → Import | Hosts appear in Zabbix |

### 9.2 Key Commands (Copy & Paste Ready)

```bash
# 1. Install PyYAML (one-time setup)
pip install pyyaml

# 2. Check Python version
python --version

# 3. Navigate to your working folder
cd C:\ZabbixConverter

# 4. Run the conversion script
python convert.py

# 5. Find your Windows username (if needed)
echo %USERNAME%
```

### 9.3 File Naming Cheatsheet

| File | Required Name | Location |
|---|---|---|
| Python script | `convert.py` | `C:\ZabbixConverter\` |
| Avaya CSV export | `InceptaExt.csv` | `C:\ZabbixConverter\` |
| Zabbix YAML output | `InceptaExt.yaml` | Created automatically |

---

## Notes & Support

- For Avaya IP Office export issues, consult your Avaya documentation or system administrator.
- For Zabbix import issues, refer to the [Zabbix 7.0 documentation](https://www.zabbix.com/documentation/7.0/).
- For Python installation issues, visit [https://docs.python.org/](https://docs.python.org/).

---

*Version 1.0 — For Internal Use*  
*IT Infrastructure Team*
