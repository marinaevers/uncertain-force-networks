import time
from timeit import default_timer as timer
from typing import Counter
from dash import callback, Output, Input, State, ctx, callback_context
import base64
import json
from dash.exceptions import PreventUpdate
import visualizations
import numpy as np
import os
import uncertain_graph_view
import sankey_tracking_graph
import pickle
import concurrent.futures
from flask import request
from datetime import datetime
import time

def log_user_action(username, message):
    """Log user actions with timestamp to user-specific log file"""
    if username == 'notrack':
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_filename = f"log_{username}_backend.txt"
    log_entry = f"[{timestamp}] {message}\n"
    
    try:
        with open(log_filename, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print(f"Error writing to log file {log_filename}: {e}")

# Global data structure
app_data = {
    # Shared data that doesn't change based on user input
    'data': None,  # Will store the loaded dataset
    'packing_fractions': None,  # Will store packing fractions from dataset
    'heatmap_cache': {},  # Cached heatmap computations
    
    # User-specific data - each user gets their own dictionary
    'users': {}  # Will contain user-specific settings and cached data
}

def get_user_data(username):
    """Get or create user-specific data dictionary"""
    if username not in app_data['users']:
        app_data['users'][username] = {
            # User-modifiable data from original 'data' dictionary
            'force_selection': 0,
            'uncertainty_selection': 0,
            'ccs': None,
            
            # User-specific cached data
            'thresholds_cache': {},
            'avg_node_degree_step': -1,
            'avg_node_degree_data': None,
            'mean_cc_size_step': -1,
            'mean_cc_size_data': None,
            'nonparticipating_step': -1,
            'nonparticipating_data': None,
        }
    return app_data['users'][username]

def avg_degree(forces):
    start = time.time()
    counts = np.count_nonzero(forces, axis=-1)
    avg_degree = np.mean(counts, axis=-1)
    log_user_action('timings', f"Avg degree computation took {time.time() - start:.5f}s")
    return avg_degree

def avg_degree_over_time(forces, stepSelection, user_data):
    if stepSelection != user_data['avg_node_degree_step'] and user_data['avg_node_degree_data'] is not None:
        user_data['avg_node_degree_step'] = stepSelection
        # print("Returning cached avg node degree data")
        return user_data['avg_node_degree_data']
    # else:
    #     print("Step selection: ", stepSelection, "Avg node degree step: ", user_data['avg_node_degree_step'])
    counts = [np.count_nonzero(forces[i], axis=-1) for i in range(len(forces))]
    avg_degree = [np.mean(counts[i], axis=-1) for i in range(len(counts))]
    user_data['avg_node_degree_step'] = stepSelection
    user_data['avg_node_degree_data'] = avg_degree
    return avg_degree

def nonparticipating(forces):
    start = time.time()
    counts = np.sum(forces, axis=-1)
    nonparticipating = np.count_nonzero(counts==0, axis=-1)
    log_user_action('timings', f"Non-participating computation took {time.time() - start:.5f}s")
    return nonparticipating

def nonparticipating_over_time(forces, stepSelection, user_data):
    # start = time.time()
    if stepSelection != user_data['nonparticipating_step'] and user_data['nonparticipating_data'] is not None:
        # print("Time to enter if statement: ", time.time() - start)
        user_data['nonparticipating_step'] = stepSelection
        # print("Timing for return nonparticipating Test: ", time.time() - start)
        # print("Returning cached non-participating data", str(user_data['nonparticipating_step']))
        # print("Timing for return nonparticipating: ", time.time() - start)
        return user_data['nonparticipating_data']
    # else:
        # print("Step selection: ", stepSelection, "Non-participating step: ", user_data['nonparticipating_step'])
    # print("Timing before non-participating computation: ", time.time() - start)
    counts = [np.sum(forces[i], axis=-1) for i in range(len(forces))]
    nonparticipating = [np.count_nonzero(counts[i]==0, axis=-1) for i in range(len(counts))]
    user_data['nonparticipating_step'] = stepSelection
    user_data['nonparticipating_data'] = nonparticipating
    return nonparticipating

import concurrent.futures

def connected_components_size_over_time(forces, stepSelection, user_data):
    if stepSelection != user_data['mean_cc_size_step'] and user_data['mean_cc_size_data'] is not None:
        user_data['mean_cc_size_step'] = stepSelection
        # print("Returning cached mean CC size data")
        return user_data['mean_cc_size_data']
    # else:
    #     print("Step selection: ", stepSelection, "Mean CC size step: ", user_data['mean_cc_size_step'])
    #print("Test")
    #print(len(forces))
    #print(len(forces[0]))
    def compute_size(sample):
        return connected_components_size(forces[sample])
    #     ccs = compute_connected_components_single_graph(forces[sample])
    #     mask = ccs != 0
    #     column = ccs[mask]
    #     if column.size == 0:
    #         return 0
    #     else:
    #         _, counts = np.unique(column, return_counts=True)
    #         return np.mean(counts)
    num_samples = len(forces)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(compute_size, range(num_samples)))
    user_data['mean_cc_size_step'] = stepSelection
    user_data['mean_cc_size_data'] = results
    return results

