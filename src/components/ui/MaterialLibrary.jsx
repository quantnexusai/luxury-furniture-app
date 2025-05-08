import React, { useState } from 'react';
import { Card, CardContent } from './card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './tabs';

export default function MaterialLibrary({ onSelectMaterial }) {
  const [selectedCategory, setSelectedCategory] = useState('wood');
  
  // Material categories
  const materialCategories = {
    wood: [
      { name: 'Walnut', color: '#5D4037', roughness: 0.6 },
      { name: 'Oak', color: '#A1887F', roughness: 0.5 },
      { name: 'Maple', color: '#D7CCC8', roughness: 0.4 },
      { name: 'Mahogany', color: '#3E2723', roughness: 0.4 },
      { name: 'Ebony', color: '#212121', roughness: 0.3 },
      { name: 'Cherry', color: '#A1554D', roughness: 0.5 },
    ],
    stone: [
      { name: 'White Marble', color: '#ECEFF1', roughness: 0.2 },
      { name: 'Black Marble', color: '#263238', roughness: 0.2 },
      { name: 'Travertine', color: '#E0E0E0', roughness: 0.4 },
      { name: 'Granite', color: '#546E7A', roughness: 0.5 },
      { name: 'Terrazzo', color: '#CFD8DC', roughness: 0.6, multiColor: true },
      { name: 'Onyx', color: '#4E342E', roughness: 0.1 },
    ],
    metal: [
      { name: 'Brass', color: '#D4AC0D', metalness: 0.7, roughness: 0.3 },
      { name: 'Chrome', color: '#BDBDBD', metalness: 0.9, roughness: 0.1 },
      { name: 'Copper', color: '#CB6D51', metalness: 0.8, roughness: 0.2 },
      { name: 'Brushed Steel', color: '#9E9E9E', metalness: 0.6, roughness: 0.4 },
      { name: 'Bronze', color: '#CD7F32', metalness: 0.7, roughness: 0.3 },
      { name: 'Platinum', color: '#E5E4E2', metalness: 0.9, roughness: 0.1 },
    ],
    upholstery: [
      { name: 'Leather Black', color: '#212121', roughness: 0.8 },
      { name: 'Leather Brown', color: '#5D4037', roughness: 0.7 },
      { name: 'Linen', color: '#EFEBE9', roughness: 0.9 },
      { name: 'Velvet Blue', color: '#1A237E', roughness: 0.8 },
      { name: 'Velvet Green', color: '#1B5E20', roughness: 0.8 },
      { name: 'Cotton White', color: '#FFFFFF', roughness: 0.9 },
    ],
    glass: [
      { name: 'Clear Glass', color: '#E0F7FA', roughness: 0.1, opacity: 0.3 },
      { name: 'Frosted Glass', color: '#E0F7FA', roughness: 0.6, opacity: 0.7 },
      { name: 'Tinted Glass', color: '#B2DFDB', roughness: 0.1, opacity: 0.5 },
      { name: 'Smoked Glass', color: '#424242', roughness: 0.1, opacity: 0.6 },
      { name: 'Bronze Glass', color: '#A1887F', roughness: 0.1, opacity: 0.5 },
      { name: 'Mirror', color: '#ECEFF1', roughness: 0.1, metalness: 0.9 },
    ]
  };
  
  return (
    <div className="p-4">
      <h3 className="text-lg font-medium mb-4">Material Library</h3>
      
      <Tabs defaultValue="wood" onValueChange={setSelectedCategory}>
        <TabsList className="grid grid-cols-3 mb-4">
          <TabsTrigger value="wood">Wood</TabsTrigger>
          <TabsTrigger value="stone">Stone</TabsTrigger>
          <TabsTrigger value="metal">Metal</TabsTrigger>
        </TabsList>
        <TabsList className="grid grid-cols-2 mb-6">
          <TabsTrigger value="upholstery">Fabric</TabsTrigger>
          <TabsTrigger value="glass">Glass</TabsTrigger>
        </TabsList>
        
        {Object.entries(materialCategories).map(([category, materials]) => (
          <TabsContent key={category} value={category}>
            <div className="grid grid-cols-3 gap-2">
              {materials.map((material) => (
                <Card 
                  key={material.name}
                  className="cursor-pointer hover:shadow-md transition-all"
                  onClick={() => onSelectMaterial(material)}
                >
                  <CardContent className="p-2">
                    <div 
                      className="aspect-square rounded-sm mb-2" 
                      style={{ backgroundColor: material.color }}
                    />
                    <p className="text-xs font-medium text-center truncate">{material.name}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
}