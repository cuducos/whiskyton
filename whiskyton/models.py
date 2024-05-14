from collections import namedtuple

Correlation = namedtuple("Correlation", "value distillery chart")


class Whisky:
    def __init__(self, distillery, slug, tastes, correlations):
        self.distillery = distillery
        self.slug = slug
        self.tastes = tastes

        correlations = correlations or tuple()
        self.correlations = tuple(Correlation(*args) for args in correlations)
