from row_result import RowResult
from typing import List
import json
from datetime import datetime

class SingleScrape:
    def __init__(self, rowResults: List[RowResult]):
        self.rowResults = rowResults
        self.scrapeTime = datetime.utcnow().strftime("%m:%d:%Y,%H:%M:%S")

    def serialize(self):
        result = {}
        json_string = [ob.serialize() for ob in self.rowResults]
        result["rowResults"] = json_string
        result["scrapeTime"] = self.scrapeTime
        return json.dumps(result)
