import sys
from typing import Union
import pandas as pd
import numpy as np
from transparentpath import Path

from adparallelengine import Engine


def dummy_prod(xx):
    return [2 * sx for sx in xx]


def fib(limit):
    """Fibonacci pairs generator"""
    a, b = 0, 1
    while a < limit:
        yield [a, b]
        a, b = b, a + b
        a, b = b, a + b


class Dummy:
    some_attr = 0


def method_in_processes(a):
    Dummy.some_attr = a


def method(
    element: pd.DataFrame,
    some_other_stuff: Union[float, pd.DataFrame, pd.Series, np.ndarray],
    some_float: float,
):
    assert Dummy.some_attr == 1
    to_ret = (
        element * some_other_stuff + some_float + Dummy.some_attr,
        3 * (element * some_other_stuff + some_float + Dummy.some_attr),
    )
    return to_ret


if __name__ == "__main__":

    which = sys.argv[1]
    gather = True if sys.argv[2] == "True" else False
    batched = True if sys.argv[3] == "True" else False if sys.argv[3] == "False" else int(sys.argv[3])
    share = True if sys.argv[4] == "True" else False
    generator = True if sys.argv[5] == "True" else False
    max_cpu = None if sys.argv[6] == "None" else int(sys.argv[6])

    print("which", which)
    print("gather", gather)
    print("batched", batched)
    print("share", share)
    print("generator", generator)
    print("max_cpu", max_cpu)

    if not generator:

        Dummy.some_attr = 1

        dfs = [
            pd.DataFrame([[0, 1], [2, 3]]),
            pd.DataFrame([[4, 5], [6, 7]]),
            pd.DataFrame([[8, 9], [10, 11]]),
            pd.DataFrame([[12, 13], [14, 15]]),
            pd.DataFrame([[16, 17], [18, 19]]),
            pd.DataFrame([[21, 22], [23, 24]]),
        ]
        s = pd.Series([2, 3])
        f = 5.0

        if share is True:
            share_kwargs = {"share": {"some_other_stuff": s}}
        else:
            share_kwargs = {"some_other_stuff": s}
        engine = Engine(kind=which, path_shared=Path("tests") / "data" / "shared", max_workers=max_cpu)
        res = engine(
            method,
            dfs,
            init_method={"method": method_in_processes, "kwargs": {"a": 1}},
            some_float=f,
            gather=gather,
            batched=batched,
            **share_kwargs
        )

        if which != "serial":
            if share is True:
                assert len(list(engine.path_shared.ls())) == 1
            else:
                if engine.path_shared.isdir():
                    assert len(list(engine.path_shared.ls())) == 0
        else:
            assert engine.path_shared is None

        engine.close()
        if which != "serial":
            assert not engine.path_shared.isdir()

        expected = [dfs[int(i / 2)] * s + f + Dummy.some_attr for i in range(0, len(dfs), 2)] + 3 * [
            dfs[int(i / 2)] * s + f + Dummy.some_attr for i in range(0, len(dfs), 2)
        ]
        assert len(expected) == len(res) if gather else len(expected) == 2 * len(res)
        for exp in expected:
            found = False
            for re in res:
                if gather:
                    re = [re]
                for _re in re:
                    try:
                        pd.testing.assert_frame_equal(exp, _re)
                        found = True
                        break
                    except AssertionError:
                        continue
            if found is False:
                raise AssertionError

    else:

        x = fib(25)  # will have 5 elements: (0, 1), (1, 2), (3, 5), (8, 13), (21, 34)
        engine = Engine(kind=which, path_shared=Path("tests") / "data" / "shared", max_workers=max_cpu)
        results = engine(dummy_prod, x, length=5, batched=2 if batched is True else False, gather=gather)
        if which != "serial":
            assert len(list(engine.path_shared.ls())) == 0
        else:
            assert engine.path_shared is None

        if gather:
            results.sort()
            expected = [0, 2, 2, 4, 6, 10, 16, 26, 42, 68]
        else:
            expected = [[0, 2], [2, 4], [6, 10], [16, 26], [42, 68]]
        assert len(expected) == len(results)
        for exp in expected:
            assert exp in results
