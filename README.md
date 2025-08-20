# Shipping-File-Automation

**Setup and Usage**
1. Create a main folder (Already created, you can skip this step or create a new one if you want)

  ```mkdir ~/mainfolder```


3. Navigate into the working folder

  ```cd ~/mainfolder```

4. Create a new Conda environment 

  ```conda create -n shipenv python=3.11 pip```

shipenv = environment name
python=3.11 = Python version
pip = install pip inside the environment

When prompted Proceed ([y]/n)?, type y and press Enter ✅

4. Activate the environment

  ```conda activate shipenv```

5. Install required libraries and the dependencies

  ```pip install --upgrade pip```

  ```pip install pandas openpyxl xlsxwriter pyinstaller```

6. Compile Python file into .exe

  ```pyinstaller --onefile run_file.py```


The compiled .exe will be generated inside the dist/ folder
📂 Project Structure (after compilation)
```axlsx/
│── output/
│── input/    
│── run_file.py
│── shipenv/        # Conda environment
│── build/          # Temporary files from PyInstaller
│── dist/           # Final executable output
│    └── run_file.exe```


**Usage**
1. Put the file(s) you want to process into the input folder (you can add more than one file).
2. Go to the dist/ folder and double-click run_file.exe.
3. The processed file(s) will appear in the output folder.


