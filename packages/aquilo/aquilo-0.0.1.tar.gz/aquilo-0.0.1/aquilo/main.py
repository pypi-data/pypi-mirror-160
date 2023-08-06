import os
from typing import Any, Callable, List, Tuple, Dict

from aquilo.browser.elements.containers import div
from aquilo.html import get_404, build
from aquilo.http import serve, get_patterns, urlpatterns


class Aquilo:
    def __init__(
        self,
        host: str = None,
        ip: str = "127.0.0.1",
        port: int = 8000,
        debug: bool = True,
    ):
        self.host = host
        self.ip = ip
        self.port = port
        self.element_tree = None
        self._pages: Dict[str, Any] = {}
        self.root = None
        self._patterns: List[Tuple[str, Callable]] = list()
        self.debug: bool = debug

    def page(self, function: Callable) -> Callable:
        function_name_with_dashes: str = function.__name__.replace("_", "/").lower()
        name: List[str] = function_name_with_dashes.split("page/")

        if len(name) == 1:
            raise ValueError("Invalid page name.")

        path_name: str = "{}".format(name[1] + "/")

        try:
            path_list: List[str] = path_name.split("/")[:-1]

            if path_list[0] == path_list[1]:
                path_name = path_list[0] + "/"

        except IndexError:
            pass

        self._pages[path_name] = {"function": function}

        pattern: Tuple[str, Callable] = (path_name, function)
        self._patterns.append(pattern)

        return function

    def register_root(self, root: div) -> None:
        if not isinstance(root, div):
            raise TypeError("root must be a div")
        self.root: div = root

    def _application(self, environ, start_response) -> List[bytes]:
        start_response("200 OK", [("Content-Type", "text/html")])

        path: str = environ.get("PATH_INFO", "").lstrip("/")

        if not path.endswith("/"):
            path = path + "/"

        pages: List[str] = list(self._pages.keys())

        if path == "/" or path == "":
            html = self._pages[pages[0]]["function"]().encode()
            return [html]

        for pattern in get_patterns():
            if path in pages:
                html = self._pages[path]["function"]().encode()
                return [html]

        return [get_404()]

    def run(self) -> None:
        urlpatterns(self._patterns)
        serve(self.host, self.ip, self.port, self._application, self.debug)

    def __call__(self, *args, **kwargs):
        print(args, kwargs)
        return self._application(*args)

    def build_html(self, dir_path):
        if os.path.exists(os.path.join(dir_path, "build")):
            import shutil

            shutil.rmtree(os.path.join(dir_path, "build"), ignore_errors=True)

        os.mkdir(os.path.join(dir_path, "build"))

        pages = list(self._pages.keys())

        for page in pages:
            with open(os.path.join(dir_path, "build", f"{page}.html"), "w") as file:
                file.write(build(self._pages[page]["function"], title=page))
