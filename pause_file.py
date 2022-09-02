class Pause(object):
    def __init__(self, paused=False):
        self.paused = paused
        self.duration = 0
        self.pauseTime = None
        self.func = None

    def update(self, dt):
        if self.pauseTime is not None:
            self.duration += dt
            if self.duration >= self.pauseTime:
                self.duration = 0
                self.paused = False
                self.pauseTime = None
                return self.func
        return None

    def switch(self):
        self.paused = not self.paused

    def setPause(self, playerPaused=False, pauseTime=None, func=None):
        self.duration = 0
        self.func = func
        self.pauseTime = pauseTime
        self.switch()