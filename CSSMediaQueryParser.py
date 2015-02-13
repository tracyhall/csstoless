from tinycss.css21 import CSS21Parser

class CSSMediaQueryParser(CSS21Parser):
    def parse_media(self, tokens):
        media = ''.join(value.as_css() for value in tokens)
        return media
