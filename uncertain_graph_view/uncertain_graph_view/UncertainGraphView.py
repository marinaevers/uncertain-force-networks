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


class UncertainGraphView(Component):
    """An UncertainGraphView component.


Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- ccs (list; required):
    Connected components of the graph for each member.

- clickData (string; optional):
    A string representing data from the last click event for logging
    purposes.  This is not used for rendering but can be used to log
    click events.

- colormap (string; default 'ZIEGLER'):
    A string for the name of the colormap.

- edges (list; optional):
    Edges between the nodes including the probability  Structure:
    [[source, target, probability], ...].

- height (number; optional):
    The height of the plot.

- orderByColorSimilarity (boolean; optional):
    Define the ordering of the pie charts:  if True, order by color
    similarity  otherwise use the member order.

- positions (list; required):
    The positions of the nodes for each member of the graph.

- radii (list; required):
    The radii of the nodes (one per node, do not capture uncertainty
    in the radii).

- saveOnClick (boolean; optional):
    A boolean value to indicate whether clicking should open  a file
    diaglog to save the graph as an image.

- showBoundaries (boolean; optional):
    Show boundaries.

- showEdges (boolean; optional):
    Show the edges.

- useSizeForProbabilities (boolean; optional):
    Define if a node that is only partially part of a connected
    component   should encode the probability of being part of that
    component by the size,  otherwise use gray for showing parts that
    do not belong.

- userDefinedCCColors (list; optional):
    A list of colors for specific user-defined connected components.
    If not provided, default colors will be used based on the average
    position.

- width (number; optional):
    The width of the plot."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'uncertain_graph_view'
    _type = 'UncertainGraphView'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        positions: typing.Optional[typing.Sequence] = None,
        ccs: typing.Optional[typing.Sequence] = None,
        radii: typing.Optional[typing.Sequence] = None,
        edges: typing.Optional[typing.Sequence] = None,
        orderByColorSimilarity: typing.Optional[bool] = None,
        useSizeForProbabilities: typing.Optional[bool] = None,
        showEdges: typing.Optional[bool] = None,
        showBoundaries: typing.Optional[bool] = None,
        height: typing.Optional[NumberType] = None,
        width: typing.Optional[NumberType] = None,
        colormap: typing.Optional[str] = None,
        saveOnClick: typing.Optional[bool] = None,
        clickData: typing.Optional[str] = None,
        userDefinedCCColors: typing.Optional[typing.Sequence] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'ccs', 'clickData', 'colormap', 'edges', 'height', 'orderByColorSimilarity', 'positions', 'radii', 'saveOnClick', 'showBoundaries', 'showEdges', 'useSizeForProbabilities', 'userDefinedCCColors', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ccs', 'clickData', 'colormap', 'edges', 'height', 'orderByColorSimilarity', 'positions', 'radii', 'saveOnClick', 'showBoundaries', 'showEdges', 'useSizeForProbabilities', 'userDefinedCCColors', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'ccs', 'positions', 'radii']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(UncertainGraphView, self).__init__(**args)

setattr(UncertainGraphView, "__init__", _explicitize_args(UncertainGraphView.__init__))
