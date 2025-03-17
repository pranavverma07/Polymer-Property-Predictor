import React from 'react';
import Plot from 'react-plotly.js';

interface PropertyGraphProps {
  title: string;
  data: number[];
  labels: string[];
}

const PropertyGraph: React.FC<PropertyGraphProps> = ({ title, data, labels }) => {
  return (
    <div className="w-full h-[300px] bg-white rounded-lg shadow-lg p-4">
      <Plot
        data={[
          {
            type: 'scatter',
            mode: 'lines+markers',
            x: labels,
            y: data,
            marker: { color: '#00ff88' },
          },
        ]}
        layout={{
          title: title,
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(0,0,0,0)',
          font: { color: '#333' },
          margin: { t: 50, r: 20, l: 50, b: 50 },
        }}
        config={{ responsive: true }}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
};

export default PropertyGraph;