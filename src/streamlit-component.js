import React from 'react';
import ReactDOM from 'react-dom';
import FurnitureConfigurator from './components/ui/FurnitureConfigurator';
import './index.css';

// Parse data from Streamlit
const streamlitArgs = window.parent.streamlitArgs || {};
const theme = streamlitArgs.theme || {};
const initialModelId = streamlitArgs.args?.modelId || 'sofa';

// Set up communication with Streamlit
const Streamlit = {
  setComponentValue: function(value) {
    if (window.parent && window.parent.postMessage) {
      window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: value
      }, '*');
    }
  },
  setFrameHeight: function(height) {
    if (window.parent && window.parent.postMessage) {
      window.parent.postMessage({
        type: 'streamlit:setFrameHeight',
        height: height
      }, '*');
    }
  }
};

// Render the component
ReactDOM.render(
  <React.StrictMode>
    <FurnitureConfigurator 
      initialModelId={initialModelId}
      streamlit={Streamlit}
    />
  </React.StrictMode>,
  document.getElementById('root')
);

// Set initial height
window.addEventListener('load', function() {
  Streamlit.setFrameHeight(document.body.offsetHeight);
});

// Update height on resize
window.addEventListener('resize', function() {
  Streamlit.setFrameHeight(document.body.offsetHeight);
});