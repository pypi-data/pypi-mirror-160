"""Module to export as an Excel workbook."""
from pathlib import Path
from typing import Dict, Optional, Union

from openpyxl.workbook import Workbook
from raesl.excel import defaults, sheets
from raesl.utils import get_scoped_nodes

# Compile module is excluded during docs generation.
try:
    from raesl.compile import to_graph
except ImportError:
    pass


def convert(
    *paths: Union[str, Path],
    output: Optional[Union[str, Path]] = defaults.OUTPUT,
    scopes: Dict[str, Optional[int]] = defaults.SCOPES,
) -> Workbook:
    """Write (part of) an ESL specification to a Excel workbook.

    Arguments:
        paths: ESL specification paths.
        output: Optional Workbook output path (will be overwritten without warning).
        scopes: Dictionary of component paths to relative depths of subcomponents to
            include as scopes for the generated output. Defaults to the complete tree.

    Returns:
        Excel workbook instance.
    """
    graph = to_graph(*paths)

    # Create workbook, but delete default sheet.
    wb = Workbook()
    wb.remove(wb["Sheet"])

    # Derive components from scopes.
    components = [
        node for node in get_scoped_nodes(graph, scopes) if node.kind == "component"
    ]
    if not components:
        raise ValueError(
            f"No components found in selected scopes ('{scopes}'). Please reconsider."
        )

    # Add sheets.
    _, components = sheets.add_components_sheet(wb, components)
    _, goals = sheets.add_goals_sheet(wb, graph, components)
    _, transformations = sheets.add_transformations_sheet(wb, graph, components)
    _, designs = sheets.add_designs_sheet(wb, graph, components)
    _, behaviors = sheets.add_behaviors_sheet(wb, graph, components)
    _, needs = sheets.add_needs_sheet(wb, graph, components)
    _, variables = sheets.add_variable_sheet(wb, graph, components)

    sheets.add_overview_sheet(
        wb, graph, components, goals, transformations, designs, behaviors, needs
    )

    # Protect all sheets.
    for sheet in wb.sheetnames:
        wb[sheet].protection = defaults.SHEETPROTECTION

    # Write output if path is given.
    if output:
        wb.save(str(output))
    return wb
