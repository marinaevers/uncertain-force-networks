# AUTO GENERATED FILE - DO NOT EDIT

#' @export
''UncertainGraphView <- function(id=NULL, ccs=NULL, clickData=NULL, colormap=NULL, edges=NULL, height=NULL, orderByColorSimilarity=NULL, positions=NULL, radii=NULL, saveOnClick=NULL, showBoundaries=NULL, showEdges=NULL, useSizeForProbabilities=NULL, userDefinedCCColors=NULL, width=NULL) {
    
    props <- list(id=id, ccs=ccs, clickData=clickData, colormap=colormap, edges=edges, height=height, orderByColorSimilarity=orderByColorSimilarity, positions=positions, radii=radii, saveOnClick=saveOnClick, showBoundaries=showBoundaries, showEdges=showEdges, useSizeForProbabilities=useSizeForProbabilities, userDefinedCCColors=userDefinedCCColors, width=width)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'UncertainGraphView',
        namespace = 'uncertain_graph_view',
        propNames = c('id', 'ccs', 'clickData', 'colormap', 'edges', 'height', 'orderByColorSimilarity', 'positions', 'radii', 'saveOnClick', 'showBoundaries', 'showEdges', 'useSizeForProbabilities', 'userDefinedCCColors', 'width'),
        package = 'uncertainGraphView'
        )

    structure(component, class = c('dash_component', 'list'))
}