def connected_components_size(forces):
    start = time.time()
    ccs = np.array(compute_connected_components(forces, forces.shape))
    #     # Ignore zeros (non-participating)
    # mask = ccs != 0
    # # For each sample (column), count occurrences of each label
    # label_counts = []
    # for i in range(ccs.shape[1]):
    #     column = ccs[:, i]
    #     column = column[mask[:, i]]
    #     if column.size == 0:
    #         label_counts.append(0)
    #     else:
    #         # np.unique returns unique labels and their counts
    #         _, counts = np.unique(column, return_counts=True)
    #         label_counts.append(np.mean(counts))
    # return label_counts
    label_counts = []
    for i in range(ccs.shape[1]):
        column = ccs[:, i]
        column = column[column != 0]
        vals = list(Counter(column).values())
        mean = 0
        if vals:
            # print(vals)
            # print("Column ",column)
            # print("CCs ", ccs)
            mean = np.mean(vals)
        label_counts.append(mean)
    # Count occurrences of each string
    log_user_action('timings', f"Mean CC size computation took {time.time() - start:.5f}s")
    #print(forces.shape)
    return label_counts

def create_line_plot(dataThresholds, yLabel, function, stepSelection, pf):
    # start = time.time()
    #pf = data["packingFractions"]
    # Compute lineplot
    vals = function(dataThresholds, stepSelection)#[function(dataThresholds[i]) for i in range(len(dataThresholds))]
    # print("Timing before line plot computation: ", time.time() - start)
    numSteps = len(dataThresholds)
    central = [np.mean(vals[i]) for i in range(numSteps)]
    min = [np.min(vals[i]) for i in range(numSteps)]
    max = [np.max(vals[i]) for i in range(numSteps)]
    band = [min, max]
    # print(f"Line plot computation took {time.time() - start:.2f}s")
    # start = time.time()
    vis = visualizations.lineUncertainty(pf, central, band, yLabel=yLabel, stepSelection=stepSelection)
    # print(f"Line plot visualization took {time.time() - start:.2f}s")
    return vis

def compute_connected_components_single_graph(graph, startLabel=1):
    visited = np.zeros(len(graph))
    queue = []
    currentLabel = startLabel
    startLabel += 1
    hasNeighbors = np.sum(graph, axis=0)>0
    labels = np.zeros(len(graph))
    if np.count_nonzero(hasNeighbors) == 0:
        return labels
    start = np.where(hasNeighbors)[0][0]
    visited[np.logical_not(hasNeighbors)] = 1
    queue.append(start)
    while len(queue) > 0:
        # First sample, no matching required
        current = queue.pop(0)
        if visited[current] != 1:
            visited[current] = 1
            labels[current] = currentLabel
            filter = graph[current] > 0
            neighbors = np.argwhere(filter)
            for idx in np.array(neighbors).flatten():
                if visited[idx] == 0 and graph[current][idx] > 0:
                    queue.append(idx)
        if len(queue) == 0:
            if np.any(visited == 0):
                queue.append(np.where(visited == 0)[0][0])
            if len(queue) > 0:
                currentLabel = startLabel
                startLabel += 1
    return labels

#@functools.lru_cache(maxsize=None)
def compute_connected_components(distributions, dist_shape):
    #distributions = np.frombuffer(distributions, dtype=np.float64).reshape(dist_shape)
    numParticles = distributions.shape[1]
    numSamples = distributions.shape[0]
    labels = np.zeros((numParticles, numSamples), dtype=int)
    startLabel = 1
    # Loop over all samples
    for sample in range(numSamples):
        labels[:, sample] = compute_connected_components_single_graph(distributions[sample], startLabel=startLabel)
        startLabel = np.max(labels[:, sample]) + 1
    return labels




def compute_minor_major_components(distributions, avg_force):


    numParticles = distributions.shape[1]


    numSamples = distributions.shape[0]


    labels = np.zeros((numParticles, numSamples), dtype=int)


    minorLabel = 2


    majorLabel = 1


    for sample in range(numSamples):


        labels[:, sample] = np.zeros(len(distributions[sample]))


        # Check if there is any force > avg in distributions[sample]


        #print(distributions[sample].shape)


        #print(np.sum(distributions[sample] > 0, axis=1)[:5])


        labels[:, sample][np.sum(distributions[sample] > 0, axis=1) > 0] = minorLabel


        labels[:, sample][np.sum(distributions[sample] > avg_force, axis=1) > 0] = majorLabel


    return labels

