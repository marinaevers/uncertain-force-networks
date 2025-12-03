# AUTO GENERATED FILE - DO NOT EDIT

export ''_sankeytrackinggraph

"""
    ''_sankeytrackinggraph(;kwargs...)

A SankeyTrackingGraph component.

Keyword arguments:
- `id` (String; required): The ID used to identify this component in Dash callbacks.
- `clickData` (String; optional): Click data containing information about user interactions with the Sankey view
Structure: string with click details for logging
- `colorPositions` (Dict; optional): A map mapping the nodes to normalized 2D coordinates
of a 2D colormap
- `colormap` (String; optional): A string for the name of the colormap
- `height` (Real; optional): The height of the graph
- `links` (Array; optional): An array containing the links (first entry source, second entry target, third entry value)
- `nodeMap` (Dict; optional): A map containing the node/particle indices for each Sankey node
- `pf` (Array; optional)
- `step` (Real; optional): Step selection
- `width` (Real; optional): The width of the graph
"""
function ''_sankeytrackinggraph(; kwargs...)
        available_props = Symbol[:id, :clickData, :colorPositions, :colormap, :height, :links, :nodeMap, :pf, :step, :width]
        wild_props = Symbol[]
        return Component("''_sankeytrackinggraph", "SankeyTrackingGraph", "sankey_tracking_graph", available_props, wild_props; kwargs...)
end

