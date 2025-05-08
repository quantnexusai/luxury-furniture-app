import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default function MoodBoard() {
  const [activeTab, setActiveTab] = useState('materials');
  const [selectedItems, setSelectedItems] = useState({
    materials: [],
    colors: [],
    styles: [],
    inspirations: []
  });
  
  // Mood board items data
  const moodBoardData = {
    materials: [
      { id: 'm1', name: 'Walnut Wood', image: '/assets/textures/walnut.jpg', description: 'Rich, dark grain with luxurious finish' },
      { id: 'm2', name: 'Calacatta Marble', image: '/assets/textures/marble.jpg', description: 'Pristine white with dramatic veining' },
      { id: 'm3', name: 'Brushed Brass', image: '/assets/textures/brass.jpg', description: 'Warm metallic with subtle texture' },
      { id: 'm4', name: 'Full-Grain Leather', image: '/assets/textures/leather.jpg', description: 'Natural hide with rich patina development' },
      { id: 'm5', name: 'Smoked Oak', image: '/assets/textures/smoked_oak.jpg', description: 'Dark, sophisticated with visible grain' },
      { id: 'm6', name: 'Velvet', image: '/assets/textures/velvet.jpg', description: 'Plush pile with light-catching sheen' }
    ],
    colors: [
      { id: 'c1', name: 'Deep Navy', hex: '#1A2A40', description: 'Rich blue with depth and sophistication' },
      { id: 'c2', name: 'Burnished Gold', hex: '#D4AF37', description: 'Warm, antique gold tone' },
      { id: 'c3', name: 'Forest Green', hex: '#2C5F2D', description: 'Deep natural green with earthy undertones' },
      { id: 'c4', name: 'Ivory', hex: '#FFFFF0', description: 'Warm off-white with subtle depth' },
      { id: 'c5', name: 'Bordeaux', hex: '#5E1914', description: 'Deep wine red with brown notes' },
      { id: 'c6', name: 'Charcoal', hex: '#36454F', description: 'Dark gray with blue undertones' }
    ],
    styles: [
      { id: 's1', name: 'Modern Minimalist', image: '/assets/styles/minimalist.jpg', description: 'Clean lines with focus on materials' },
      { id: 's2', name: 'Art Deco', image: '/assets/styles/art_deco.jpg', description: 'Geometric patterns and bold contrasts' },
      { id: 's3', name: 'Contemporary Craftsman', image: '/assets/styles/craftsman.jpg', description: 'Focus on artisanal details and natural materials' },
      { id: 's4', name: 'Scandinavian Luxury', image: '/assets/styles/scandinavian.jpg', description: 'Light, bright with natural elements' },
      { id: 's5', name: 'Industrial Elegance', image: '/assets/styles/industrial.jpg', description: 'Raw materials refined through exceptional craft' },
      { id: 's6', name: 'Japanese Influence', image: '/assets/styles/japanese.jpg', description: 'Minimal, intentional with reverence for natural beauty' }
    ],
    inspirations: [
      { id: 'i1', name: 'Modern Parisian Apartment', image: '/assets/inspirations/paris.jpg', description: 'Classic architecture with contemporary furnishings' },
      { id: 'i2', name: 'New York Penthouse', image: '/assets/inspirations/nyc.jpg', description: 'Urban sophistication with panoramic views' },
      { id: 'i3', name: 'Kyoto Tea House', image: '/assets/inspirations/kyoto.jpg', description: 'Serene spaces with perfect proportions' },
      { id: 'i4', name: 'Copenhagen Design Studio', image: '/assets/inspirations/copenhagen.jpg', description: 'Thoughtful minimalism with artistic touches' },
      { id: 'i5', name: 'Milan Fashion House', image: '/assets/inspirations/milan.jpg', description: 'Bold expression with impeccable craftsmanship' },
      { id: 'i6', name: 'California Modernism', image: '/assets/inspirations/california.jpg', description: 'Indoor-outdoor living with warm minimalism' }
    ]
  };
  
  // Toggle selection for an item
  const toggleSelection = (itemId) => {
    setSelectedItems(prev => {
      const currentSelection = prev[activeTab];
      const isSelected = currentSelection.includes(itemId);
      
      return {
        ...prev,
        [activeTab]: isSelected
          ? currentSelection.filter(id => id !== itemId)
          : [...currentSelection, itemId]
      };
    });
  };
  
  // Get current tab data
  const currentTabData = moodBoardData[activeTab] || [];
  
  return (
    <div className="flex flex-col h-full">
      <h2 className="text-3xl font-serif mb-6">Design Mood Board</h2>
      
      <Tabs defaultValue="materials" onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid grid-cols-4 mb-8">
          <TabsTrigger value="materials">Materials</TabsTrigger>
          <TabsTrigger value="colors">Colors</TabsTrigger>
          <TabsTrigger value="styles">Styles</TabsTrigger>
          <TabsTrigger value="inspirations">Inspirations</TabsTrigger>
        </TabsList>
        
        {Object.keys(moodBoardData).map(category => (
          <TabsContent key={category} value={category} className="mt-0">
            <div className="grid grid-cols-3 gap-4">
              {moodBoardData[category].map(item => (
                <Card 
                  key={item.id}
                  className={`cursor-pointer transition-all ${
                    selectedItems[category].includes(item.id) ? 'ring-2 ring-primary shadow-lg' : ''
                  }`}
                  onClick={() => toggleSelection(item.id)}
                >
                  <CardContent className="p-3">
                    {/* Item content varies by category */}
                    {category === 'colors' ? (
                      <div className="aspect-square rounded-sm mb-2" style={{ backgroundColor: item.hex }}></div>
                    ) : (
                      <div className="aspect-square bg-gray-100 rounded-sm mb-2">
                        {/* In a real app, this would be an actual image */}
                        <div className="w-full h-full flex items-center justify-center text-sm text-gray-500">
                          {item.name}
                        </div>
                      </div>
                    )}
                    <h3 className="text-sm font-medium">{item.name}</h3>
                    <p className="text-xs text-gray-500">{item.description}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        ))}
      </Tabs>
      
      {/* Selected items preview */}
      <div className="mt-8">
        <h3 className="text-xl font-serif mb-4">Your Selections</h3>
        <div className="flex flex-wrap gap-2">
          {Object.entries(selectedItems).flatMap(([category, itemIds]) => 
            itemIds.map(id => {
              const item = moodBoardData[category].find(item => item.id === id);
              return item ? (
                <div 
                  key={id}
                  className="px-3 py-1 bg-slate-100 rounded-full text-sm flex items-center gap-2"
                >
                  {category === 'colors' && (
                    <div 
                      className="w-3 h-3 rounded-full" 
                      style={{ backgroundColor: item.hex }}
                    ></div>
                  )}
                  <span>{item.name}</span>
                </div>
              ) : null;
            })
          )}
        </div>
      </div>
      
      <div className="mt-8 flex gap-4">
        <Button className="flex-1">Save Mood Board</Button>
        <Button variant="outline" className="flex-1">Share</Button>
      </div>
    </div>
  );
}