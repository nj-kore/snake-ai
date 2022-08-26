class Observable:
    def __init__(self):
        self.subscriber_id = 0
        self.subscribers = dict()

    def subscribe(self, func):
        _subscriber_id = self.subscriber_id
        self.subscribers[_subscriber_id] = func
        self.subscriber_id += 1

        def unsubscribe_func():
            del self.subscribers[_subscriber_id]

        return unsubscribe_func

    def notify(self):
        for s in self.subscribers.values():
            s()
