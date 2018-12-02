class linear:
    def __init__(self, dots):
        dot_size = len(dots)
        avgx = sum([dots[i][0] for i in range(dot_size)]) / dot_size
        avgy = sum([dots[i][1] for i in range(dot_size)]) / dot_size

        upper = -(dot_size) * avgx * avgy
        upper += sum([dots[i][0] * dots[i][1] for i in range(dot_size)])
        down = -(dot_size) * avgx * avgx
        down += sum([dots[i][0] ** 2 for i in range(dot_size)])

        self.D = (upper / down)
        self.C = (avgy - self.D * avgx)
        self.avgx = avgx
        self.avgy = avgy

    def get(self, x):
        return self.D * x + self.C

    def get_avg(self):
        return self.avgx, self.avgy
