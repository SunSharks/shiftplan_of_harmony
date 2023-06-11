import logging
import csv
import pandas as pd 
from os.path import join


class Upload:

    final_dir = "media"
    tmp_file = "media/tmp"

    def __init__(self, file):
        self.file = file
        self.delimiter = None
        self.df = None
        self.error = ""
        if self.file.name.endswith(".csv"):
            self.run_csv_upload()
            self.write_final_file()
        elif self.file.name.endswith(".xlsx"):
            self.run_xlsx_upload()
            self.write_final_file()
        else:
            ending = self.file.name.split(".")
            if len(ending) == 1:
                ending = ending[0]
                self.error = f"Missing file ending. Missing dot in filename '{ending}'"
                logging.error(self.error)
            else:
                ending = ending[-1]
                self.error = f"File ending '{ending}' not supported."
                logging.error(self.error)


    def get_result_df_or_error(self):
        """
        Returns
            (True, pandas.DataFrame) if self.df exists,
            (False, error_str) otherwise.

        """
        if not self.df is None:
            return (True, self.df)
        else:
            return (False, self.error)


    def run_csv_upload(self):
        for chunk in self.file.chunks():
            self.get_delimiter(str(chunk))
            break
        self.write_tmp()
        self.df = pd.read_csv(self.tmp_file, delimiter=self.delimiter)
        
        
    def run_xlsx_upload(self):
        self.write_tmp()
        self.df = pd.read_excel(self.tmp_file)


    def write_tmp(self):
        with open(self.tmp_file, "wb+") as destination:
                for chunk in self.file.chunks():
                    destination.write(chunk)
       

    def get_delimiter(self, chunk):
        sniffer = csv.Sniffer()
        self.delimiter = sniffer.sniff(chunk).delimiter


    def write_final_file(self):
        with open(join(self.final_dir, self.file.name), "wb+") as destination:
                for chunk in self.file.chunks():
                    destination.write(chunk) 


    def __str__(self):
        if not self.df is None:
            return str(self.df)
        else:
            return f"Upload not possible. {self.error}"
