import math
from typing import Union, List


class Rational:
    def __init__(self, *args):
        if len(args) == 2:
            n, d = args
            if d == 0:
                raise ValueError("Знаменник не може бути нулем")
        elif len(args) == 1 and isinstance(args[0], str):
            parts = args[0].split('/')
            if len(parts) != 2:
                raise ValueError("Рядок має бути у форматі 'n/d'")
            n, d = map(int, parts)
            if d == 0:
                raise ValueError("Знаменник не може бути нулем")
        else:
            raise ValueError("Невірні аргументи для конструктора Rational")

        common_divisor = math.gcd(abs(n), abs(d))
        self.n = n // common_divisor
        self.d = d // common_divisor

        if self.d < 0:
            self.n *= -1
            self.d *= -1

    def __add__(self, other):
        if isinstance(other, int):
            other = Rational(other, 1)
        if not isinstance(other, Rational):
            raise TypeError("Непідтримуваний тип операнда")

        new_n = self.n * other.d + other.n * self.d
        new_d = self.d * other.d
        return Rational(new_n, new_d)

    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self):
        return f"{self.n}/{self.d}" if self.d != 1 else str(self.n)

    def __repr__(self):
        return f"Rational({self.n}, {self.d})"


class RationalList:
    def __init__(self, data: List[Union[Rational, int]] = None):
        self.data = []
        if data:
            for item in data:
                self.append(item)

    def append(self, item: Union[Rational, int]):
        if isinstance(item, int):
            item = Rational(item, 1)
        if not isinstance(item, Rational):
            raise TypeError("Елемент повинен бути типу Rational або int")
        self.data.append(item)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        if isinstance(value, int):
            value = Rational(value, 1)
        if not isinstance(value, Rational):
            raise TypeError("Елемент повинен бути типу Rational або int")
        self.data[index] = value

    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        new_list = RationalList(self.data.copy())
        if isinstance(other, (Rational, int)):
            new_list.append(other)
        elif isinstance(other, RationalList):
            new_list.data.extend(other.data)
        else:
            raise TypeError("Непідтримуваний тип операнда")
        return new_list

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        if isinstance(other, (Rational, int)):
            self.append(other)
        elif isinstance(other, RationalList):
            self.data.extend(other.data)
        else:
            raise TypeError("Непідтримуваний тип операнда")
        return self

    def __str__(self):
        return str([str(item) for item in self.data])

    def sum(self):
        total = Rational(0, 1)
        for num in self.data:
            total += num
        return total


def parse_numbers_from_file(filename: str) -> RationalList:
    rational_list = RationalList()
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            for part in parts:
                try:
                    if '/' in part:
                        rational = Rational(part)
                    else:
                        rational = Rational(int(part), 1)
                    rational_list.append(rational)
                except ValueError as e:
                    print(f"Помилка при парсингу числа '{part}': {e}")
    return rational_list


def process_files(input_files: List[str]):
    for filename in input_files:
        try:
            print(f"\nОбробка файлу {filename}:")
            numbers = parse_numbers_from_file(filename)
            print(f"Знайдені числа: {numbers}")
            total = numbers.sum()
            print(f"Сума чисел: {total}")

            # Зберігаємо результати у файл
            output_filename = filename.replace('input', 'output')
            with open(output_filename, 'w', encoding='utf-8') as out_file:
                out_file.write(f"Числа з файлу {filename}:\n")
                out_file.write(f"{numbers}\n\n")
                out_file.write(f"Сума чисел: {total}\n")

            print(f"Результати збережено у {output_filename}")
        except FileNotFoundError:
            print(f"Файл {filename} не знайдено")
        except Exception as e:
            print(f"Помилка при обробці файлу {filename}: {e}")


if __name__ == "__main__":
    input_files = ['input02.txt', 'input03.txt', 'input04.txt']
    process_files(input_files)