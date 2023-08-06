from typing import Union, Iterable

from aquilo.browser.elements import Element
from aquilo.html.generators import generate_dom_tree


class div(Element):
    def __init__(
        self,
        *args: Union[Iterable, Element],
    ):
        etype = self.__class__.__name__
        super().__init__(etype)
        self.elements = args

    def get_elements(self):
        return self.elements

    def __call__(self, *args, **kwargs):
        return generate_dom_tree(self.elements)
