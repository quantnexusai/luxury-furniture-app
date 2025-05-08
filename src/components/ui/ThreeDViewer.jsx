import React, { useRef, useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { 
  OrbitControls, 
  Environment, 
  ContactShadows,
  useGLTF,
  Html,
  useProgress
} from '@react-three/drei';

// Loading indicator component
function Loader() {
  const { progress } = useProgress();
  return <Html center>{progress.toFixed(0)}% loaded</Html>;
}

// Model component with material customization
function Model({ modelPath, materialConfig, ...props }) {
  const { scene } = useGLTF(modelPath);
  const ref = useRef();
  
  // Apply materials based on configuration
  useEffect(() => {
    if (scene) {
      scene.traverse((child) => {
        if (child.isMesh) {
          // Apply material configurations based on mesh names
          // Primary material (usually the largest part)
          if (child.name.includes('primary') && materialConfig.primaryColor) {
            child.material.color.set(materialConfig.primaryColor);
          }
          
          // Secondary materials (accents, details)
          if (child.name.includes('secondary') && materialConfig.secondaryColor) {
            child.material.color.set(materialConfig.secondaryColor);
          }
          
          // Metal parts
          if (child.name.includes('metal') && materialConfig.metalness !== undefined) {
            child.material.metalness = materialConfig.metalness;
            if (materialConfig.metalColor) {
              child.material.color.set(materialConfig.metalColor);
            }
          }
          
          // Apply global material properties
          if (materialConfig.roughness !== undefined) {
            child.material.roughness = materialConfig.roughness;
          }
        }
      });
    }
  }, [scene, materialConfig]);
  
  return <primitive ref={ref} object={scene} {...props} />;
}

// Main 3D viewer component
export default function ThreeDViewer({ 
  modelPath, 
  materialConfig = {}, 
  cameraPosition = [0, 0, 5],
  autoRotate = false,
  environmentPreset = "apartment",
  scale = [1, 1, 1]
}) {
  // Handle model loading errors
  const [error, setError] = useState(null);
  
  // Handle screen resize
  const [size, setSize] = useState({ width: '100%', height: '600px' });
  
  useEffect(() => {
    const updateSize = () => {
      setSize({
        width: '100%',
        height: window.innerHeight * 0.7 + 'px'
      });
    };
    
    window.addEventListener('resize', updateSize);
    updateSize();
    
    return () => window.removeEventListener('resize', updateSize);
  }, []);
  
  return (
    <div style={{ width: size.width, height: size.height }}>
      <Canvas 
        camera={{ position: cameraPosition, fov: 45 }}
        shadows
      >
        {/* Fallback for error handling */}
        {error ? (
          <Html center>
            <div style={{ color: 'red' }}>
              Error loading model: {error.message}
            </div>
          </Html>
        ) : (
          <>
            {/* Lighting setup */}
            <ambientLight intensity={0.5} />
            <spotLight 
              position={[10, 10, 10]} 
              angle={0.15} 
              penumbra={1} 
              castShadow 
              intensity={1.5} 
            />
            <pointLight position={[-10, -10, -10]} intensity={0.5} />
            
            {/* Environment and background */}
            <Environment preset={environmentPreset} />
            
            {/* Loading indicator */}
            <Suspense fallback={<Loader />}>
              {/* Model with material configuration */}
              <Model 
                modelPath={modelPath}
                materialConfig={materialConfig}
                scale={scale}
                position={[0, -1, 0]}
                onError={(e) => setError(e)}
              />
              
              {/* Shadows under the model */}
              <ContactShadows 
                rotation={[-Math.PI / 2, 0, 0]} 
                position={[0, -1.5, 0]} 
                opacity={0.6} 
                width={10} 
                height={10} 
                blur={1.5} 
                far={4} 
              />
            </Suspense>
            
            {/* Camera controls */}
            <OrbitControls 
              enableZoom={true} 
              enablePan={true} 
              enableRotate={true}
              autoRotate={autoRotate}
              autoRotateSpeed={1}
              minDistance={2}
              maxDistance={10}
            />
          </>
        )}
      </Canvas>
    </div>
  );
}

// Preload models for better performance
useGLTF.preload('/models/milano_sofa.glb');
useGLTF.preload('/models/vienna_coffee_table.glb');