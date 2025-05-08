import { TextureLoader } from 'three';

// Function to load textures
export const loadTexture = (texturePath) => {
  return new Promise((resolve, reject) => {
    const loader = new TextureLoader();
    loader.load(
      texturePath,
      (texture) => {
        resolve(texture);
      },
      undefined,
      (error) => {
        console.error('Error loading texture:', error);
        reject(error);
      }
    );
  });
};

// Common material textures
export const materialTextures = {
  wood: {
    oak: '/textures/oak.jpg',
    walnut: '/textures/walnut.jpg',
    maple: '/textures/maple.jpg',
    mahogany: '/textures/mahogany.jpg',
    ebony: '/textures/ebony.jpg'
  },
  stone: {
    marble: '/textures/marble.jpg',
    granite: '/textures/granite.jpg',
    travertine: '/textures/travertine.jpg'
  },
  metal: {
    brass: '/textures/brass.jpg',
    chrome: '/textures/chrome.jpg',
    copper: '/textures/copper.jpg'
  },
  fabric: {
    linen: '/textures/linen.jpg',
    velvet: '/textures/velvet.jpg',
    leather: '/textures/leather.jpg'
  }
};

// Preload common textures
export const preloadTextures = (textureList) => {
  const promises = [];
  const textures = {};
  
  textureList.forEach((path) => {
    const promise = loadTexture(path).then(texture => {
      const key = path.split('/').pop().split('.')[0];
      textures[key] = texture;
      return texture;
    });
    promises.push(promise);
  });
  
  return Promise.all(promises).then(() => textures);
};