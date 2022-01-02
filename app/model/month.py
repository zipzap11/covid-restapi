class MonthResponse:
    def __init__(
        self, moth: str, positive: int, recovered: int, deaths: int, active: int
    ):
        self.moth = moth
        self.positive = positive
        self.recovered = recovered
        self.deaths = deaths
        self.active = active
