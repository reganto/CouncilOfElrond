from tornado.web import UIModule


class Pluralize(UIModule):
    def render(self, word: str, count: int) -> str:
        if count > 1:
            return word + "s"
        return word

