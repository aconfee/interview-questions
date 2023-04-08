"""
Given two strings of uppercase letters source and target, list (in string form) a sequence of
edits to convert from source to target that uses the least edits possible.
"""


def getMatrix(source, target):
    """
    This matrix can be constructed in any order. Top left to bottom right, bottom right to top left,
    top right to bottom left, bottom left to top right. It literally doesn't matter and will give me
    an optimal solution, it just changes what position the final solution is in. Order doesn't matter
    because the sub-problems calculated in each respective position are always the same anyway.

    When I construct / backtrack my solution after this matrix gen step, I must start from the solution
    index in order to reconstruct the optimal path. 

    I only mention this because pramp is a bitch about the order they want the solution returned in,
    and the items returned are stateful, so that specific solution requires a bottom-up matrix gen
    (bottom right to top left) so that construction can happen from the start of the strings in the
    top left, and go in left to right string order.

    Or, do like me and hack it by reversing the strings instead of all the construction steps. Just 
    mentioning to realize there's nothing magic about constructing one way or another, just know 
    the relationship between where the solution ends up, retracing from it, and the source and target
    provided.
    """

    # vertical (left) target
    matrix = list(range(0, len(target) + 1))

    # horizontal (top) source
    for i in range(len(target) + 1):
        matrix[i] = list(range(0, len(source) + 1))
        matrix[i][0] = i

    # populate matrix
    # matrix is going to be the cound of edits required, since we're finding minimum edits
    for t in range(1, len(target) + 1):  # vertical movement
        for s in range(1, len(source) + 1):  # horizontal movement

            # if match, no edit required, so take previous edits required
            if source[s - 1] == target[t - 1]:
                matrix[t][s] = matrix[t - 1][s - 1]
            # if not match, take least number of edits so far, plus one new additional edit
            else:
                matrix[t][s] = 1 + min(matrix[t - 1][s], matrix[t][s - 1])

    return matrix


def diffBetweenTwoStrings(a, b):
    """
    @param source: str
    @param target: str
    @return: str[]
    """

    """
    hack to match their bottom-up approach without actually reversing
    construction order of matrix and solution. Just to match pramp and
    pass all tests.
    *** will also need to do <= comparison below on line 86 to match exactly
    and don't reverse solution.
    """
    # source = a[::-1]
    # target = b[::-1]

    matrix = getMatrix(source, target)

    # backtrack solution
    res = []
    t = len(target)
    s = len(source)
    while t > 0 and s > 0:

        # if match, take unedited letter and continue to next sub problem (diagonal)
        # diagonal is optimal path because no edit required
        if source[s - 1] == target[t - 1]:
            # arbitrarily choosing source, could be target since match.
            res.append(source[s - 1])
            t = t - 1
            s = s - 1

        # if not match, take path with least number of edits
        else:

            # if source least edits, take "-[source]" and go left (keep iterating)
            # per requirements, prefer omitting from source over adding to target
            if matrix[t][s - 1] < matrix[t - 1][s]:
                res.append("-" + source[s - 1])
                s = s - 1

            # if target least edits, take "+[target]" and go up (break horizontal iteration)
            else:
                res.append("+" + target[t - 1])
                t = t - 1

        """
        the reason for +[left] and -[top] instead of -[left] and +[top] is because this question
        is asking for edits to source to become target, not the other way around. Everything with
        respect to source.
        """

    # apply remaining edits if one string exists
    while t > 0:
        res.append("+" + target[t - 1])
        t = t - 1

    while s > 0:
        res.append("-" + source[s - 1])
        s = s - 1

    res.reverse()

    return res


def run_test(source, target, solution):
    edit_count = sum(
        1 for i in solution if i.find("+") > -1 or i.find("-") > -1)

    min_edit_count = getMatrix(source, target)[len(target)][len(source)]
    if min_edit_count == edit_count:
        print("✅ edit distance")
    else:
        print("❌ edit distance")
        print("Expected:")
        print(edit_count)
        print("Actual:")
        print(min_edit_count)

    my_solution = diffBetweenTwoStrings(source, target)
    if my_solution == solution:
        print("✅ edit solution")
    else:
        print("❌ edit solution")
        print("Expected:")
        print(solution)
        print("Actual:")
        print(my_solution)


def print_title(title):
    print("####################")
    print("## " + title)
    print("####################")


print("Running...")

# test that min edits needed are all correct (correct matrix)

print_title("TEST 1")
source = "ABCDEFG"
target = "ABDFFGH"
solution = ["A", "B", "-C", "D", "-E", "F", "+F", "G", "+H"]
run_test(source, target, solution)

print_title("TEST 2")
source = "CCBC"
target = "CCBC"
solution = ["C", "C", "B", "C"]
run_test(source, target, solution)

print_title("TEST 3")
source = "CBBC"
target = "CABAABBC"
solution = ["C", "+A", "B", "+A", "+A", "B", "+B", "C"]
run_test(source, target, solution)

print_title("TEST 4")
source = "CABAAABBC"
target = "CBBC"
solution = ["C", "-A", "B", "-A", "-A", "-A", "B", "-B", "C"]
run_test(source, target, solution)

print_title("TEST 5")
source = "AABACC"
target = "BABCAC"
solution = ["-A", "-A", "B", "A", "+B", "C", "+A", "C"]
run_test(source, target, solution)

print_title("TEST 6")
source = "HMXPHHUM"
target = "HLZPLUPH"
solution = ["H", "-M", "-X", "+L", "+Z", "P",
            "-H", "-H", "+L", "U", "-M", "+P", "+H"]
run_test(source, target, solution)

print_title("TEST 7")
source = "GHMXGHUGXL"
target = "PPGGXHHULL"
solution = ["+P", "+P", "G", "-H", "-M", "-X", "G",
            "+X", "H", "+H", "U", "-G", "-X", "L", "+L"]
run_test(source, target, solution)

print_title("TEST 8")
source = "GMMGZGGLUGUH"
target = "HPGPPMGLLUUU"
solution = ["+H", "+P", "G", "-M", "+P", "+P", "M", "G",
            "-Z", "-G", "-G", "L", "+L", "U", "-G", "U", "-H", "+U"]
run_test(source, target, solution)

print("Stopping...")
