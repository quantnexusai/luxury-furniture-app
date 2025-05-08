import React from 'react';
import { Card, CardContent } from './card';
import { Slider } from './slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './select';

export default function EnvironmentSettings({ settings, onUpdateSettings }) {
  // Available environment presets
  const environmentPresets = [
    { value: 'apartment', label: 'Apartment' },
    { value: 'city', label: 'City' },
    { value: 'dawn', label: 'Dawn' },
    { value: 'forest', label: 'Forest' },
    { value: 'lobby', label: 'Lobby' },
    { value: 'night', label: 'Night' },
    { value: 'park', label: 'Park' },
    { value: 'studio', label: 'Studio' },
    { value: 'sunset', label: 'Sunset' },
    { value: 'warehouse', label: 'Warehouse' },
  ];
  
  return (
    <div className="p-4">
      <h3 className="text-lg font-medium mb-4">Lighting & Environment</h3>
      
      <div className="space-y-6">
        {/* Environment Preset */}
        <div>
          <label className="text-sm font-medium mb-2 block">Environment</label>
          <Select 
            value={settings.environmentPreset}
            onValueChange={(value) => onUpdateSettings({ environmentPreset: value })}
          >
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Select environment" />
            </SelectTrigger>
            <SelectContent>
              {environmentPresets.map(preset => (
                <SelectItem key={preset.value} value={preset.value}>
                  {preset.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        
        {/* Light Intensity */}
        <div>
          <label className="text-sm font-medium mb-2 block">
            Light Intensity: {settings.lightIntensity.toFixed(1)}
          </label>
          <Slider
            value={[settings.lightIntensity * 10]}
            min={0}
            max={30}
            step={1}
            onValueChange={(value) => onUpdateSettings({ 
              lightIntensity: value[0] / 10
            })}
          />
        </div>
        
        {/* Ambient Light */}
        <div>
          <label className="text-sm font-medium mb-2 block">
            Ambient Light: {settings.ambientIntensity.toFixed(1)}
          </label>
          <Slider
            value={[settings.ambientIntensity * 10]}
            min={0}
            max={20}
            step={1}
            onValueChange={(value) => onUpdateSettings({ 
              ambientIntensity: value[0] / 10
            })}
          />
        </div>
        
        {/* Shadow Intensity */}
        <div>
          <label className="text-sm font-medium mb-2 block">
            Shadow Intensity: {settings.shadowOpacity.toFixed(1)}
          </label>
          <Slider
            value={[settings.shadowOpacity * 10]}
            min={0}
            max={10}
            step={1}
            onValueChange={(value) => onUpdateSettings({ 
              shadowOpacity: value[0] / 10
            })}
          />
        </div>
        
        {/* Environment Examples */}
        <div>
          <label className="text-sm font-medium mb-2 block">Environment Examples</label>
          <div className="grid grid-cols-3 gap-2">
            {['studio', 'apartment', 'sunset'].map(preset => (
              <Card 
                key={preset}
                className={`cursor-pointer transition-all ${
                  settings.environmentPreset === preset ? 'ring-2 ring-primary' : ''
                }`}
                onClick={() => onUpdateSettings({ environmentPreset: preset })}
              >
                <CardContent className="p-2">
                  <div className="aspect-square bg-gray-200 rounded-sm mb-1 flex items-center justify-center">
                    <span className="text-xs">{preset}</span>
                  </div>
                  <p className="text-xs text-center capitalize">{preset}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}