def create_heatmaps(user_data, function1, function2, function3, stepData):
    uRes = len(app_data['data'][stepData]["forces"])
    fRes = 15
    heatmap1 = np.zeros((uRes, fRes))
    heatmap2 = np.zeros((uRes, fRes))
    heatmap3 = np.zeros((uRes, fRes))
    uncertaintyT = np.linspace(0.0, 1.0, uRes)
    fMax = np.max(app_data['data'][stepData]["forces"])
    forceT = np.linspace(0.0, fMax, fRes)
    if stepData in app_data['heatmap_cache']:
        heatmap1, heatmap2, heatmap3 = app_data['heatmap_cache'][stepData]
    else:
        step = stepData
        fMax = np.max(app_data['data'][step]["forces"])
        forceT = np.linspace(0.0, fMax, fRes)
        heatmap1 = np.zeros((uRes, fRes))
        heatmap2 = np.zeros((uRes, fRes))
        heatmap3 = np.zeros((uRes, fRes))
        forces = np.array(app_data['data'][step]["forces"])

        def compute_cell(i, j):
            f = forceT[j]
            #print("Force: " + str(f/fMax))
            u = uncertaintyT[i]
            forcesCp = np.copy(forces)
            forcesCp[forcesCp < f] = 0
            forceProb = np.count_nonzero(forcesCp > 0, axis=0)/forcesCp.shape[0]
            forcesCp2 = np.copy(forcesCp)
            forcesCp2[:, forceProb < u] = 0
            return (
                np.mean(function1(forcesCp2)),
                np.mean(function2(forcesCp2)),
                np.mean(function3(forcesCp2)),
                i, j
            )

        #with concurrent.futures.ThreadPoolExecutor() as executor:
        #    futures = [executor.submit(compute_cell, i, j) for i in range(uRes) for j in range(fRes)]
        for i in range(uRes):
            for j in range(fRes):
            #for future in concurrent.futures.as_completed(futures):
                h1, h2, h3, i, j = compute_cell(i,j)#future.result()
                heatmap1[i, j] = h1
                heatmap2[i, j] = h2
                heatmap3[i, j] = h3
        app_data['heatmap_cache'][stepData] = (heatmap1, heatmap2, heatmap3)
        if len(app_data['heatmap_cache']) == 19:
            with open("heatmap_cache.pkl", "wb") as f:
                pickle.dump(app_data['heatmap_cache'], f)
                print("Heatmap cache saved to disk.")

    return (
        visualizations.heatmap(heatmap1, forceT, uncertaintyT, user_data["uncertainty_selection"], user_data["force_selection"]),
        visualizations.heatmap(heatmap2, forceT, uncertaintyT, user_data["uncertainty_selection"], user_data["force_selection"]),
        visualizations.heatmap(heatmap3, forceT, uncertaintyT, user_data["uncertainty_selection"], user_data["force_selection"])
    )

# def create_heatmaps(data, function1, function2, function3, stepData):
#     start = timer()
#     step = stepData
#     uRes = 15
#     fRes = 15
#     fMax = np.max(data["data"][step]["forces"])
#     heatmap1 = np.zeros((uRes, fRes))
#     heatmap2 = np.zeros((uRes, fRes))
#     heatmap3 = np.zeros((uRes, fRes))
#     forces = np.array(data["data"][step]["forces"])
#     uncertaintyT = np.linspace(0.0, 1.0, uRes)
#     forceT = np.linspace(0.0, fMax, fRes)
#     f1 = 0
#     f2 = 0
#     f3 = 0
#     for j, f in enumerate(forceT):
#         forcesCp = np.copy(forces)
#         forcesCp[forcesCp < f] = 0
#         forceProb = np.count_nonzero(forcesCp > 0, axis=0)/forcesCp.shape[0]
#         for i, u in enumerate(uncertaintyT):
#             forcesCp2 = np.copy(forcesCp)
#             forcesCp2[:, forceProb < u] = 0
#             f1_s = time.time()
#             heatmap1[i,j] = np.mean(function1(forcesCp2))
#             f1 += time.time() - f1_s
#             f2_s = time.time()
#             heatmap2[i,j] = np.mean(function2(forcesCp2))
#             f2 += time.time() - f2_s
#             f3_s = time.time()
#             heatmap3[i,j] = np.mean(function3(forcesCp2))
#             f3 += time.time() - f3_s
#     callback_context.record_timing('heatmap_computation', timer() - start, 'Heatmap Computation')
#     print(f"Heatmap 1: {f1:.2f}s, Heatmap 2: {f2:.2f}s, Heatmap 3: {f3:.2f}s")
#     return visualizations.heatmap(heatmap1, forceT, uncertaintyT, data["uncertainty_selection"], data["force_selection"]), \
#               visualizations.heatmap(heatmap2, forceT, uncertaintyT, data["uncertainty_selection"], data["force_selection"]), \
#                 visualizations.heatmap(heatmap3, forceT, uncertaintyT, data["uncertainty_selection"], data["force_selection"])

