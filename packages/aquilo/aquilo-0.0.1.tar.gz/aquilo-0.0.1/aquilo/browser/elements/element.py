class Element:
    def __init__(self, etype: str, text: str = None, eid: str = None):
        self.etype = etype
        self.hidden: bool = False
        self.eid: str = eid
        self.innerHTML: str = text
        self.innerText: str = text
        self.tagName: str = etype.upper()
        self.title: str = ""

    def __call__(self, *args, **kwargs):
        return f"<{self.etype}>{self.innerHTML}</{self.etype}>"
