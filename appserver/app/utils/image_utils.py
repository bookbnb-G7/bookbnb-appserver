import itertools

class IdGenerator:
    gen = itertools.count()

    @staticmethod
    def generate() -> int:
        return next(IdGenerator.gen)
