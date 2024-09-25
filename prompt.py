import nltk
from nltk.tokenize import sent_tokenize
from googletrans import Translator

# nltk.download('punkt_tab')


class Prompt():
    def __init__(self,
                 translator: Translator,
                 text: str = " ") -> None:
        self.text: str = text
        self.translator: Translator = translator

    def translate(self):
        self.text = self.translator\
            .translate(
                text=self.text,
                dest="en",
                src="vi"
            ).text

        return self

    def tokenize(self) -> list[str]:
        return sent_tokenize(self.text)