def compute_transitions(ccs):
    transitions = {}
    for i in range(len(ccs)-1):
        current = ccs[i]
        next = ccs[i+1]
        for j in range(len(current)):
            if True:#current[j] != 0 and next[j] != 0:
                first = int(current[j])
                second = int(next[j])
                if current[j] == 0:
                    first = -(i+1)
                if next[j] == 0:
                    second = -(i+2)
                pair = (first, second)
                if pair in transitions:
                    transitions[pair] += 1
                else:
                    transitions[pair] = 1
    transitions = [[key[0], key[1], value] for key, value in transitions.items()]
    return transitions

@callback(
    Output('step-data', 'data'),
    Input('sankey-diagram', 'step'),
)
def update_step_data(sankeyStep):
    username = request.authorization['username'] if request.authorization else 'default'
    #log_user_action(username, f"update_step_data called with sankeyStep: {sankeyStep}")
    
    if not sankeyStep:
        return {'step': 0}
    return {'step': sankeyStep}

@callback(
    Output('store-data', 'data'),
    Output('avg-force-text', 'children'),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('avg-degree-heatmap', 'clickData'),
    Input('cc-size-heatmap', 'clickData'),
    Input('nonparticipating-heatmap', 'clickData'),
    #State('store-data', 'data'),
    State('step-data', 'data')
)
def update_data(contentsData,filename, 
                avgDegreeHeatmapClickData, edgesHeatmapClickData, nonparticipatingHeatmapClickData,
                stepData):
    username = request.authorization['username'] if request.authorization else 'default'
    user_data = get_user_data(username)
    #log_user_action(username, f"update_data called - trigger: {ctx.triggered_id}, stepData: {stepData}")
    
    if not stepData:
        stepData = 0
    else:
        stepData = stepData["step"]
    changed = ctx.triggered_id
    if app_data['data']:
        recomputeCCS = False
        if changed == 'avg-degree-heatmap':
            if 'x' in avgDegreeHeatmapClickData['points'][0]:
                user_data["uncertainty_selection"] = avgDegreeHeatmapClickData['points'][0]['x']
                user_data["force_selection"] = avgDegreeHeatmapClickData['points'][0]['y']
                log_user_action(username, f"Heatmap click - avg-degree: uncertainty={user_data['uncertainty_selection']:.3f}, force={user_data['force_selection']:.3f}")
                recomputeCCS = True
            else:
                return True, f"Avg. force: {app_data['avg_force']:.4f}"
        if changed == 'cc-size-heatmap':
            if 'x' in edgesHeatmapClickData['points'][0]:
                user_data["uncertainty_selection"] = edgesHeatmapClickData['points'][0]['x']
                user_data["force_selection"] = edgesHeatmapClickData['points'][0]['y']
                log_user_action(username, f"Heatmap click - cc-size: uncertainty={user_data['uncertainty_selection']:.3f}, force={user_data['force_selection']:.3f}")
                recomputeCCS = True
            else:
                return True, f"Avg. force: {app_data['avg_force']:.4f}"
        if changed == 'nonparticipating-heatmap':
            if 'x' in nonparticipatingHeatmapClickData['points'][0]:
                user_data["uncertainty_selection"] = nonparticipatingHeatmapClickData['points'][0]['x']
                user_data["force_selection"] = nonparticipatingHeatmapClickData['points'][0]['y']
                log_user_action(username, f"Heatmap click - nonparticipating: uncertainty={user_data['uncertainty_selection']:.3f}, force={user_data['force_selection']:.3f}")
                recomputeCCS = True
            else:
                return True, f"Avg. force: {app_data['avg_force']:.4f}"
        if recomputeCCS == True:
            distributions = np.array(app_data['data'][stepData]["forces"])
            distributions[distributions < user_data["force_selection"]] = 0
            #distributions[distributions > user_data["force_selection"]] = 1
            user_data["ccs"] = compute_connected_components(distributions, distributions.shape)
            return True, f"Avg. force: {app_data['avg_force']:.4f}"
    if contentsData:
        log_user_action(username, f"Data upload started - {len(contentsData)} files")
        dataArr = []
        data = {}
        app_data['heatmap_cache'].clear()
        # Load heatmap cache if available
        cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "heatmap_cache.pkl")
        if os.path.exists(cache_path):
            with open(cache_path, "rb") as f:
                print("Load heatmap cache from disk")
                app_data['heatmap_cache'].update(pickle.load(f))
        data["packingFractions"] = []
        sorted_indices = np.argsort(filename)
        contentsData = [contentsData[i] for i in sorted_indices]
        for i, d in enumerate(contentsData):
            _, contents = d.split(',')
            contents = base64.b64decode(contents)
            dataArr.append(json.loads(contents))
            #dataArr[-1]["forces"] = np.array(dataArr[-1]["forces"])
            data["packingFractions"].append(dataArr[-1]['packing_fraction'])
        data["data"] = dataArr
        data["packingFractions"] = np.array(data["packingFractions"])
        #data["data"] = np.array(data["data"])
        
        # Store shared data
        app_data['data'] = data["data"]
        if False:
            num_disks = len(app_data['data'][0]['disk_positions'][0][0])
            num_samples = len(app_data['data'][0]['forces'])
            is_real_data = num_disks == 832 and num_samples == 10
            if is_real_data:
                for stepData in range(len(app_data['data'])):
                    if len(app_data['data'][stepData]["forces"]) == 10:
                        print("Change for step ", stepData, " to reduced disk set")
                        app_data['data'][stepData]["forces"] = np.array(app_data['data'][stepData]["forces"])[[0, 1, 2, 3, 4, 5, 6, 9]]
                        app_data['data'][stepData]["disk_positions"] = np.array(app_data['data'][stepData]["disk_positions"])[[0, 1, 2, 3, 4, 5, 6, 9]]
        app_data['packing_fractions'] = data["packingFractions"]
        
        # Initialize user-specific data
        user_data["force_selection"] = 0
        user_data["uncertainty_selection"] = 0
        distributions = np.array(app_data['data'][stepData]["forces"])
        distributions[distributions < user_data["force_selection"]] = 0
        distributions[distributions > user_data["force_selection"]] = 1
        user_data["ccs"] = compute_connected_components(distributions, distributions.shape)
        log_user_action(username, "Data upload completed successfully")
        
        log_user_action("timings", "Experiment with number of disks: " + str(len(app_data['data'][0]['disk_positions'][0][0])))
        log_user_action("timings", "Experiment with number of steps: " + str(len(data["packingFractions"])))
        log_user_action("timings", "Experiment with number of samples per step: " + str(len(app_data['data'][0]['forces'])))
        
        # Compute avg. force of jammed states
        LOWER_BOUND_JAMMED = 0.7744 # copied from visualizations.py
        mask_jammed = np.array(app_data['packing_fractions'], dtype=float) > LOWER_BOUND_JAMMED
        # Assume that 0 is included in the average
        app_data['avg_force'] = np.mean([
            np.mean(np.array(app_data['data'][i]["forces"])[np.array(app_data['data'][i]["forces"]) > 0])
            for i in range(len(app_data['data'])) if mask_jammed[i]
        ])
        return True, f"Avg. force: {app_data['avg_force']:.4f}"
    else:
    #if True:  # Always load synthetic data since upload is commented out
        log_user_action(username, "Loading synthetic data for debugging")
        # For debugging load artificial data
        app_data['heatmap_cache'].clear()
        dataArr = []
        data = {}
        data["packingFractions"] = []
        synthetic_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
        for filename in sorted(os.listdir(synthetic_data_path)):
            if filename.endswith('.json') and '-' in filename:
                with open(os.path.join(synthetic_data_path, filename), 'r') as file:
                    d = json.load(file)
                    dataArr.append(d)
                    #dataArr[-1]["forces"] = np.array(dataArr[-1]["forces"])
                    data["packingFractions"].append(dataArr[-1]['packing_fraction'] + 0.2)
        data["data"] = dataArr
        # mean_positions = np.zeros(np.array(data["data"][0]["disk_positions"]).shape)
        # mean_radii = np.zeros(np.array(data["data"][0]["radii"]).shape)
        # for d in data["data"]:
        #     mean_positions += d["disk_positions"]
        #     mean_radii += d["radii"]
        #data["radii_mean"] = mean_radii/len(data["data"])
        #data["positions_mean"] = mean_positions/len(data["data"])
        
        # Store shared data
        app_data['data'] = data["data"]
        app_data['packing_fractions'] = data["packingFractions"]
        
        # Initialize user-specific data
        user_data["force_selection"] = 0
        user_data["uncertainty_selection"] = 0
        distributions = np.array(app_data['data'][stepData]["forces"])
        distributions[distributions < user_data["force_selection"]] = 0
        distributions[distributions > user_data["force_selection"]] = 1
        user_data["ccs"] = compute_connected_components(distributions, distributions.shape)
        log_user_action(username, "Synthetic data loaded for debugging")

        # Compute avg. force of jammed states
        LOWER_BOUND_JAMMED = 0.7744 # copied from visualizations.py
        mask_jammed = np.array(app_data['packing_fractions'], dtype=float) > LOWER_BOUND_JAMMED
        # Assume that 0 is included in the average
        app_data['avg_force'] = np.mean([
            np.mean(np.array(app_data['data'][i]["forces"])[np.array(app_data['data'][i]["forces"]) > 0])
            for i in range(len(app_data['data'])) if mask_jammed[i]
        ])
        return True, f"Avg. force: {app_data['avg_force']:.4f}"
    
