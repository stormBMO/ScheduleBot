def weekday_to_int(weekday):
    if weekday == "Понедельник":
        return 1
    if weekday == "Вторник":
        return 2
    if weekday == "Среда":
        return 3
    if weekday == "Четверг":
        return 4
    if weekday == "Пятница":
        return 5
    if weekday == "Суббота":
        return 6

def pair_to_int(pair):
    if pair == "Числитель":
        return 1
    if pair == "Знаменатель":
        return 2
    if pair == "Всегда одинаковые пары":
        return 3