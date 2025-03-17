import React, { useState } from 'react';
import { Search, BarChart2, FileText, Molecule } from 'lucide-react';
import MoleculeViewer from './components/MoleculeViewer';
import PropertyGraph from './components/PropertyGraph';

function App() {
  const [smilesInput, setSmilesInput] = useState('');
  const [predictions, setPredictions] = useState<null | any>(null);
  const [description, setDescription] = useState<string>('');

  const handlePredict = () => {
    // Simulated prediction data
    setPredictions({
      property1: [0.5, 0.7, 0.3, 0.8],
      property2: [0.3, 0.6, 0.9, 0.4],
      property3: [0.7, 0.2, 0.5, 0.6],
      property4: [0.4, 0.8, 0.3, 0.7],
    });
  };

  const handleGenerateDescription = () => {
    setDescription('This polymer exhibits excellent thermal stability and mechanical properties...');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-blue-500">
            SMILES Predictor
          </h1>
          <p className="text-gray-400">Predict polymer properties using SMILES notation</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <div className="bg-gray-800 p-6 rounded-lg shadow-xl">
            <div className="flex gap-4 mb-6">
              <input
                type="text"
                value={smilesInput}
                onChange={(e) => setSmilesInput(e.target.value)}
                placeholder="Enter SMILES string..."
                className="flex-1 px-4 py-2 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-400"
              />
              <button
                onClick={handlePredict}
                className="px-6 py-2 bg-green-500 hover:bg-green-600 rounded-lg flex items-center gap-2 transition-colors"
              >
                <Search size={20} />
                Predict
              </button>
            </div>
            <MoleculeViewer />
          </div>

          <div className="bg-gray-800 p-6 rounded-lg shadow-xl">
            <div className="mb-4 flex justify-between items-center">
              <h2 className="text-xl font-semibold flex items-center gap-2">
                <FileText size={24} />
                Description
              </h2>
              <button
                onClick={handleGenerateDescription}
                className="px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg flex items-center gap-2 transition-colors"
              >
                Generate
              </button>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg min-h-[200px]">
              {description || 'Description will appear here...'}
            </div>
          </div>
        </div>

        {predictions && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <PropertyGraph
              title="Thermal Properties"
              data={predictions.property1}
              labels={['Tg', 'Tm', 'Td', 'Tc']}
            />
            <PropertyGraph
              title="Mechanical Properties"
              data={predictions.property2}
              labels={['E', 'σy', 'εb', 'H']}
            />
            <PropertyGraph
              title="Chemical Properties"
              data={predictions.property3}
              labels={['pH', 'Solubility', 'Reactivity', 'Stability']}
            />
            <PropertyGraph
              title="Physical Properties"
              data={predictions.property4}
              labels={['Density', 'MW', 'PDI', 'Crystallinity']}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;