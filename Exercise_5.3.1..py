import math


class Rational:
    def __init__(self, *args):
        if len(args) == 2:  # Два цілих аргументи (чисельник, знаменник)
            n, d = args
            if d == 0:
                raise ValueError("Знаменник не може бути нулем")
        elif len(args) == 1 and isinstance(args[0], str):  # Рядок у форматі 'n/d'
            parts = args[0].split('/')
            if len(parts) != 2:
                raise ValueError("Рядок має бути у форматі 'n/d'")
            n, d = map(int, parts)
            if d == 0:
                raise ValueError("Знаменник не може бути нулем")
        else:
            raise ValueError("Невірні аргументи для конструктора Rational")

        # Скорочення дробу
        common_divisor = math.gcd(abs(n), abs(d))
        self.n = n // common_divisor
        self.d = d // common_divisor

        # Якщо знаменник від'ємний, переносимо мінус до чисельника
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

    def __sub__(self, other):
        if isinstance(other, int):
            other = Rational(other, 1)
        if not isinstance(other, Rational):
            raise TypeError("Непідтримуваний тип операнда")

        new_n = self.n * other.d - other.n * self.d
        new_d = self.d * other.d
        return Rational(new_n, new_d)

    def __mul__(self, other):
        if isinstance(other, int):
            other = Rational(other, 1)
        if not isinstance(other, Rational):
            raise TypeError("Непідтримуваний тип операнда")

        new_n = self.n * other.n
        new_d = self.d * other.d
        return Rational(new_n, new_d)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = Rational(other, 1)
        if not isinstance(other, Rational):
            raise TypeError("Непідтримуваний тип операнда")
        if other.n == 0:
            raise ZeroDivisionError("Ділення на нуль")

        new_n = self.n * other.d
        new_d = self.d * other.n
        return Rational(new_n, new_d)

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return Rational(other, 1).__sub__(self)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        return Rational(other, 1).__truediv__(self)

    def __call__(self):
        return self.n / self.d

    def __getitem__(self, key):
        if key == "n":
            return self.n
        elif key == "d":
            return self.d
        else:
            raise KeyError("Невірний ключ. Допустимі значення: 'n' або 'd'")

    def __setitem__(self, key, value):
        if key == "n":
            self.n = value
        elif key == "d":
            if value == 0:
                raise ValueError("Знаменник не може бути нулем")
            self.d = value
        else:
            raise KeyError("Невірний ключ. Допустимі значення: 'n' або 'd'")

        # Після зміни скорочуємо дріб
        common_divisor = math.gcd(abs(self.n), abs(self.d))
        self.n = self.n // common_divisor
        self.d = self.d // common_divisor

        # Якщо знаменник від'ємний, переносимо мінус до чисельника
        if self.d < 0:
            self.n *= -1
            self.d *= -1

    def __str__(self):
        if self.d == 1:
            return str(self.n)
        return f"{self.n}/{self.d}"

    def __repr__(self):
        return f"Rational({self.n}, {self.d})"


def evaluate_expression(expr_str):
    tokens = expr_str.split()
    if not tokens:
        return None

    # Обробляємо перший токен
    if '/' in tokens[0]:
        current = Rational(tokens[0])
    else:
        current = Rational(int(tokens[0]), 1)

    i = 1
    while i < len(tokens):
        operator = tokens[i]
        next_token = tokens[i + 1]

        if '/' in next_token:
            next_num = Rational(next_token)
        else:
            next_num = Rational(int(next_token), 1)

        if operator == '+':
            current += next_num
        elif operator == '-':
            current -= next_num
        elif operator == '*':
            current *= next_num
        elif operator == '/':
            current /= next_num
        else:
            raise ValueError(f"Невідомий оператор: {operator}")

        i += 2

    return current


def process_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile, \
            open(output_filename, 'w', encoding='utf-8') as outfile:

        for line_num, line in enumerate(infile, 1):
            line = line.strip()
            if not line:
                continue

            try:
                result = evaluate_expression(line)
                decimal_value = result()
                outfile.write(f"Вираз {line_num}: {line}\n")
                outfile.write(f"Результат: {result} (або {decimal_value:.6f})\n\n")
            except Exception as e:
                outfile.write(f"Вираз {line_num}: {line}\n")
                outfile.write(f"Помилка: {str(e)}\n\n")


# Обробка файлів
input_file = 'input01.txt'
output_file = 'output01.txt'

try:
    process_file(input_file, output_file)
    print(f"Результати обчислень збережено у файлі {output_file}")
except FileNotFoundError:
    print(f"Файл {input_file} не знайдено")
except UnicodeDecodeError:
    print("Помилка кодування файлу. Спробуйте перевірити кодування вхідного файлу.")
except Exception as e:
    print(f"Сталася помилка: {e}")