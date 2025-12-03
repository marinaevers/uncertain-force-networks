# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args

ComponentType = typing.Union[
    str,
    int,
    float,
    Component,
    None,
    typing.Sequence[typing.Union[str, int, float, Component, None]],
]

NumberType = typing.Union[
    typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
]


class SankeyTrackingGraph(Component):
    """A SankeyTrackingGraph component.


Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- clickData (string; optional):
    Click data containing information about user interactions with the
    Sankey view  Structure: string with click details for logging.

- colorPositions (dict; optional):
    A map mapping the nodes to normalized 2D coordinates  of a 2D
    colormap.

- colormap (string; optional):
    A string for the name of the colormap.

- height (number; optional):
    The height of the graph.

- links (list; optional):
    An array containing the links (first entry source, second entry
    target, third entry value).

- nodeMap (dict; optional):
    A map containing the node/particle indices for each Sankey node.

- pf (list; optional)

- step (number; optional):
    Step selection.

- width (number; optional):
    The width of the graph."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'sankey_tracking_graph'
    _type = 'SankeyTrackingGraph'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        links: typing.Optional[typing.Sequence] = None,
        colorPositions: typing.Optional[dict] = None,
        width: typing.Optional[NumberType] = None,
        height: typing.Optional[NumberType] = None,
        colormap: typing.Optional[str] = None,
        step: typing.Optional[NumberType] = None,
        nodeMap: typing.Optional[dict] = None,
        pf: typing.Optional[typing.Sequence] = None,
        clickData: typing.Optional[str] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'clickData', 'colorPositions', 'colormap', 'height', 'links', 'nodeMap', 'pf', 'step', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'clickData', 'colorPositions', 'colormap', 'height', 'links', 'nodeMap', 'pf', 'step', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(SankeyTrackingGraph, self).__init__(**args)

setattr(SankeyTrackingGraph, "__init__", _explicitize_args(SankeyTrackingGraph.__init__))
