from tornado.web import UIModule


class StrPlural(UIModule):
    def render(self, word: str, value: int):
        if value > 1:
            return self.render_string(
                'uimodules/str_plural.html',
                word=word+'s')
        return self.render_string('uimodules/str_plural.html', word=word)

