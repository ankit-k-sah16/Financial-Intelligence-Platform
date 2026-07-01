from pathlib import Path
import pandas as pd


class ExcelLoader:
    """
    Loads Excel files from raw data directory.
    """

    def __init__(self, raw_dir: str | Path):
        self.raw_dir = Path(raw_dir)

    def load_file(self, filename, header=1 ): 
        """
        Load a single Excel file using header=1.
        """
        file_path = self.raw_dir / filename

        return pd.read_excel(
            file_path,
            header=header
        )

    def load_all(self, file_mapping: dict) -> dict:
        """
        Load multiple files.
        """

        datasets = {}

        for dataset_name, filename in file_mapping.items():

            datasets[dataset_name] = self.load_file(
                filename
            )

            print(
                f"Loaded {dataset_name}: "
                f"{datasets[dataset_name].shape}"
            )

        return datasets