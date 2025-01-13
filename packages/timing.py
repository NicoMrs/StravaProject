# timing.py

from datetime import datetime, timedelta


class Date:
    """ Class that define a datetime """

    TOL = 12 * 60 * 60  # half a day tolerance
    TRAINING_DURATION = 16 # weeks

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

        self._date = datetime(year=self.year, month=self.month, day=self.day)

    @property
    def timestamp(self):
        """ Convert datetime object into a timestamp """
        return int(round(self._date.timestamp()))

    @property
    def start_training(self):
        """ returns start training date """
        date = self._date - timedelta(weeks=16)
        return type(self)(year=date.year, month=date.month, day =date.day)

    @property
    def tolerance_up(self):
        return self.timestamp + self.TOL

    @property
    def tolerance_down(self):
        return self.timestamp - self.TOL

    def __repr__(self):
        return f"{type(self).__name__}(day={self.day!r}, month={self.month!r}, year={self.year!r})"


if __name__ == '__main__':
    hamburg = Date(2022, 4, 24)
    print(hamburg.tolerance_up, hamburg.tolerance_down)

