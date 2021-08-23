class Observable:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, func):
        self.subscribers.append(func)

    def notify(self):
        for s in self.subscribers:
            s()
