def sizer_score(predictions: list, expected: list) -> float:
    score = []          # List of bools, 1 if course size was in ideal range, 0 otherwise
    avg_score = 0

    for course in predictions.keys():
        ideal_size_min = expected[course]
        ideal_size_max = expected[course] * 1.1

        if ideal_size_min <= predictions[course] and predictions[course] <= ideal_size_max:
            score.append(1)
        else:
            score.append(0)

    for entry in score:
        avg_score += entry

    avg_score /= len(score)
    avg_score *= 100

    return avg_score


def sequencer_score(predictions: dict, expected: dict) -> float:
    score = []          # List of bools, 1 if course size was in ideal range, 0 otherwise
    avg_score = 0

    for course in predictions.keys():
        for pred_semester_size, actual_semester_size in zip(predictions[course], expected[course]):
            ideal_size_min = actual_semester_size
            ideal_size_max = actual_semester_size * 1.1

            if ideal_size_min <= pred_semester_size and pred_semester_size <= ideal_size_max:
                score.append(1)
            else:
                score.append(0)

    for entry in score:
        avg_score += entry

    avg_score /= len(score)
    avg_score *= 100

    return avg_score
