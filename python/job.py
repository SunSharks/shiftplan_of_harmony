
"""
CREATE TABLE Jobs (
    id            INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    abs_start     INT,
    abs_end       INT,
    during        INT,
    start_day_id  INT,
    end_day_id    INT,
    dt_start      INT,
    dt_end        INT,
    jt_primary    INT
);"""
class Job:
    def __init__(self, id, jobtype_id, abs_start, abs_end, during, start_day_id, end_day_id, dt_start, dt_end):
        self.id = id
        self.jobtype_id = jobtype_id
        self.abs_start = abs_start
        self.abs_end = abs_end
        self.during = during
        self.start_day_id = start_day_id
        self.end_day_id = end_day_id
        self.dt_start = dt_start
        self.dt_end = dt_end

        #  TODO
        self.nacht = self.translate_linear_time(self.begin)[0] < 8 or self.translate_linear_time(self.end)[0] <8


    def translate_linear_time(self, hour):
        ''' For a given hour in absolute hours, this func returns
        a tuple containing <day, hour>. '''

        lDays = ['Freitag', 'Samstag', 'Sonntag', 'Montag']
        return (hour%24, lDays[hour//24])
