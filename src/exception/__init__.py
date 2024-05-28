import traceback
import os, sys


class CustomException(Exception):
    def __init__(self, error, error_detail):
        self.error = error
        self.error_detail = error_detail
        self.format_error_message()

    def format_error_message(self):
        exc_type, exc_value, exc_traceback = self.error_detail.exc_info()
        filename, line_number, function_name, code = traceback.extract_tb(
            exc_traceback
        )[-1]

        filename = os.path.relpath(filename, os.getcwd())

        self.error_message = f"Exception occurred in [{filename}] at line number [{line_number}] with error: {str(self.error)}"

    def __str__(self):
        return self.error_message
