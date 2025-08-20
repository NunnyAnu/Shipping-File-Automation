import re
import sys
import time
from pathlib import Path

import pandas as pd
import yaml


class DataProcessor:
    def __init__(self, excel_path, mapping_path, col_range, sheet_name, start_row):
        self.excel_path = excel_path
        self.mapping_path = mapping_path
        self.col_range = col_range
        self.sheet_name = sheet_name
        self.start_row = start_row
        self.df = None
        self.item_to_code = {}
        self.final_dict = {}
        self.attribute_list = []
        self.year = None
        self.quarter = None

    def get_item(self, row):
        for val in reversed(row):
            if pd.notna(val):
                return val
        return None

    def load_data(self):
        self.df = pd.read_excel(self.excel_path, sheet_name=self.sheet_name, header=None)
        mapping_df = pd.read_csv(self.mapping_path)
        self.item_to_code = dict(zip(mapping_df['AccName'], mapping_df['AccCode']))
        match = re.search(r"_(\d{2})-(Q\d)", self.excel_path,)      # find year and quarter from file name
        if match:
            self.year = int("20" + match.group(1))    # millennium 20xx
            self.quarter = match.group(2)
            print(f"Year: {self.year}")
            print(f"Quarter: {self.quarter}")
        else:
            print("No year and quarter found in filename.")

        # find header from attribute_row and after col_range (column after item)
        # stop find at first NaN after data started and dont keep Nan
        header_row = self.start_row
        attr_start_col = self.col_range[1]
        raw_attrs = self.df.iloc[header_row, attr_start_col:].tolist()
        started = False
        for attr in raw_attrs:
            if pd.isna(attr):
                if started:
                    break  # stop at first NaN after data started
                else:
                    continue  # skip initial NaNs
            self.attribute_list.append(attr)
            started = True


    def extract_items(self):
        part = self.df.iloc[self.start_row:, self.col_range[0]:self.col_range[1]].values.tolist()
        items = [self.get_item(row) for row in part]
        return pd.Series(items).dropna()

    def build_dict(self, items, value_data_start_col):
        value_data = self.df.iloc[self.start_row:, value_data_start_col:]
        for idx, item in items.items():
            item_str = str(item).strip()
            code = self.item_to_code.get(item_str)
            if code:
                row_values = pd.to_numeric(value_data.iloc[idx], errors='coerce').fillna(0).astype(float).tolist()
                self.final_dict[int(code)] = row_values
        

    def to_dataframe(self):
        output_data = []
        for acc_code, values in self.final_dict.items():
            for i, value in enumerate(values):
                if i < len(self.attribute_list):
                    output_data.append({
                        "AccCode": acc_code,
                        "Year": self.year,
                        "Qrt": f"{self.quarter}",
                        "OrgCode": self.attribute_list[i],
                        "Acu_QtrAmt": value
                    })
        return pd.DataFrame(output_data)


    def run(self, value_data_start_col):
        start_time = time.time()
        self.load_data()
        items = self.extract_items()
        self.build_dict(items, value_data_start_col)
        df_output = self.to_dataframe()
        print(f"Processed sheet: {self.sheet_name}")
        print(f"Runtime: {time.time() - start_time:.4f} seconds")
        return df_output


def resource_path(rel_path: str) -> Path:
    """Return absolute Path to resource."""
    base = getattr(sys, "_MEIPASS", Path(__file__).parent)
    return Path(base) / rel_path

def load_config():
    config_path = resource_path("config.yaml")  # always bundled one
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    # === Folder with Excel input files ===
    config = load_config()
    input_folder  = Path(config["paths"]["input_folder"])
    output_folder = Path(config["paths"]["output_folder"])
    mapping_path  = str(resource_path(Path(config["paths"]["mapping_file"]).name))

    # Find all Excel files in the folder
    excel_files = list(input_folder.glob("*.xlsx"))
    if not excel_files:
        print(f"❌ No Excel files found in {input_folder}, skipping...")
        return  # Exit without error

    for file_path in excel_files:
        print(f"📄 Processing: {file_path}")

        # Process BS_T sheet
        bs_processor = DataProcessor(
            excel_path=str(file_path),
            mapping_path=mapping_path,
            col_range=(1, 5),
            sheet_name="BS_T",
            start_row=4
        )
        df_bs = bs_processor.run(value_data_start_col=5)

        # Process PL_T sheet
        pl_processor = DataProcessor(
            excel_path=str(file_path),
            mapping_path=mapping_path,
            col_range=(1, 2),
            sheet_name="PL_T",
            start_row=6
        )
        df_pl = pl_processor.run(value_data_start_col=3)
        df_combined = pd.concat([df_bs, df_pl], ignore_index=True)

        # Output path (year & quarter taken from filename)
        output_path = output_folder / f"Import-fPL-fBS-{bs_processor.year}-{bs_processor.quarter}.xlsx"

        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            df_combined.to_excel(writer, sheet_name="ALL", index=False)
            df_bs.to_excel(writer, sheet_name="BS_C", index=False)
            df_pl.to_excel(writer, sheet_name="PL_C", index=False)

        print(f"✅ Saved: {output_path}")

if __name__ == "__main__":
    main()




