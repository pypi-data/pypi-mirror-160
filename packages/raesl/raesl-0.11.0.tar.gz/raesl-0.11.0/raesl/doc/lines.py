"""Module to generate text lines that describe ESL objects."""

from typing import Dict, Generator, Iterable, List, Optional

from raesl.doc.locales import _, hookspec, pm
from ragraph.graph import Graph
from ragraph.node import Node

LineGen = Generator[str, None, None]


class Hookspecs:
    @hookspec(firstresult=True)
    def linguistic_enumeration(items: List[str]) -> str:
        """Get a natural language enumeration of items."""

    @hookspec(firstresult=True)
    def linguistic_options(items: List[str]) -> str:
        """Get a natural language enumeration of options."""

    @hookspec(firstresult=True)
    def function_spec_node(node: Node, graph: Graph) -> LineGen:
        """Yield the function spec in natural language."""

    @hookspec(firstresult=True)
    def design_spec_node(node: Node, graph: Graph) -> LineGen:
        """Yield the design spec in natural language."""

    @hookspec(firstresult=True)
    def behavior_spec_node(node: Node, graph: Graph) -> LineGen:
        """Yield the behavior spec in natural language."""

    @hookspec(firstresult=True)
    def need_node(node: Node, graph: Graph) -> LineGen:
        """Yield the need spec in natural language."""


pm.add_hookspecs(Hookspecs)
hook = pm.hook


def hs(h: int):
    """Get header pound (#) signs."""
    return h * "#"


def header(h: int, text: str, capitalize: bool = True) -> str:
    """Get a header with surrounding whitespace and optional capitalization."""
    if capitalize:
        text = cap(text)
    return "\n\n{} {}\n\n".format(hs(h), text)


def boldhead(text: str, capitalize: bool = True, newlines: bool = True) -> str:
    """Get a bold header (without numbering) with surrounding whitespace."""
    if capitalize:
        text = cap(text)

    text = bold(text)

    if newlines:
        text = "\n{}\n".format(text)

    return text


def emph(text: str) -> str:
    """Return text as emphasized (Markdown)."""
    return "*{}*".format(text.strip())


def cap(text: str) -> str:
    """Capitalize first char of text."""
    return text[0].upper() + text[1:]


def bold(text: str) -> str:
    """Return text as bold (markdown)."""
    return "**{}**".format(text.strip())


def snt(text: str) -> str:
    """Text to a sentence. Capitalizes first character and adds a period."""
    if not text.endswith("."):
        text += "."
    return cap(text)


def ordered(items: Iterable[str], indent: int = 0) -> LineGen:
    """Generate an ordered Markdown list."""
    yield ""
    for item in items:
        if type(item) == str:
            yield "{}1. {}".format(indent * " ", item)  # Markdown handles numbering.
        else:
            yield from ordered(item, indent=2)
    if indent == 0:
        yield "\n<!-- end of list -->\n"  # Ensures list is ended here.


def unordered(items: Iterable[str], indent: int = 0) -> LineGen:
    """Generate an unordered Markdown list."""
    yield ""
    for item in items:
        if type(item) == str:
            yield "{}* {}".format(indent * " ", item)
        else:
            yield from unordered(item, indent=2)
    if indent == 0:
        yield "\n<!-- end of list -->\n"  # Ensures list is ended here.


def image(
    path: str,
    caption: Optional[str] = None,
    label: Optional[str] = None,
    sizing: Optional[str] = None,
) -> str:
    """Get Pandoc Markdown for an image."""
    line = "\n\n![{}]({})".format(caption, path)
    attrs = ""
    if label:
        attrs += "#fig:{}".format(label)
    if sizing:
        attrs += " {}".format(sizing)
    if attrs:
        line += "{" + attrs + "}"
    return line + "\n\n"


def node_path(
    path: str, italic: bool = False, arrows: bool = True, skip: str = "world"
):
    """Get a friendly representation of a node path."""
    skips = skip.split(".")
    for skip in skips:
        if path.startswith(skip):
            idx = len(skip) + 1
            path = path[idx:]
        else:
            break

    if arrows:
        path = path.replace(".", " &rarr; ")
    path = path.strip()
    if italic:
        return "*" + path + "*"
    else:
        return path


