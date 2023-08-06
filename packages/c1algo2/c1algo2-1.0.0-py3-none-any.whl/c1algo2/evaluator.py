def sizer_score(predictions: list, expected: list) -> float:
    score = []          # List of bools, 1 if course size was in ideal range, 0 otherwise
    avg_score = 0

    for year in range(len(predictions)):
        for course in predictions[year].keys():
            ideal_size_min = expected[year][course]
            ideal_size_max = expected[year][course] * 1.1

            if ideal_size_min <= predictions[year][course] and predictions[year][course] <= ideal_size_max:
                score.append(1)
            else:
                score.append(0)

    for entry in score:
        avg_score += entry

    avg_score /= len(score)
    avg_score *= 100

    return avg_score


def sequencer_score(predictions: list, expected: list) -> float:
    score = []          # List of bools, 1 if course size was in ideal range, 0 otherwise
    avg_score = 0

    for year in range(len(predictions)):
        for course in predictions[year].keys():
            for sem in range(3):
                ideal_size_min = expected[year][course][sem]
                ideal_size_max = expected[year][course][sem] * 1.1

                if ideal_size_min <= predictions[year][course][sem] and predictions[year][course][sem] <= ideal_size_max:
                    score.append(1)
                else:
                    score.append(0)

    for entry in score:
        avg_score += entry

    avg_score /= len(score)
    avg_score *= 100

    return avg_score
