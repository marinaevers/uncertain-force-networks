from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

TEMPLATE = 'simple_white'

def createGraphMeasureView(id_prefix):
    return dbc.Row([
        dcc.Graph(id=id_prefix + '-lineplot', style={'height': '200px', 'width': '65%'}),
        dcc.Graph(id=id_prefix + '-heatmap', style={'height': '200px', 'width': '35%'})
    ])

def lineUncertainty(xLabel, central, band, yLabel="", stepSelection=None):
    fig = go.Figure()
    x = np.arange(len(xLabel))
    fig.add_trace(go.Scatter(x=np.concatenate([x, x[::-1]]), y=np.concatenate([band[0], band[1][::-1]]),
                            fill='toself',
                            fillcolor='rgba(0, 0, 255, 0.3)',  # Blue with low opacity
                            line=dict(color='rgba(255, 255, 255, 0)'), name='Range'))
    fig.add_trace(go.Scatter(x=x, y=central, mode='lines', name='Mean', line=dict(color='rgba(0, 0, 255, 1.0)')))
    # if np.any(outliers):
    #     for o in outliers:
    #         fig.add_trace(go.Scatter(x=x, y=o, mode='lines', marker=dict(color='red'), name='Outlier'))
    LOWER_BOUND_JAMMED = 0.7744
    mask_jammed = np.array(xLabel, dtype=float) > LOWER_BOUND_JAMMED
    xLabel = [f"{x:.4f}" for x in xLabel]
    fig.update_layout(
        xaxis_title='Packing Fraction',
        yaxis_title=yLabel,
        margin=dict(l=40, r=0, t=25, b=0),
        template=TEMPLATE,
        xaxis=dict(
            tickmode='array',
            tickvals=np.arange(len(xLabel)),#[::4],
            ticktext=xLabel,#[::4],
            #range=[0, np.max(s_values)+1]
        )
    )
    if stepSelection != None:
        fig.add_vline(x=stepSelection, line=dict(color='red'), opacity=1, line_width=2)
    if np.any(mask_jammed):
        start_idx = np.argmax(mask_jammed)
        end_idx = len(mask_jammed) - 1 - np.argmax(mask_jammed[::-1])
        # print(start_idx, end_idx)
        # print(x)
        fig.add_vrect(
            x0=x[start_idx]-0.5, x1=x[end_idx]+0.5,
            fillcolor='green', opacity=0.1, row=1, col=1, 
            layer="below", line_width=0,
        )
        fig.add_annotation(
            x=(x[start_idx] + x[end_idx]) / 2,
            y=1.0,
            text="Jammed",
            showarrow=False,
            font=dict(size=14, color='green'),
            xref="x",
            yref="paper",
            yanchor="middle",
            xanchor="center"
        )
    return fig

def heatmap(heatmap, force, uncertainty, uncertaintyThreshold, forceThreshold):
    fig = go.Figure()
    fig.add_trace(go.Heatmap(z=heatmap.T, x=uncertainty, y=force))
    fig.add_trace(go.Scatter(x=[uncertaintyThreshold], y=[forceThreshold], line=dict(color='red')))
    fig.update_layout(
        xaxis_title='Probability',
        yaxis_title='Force',
        margin=dict(l=40, r=0, t=25, b=0),
        template=TEMPLATE,
    )
    return fig