from pygameHelper import (
    TileMap,
    CameraObject,
    Surface,
    TimerTask,
    Manger
)

class AnimationTileMap(TileMap):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, tiles, sheet_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name, tiles, sheet_name)
        self.animation = TimerTask(300)
        self.index = 0

    def update(self):
        if self.animation.run_periodic_task():
            self.index += 1
            if self.index == 4:
                self.index = 0

    def render(self, surface: Surface, camera: CameraObject):
        HALF_WIDTH = Manger.WIDTH / (self.size * 2)
        HALF_HEIGHT = Manger.HEIGHT / (self.size * 2)
        tile_camera = camera.location.world_position / self.size
        xrange = int(tile_camera.x - HALF_WIDTH)-1, int(tile_camera.x + HALF_WIDTH) + 2
        yrange = int(tile_camera.y - HALF_HEIGHT)-1, int(tile_camera.y + HALF_HEIGHT) + 2
        for y in range(*yrange):
            for x in range(*xrange):
                tile_n = self.get_tile((x, y))
                if tile_n != None:
                    image = self.canvas[tile_n+self.index]
                    if image != None:
                        cx = (HALF_WIDTH + x) * self.size - camera.location.world_position.x
                        cy = (HALF_HEIGHT - y) * self.size + camera.location.world_position.y
                        surface.blit(image, (cx, cy))