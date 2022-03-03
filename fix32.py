import re
from decimal import Decimal


class Fix32:
    # Number of decimal bits
    q: int = 16

    def __init__(self, value: str = '0.0') -> None:
        # Validation
        if not isinstance(value, str):
            raise TypeError(f"argument must be str, not {type(value)}")
        match = re.fullmatch(r'^\d+\.\d+', value)
        if not match:
            raise ValueError(
                "argument must contain '.' and at least one integer before and after it"
            )
        self.value = value.lstrip('0').rstrip('0')
        if self.value[0] == '.':
            self.value = '0' + self.value

        # Integer part, Decimal part
        self.i, self.d = self.value.split('.')
        if self.is_overflow():
            raise ValueError(f"Integer part should be less than {2 << __class__.q}")

        # As binary above
        self.bit_i = f'{int(self.i):b}'
        self.bit_d = self._decimal2bit()
        self.bit_fi = f'{self.bit_i}{self.bit_d}'

    def _decimal2bit(self) -> str:
        """To convert decimal into bit

        Returns:
            bit: str
        """
        dec = Decimal(f'0.{self.d}')
        bits = ''
        while dec and len(bits) < __class__.q:
            dec *= 2
            bits += '1' if dec >= 1 else '0'
            dec -= 1 if dec >= 1 else 0
            if not dec: break
        # save the fraction point
        self.fraction = len(bits)
        bits = bits.ljust(__class__.q, '0')
        return bits

    def _bit2decimal(self, bits: str) -> str:
        """To convert bit into decimal

        Returns:
            decimal: str
        """
        decimal = 0
        for i, bit in enumerate(bits, 1):
            i, bit = i*-1, int(bit)
            decimal += (bit * 2**i)
        decimal = str(decimal)[2:]
        return decimal

    def __operand_checker(self, obj: 'Fix32'):
        if not isinstance(obj, __class__):
            raise TypeError("arguments must be the type of 'Fix32'")

    def is_overflow(self) -> bool:
        return int(self.i) > (2 << __class__.q)


    def __add__(self, other: 'Fix32') -> str:
        """Addition"""
        self.__operand_checker(other)
        bits = bin(int('0b' + self.bit_fi, 2) + int('0b' + other.bit_fi, 2))

        # integer part
        integer = bits[:-__class__.q]
        add_i = int(integer, 2)
        # decimal part
        decimal = bits[-__class__.q:]
        add_d = self._bit2decimal(decimal)
        return f'{add_i}.{add_d}'


    def __sub__(self, other: 'Fix32') -> str:
        """Subtraction"""
        self.__operand_checker(other)
        bits = bin(int('0b' + self.bit_fi, 2) - int('0b' + other.bit_fi, 2))

        sign, bits = ('-', bits[3:]) if int(self.i) - int(other.i) < 0 else ('', bits[2:])
        # integer part
        integer = bits[:-__class__.q]
        sub_i = int(integer, 2)
        # decimal part
        decimal = bits[-__class__.q:]
        sub_d = self._bit2decimal(decimal)
        return f'{sign}{sub_i}.{sub_d}'


    def __mul__(self, other: 'Fix32') -> str:
        """Multiplication"""
        self.__operand_checker(other)
        bits = bin(int('0b' + self.bit_fi, 2) * int('0b' + other.bit_fi, 2))[2:]

        fraction = self.fraction + other.fraction
        # integer part
        integer = bits[:-fraction] if len(bits) > fraction else '0'
        mul_i = int(integer, 2)
        # decimal part
        decimal = bits[-fraction:]
        mul_d = self._bit2decimal(decimal)
        return f'{mul_i}.{mul_d}'


    def __truediv__(self, other: 'Fix32') -> str:
        """Division"""
        self.__operand_checker(other)
        q = __class__.q
        bits = bin((int('0b' + self.bit_fi, 2) << q) // int('0b' + other.bit_fi, 2))[2:]

        # integer part
        integer = int(self.i) // int(other.i) if int(self.i) > int(other.i) else 0
        div_i = integer
        # decimal part
        decimal = bits[-q:] if len(bits) >= q else bits.rjust(q, '0')[-q:]
        div_d = self._bit2decimal(decimal)
        return f'{div_i}.{div_d}'
