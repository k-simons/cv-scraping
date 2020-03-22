
class RowResult:
    def __init__(self, state: str, total: int, newCases: int, totalDeaths: int, newDeaths: int, totalRecovered: int, activeCases: int):
        self.state = state
        self.total = total
        self.newCases = newCases
        self.totalDeaths = totalDeaths
        self.newDeaths = newDeaths
        self.totalRecovered = totalRecovered
        self.activeCases = activeCases

    def serialize(self):
        return self.__dict__
