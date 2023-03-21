
def calc_trains(max_reps: int):
    percent_per_workout = 0.07 # процент увеличения максимума на каждой тренировке
    trains = [[], [], []]
    # расчет тренировок
    for i in range(1, 4):  # три тренировки по 5 подходов
        reps = int((max_reps / 2) * (1 + i * percent_per_workout))  # количество повторений на первом подходе
        trains[i-1].append(reps)
        for j in range(1, 5):  # четыре следующих подхода с уменьшением количества повторений на 10%
            reps = int(reps * 0.9)
            trains[i-1].append(reps)
        max_reps *= (1 + percent_per_workout)

    return trains
