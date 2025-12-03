
module UncertainGraphView
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "0.0.4"

include("jl/''_uncertaingraphview.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "uncertain_graph_view",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "uncertain_graph_view.min.js",
    external_url = nothing,
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "uncertain_graph_view.min.js.map",
    external_url = nothing,
    dynamic = true,
    async = nothing,
    type = :js
)
            ]
        )

    )
end
end
