from irsdk import IRSDK

class IRacingDataFetcher:
    def __init__(self, sdk: IRSDK):
        self.sdk = sdk

    def get_all_values(self) -> dict:
        """
        מחזיר את כל המשתנים הפעילים כ-dict
        """
        data = {}
        for var_name in self.sdk.var_headers:
            try:
                value = self.sdk.get_var(var_name)
                data[var_name] = value
            except Exception:
                continue
        return data

    def get_values_by_prefix(self, prefix: str) -> dict:
        """
        מחזיר רק משתנים שמתחילים ב-prefix מסוים (למשל "Car", "Session")
        """
        data = {}
        for var_name in self.sdk.var_headers:
            if var_name.startswith(prefix):
                try:
                    value = self.sdk.get_var(var_name)
                    data[var_name] = value
                except Exception:
                    continue
        return data

    def get_single_value(self, name: str):
        """
        מחזיר משתנה בודד אם קיים
        """
        try:
            return self.sdk.get_var(name)
        except Exception:
            return None
