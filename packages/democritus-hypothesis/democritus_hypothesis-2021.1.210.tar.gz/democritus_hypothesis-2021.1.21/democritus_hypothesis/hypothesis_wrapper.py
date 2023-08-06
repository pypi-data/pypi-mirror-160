def hypothesis_get_strategy_results(strategy, *args, n: int = 10, **kwargs):
    """Return the given n of results from the given hypothesis strategy. For a list of hypothesis strategies, see: https://hypothesis.readthedocs.io/en/latest/data.html."""
    from hypothesis import given, settings

    class A(object):
        def __init__(self):
            self.l = []

        @given(strategy(*args))
        @settings(max_examples=n, **kwargs)
        def a(self, value):
            self.l.append(value)

    obj = A()
    obj.a()
    return obj.l
