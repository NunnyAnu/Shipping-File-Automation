# Shipping-File-Automation

## Installation


### 1. Clone this repository
```
git clone https://github.com/NunnyAnu/Shipping-File-Automation
```
### 2. Navigate into the working folder

  ```
  cd Shipping-File-Automation/mainfolder
  ```

### 3. Create a new Python environment 
#### With Python VENV
  ```
  python -m venv shipenv
  source shipenv/bin/activate   # (Linux / macOS)
  shipenv\Scripts\activate      # (Windows PowerShell / CMD)
  ```

#### With Conda
  ```
  conda create -n shipenv python=3.11 pip
  conda activate shipenv
  ```

### 4. Install required libraries and the dependencies

  ```
  pip install --upgrade pip
  pip install pandas openpyxl xlsxwriter pyinstaller
  ```

### 5. Edit Input and Output paths in ```config.yaml```
```
paths:
  input_folder: {INPUT FOLDER PATH}
  output_folder: {OUTPUT FOLDER PATH}
  mapping_file: {MAPPING FILE PATH}
```


### 6. Compile Python file into .exe
#### Linux / macOS
  ```
  pyinstaller --onefile --name MainApp \
    --add-data=config.yaml:. \ 
    --add-data=AccCode_Mapping.csv:. \
    --hidden-import=openpyxl \
    --hidden-import=xlsxwriter \
    main.py
  ```
#### Windows (PowerShell or CMD)
  ```
  pyinstaller --onefile --name MainApp `
    --add-data "config.yaml;." `
    --add-data "AccCode_Mapping.csv;." `
    --hidden-import openpyxl `
    --hidden-import xlsxwriter `
    main.py
  ```
The compiled .exe will be generated inside the `dist/` folder

### 📂 Project Structure (after compilation)
```
mainfolder/
│── input/    
│── output/
│── main.py
│── AccCode_Mapping.csv    # CSV for Code Mapping
│── config.yaml            # Paths config
│── shipenv/               # Python environment
│── build/                 # Temporary files from PyInstaller
│── dist/                  # Final executable output
│    └── MainApp.exe
```


## Usage
1. Put the file(s) you want to process into the `/input` folder (you can add more than one file).
2. Go to the dist/ folder and double-click `MainApp.exe`.
3. The processed file(s) will appear in the `/output` folder.


