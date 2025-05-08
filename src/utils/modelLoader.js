import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

// Function to load 3D models
export const loadModel = (modelPath) => {
  return new Promise((resolve, reject) => {
    const loader = new GLTFLoader();
    loader.load(
      modelPath,
      (gltf) => {
        resolve(gltf);
      },
      (xhr) => {
        console.log((xhr.loaded / xhr.total) * 100 + '% loaded');
      },
      (error) => {
        console.error('An error happened while loading the model:', error);
        reject(error);
      }
    );
  });
};

// Function to apply materials to a model
export const applyMaterialToModel = (model, materialConfig) => {
  if (!model || !model.scene) return model;

  model.scene.traverse((child) => {
    if (child.isMesh) {
      // Apply material properties based on configuration
      if (materialConfig.color && child.material) {
        child.material.color.set(materialConfig.color);
      }
      
      if (materialConfig.metalness !== undefined && child.material) {
        child.material.metalness = materialConfig.metalness;
      }
      
      if (materialConfig.roughness !== undefined && child.material) {
        child.material.roughness = materialConfig.roughness;
      }
      
      // Apply textures if needed
      if (materialConfig.textureMap && child.material) {
        // Implementation for texture mapping would go here
      }
    }
  });

  return model;
};

// Preload common models
export const preloadModels = (modelPaths) => {
  const promises = [];
  const models = {};
  
  Object.entries(modelPaths).forEach(([key, path]) => {
    const promise = loadModel(path).then(model => {
      models[key] = model;
      return model;
    });
    promises.push(promise);
  });
  
  return Promise.all(promises).then(() => models);
};