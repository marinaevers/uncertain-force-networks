# AUTO GENERATED FILE - DO NOT EDIT

#' @export
''SankeyTrackingGraph <- function(id=NULL, clickData=NULL, colorPositions=NULL, colormap=NULL, height=NULL, links=NULL, nodeMap=NULL, pf=NULL, step=NULL, width=NULL) {
    
    props <- list(id=id, clickData=clickData, colorPositions=colorPositions, colormap=colormap, height=height, links=links, nodeMap=nodeMap, pf=pf, step=step, width=width)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'SankeyTrackingGraph',
        namespace = 'sankey_tracking_graph',
        propNames = c('id', 'clickData', 'colorPositions', 'colormap', 'height', 'links', 'nodeMap', 'pf', 'step', 'width'),
        package = 'sankeyTrackingGraph'
        )

    structure(component, class = c('dash_component', 'list'))
}
