% Auto-generated: do not edit by hand
\name{''UncertainGraphView}

\alias{''UncertainGraphView}

\title{UncertainGraphView component}

\description{

}

\usage{
''UncertainGraphView(id=NULL, ccs=NULL, clickData=NULL, colormap=NULL,
edges=NULL, height=NULL, orderByColorSimilarity=NULL,
positions=NULL, radii=NULL, saveOnClick=NULL,
showBoundaries=NULL, showEdges=NULL,
useSizeForProbabilities=NULL, userDefinedCCColors=NULL,
width=NULL)
}

\arguments{
\item{id}{Character. The ID used to identify this component in Dash callbacks.}

\item{ccs}{Unnamed list. Connected components of the graph for each member}

\item{clickData}{Character. A string representing data from the last click event for logging purposes.
This is not used for rendering but can be used to log click events.}

\item{colormap}{Character. A string for the name of the colormap}

\item{edges}{Unnamed list. Edges between the nodes including the probability
Structure: [[source, target, probability], ...]}

\item{height}{Numeric. The height of the plot}

\item{orderByColorSimilarity}{Logical. Define the ordering of the pie charts:
if true, order by color similarity
otherwise use the member order}

\item{positions}{Unnamed list. The positions of the nodes for each member of the graph}

\item{radii}{Unnamed list. The radii of the nodes (one per node, do not capture uncertainty in the radii)}

\item{saveOnClick}{Logical. A boolean value to indicate whether clicking should open
a file diaglog to save the graph as an image}

\item{showBoundaries}{Logical. Show boundaries}

\item{showEdges}{Logical. Show the edges}

\item{useSizeForProbabilities}{Logical. Define if a node that is only partially part of a connected component 
should encode the probability of being part of that component by the size,
otherwise use gray for showing parts that do not belong}

\item{userDefinedCCColors}{Unnamed list. A list of colors for specific user-defined connected components.
If not provided, default colors will be used based on the average position.}

\item{width}{Numeric. The width of the plot}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

