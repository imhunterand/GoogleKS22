# Copyright (c) 2022 imhunterand. All rights reserved.
#
# Google Kick Start 2022 Round B - Problem D. Hamiltonian Tour
# https://codingcompetitions.withgoogle.com/kickstart/round/00000000008caa74/0000000000acf318
#
# Time:  O(R * C), pass in PyPy3 but Python3
# Space: O(R * C)
#

def spanning_tree(B):
    edges = set()
    lookup = [[False]*len(B[0]) for _ in range(len(B))]
    lookup[0][0] = True
    q = [(0, 0)]
    while q:
        new_q = []
        for r, c in q:
            for dr, dc, _ in DIRECTIONS:
                nr, nc = r+dr, c+dc
                if not (0 <= nr < len(B) and 0 <= nc < len(B[0]) and B[nr][nc] == '*' and not lookup[nr][nc]):
                    continue
                lookup[nr][nc] = True
                new_q.append((nr, nc))
                edges.add(((r, c), (nr, nc)) if (r, c) < (nr, nc) else ((nr, nc), (r, c)))
        q = new_q
    return edges

def check(parent, curr, walls):
    if (parent[0]//2, parent[1]//2) != (curr[0]//2, curr[1]//2):
        return True
    if parent[0]%2 == curr[0]%2:
        return (((parent[0]-1)//2, parent[1]//2), ((curr[0]+1)//2, curr[1]//2)) not in walls
    if parent[1]%2 == curr[1]%2:
        return ((parent[0]//2, (parent[1]-1)//2), (curr[0]//2, (curr[1]+1)//2)) not in walls

def wall_follower(B, walls):
    result = []
    r, c = (0, 0)
    i = 3  # facing north at the beginning as we expect to be facing north at the end
    while not (result and (r, c) == (0, 0)):
        for j in reversed(range(i-1, i+2)):  # right-hand rule
            j %= len(DIRECTIONS)
            dr, dc, d = DIRECTIONS[j]
            nr, nc = r+dr, c+dc
            if 0 <= nr < 2*len(B) and 0 <= nc < 2*len(B[0]) and B[nr//2][nc//2] == '*' and check((r, c), (nr, nc), walls):
                break
        r, c = nr, nc
        i = j
        result.append(d)
    return result

def hamiltonian_tour():
    R, C = map(int, input().split())
    B = [input() for _ in range(R)]
    walls = spanning_tree(B)
    result = wall_follower(B, walls)
    return "".join(result) if len(result) == 4*(R*C-sum(row.count('#') for row in B)) else "IMPOSSIBLE"

DIRECTIONS = [(0, 1, 'E'), (1, 0, 'S'), (0, -1, 'W'), (-1, 0, 'N')]
for case in range(int(input())):
    print('Case #%d: %s' % (case+1, hamiltonian_tour()))
