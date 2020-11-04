from queue import Queue
import time
import random

class NQueens:
    def __init__(self, size):
        self.size = size

    def dfs(self):
        begin = time.time()
        solutions = []
        stack = [[]]
        while stack:
            solution = stack.pop()
            # if self.conflict(solution):
            #     continue
            row = len(solution)
            print(solution)
            if row == self.size:
                solution = self.find_solution(solution)
                solutions.append(solution)
                continue # Lay het tat ca dap an
                # break # Lay 1 dap an dau tien
            for col in range(self.size):
                queen = (row, col)
                if not self.conflict_first(queen, solution):
                    queens = solution.copy()
                    queens.append(queen)
                    stack.append(queens)

        end = time.time()
        t = end - begin
        return (solutions, t)

    def bfs(self):
        begin = time.time()
        solutions = []
        queue = Queue()
        queue.put([])
        while not queue.empty():
            solution = queue.get()
            # if self.conflict(solution):
            #     continue
            row = len(solution)
            print(solution)
            if row == self.size:
                solution = self.find_solution(solution)
                solutions.append(solution)
                continue # Lay het tat ca dap an
                # break # Lay 1 dap an dau tien
            for col in range(self.size):
                queen = (row, col)
                if not self.conflict_first(queen, solution):
                    queens = solution.copy()
                    queens.append(queen)
                    queue.put(queens)

        end = time.time()
        t = end - begin
        return (solutions, t)

    def conflict(self, queens):
        for i in range(1, len(queens)):
            a, b = queens[i]
            for j in range(0, i):
                c, d = queens[j]
                if a == c or b == d or abs(a - c) == abs(b - d):
                    return True
        return False

    def conflict_first(self, queen, queens):
        a, b = queen
        for i in range(0, len(queens)):
            c, d = queens[i]
            if a == c or b == d or abs(a - c) == abs(b - d):
                return True
        return False

    def createRandomBoard(self):
        queens = []
        for row in range(self.size):
            randomCol = random.randint(0, self.size - 1)
            queen = (row, randomCol)
            queens.append(queen)
        return queens

    def find_solution(self, queens):
        sol = []
        for i in range(self.size):
            pos = 0
            for j in range(self.size):
                if (i, j) in queens:
                    sol.append(pos)
                pos += 1
        return sol

    def print_solution(self, queens):
        print(queens)

    def find_conflicts(self, solution):
        return [self.hits(solution, col, solution[col]) for col in range(self.size)]

    def hits(self, solution, col, row):
        """ Hàm trả về tổng conflict của 1 cột 
        Solution: Mảng chứa solution cần giải
        col: cột đang xét
        row: hàng của cột đang xét
        """
        total = 0
        for index in range(self.size):
            if index == col:
                continue  #Không xét cột của nó
            if solution[index] == row or abs(index - col) == abs(solution[index] - row):  #cùng hàng hoặc đường chéo
                total += 1
        return total

    def min_conflict(self, solution, iters=1000):
        def random_pos(lst, func):
            return random.choice([i for i in range(self.size) if func(lst[i])])

        for i in range(iters):
            confs = self.find_conflicts(solution)
            if sum(confs) == 0:
                return solution
            col = random_pos(confs, lambda element: element > 0)
            vconfs = [self.hits(solution, col, row) for row in range(self.size)]
            solution[col] = random_pos(vconfs, lambda element: element == min(vconfs))

    def heuristic(self):
        begin = time.time()
        board = self.createRandomBoard()
        pre_solution = self.find_solution(board)
        solutions = self.min_conflict(pre_solution)
        end = time.time()
        t = end - begin
        return ([solutions], t)


def choose():
    print("What algorithm do you want to run?")
    print("1: Depth first search")
    print("2: Breadth first search")
    print("3: Heuristic (Min-Conflict)")
    a = input('Please enter algorithm: ')
    #Check if the input given is an integer
    if a.isdigit():
        a = int(a)
        if a == 1 or a == 2 or a == 3:
            return a
        print("ERROR: Invalid Input")
        return choose()
    #If no input is given, use the default 1
    elif input == "":
        return 1
    else:
        print("ERROR: Invalid Input")
        return choose()


def confirm(method, n = None):
    print("Do you want to run again? Please enter Y/N")
    a = input()
    #Check if the input given is Y or N
    if a == "Y" or a == "y":
        return init(method)
    #Also accept an empty string in place of N
    elif (a == "N" or a == "n" or a == "") and n < 4:
        exit(1)
    elif (a == "N" or a == "n" or a == "") and (method == 1 or method == 2):
        return n
    print("ERROR: Invalid Input")
    return confirm(method)


def init(method):
    n = input('Please enter number of queens: ')
    #Check if the input given is an integer
    if n.isdigit():
        n = int(n)
        if n < 4:
            print("ERROR: A solution is not available for this few number of queens")
            return confirm(method, n)
        elif n > 14 and method == 1:
            print("WARNING: This solution would take too long to calculate, and your computer would probably run out of memory!")
            return confirm(method, n)
        elif n > 29 and method == 2:
            print("WARNING: This solution would take too long to calculate, and your computer would probably run out of memory!")
            return confirm(method, n)
        else:
            return n
    #If no input is given, use the default 8
    elif n == "":
        return 8
    else:
        print("ERROR: Invalid Input")
        return confirm(method)


def main():
    method = choose()
    n = init(method)
    n_queens = NQueens(n)
    if method == 1:
        solutions, t = n_queens.dfs()
    elif method == 2:
        solutions, t = n_queens.bfs()
    elif method == 3:
        solutions, t = n_queens.heuristic()

    for i, solution in enumerate(solutions):
        print('Solution %d:' % (i + 1))
        n_queens.print_solution(solution)

    print("\nTime running:", t)

    file = "./log.txt"
    fo = open(file, "a")
    fo.write("Algorithm: " + str(method) + ". Number of: " + str(n) + ". Time: " + str(t) + "s\n")


if __name__ == '__main__':
    main()
