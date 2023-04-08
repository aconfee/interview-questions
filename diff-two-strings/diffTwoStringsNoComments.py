def diffBetweenTwoStrings(source, target):

    matrix = list(range(0, len(target) + 1))
    for i in range(len(target) + 1):
        matrix[i] = list(range(0, len(source) + 1))
        matrix[i][0] = i

    for t in range(1, len(target) + 1):
        for s in range(1, len(source) + 1):
            if source[s - 1] == target[t - 1]:
                matrix[t][s] = matrix[t - 1][s - 1]
            else:
                matrix[t][s] = 1 + min(matrix[t - 1][s], matrix[t][s - 1])

    res = []
    t = len(target)
    s = len(source)
    while t > 0 and s > 0:
        if source[s - 1] == target[t - 1]:
            res.append(source[s - 1])
            t = t - 1
            s = s - 1
        else:
            if matrix[t][s - 1] < matrix[t - 1][s]:
                res.append("-" + source[s - 1])
                s = s - 1
            else:
                res.append("+" + target[t - 1])
                t = t - 1

    while t > 0:
        res.append("+" + target[t - 1])
        t = t - 1

    while s > 0:
        res.append("-" + source[s - 1])
        s = s - 1

    res.reverse()

    return res
