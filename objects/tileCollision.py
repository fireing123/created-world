from pygameHelper import TileMap, Rect

from pygameHelper.objects.components.physics import physics_grounds

from collections import deque

class CollisionTile(TileMap):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, tiles, sheet_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name, tiles, sheet_name)
        self.map_to_list()

    # 원점은 2사분변 1칸으로 

    def map_to_list(self):
        xcenter = max(max(self.tiles[1], key=lambda x: len(x)), max(self.tiles[2], key=lambda x: len(x)), key=lambda x: len(x)).__len__()-1
        xl = max(max(self.tiles[0], key=lambda x: len(x)), max(self.tiles[3], key=lambda x: len(x)), key=lambda x: len(x)).__len__() + xcenter
        ycenter = max(self.tiles[0], self.tiles[1], key=lambda x: len(x)).__len__()-1
        yl = max(self.tiles[2], self.tiles[3], key=lambda x: len(x)).__len__() + ycenter
        
        arr = [[None] * (xl+1) for i in range(yl+1)]
        tile0 = self.tiles[0].copy()
        tile1 = self.tiles[1].copy()
        tile2 = self.tiles[2].copy()
        tile3 = self.tiles[3].copy()

        for i in range(len(tile0)):
            for j in range(len(tile0[i])):
                arr[ycenter - i][xcenter + j+1] = tile0[i][j]

        for i in range(len(tile1)):
            for j in range(len(tile1[i])):
                arr[ycenter - i][xcenter - j] = tile1[i][j]

        for i in range(len(tile2)):
            for j in range(len(tile2[i])):
                arr[ycenter + i+1][xcenter - j] = tile2[i][j]

        for i in range(len(tile3)):
            for j in range(len(tile3[i])):
                arr[ycenter + i+1][xcenter + j+1] = tile3[i][j]
        visit = [[False] * len(arr[0]) for i in range(len(arr))]

        for i in range(len(arr)):
            for j in range(len(arr[0])):
                if arr[i][j] != None:
                    bfs(arr, j, i, visit)

        for rx in range(len(arr[0])):
            bef = False
            h = self.size
            for ry in range(len(arr)):
                if arr[ry][rx] == -1:
                    if bef:
                        h += self.size
                    else:
                        bef = True
                else:
                    if bef:
                        rect = Rect((rx-xcenter-1) * self.size, -(ry-ycenter-1) * self.size, self.size, h)
                        physics_grounds.append(rect)
                        bef = False
                        h = self.size

    def render(self, surface, camera):
        super().render(surface, camera)
        #for gr in self.grounds:
        #    ne = gr.copy()
        #    x, y = ne.center
        #    y = Manger.HEIGHT - y
        #    ne.center = camera((x, y))
        #    pygame.draw.rect(surface, (127, 127, 127), ne)

def visible(arr):
    for i in arr:
        for j in i:
            if j == None:
                print(" ", end="")
            else:
                print(j, end="")
        print()
dx = [0, 0, -1, 1]
dy = [-1, 1, 0, 0]

def bfs(arr, x, y, visit):
    queue = deque([(x, y)])

    while queue:
        xx, yy = queue.popleft()
        check_air = False
        for i in range(4):
            nx = dx[i] + xx
            ny = dy[i] + yy

            if 0 <= nx < len(arr[0]) and 0 <= ny < len(arr):
                if not visit[ny][nx]:
                    visit[ny][nx] = True
                    if arr[ny][nx] != None:
                        queue.append((nx, ny))
                if arr[ny][nx] == None:
                    check_air = True
        if check_air:
            arr[y][x] = -1
