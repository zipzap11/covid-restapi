class DayResponse:
    def __init__(
        self, date: str, positive: int, recovered: int, deaths: int, active: int
    ):
        self.date = date
        self.positive = positive
        self.recovered = recovered
        self.deaths = deaths
        self.active = active
