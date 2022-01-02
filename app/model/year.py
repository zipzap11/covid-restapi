class YearResponse:
    def __init__(
        self, year: str, positive: int, recovered: int, deaths: int, active: int
    ):
        self.year = year
        self.positive = positive
        self.recovered = recovered
        self.deaths = deaths
        self.active = active
