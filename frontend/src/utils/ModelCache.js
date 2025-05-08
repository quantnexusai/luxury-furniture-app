import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { TextureLoader } from 'three';

// Create singleton cache for models and textures
class ModelCache {
  constructor() {
    this.models = {};
    this.textures = {};
    this.gltfLoader = new GLTFLoader();
    this.textureLoader = new TextureLoader();
  }
  
  // Load a model and cache it
  loadModel(modelPath) {
    // Return from cache if already loaded
    if (this.models[modelPath]) {
      return Promise.resolve(this.models[modelPath]);
    }
    
    // Load and cache the model
    return new Promise((resolve, reject) => {
      this.gltfLoader.load(
        modelPath,
        (gltf) => {
          this.models[modelPath] = gltf;
          resolve(gltf);
        },
        (xhr) => {
          console.log((xhr.loaded / xhr.total) * 100 + '% loaded');
        },
        (error) => {
          console.error('Error loading model:', error);
          reject(error);
        }
      );
    });
  }
  
  // Load a texture and cache it
  loadTexture(texturePath) {
    // Return from cache if already loaded
    if (this.textures[texturePath]) {
      return Promise.resolve(this.textures[texturePath]);
    }
    
    // Load and cache the texture
    return new Promise((resolve, reject) => {
      this.textureLoader.load(
        texturePath,
        (texture) => {
          this.textures[texturePath] = texture;
          resolve(texture);
        },
        undefined,
        (error) => {
          console.error('Error loading texture:', error);
          reject(error);
        }
      );
    });
  }
  
  // Preload multiple models
  preloadModels(modelPaths) {
    return Promise.all(
      Object.values(modelPaths).map(path => this.loadModel(path))
    );
  }
  
  // Preload multiple textures
  preloadTextures(texturePaths) {
    return Promise.all(
      Object.values(texturePaths).map(path => this.loadTexture(path))
    );
  }
}

// Export singleton instance
export default new ModelCache();