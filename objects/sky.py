from pygameHelper import GameObject, TimerTask

from objects.cloud import Cloud

import random

class Sky(GameObject):
    def __init__(self, pos):
        super().__init__("sky", 3, "sky", True, [0, 0], 0, "parent")
        self.wait = TimerTask(1000)

        for i in range (20):
            cloud = Cloud("cloud", 2, "cloud", True, [random.random()*4000-2300, 500+random.choice([25, -25, -50])], 0, "parent", random.choice([0, 1, 2]), random.choice([1, 0.7, 0.5]))
            cloud.init_instantiate()
    
    def update(self):
        if self.wait.run_periodic_task():
            cloud = Cloud("cloud", 2, "cloud", True, [-1500, 500+random.choice([25, -25, -50])], 0, "parent", random.choice([0, 1, 2]), random.choice([1, 0.7, 0.5]))
            cloud.instantiate()
            self.wait.tick = random.choice([4000, 8000, 5000])