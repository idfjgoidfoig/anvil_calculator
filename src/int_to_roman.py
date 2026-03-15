def int_to_roman(num: int):
    int_to_roman = [(1000, "M"), (900, "CM"), (500, "D"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"), ]
    roman_num = ""
    for number, roman in int_to_roman:
        count, num = divmod(num, number)
        roman_num += roman * count
        if num == 0:
            break
    return roman_num
