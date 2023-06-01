from numpy import double


class ReadTest:
    def __init__(self, filename):
        self.filename = filename

        data = open(filename, 'r')

        self.capacity = double(data.readline())
        self.init_charge = double(data.readline())

        price_schedule_raw = data.readline().split(', ')
        self.price_schedule = [double(x) for x in price_schedule_raw]

        load_schedule_raw = data.readline().split(', ')
        self.load_schedule = [double(x) for x in load_schedule_raw]

        self.constant_load = double(data.readline())
        self.target_charge = double(data.readline())
