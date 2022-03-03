import unittest
from decimal import Decimal
from fix32 import Fix32


def is_close(fix: str, fl: float) -> bool:
    d1 = Decimal(fix)
    d2 = Decimal(f'{fl}')
    return round(d1 / d2) == 1


class TestFix32(unittest.TestCase):
    def setUp(self) -> None:
        self.f = open('./tests/dataset.csv', 'r')
        self.units = self.f.readlines()

    def tearDown(self) -> None:
        return self.f.close()

    def test_addition(self) -> None:
        print('---addition---')
        for unit in self.units:
            a, b = list(map(lambda x: x.strip(), unit.split(',')))
            # Fixed Point
            fi = Fix32(a) + Fix32(b)
            # Float Point
            fl = float(a) + float(b)
            assert is_close(fi, fl)

    def test_subtraction(self) -> None:
        print('---substraction---')
        for unit in self.units:
            a, b = list(map(lambda x: x.strip(), unit.split(',')))
            fi = Fix32(a) - Fix32(b)
            fl = float(a) - float(b)
            assert is_close(fi, fl)

    def test_multiplication(self) -> None:
        print('---multiplication---')
        for unit in self.units:
            a, b = list(map(lambda x: x.strip(), unit.split(',')))
            fi = Fix32(a) * Fix32(b)
            fl = float(a) * float(b)
            assert is_close(fi, fl)

    def test_division(self) -> None:
        print('---division---')
        for unit in self.units:
            a, b = list(map(lambda x: x.strip(), unit.split(',')))
            fi = Fix32(a) / Fix32(b)
            fl = float(a) / float(b)
            assert is_close(fi, fl)


if __name__ == '__main__':
    unittest.main()
