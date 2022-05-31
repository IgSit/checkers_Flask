import pygame

class DeltaTime():
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.measure = 0
        self.measure_start = False
        self.dt = 0
        self.prev = 0

    def measure_dt(self, ms: int) -> bool:
        self.measure += self.clock.tick()
        if self.measure > ms:
            self.measure = 0
            return True
        if self.measure_start == False:
            self.measure_start = True
            return True
        return False
    
