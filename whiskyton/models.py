class Whisky:
    def __init__(self, distillery, slug, tastes):
        self.distillery = distillery
        self.slug = slug
        self.tastes = tastes


class Correlation:
    def __init__(self, reference, other, value, chart):
        self.reference = Whisky(*reference)
        self.other = Whisky(*other)
        self.value = value
        self.chart = chart
