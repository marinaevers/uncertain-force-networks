% Auto-generated: do not edit by hand
\name{''SankeyTrackingGraph}

\alias{''SankeyTrackingGraph}

\title{SankeyTrackingGraph component}

\description{

}

\usage{
''SankeyTrackingGraph(id=NULL, clickData=NULL, colorPositions=NULL, colormap=NULL,
height=NULL, links=NULL, nodeMap=NULL, pf=NULL, step=NULL,
width=NULL)
}

\arguments{
\item{id}{Character. The ID used to identify this component in Dash callbacks.}

\item{clickData}{Character. Click data containing information about user interactions with the Sankey view
Structure: string with click details for logging}

\item{colorPositions}{Named list. A map mapping the nodes to normalized 2D coordinates
of a 2D colormap}

\item{colormap}{Character. A string for the name of the colormap}

\item{height}{Numeric. The height of the graph}

\item{links}{Unnamed list. An array containing the links (first entry source, second entry target, third entry value)}

\item{nodeMap}{Named list. A map containing the node/particle indices for each Sankey node}

\item{pf}{Unnamed list. }

\item{step}{Numeric. Step selection}

\item{width}{Numeric. The width of the graph}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

