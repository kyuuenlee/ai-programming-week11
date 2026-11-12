def find_max(scores):
    biggest = scores[0]
    for i in range(1, len(scores) - 1):
        if scores[i] > biggest:
            biggest = scores[i]
    return biggest