@callback(
    Output('thresholded-forces-data', 'data'),
    Input('store-data', 'data')
)
def update_thresholded_forces_data(dataFlag):
    username = request.authorization['username'] if request.authorization else 'default'
    user_data = get_user_data(username)
    #log_user_action(username, "update_thresholded_forces_data called")
    
    if not app_data['data']:
        raise PreventUpdate
    if len(app_data['data']) == 1:
        raise PreventUpdate
    # Compute thresholded forces
    dataThresholds = []
    for i in range(len(app_data['data'])):
        forcesCp = np.array(app_data['data'][i]["forces"])
        forcesCp[forcesCp < user_data["force_selection"]] = 0
        forceProb = np.count_nonzero(forcesCp > 0, axis=0)/forcesCp.shape[0]
        forcesCp[:,forceProb < user_data["uncertainty_selection"]] = 0
        # Why does this remove all variability?
        forcesCp[forcesCp > 0] = 1
        dataThresholds.append(forcesCp)
    user_data['thresholds_cache'] = dataThresholds
    return True#dataThresholds

@callback(
    Output('avg-degree-lineplot', 'figure'),
    Input('thresholded-forces-data', 'data'),
    Input('step-data', 'data'),
    #State('store-data', 'data'),
)
def update_avg_degree_plots(dataThresholds, stepData):
    username = request.authorization['username'] if request.authorization else 'default'
    user_data = get_user_data(username)
    #log_user_action(username, f"update_avg_degree_plots called - stepData: {stepData}")
    
    if stepData is None:
        stepData = 0
    else:
        stepData = stepData["step"]
    # dataThresholds = [np.array(dataThresholds[i]) for i in range(len(dataThresholds))]
    dataThresholds = user_data['thresholds_cache']
    # return create_line_plot(dataThresholds, "Avg. node degree", avg_degree, stepData, app_data['packing_fractions'])
    return create_line_plot(dataThresholds, "Avg. coord. number", lambda forces, step: avg_degree_over_time(forces, step, user_data), stepData, app_data['packing_fractions'])