def bundle_path(
    path: str, root: str, italic: bool = False, arrows: bool = True, skip: str = "world"
):
    """Get a friendly representation of a bundle path."""
    path_parts = path.split("." + root + ".")

    if path_parts[0] in skip:
        path = root + "." + path_parts[-1]
    else:
        path = (
            node_path(path=path_parts[0] + ".", italic=False, arrows=arrows, skip=skip)
            + " "
            + root
            + "."
            + path_parts[-1]
        )

    return "*" + path + "*" if italic else path


def var_path(v: Node, italic: bool = False, arrows: bool = True, skip: str = "world"):
    """Get a friendly representation of a variable path."""
    if v.annotations.esl_info.get("bundle_root_name"):
        return bundle_path(
            path=v.name,
            root=v.annotations.esl_info["bundle_root_name"],
            arrows=arrows,
            skip=skip,
            italic=italic,
        )
    else:
        return node_path(v.name, italic=italic, arrows=arrows, skip=skip)


def var_clarification(bvars: List[Node]):
    """Yield variable clarification section."""
    if len(bvars) == 1:
        yield "\n"
        yield snt(
            _("where the full name of variable {} is {}").format(
                bvars[0].name.split(".")[-1],
                bundle_path(
                    path=bvars[0].name,
                    root=bvars[0].annotations.esl_info["bundle_root_name"],
                ),
            )
        )
    elif len(bvars) > 1:
        yield "\n"
        yield cap(_("where, respectively:"))
        yield from unordered(
            [
                _("variable {} has full name {}").format(
                    v.name.split(".")[-1],
                    bundle_path(
                        path=v.name,
                        root=v.annotations.esl_info["bundle_root_name"],
                    ),
                )
                for v in bvars
            ]
        )


def bundle_clarification(brvdict: Dict[str, List[Node]]):
    """Yield bundle clarification section"""
    yield "\n"
    verbs = _("is a bundle") if len(brvdict) == 1 else _("are bundles")
    yield cap(
        _("where {} {} of which the following variables are used:").format(
            pm.hook.linguistic_enumeration(items=list(brvdict.keys())), verbs
        )
    )
    yield "\n"
    yield from unordered(
        [bundle_path(path=vname, root=key) for key in brvdict for vname in brvdict[key]]
    )


def component_node(node: Node, h: int) -> LineGen:
    """Yield component section"""
    nameparts = node.name.split(".")
    yield header(h, "{}".format(nameparts[-1]))
    yield snt(_("this section describes **{}**".format(nameparts[-1])))
    if node.parent.name != "world":
        yield snt(
            _("this component is a sub-component of {}").format(
                node_path(node.parent.name)
            )
        )

    comments = node.annotations.esl_info.get("comments", [])
    if comments:
        yield "\n"
        yield boldhead(_("comments")).replace("\n", "")
        yield "\n"
        yield from comments

    for key, comments in node.annotations.esl_info.get("tagged_comments", {}).items():
        yield "\n"
        yield boldhead(key).replace("\n", "")
        yield "\n"
        yield from comments


kind_mapping = {
    "component": component_node,
    "function_spec": hook.function_spec_node,
    "design_spec": hook.design_spec_node,
    "behavior_spec": hook.behavior_spec_node,
    "need": hook.need_node,
}


def lines(node: Node, **kwargs) -> LineGen:
    """Yield lines that describes a Node.

    Arguments:
        node: Node to generate the lines from.
    """

    genfunc = kind_mapping[node.kind]
    yield from genfunc(node=node, **kwargs)


def get_design_rule_line_vars(rules: List[Dict[str, str]], g: Graph):
    """Get variables that are used within a design rule line"""
    vrs = [
        g[r["subject"]]
        for r in rules
        if g[r["subject"]].annotations.esl_info.get("bundle_root_name")
    ]

    vrs += [
        g[r["bound"]["value"]]
        for r in rules
        if g.node_dict.get(r["bound"]["value"], None)
        and g[r["bound"]["value"]].annotations.esl_info.get("bundle_root_name")
    ]

    return vrs
