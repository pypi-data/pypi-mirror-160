from aquilo.browser.elements import Element


class Text(Element):
    def __init__(
        self,
        etype: str,
        text: str,
        eid: str = None,
    ):
        super().__init__(etype, text, eid)


class h1(Text):
    def __init__(
        self,
        text: str,
        eid: str = None,
    ):
        super().__init__(self.__class__.__name__, text, eid)


class h2(Text):
    def __init__(
        self,
        text: str,
        eid: str = None,
    ):
        super().__init__(self.__class__.__name__, text, eid)


class h3(Text):
    def __init__(
        self,
        text: str,
        eid: str = None,
    ):
        super().__init__(self.__class__.__name__, text, eid)


class h4(Text):
    def __init__(
        self,
        text: str,
        eid: str = None,
    ):
        super().__init__(self.__class__.__name__, text, eid)


class h5(Text):
    def __init__(
        self,
        text: str,
        eid: str = None,
    ):
        super().__init__(self.__class__.__name__, text, eid)


class h6(Text):
    def __init__(
        self,
        text: str,
        eid: str = None,
    ):
        super().__init__(self.__class__.__name__, text, eid)


class p(Text):
    def __init__(
        self,
        text: str,
        eid: str = None,
    ):
        super().__init__(self.__class__.__name__, text, eid)


class strong(Text):
    def __init__(
        self,
        text: str,
        eid: str = None,
    ):
        super().__init__(self.__class__.__name__, text, eid)


class small(Text):
    def __init__(
        self,
        text: str,
        eid: str = None,
    ):
        super().__init__(self.__class__.__name__, text, eid)


class a(Text):
    def __init__(
        self,
        text: str,
        href: str,
        eid: str = None,
    ):
        super().__init__(self.__class__.__name__, text, eid)
        self.href = href

    def __call__(self, *args, **kwargs):
        return f'<{self.etype} href="{self.href}">{self.innerHTML}</{self.etype}>'