@callback(
    Output('cc-size-lineplot', 'figure'),
    Input('thresholded-forces-data', 'data'),
    Input('step-data', 'data'),
    #State('store-data', 'data'),
)
def update_cc_size_plots(dataThresholds, stepData):
    username = request.authorization['username'] if request.authorization else 'default'
    user_data = get_user_data(username)
    #log_user_action(username, f"update_cc_size_plots called - stepData: {stepData}")
    
    if stepData is None:
        stepData = 0
    else:
        stepData = stepData["step"]
    #dataThresholds = [np.array(dataThresholds[i]) for i in range(len(dataThresholds))]
    dataThresholds = user_data['thresholds_cache']
    # return create_line_plot(dataThresholds, "Mean CC Size", connected_components_size, stepData, app_data['packing_fractions'])
    return create_line_plot(dataThresholds, "Avg. CC Size", lambda forces, step: connected_components_size_over_time(forces, step, user_data), stepData, app_data['packing_fractions'])


@callback(
    Output('nonparticipating-lineplot', 'figure'),
    Input('thresholded-forces-data', 'data'),
    Input('step-data', 'data'),
    #State('store-data', 'data'),
)
def update_nonparticipating_plots(dataThresholds, stepData):
    username = request.authorization['username'] if request.authorization else 'default'
    user_data = get_user_data(username)
    #log_user_action(username, f"update_nonparticipating_plots called - stepData: {stepData}")
    
    if stepData is None:
        stepData = 0
    else:
        stepData = stepData["step"]
    # dataThresholds = [np.array(dataThresholds[i]) for i in range(len(dataThresholds))]
    dataThresholds = user_data['thresholds_cache']
    # return create_line_plot(dataThresholds, "Non-participating nodes", nonparticipating, stepData, app_data['packing_fractions'])
    return create_line_plot(dataThresholds, "Non-participating nodes", lambda forces, step: nonparticipating_over_time(forces, step, user_data), stepData, app_data['packing_fractions'])

@callback(
    Output('avg-degree-heatmap', 'figure'),
    Output('cc-size-heatmap', 'figure'),
    Output('nonparticipating-heatmap', 'figure'),
    Input('store-data', 'data'),
    Input('step-data', 'data')
)
def update_heatmaps(dataAll, stepData):
    username = request.authorization['username'] if request.authorization else 'default'
    user_data = get_user_data(username)
    #log_user_action(username, f"update_heatmaps called - stepData: {stepData}")
    
    if not stepData:
        stepData = 0
    else:
        stepData = stepData["step"]
    h1, h2, h3 = create_heatmaps(user_data, avg_degree, connected_components_size, nonparticipating, stepData)
    return h1, h2, h3

