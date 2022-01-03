class GeneralResponse:
    def __init__(
        self,
        total_positive: int,
        total_recovered: int,
        total_deaths: int,
        total_active: int,
        new_positive: int,
        new_recovered: int,
        new_deaths: int,
        new_active: int,
    ):
        self.total_positive = total_positive
        self.total_recovered = total_recovered
        self.total_deaths = total_deaths
        self.total_active = total_active
        self.new_positive = new_positive
        self.new_recovered = new_recovered
        self.new_deaths = new_deaths
        self.new_active = new_active
