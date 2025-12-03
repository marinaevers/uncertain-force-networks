/* eslint no-magic-numbers: 0 */
import React, { useState } from 'react';

import { SankeyTrackingGraph } from '../lib';

const App = () => {

    const [state, setState] = useState({id:'Test', 
        links:[[0,1,5],[0,2,3],[2,3,3], [1,3,3], [1,4,2]], 
        colorPositions:{0:[0.5, 0.5],1:[0.2, 0.5],2:[0.5, 0.7],3:[0.2, 0.9],4:[0.1, 0.2]}});
    const setProps = (newProps) => {
            setState(newProps);
        };

    return (
        <div>
            <SankeyTrackingGraph
                setProps={setProps}
                {...state}
            />
        </div>
    )
};


export default App;