@callback(
    Output('spatial', 'children'),
    Output('spatial-data', 'data'),
    Input('store-data', 'data'),
    Input('show-edges', 'value'),
    Input('order-color', 'value'),
    Input('use-size', 'value'),
    Input('select-colormap', 'value'),
    Input('save-on-click', 'value'),
    Input('step-data', 'data'),
    Input('show-major-minor', 'value'),
    Input('user-defined-threshold', 'value'),
    Input('aggregate-jammed', 'value'),
    State('spatial-data', 'data'),
    prevent_initial_call=True
)
def update_spatial_view(dataFlag, showEdges, orderColor, useSize, colormap, saveOnClick, 
                       stepData, showMajorMinor, useUserDefinedThreshold, aggregateJammed, spatialData):
    username = request.authorization['username']
    user_data = get_user_data(username)
    log_user_action(username, f"update_spatial_view called - stepData: {stepData}, trigger: {ctx.triggered_id}")
    
    # Set default values for commented-out parameters
    colormap = 'ZIEGLER'  # Default colormap
    saveOnClick = False   # Default save on click
    
    if not stepData:
        stepData = 0
    else:
        stepData = stepData["step"]
    if not app_data['data']:
        print("No data")
        raise PreventUpdate
    changed = ctx.triggered_id
    # positions = np.mean(app_data['data'][stepData]["disk_positions"], axis=0).T
    #print(stepData)
    positions = app_data['data'][stepData]["disk_positions"]
    #print(positions[0][0][:5])
    radii = app_data['data'][stepData]["radii"]
    
    #if changed == 'step-data' or changed == 'store-data':
    start = time.time()
    distributions = []
    if aggregateJammed:
        mask_jammed = np.array(app_data['packing_fractions'], dtype=float) > 0.7744
        distributions = [app_data['data'][i]["forces"] for i in range(len(app_data['data'])) if mask_jammed[i]]
        distributions = np.concatenate(distributions, axis=0)
        #print(len(distributions), " jammed states aggregated")
        distributions = np.array(distributions)
        # for i in range(len(distributions)):
        #     print("Distribution ", i, " size: ", distributions[i].shape, " sum: ", np.sum(distributions[i]>0))
    else:
        distributions = np.array(app_data['data'][stepData]["forces"])
    if not useUserDefinedThreshold:
        distributions[distributions < user_data["force_selection"]] = 0
    userDefinedCCColors = []
    if showMajorMinor:
        #print("Show major/minor components")
        forceThreshold = app_data['avg_force'] if not useUserDefinedThreshold else user_data["force_selection"]
        ccs = compute_minor_major_components(distributions, forceThreshold)
        userDefinedCCColors = [
            "rgb(179, 0, 0)",  # muted red
            "rgb(33, 118, 174)"   # muted blue
        ]
    else:
        ccs = compute_connected_components(distributions, distributions.shape)#user_data["ccs"]
    #spatialData = distributions.tolist()
    distributions = (distributions > 0).sum(axis=0)/len(distributions)
    edges = []
    if showEdges:
        #distributions = np.array(spatialData)
        edges = [edge + [distributions[edge[0], edge[1]]] for edge in np.argwhere(distributions > 0).tolist()]
    log_user_action("timings", f"Spatial view computation took {time.time() - start:.5f}s")
    return uncertain_graph_view.UncertainGraphView(
        id='spatial-diagram',
        positions=positions,
        radii=radii,
        ccs=ccs,
        edges=edges,
        showEdges=showEdges,
        orderByColorSimilarity=orderColor,
        useSizeForProbabilities=useSize,
        colormap=colormap,
        saveOnClick=saveOnClick,
        userDefinedCCColors=userDefinedCCColors,
        #clickData=None  # Initialize as None, will be updated by click events
    ), spatialData

@callback(
    Output('sankey-diagram', 'step'),
    Input('avg-degree-lineplot', 'clickData'),
    Input('cc-size-lineplot', 'clickData'),
    Input('nonparticipating-lineplot', 'clickData'),
    State('sankey-diagram', 'step')
)
def update_sankey_step(avgDegreeClickData, edgesClickData, nonparticipatingClickData, currentStep):
    username = request.authorization['username'] if request.authorization else 'default'
    log_user_action(username, f"update_sankey_step called - trigger: {ctx.triggered_id}, currentStep: {currentStep}")
    
    changed = ctx.triggered_id
    if changed == 'avg-degree-lineplot':
        if 'x' in avgDegreeClickData['points'][0]:
            step = avgDegreeClickData['points'][0]['x']
            log_user_action(username, f"Line plot click - avg-degree: step={step}")
            if step != currentStep:
                return step
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    if changed == 'cc-size-lineplot':
        if 'x' in edgesClickData['points'][0]:
            step = edgesClickData['points'][0]['x']
            log_user_action(username, f"Line plot click - cc-size: step={step}")
            if step != currentStep:
                return step
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    if changed == 'nonparticipating-lineplot':
        if 'x' in nonparticipatingClickData['points'][0]:
            step = nonparticipatingClickData['points'][0]['x']
            log_user_action(username, f"Line plot click - nonparticipating: step={step}")
            if step != currentStep:
                return step
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    raise PreventUpdate


