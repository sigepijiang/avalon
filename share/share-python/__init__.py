#-*- coding: utf-8 -*-


class AppStack(list):
    def push(self, value):
        self.append(value)
        return value

    def pop(self):
        if not self:
            return None
        return self.pop(0)

    def __call__(self):
        if not self:
            raise RuntimeError('No APP!')
        return self[0]

app_stack = AppStack()
