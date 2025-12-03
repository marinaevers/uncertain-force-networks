# AUTO GENERATED FILE - DO NOT EDIT

export ''_uncertaingraphview

"""
    ''_uncertaingraphview(;kwargs...)

An UncertainGraphView component.

Keyword arguments:
- `id` (String; required): The ID used to identify this component in Dash callbacks.
- `ccs` (Array; required): Connected components of the graph for each member
- `clickData` (String; optional): A string representing data from the last click event for logging purposes.
This is not used for rendering but can be used to log click events.
- `colormap` (String; optional): A string for the name of the colormap
- `edges` (Array; optional): Edges between the nodes including the probability
Structure: [[source, target, probability], ...]
- `height` (Real; optional): The height of the plot
- `orderByColorSimilarity` (Bool; optional): Define the ordering of the pie charts:
if true, order by color similarity
otherwise use the member order
- `positions` (Array; required): The positions of the nodes for each member of the graph
- `radii` (Array; required): The radii of the nodes (one per node, do not capture uncertainty in the radii)
- `saveOnClick` (Bool; optional): A boolean value to indicate whether clicking should open
a file diaglog to save the graph as an image
- `showBoundaries` (Bool; optional): Show boundaries
- `showEdges` (Bool; optional): Show the edges
- `useSizeForProbabilities` (Bool; optional): Define if a node that is only partially part of a connected component 
should encode the probability of being part of that component by the size,
otherwise use gray for showing parts that do not belong
- `userDefinedCCColors` (Array; optional): A list of colors for specific user-defined connected components.
If not provided, default colors will be used based on the average position.
- `width` (Real; optional): The width of the plot
"""
function ''_uncertaingraphview(; kwargs...)
        available_props = Symbol[:id, :ccs, :clickData, :colormap, :edges, :height, :orderByColorSimilarity, :positions, :radii, :saveOnClick, :showBoundaries, :showEdges, :useSizeForProbabilities, :userDefinedCCColors, :width]
        wild_props = Symbol[]
        return Component("''_uncertaingraphview", "UncertainGraphView", "uncertain_graph_view", available_props, wild_props; kwargs...)
end

