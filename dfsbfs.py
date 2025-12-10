grid = [
    [0, -1, 0, 0],
    [0, -1, 0, 1],
    [0, -1, 0, 0],
    [0, 0, 0, 0],
]  # 0为可以走，1为终点，-1为不能走


def dfs(grid):
    i = len(grid)
    j = len(grid[0])
    visited = set()

    def get_val(node):
        return grid[node[0]][node[1]]

    def find_neighbour(node):  # node形如(0,0)
        test = [
            (node[0] - 1, node[1]),
            (node[0] + 1, node[1]),
            (node[0], node[1] - 1),
            (node[0], node[1] + 1),
        ]
        ans = []
        for now in test:
            if 0 <= now[0] <= i - 1 and 0 <= now[1] <= j - 1:
                if not now in visited and not get_val(now) == -1:
                    ans.append(now)
        return ans

    stack = []  # 理论上是堆，这里简单用list 堆的值为走到这个点的路径列表
    stack.append([(0, 0)])
    while stack:
        # 一次操作为pop掉最后进来的一个，放入visited，检查是否到终点，放入find_neighbour
        now = stack.pop(-1)
        visited.add(now[0])  # now[0]才是node
        if get_val(now[0]) == 1:
            print("已到达", list(reversed(now)))
            return True
        for nbr in find_neighbour(now[0]):
            stack.append([nbr] + now)
    return False


def bfs(grid):
    i = len(grid)
    j = len(grid[0])
    visited = set()

    def get_val(node):
        return grid[node[0]][node[1]]

    def find_neighbour(node):  # node形如(0,0)
        test = [
            (node[0] - 1, node[1]),
            (node[0] + 1, node[1]),
            (node[0], node[1] - 1),
            (node[0], node[1] + 1),
        ]
        ans = []
        for now in test:
            if 0 <= now[0] <= i - 1 and 0 <= now[1] <= j - 1:
                if not now in visited and not get_val(now) == -1:
                    ans.append(now)
        return ans

    queue = []  # 理论上是队列，这里简单用list 值为走到这个点的路径列表
    queue.append([(0, 0)])
    while queue:
        # 一次操作为pop掉先进来的队首，放入visited，检查是否到终点，放入find_neighbour
        now = queue.pop(0)
        visited.add(now[0])  # now[0]才是node数组
        if get_val(now[0]) == 1:
            print("已到达", list(reversed(now)))
            return True
        for nbr in find_neighbour(now[0]):
            queue.append([nbr] + now)
    return False


print("--bfs--")
print(bfs(grid))
print("--dfs--")
print(dfs(grid))