@callback(
    Output('sankey', 'children'),
    Input('store-data', 'data'),
    # Input('select-colormap', 'value'),
    State('step-data', 'data')
)
def update_sankey(dataFlat, #colormap, 
                 stepData):
    username = request.authorization['username'] if request.authorization else 'default'
    user_data = get_user_data(username)
    
    # Set default value for commented-out parameter
    colormap = 'ZIEGLER'  # Default colormap
    
    #log_user_action(username, f"update_sankey called - stepData: {stepData}, colormap: {colormap}")
    start = time.time()
    
    if not stepData:
        stepData = 0
    else:
        stepData = stepData["step"]
    if not app_data['data']:
        raise PreventUpdate
    if len(app_data['data']) == 1:
        raise PreventUpdate
    # changed = ctx.triggered_id
    # if changed != 'step-data':
    # Compute ccs
    ccs = []
    startLabel = 1
    for step in range(len(app_data['data'])):
        distributions = np.array(app_data['data'][step]["forces"])
        distributions[distributions < user_data["force_selection"]] = 0
        probabilityGraph = np.count_nonzero(distributions > 0, axis=0)/distributions.shape[0]
        probabilityGraph[probabilityGraph < user_data["uncertainty_selection"]] = 0
        ccs.append(compute_connected_components_single_graph(probabilityGraph, startLabel))
        startLabel = np.max(ccs[-1]) + 1
    # Compute transitions
    transitions = compute_transitions(ccs)
    colorPositions = {}
    nodeMap = {}
    maxPos = np.max(np.mean(app_data['data'][0]["disk_positions"], axis=0), axis=1)
    minPos = np.min(np.mean(app_data['data'][0]["disk_positions"], axis=0), axis=1)
    for i, step in enumerate(ccs):
        maxPos = np.max(np.vstack([maxPos, np.max(np.mean(app_data['data'][i]["disk_positions"], axis=0), axis=1)]), axis=0)
        minPos = np.min(np.vstack([minPos, np.min(np.mean(app_data['data'][i]["disk_positions"], axis=0), axis=1)]), axis=0)
        for label in np.unique(step):
            if label == 0:
                #continue
                colorPositions[-(i+1)] = [0.5,0.5]
                nodeMap[-(i+1)] = np.where(step == label)[0]
            else:
                mean_position = np.mean(app_data['data'][i]["disk_positions"], axis=0)
                colorPositions[int(label)] = np.mean(mean_position[:, step == label], axis=1)
                nodeMap[int(label)] = np.where(step == label)[0]
    for key in colorPositions:
        diff = maxPos - minPos
        maxDiff = np.max(diff)
        colorPositions[key] = [(colorPositions[key][0] - minPos[0]) / maxDiff, (colorPositions[key][1] - minPos[1]) / maxDiff]
        colorPositions[key][1] = 1 - colorPositions[key][1]
    xLabel = [f"{x:.4f}" for x in app_data['packing_fractions']]
    log_user_action('timings', f"Sankey computation took {time.time() - start:.5f}s")
    return sankey_tracking_graph.SankeyTrackingGraph(
        id='sankey-diagram',
        links=transitions,
        colorPositions=colorPositions,
        colormap=colormap,
        step = stepData,
        nodeMap=nodeMap,
        pf = xLabel,
        clickData=None  # Initialize as None, will be updated by click events
    )

@callback(
    Output('spatial-diagram', 'id'),  # Dummy output since we only want to log
    Input('spatial-diagram', 'clickData'),
    prevent_initial_call=True
)
def log_spatial_click_data(clickData):
    """
    Callback to log spatial view click data. Returns the same id to prevent any visual changes.
    """
    print("Spatial view click data received:", clickData)
    username = request.authorization['username'] if request.authorization else 'default'
    
    if clickData:
        log_user_action(username, f"Spatial view interaction: {clickData}")
    
    raise PreventUpdate

@callback(
    Output('sankey-diagram', 'id'),  # Dummy output since we only want to log
    Input('sankey-diagram', 'clickData'),
    prevent_initial_call=True
)
def log_sankey_click_data(clickData):
    """
    Callback to log Sankey view ctrl+click data. Returns the same id to prevent any visual changes.
    """
    username = request.authorization['username'] if request.authorization else 'default'
    
    if clickData:
        log_user_action(username, f"Sankey view ctrl+click interaction: {clickData}")
    
    raise PreventUpdate
    #return 'spatial'  # Return the same id to prevent any changes

@callback(
    Output('user-defined-threshold', 'style'),
    Output('aggregate-jammed', 'style'),
    Input('show-major-minor', 'value')
)
def toggle_user_defined_threshold(showMajorMinor):
    if showMajorMinor:
        return {'display': 'block'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'block'}