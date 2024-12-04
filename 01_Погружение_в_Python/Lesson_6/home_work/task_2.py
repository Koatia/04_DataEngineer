SIZE = 8
A = [0] * SIZE  # Array solution
s = 0  # Global variable to count 'solutions', you can delete it!
t = 0  # Global variable to count recursion 'tests', you can delete it!

def test(queen, col):
    global t
    t += 1
    for i in range(1, queen):
        if (A[queen - i - 1] == col): return 0  # Test vertical
        if (A[queen - i - 1] == col - i): return 0  # Test diagonal 1 (\)
        if (A[queen - i - 1] == col + i): return 0  # Test diagonal 2 (/)
    return 1

def play(queen):
    global s
    for col in range(1, SIZE + 1):
        if (test(queen, col)):  # If I can play the queen...
            A[queen - 1] = col  # Add queen to the solution Array
            if (queen == SIZE):  # If the last queen was played, this is a solution
                s += 1
                print("Solution: {}, {}, {}".format(s, t, A))
            else:
                play(queen + 1)  # If not last queen, play the next one
            A[queen - 1] = 0  # Clean the solution Array

play(1)  # Start putting first queen
