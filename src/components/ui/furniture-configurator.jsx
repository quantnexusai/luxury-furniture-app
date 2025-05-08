import React, { useState, useEffect, Suspense } from 'react';
import ThreeDViewer from './ThreeDViewer';
import MaterialLibrary from './MaterialLibrary';
import EnvironmentSettings from './EnvironmentSettings';
import ModelCache from '../utils/ModelCache';
import { Card, CardContent } from './card';
import { Button } from './button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './tabs';
import { Slider } from './slider';
import { Switch } from './switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './select';
import { Skeleton } from './skeleton';

export default function FurnitureConfigurator({ initialModelId = 'sofa' }) {
  // Configuration state
  const [selectedModel, setSelectedModel] = useState(initialModelId);
  const [materialConfig, setMaterialConfig] = useState({
    primaryColor: '#8B4513',
    secondaryColor: '#5D4037',
    metalColor: '#D4AC0D',
    metalness: 0.7,
    roughness: 0.6,
  });
  const [dimensions, setDimensions] = useState({
    width: 100,
    depth: 80,
    height: 45
  });
  const [features, setFeatures] = useState([]);
  const [autoRotate, setAutoRotate] = useState(true);
  const [isLoading, setIsLoading] = useState(true);
  
  // Add environment settings state
  const [environmentSettings, setEnvironmentSettings] = useState({
    environmentPreset: 'apartment',
    lightIntensity: 1.5,
    ambientIntensity: 0.5,
    shadowOpacity: 0.6
  });
  
  // Add viewing mode state
  const [viewingMode, setViewingMode] = useState('configure');
  
  // Model paths mapping
  const modelPaths = {
    sofa: '/models/milano_sofa.glb',
    coffeeTable: '/models/vienna_coffee_table.glb',
    diningChair: '/models/oslo_dining_chair.glb',
    bookshelf: '/models/manhattan_bookshelf.glb'
  };
  
  // Material options with realistic furniture materials
  const materialOptions = [
    { name: 'Walnut', primaryColor: '#5D4037', roughness: 0.6, group: 'wood' },
    { name: 'Oak', primaryColor: '#A1887F', roughness: 0.5, group: 'wood' },
    { name: 'Mahogany', primaryColor: '#3E2723', roughness: 0.4, group: 'wood' },
    { name: 'White Marble', primaryColor: '#ECEFF1', roughness: 0.2, group: 'stone' },
    { name: 'Black Marble', primaryColor: '#263238', roughness: 0.2, group: 'stone' },
    { name: 'Brass', primaryColor: '#D4AC0D', metalness: 0.7, roughness: 0.3, group: 'metal' },
    { name: 'Chrome', primaryColor: '#BDBDBD', metalness: 0.9, roughness: 0.1, group: 'metal' },
    { name: 'Leather Black', primaryColor: '#212121', roughness: 0.8, group: 'upholstery' },
    { name: 'Leather Brown', primaryColor: '#5D4037', roughness: 0.7, group: 'upholstery' },
    { name: 'Linen', primaryColor: '#EFEBE9', roughness: 0.9, group: 'upholstery' },
    { name: 'Velvet Blue', primaryColor: '#1A237E', roughness: 0.8, group: 'upholstery' },
    { name: 'Velvet Green', primaryColor: '#1B5E20', roughness: 0.8, group: 'upholstery' }
  ];
  
  // Material options grouped by type
  const materialGroups = materialOptions.reduce((groups, material) => {
    if (!groups[material.group]) {
      groups[material.group] = [];
    }
    groups[material.group].push(material);
    return groups;
  }, {});
  
  // Features based on furniture type
  const availableFeatures = {
    sofa: [
      { id: 'premium_cushions', name: 'Premium Down Cushions', price: 499 },
      { id: 'brass_feet', name: 'Brass Feet', price: 299 },
      { id: 'contrast_piping', name: 'Contrast Piping', price: 199 },
      { id: 'usb_charger', name: 'USB Charging Port', price: 349 },
      { id: 'lumbar_pillows', name: 'Lumbar Support Pillows', price: 249 }
    ],
    coffeeTable: [
      { id: 'storage_drawer', name: 'Hidden Storage Drawer', price: 399 },
      { id: 'glass_inlay', name: 'Glass Inlay', price: 499 },
      { id: 'brass_details', name: 'Brass Detail Work', price: 299 },
      { id: 'matched_veining', name: 'Book-Matched Veining', price: 599 },
      { id: 'felt_lining', name: 'Felt-Lined Base', price: 149 }
    ],
    diningChair: [
      { id: 'premium_cushion', name: 'Premium Seat Cushion', price: 199 },
      { id: 'brass_caps', name: 'Brass Foot Caps', price: 149 },
      { id: 'leather_back', name: 'Leather Back Panel', price: 299 },
      { id: 'arm_rests', name: 'Custom Arm Rests', price: 249 },
      { id: 'caning_detail', name: 'Caning Detail', price: 349 }
    ],
    bookshelf: [
      { id: 'integrated_lighting', name: 'Integrated Lighting', price: 899 },
      { id: 'glass_doors', name: 'Glass Cabinet Doors', price: 599 },
      { id: 'cable_management', name: 'Cable Management System', price: 249 },
      { id: 'adjustable_shelves', name: 'Adjustable Shelving', price: 349 },
      { id: 'metal_accents', name: 'Metal Accent Details', price: 399 }
    ]
  };
  
  // Update material configuration
  const handleMaterialChange = (material) => {
    setMaterialConfig({
      primaryColor: material.primaryColor,
      secondaryColor: material.secondaryColor || material.primaryColor,
      metalColor: material.metalColor || '#D4AC0D',
      metalness: material.metalness !== undefined ? material.metalness : 0,
      roughness: material.roughness !== undefined ? material.roughness : 0.5,
    });
  };
  
  // Update dimensions
  const handleDimensionChange = (dimension, value) => {
    setDimensions(prev => ({
      ...prev,
      [dimension]: value
    }));
  };
  
  // Toggle features
  const toggleFeature = (featureId) => {
    setFeatures(prev => 
      prev.includes(featureId)
        ? prev.filter(id => id !== featureId)
        : [...prev, featureId]
    );
  };
  
  // Change model
  const handleModelChange = (modelId) => {
    setSelectedModel(modelId);
    setFeatures([]); // Reset features when model changes
    setIsLoading(true);
    
    // Set default dimensions based on selected model
    const defaultDimensions = {
      sofa: { width: 220, depth: 95, height: 85 },
      coffeeTable: { width: 120, depth: 80, height: 45 },
      diningChair: { width: 50, depth: 55, height: 80 },
      bookshelf: { width: 180, depth: 45, height: 240 }
    };
    
    setDimensions(defaultDimensions[modelId] || { width: 100, depth: 80, height: 45 });
  };
  
  // Calculate price based on configuration
  const calculatePrice = () => {
    // Base prices
    const basePrices = {
      sofa: 8950,
      coffeeTable: 5650,
      diningChair: 2450,
      bookshelf: 11200
    };
    
    // Material multipliers
    const materialMultipliers = {
      'wood': 1,
      'stone': 1.4,
      'metal': 1.2,
      'upholstery': 1.1
    };
    
    // Calculate base price with material
    let price = basePrices[selectedModel] || 3000;
    
    // Find the selected material and apply multiplier
    const selectedMaterialGroup = materialOptions.find(m => m.primaryColor === materialConfig.primaryColor)?.group;
    if (selectedMaterialGroup) {
      price *= materialMultipliers[selectedMaterialGroup] || 1;
    }
    
    // Add feature costs
    features.forEach(featureId => {
      const feature = availableFeatures[selectedModel]?.find(f => f.id === featureId);
      if (feature) {
        price += feature.price;
      }
    });
    
    // Apply dimension adjustments (custom sizing costs more)
    const standardDimensions = {
      sofa: { width: 220, depth: 95, height: 85 },
      coffeeTable: { width: 120, depth: 80, height: 45 },
      diningChair: { width: 50, depth: 55, height: 80 },
      bookshelf: { width: 180, depth: 45, height: 240 }
    };
    
    const standard = standardDimensions[selectedModel] || { width: 100, depth: 80, height: 45 };
    
    // If dimensions are non-standard, add 10% to the price
    if (dimensions.width !== standard.width || 
        dimensions.depth !== standard.depth || 
        dimensions.height !== standard.height) {
      price *= 1.1; // 10% premium for custom dimensions
    }
    
    return Math.round(price);
  };
  
  // Handle model loading
  useEffect(() => {
    // Simulate loading time
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1500);
    
    return () => clearTimeout(timer);
  }, [selectedModel]);
  
  // Preload models on component mount
  useEffect(() => {
    ModelCache.preloadModels(modelPaths).then(() => {
      console.log('Models preloaded successfully');
    });
  }, []);
  
  // Handle environment settings update
  const handleEnvironmentUpdate = (newSettings) => {
    setEnvironmentSettings(prev => ({
      ...prev,
      ...newSettings
    }));
  };
  
  // Save configuration to send back to Streamlit
  const saveConfiguration = () => {
    const config = {
      modelId: selectedModel,
      modelName: getModelDisplayName(selectedModel),
      materials: {
        primary: materialOptions.find(m => m.primaryColor === materialConfig.primaryColor)?.name || 'Custom',
        ...materialConfig
      },
      dimensions: dimensions,
      features: features.map(id => {
        const feature = availableFeatures[selectedModel]?.find(f => f.id === id);
        return feature ? feature.name : id;
      }),
      price: calculatePrice()
    };
    
    // In a real app, this would send the configuration to a server or parent component
    console.log('Saved configuration:', config);
    
    // If using in Streamlit, you would use the Streamlit component API to return this value
    if (window.parent) {
      try {
        // This is how Streamlit components communicate with the parent
        window.parent.postMessage({
          type: 'streamlit:setComponentValue',
          value: config
        }, '*');
      } catch (error) {
        console.error('Error saving configuration:', error);
      }
    }
    
    return config;
  };
  
  // Helper to get display name for models
  const getModelDisplayName = (modelId) => {
    const names = {
      sofa: 'Milano Sofa',
      coffeeTable: 'Vienna Coffee Table',
      diningChair: 'Oslo Dining Chair',
      bookshelf: 'Manhattan Bookshelf'
    };
    return names[modelId] || modelId;
  };
  
  return (
    <div className="flex flex-col lg:flex-row w-full bg-gray-50 rounded-lg overflow-hidden">
      {/* 3D Viewer */}
      <div className="flex-1 bg-gradient-to-b from-slate-50 to-slate-100 min-h-[500px] relative">
        {/* Add viewing mode controls */}
        <div className="absolute top-4 right-4 z-10 bg-white rounded-md shadow-sm">
          <div className="flex">
            <button
              className={`px-3 py-1 text-sm ${viewingMode === 'configure' ? 'bg-primary text-white' : 'bg-white'}`}
              onClick={() => setViewingMode('configure')}
            >
              Configure
            </button>
            <button
              className={`px-3 py-1 text-sm ${viewingMode === 'materials' ? 'bg-primary text-white' : 'bg-white'}`}
              onClick={() => setViewingMode('materials')}
            >
              Materials
            </button>
            <button
              className={`px-3 py-1 text-sm ${viewingMode === 'environment' ? 'bg-primary text-white' : 'bg-white'}`}
              onClick={() => setViewingMode('environment')}
            >
              Environment
            </button>
          </div>
        </div>
        
        {isLoading ? (
          <div className="w-full h-full flex items-center justify-center">
            <div className="text-center">
              <Skeleton className="h-[400px] w-[600px] mx-auto rounded-md" />
              <p className="mt-4 text-slate-500">Loading 3D model...</p>
            </div>
          </div>
        ) : (
          <ThreeDViewer 
            modelPath={modelPaths[selectedModel]}
            materialConfig={materialConfig}
            autoRotate={autoRotate}
            environmentPreset={environmentSettings.environmentPreset}
            lightIntensity={environmentSettings.lightIntensity}
            ambientIntensity={environmentSettings.ambientIntensity}
            shadowOpacity={environmentSettings.shadowOpacity}
            scale={[
              dimensions.width / 100,
              dimensions.height / 100,
              dimensions.depth / 100
            ]}
          />
        )}
        
        <div className="absolute bottom-4 left-4">
          <Button
            variant="outline"
            onClick={() => setAutoRotate(!autoRotate)}
            className="bg-white"
          >
            {autoRotate ? 'Stop Rotation' : 'Start Rotation'}
          </Button>
        </div>
      </div>
      
      {/* Right Panel - Switch between configurator, material library, and environment settings */}
      <div className="w-full lg:w-80 bg-white overflow-y-auto border-l border-gray-200">
        {viewingMode === 'configure' && (
          <div className="p-4">
            <h2 className="text-2xl font-serif mb-4">{getModelDisplayName(selectedModel)}</h2>
            
            <Tabs defaultValue="model">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="model">Model</TabsTrigger>
                <TabsTrigger value="material">Material</TabsTrigger>
                <TabsTrigger value="dimensions">Size</TabsTrigger>
                <TabsTrigger value="features">Features</TabsTrigger>
              </TabsList>
              
              {/* Model Selection */}
              <TabsContent value="model">
                <div className="grid grid-cols-2 gap-2 mt-2">
                  {Object.entries(modelPaths).map(([key]) => (
                    <Card 
                      key={key}
                      className={`cursor-pointer transition-all ${selectedModel === key ? 'ring-2 ring-primary' : ''}`}
                      onClick={() => handleModelChange(key)}
                    >
                      <CardContent className="p-2">
                        <div className="aspect-square bg-gray-100 rounded-sm mb-2 flex items-center justify-center text-xs">
                          {getModelDisplayName(key)}
                        </div>
                        <p className="text-center text-sm font-medium truncate">
                          {getModelDisplayName(key)}
                        </p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>
              
              {/* Material Selection */}
              <TabsContent value="material">
                <div className="space-y-4 mt-2">
                  {Object.entries(materialGroups).map(([groupKey, materials]) => (
                    <div key={groupKey}>
                      <h3 className="text-sm font-medium capitalize mb-2">{groupKey}</h3>
                      <div className="grid grid-cols-2 gap-2">
                        {materials.map((material) => (
                          <div 
                            key={material.name}
                            className={`flex flex-col items-center p-2 border rounded-sm cursor-pointer hover:bg-gray-50 ${
                              materialConfig.primaryColor === material.primaryColor ? 'ring-2 ring-primary' : ''
                            }`}
                            onClick={() => handleMaterialChange(material)}
                          >
                            <div 
                              className="w-full aspect-square rounded-sm mb-1" 
                              style={{ backgroundColor: material.primaryColor }}
                            ></div>
                            <span className="text-xs text-center">{material.name}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                  
                  {/* Advanced material controls */}
                  <div className="pt-4 border-t">
                    <h3 className="text-sm font-medium mb-2">Fine Adjustments</h3>
                    <div className="space-y-3">
                      <div>
                        <label className="text-xs text-gray-500 mb-1 block">
                          Roughness: {materialConfig.roughness.toFixed(2)}
                        </label>
                        <Slider
                          value={[materialConfig.roughness * 100]}
                          min={0}
                          max={100}
                          step={1}
                          onValueChange={(value) => setMaterialConfig(prev => ({
                            ...prev,
                            roughness: value[0] / 100
                          }))}
                        />
                      </div>
                      
                      <div>
                        <label className="text-xs text-gray-500 mb-1 block">
                          Metalness: {materialConfig.metalness.toFixed(2)}
                        </label>
                        <Slider
                          value={[materialConfig.metalness * 100]}
                          min={0}
                          max={100}
                          step={1}
                          onValueChange={(value) => setMaterialConfig(prev => ({
                            ...prev,
                            metalness: value[0] / 100
                          }))}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </TabsContent>
              
              {/* Dimensions */}
              <TabsContent value="dimensions">
                <div className="space-y-4 mt-2">
                  <div>
                    <label className="text-sm font-medium mb-1 block">
                      Width: {dimensions.width}cm
                    </label>
                    <Slider
                      value={[dimensions.width]}
                      min={Math.max(50, dimensions.width * 0.7)} // Limit minimum size
                      max={dimensions.width * 1.3} // Limit maximum size
                      step={1}
                      onValueChange={(value) => handleDimensionChange('width', value[0])}
                    />
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium mb-1 block">
                      Depth: {dimensions.depth}cm
                    </label>
                    <Slider
                      value={[dimensions.depth]}
                      min={Math.max(40, dimensions.depth * 0.7)}
                      max={dimensions.depth * 1.3}
                      step={1}
                      onValueChange={(value) => handleDimensionChange('depth', value[0])}
                    />
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium mb-1 block">
                      Height: {dimensions.height}cm
                    </label>
                    <Slider
                      value={[dimensions.height]}
                      min={Math.max(30, dimensions.height * 0.7)}
                      max={dimensions.height * 1.3}
                      step={1}
                      onValueChange={(value) => handleDimensionChange('height', value[0])}
                    />
                  </div>
                  
                  {/* Custom size warning */}
                  {(dimensions.width !== (standardDimensions[selectedModel]?.width || 100) || 
                    dimensions.depth !== (standardDimensions[selectedModel]?.depth || 80) || 
                    dimensions.height !== (standardDimensions[selectedModel]?.height || 45)) && (
                    <div className="p-2 bg-amber-50 border border-amber-200 rounded-sm text-xs text-amber-800">
                      Custom dimensions will add 10% to the final price and may extend delivery time.
                    </div>
                  )}
                </div>
              </TabsContent>
              
              {/* Features */}
              <TabsContent value="features">
                <div className="space-y-3 mt-2">
                  {availableFeatures[selectedModel]?.map((feature) => (
                    <div 
                      key={feature.id}
                      className="flex items-center justify-between p-2 border rounded-sm"
                    >
                      <div className="flex flex-col">
                        <span className="text-sm font-medium">{feature.name}</span>
                        <span className="text-xs text-gray-500">${feature.price}</span>
                      </div>
                      <Switch
                        checked={features.includes(feature.id)}
                        onCheckedChange={() => toggleFeature(feature.id)}
                      />
                    </div>
                  ))}
                  
                  {availableFeatures[selectedModel]?.length === 0 && (
                    <div className="text-center py-4 text-gray-500">
                      No additional features available for this model.
                    </div>
                  )}
                </div>
              </TabsContent>
            </Tabs>
            
            {/* Price and Actions */}
            <div className="mt-8 space-y-4">
              <div className="flex justify-between items-center p-4 bg-slate-50 rounded-md">
                <span className="text-lg font-medium">Total Price</span>
                <span className="text-2xl font-serif">${calculatePrice().toLocaleString()}</span>
              </div>
              
              <Button 
                className="w-full bg-primary text-white"
                onClick={saveConfiguration}
              >
                Save Configuration
              </Button>
              
              <Button variant="outline" className="w-full">
                Add to Project
              </Button>
            </div>
          </div>
        )}
        
        {viewingMode === 'materials' && (
          <MaterialLibrary onSelectMaterial={handleMaterialChange} />
        )}
        
        {viewingMode === 'environment' && (
          <EnvironmentSettings 
            settings={environmentSettings}
            onUpdateSettings={handleEnvironmentUpdate}
          />
        )}
      </div>
    </div>
  );
}