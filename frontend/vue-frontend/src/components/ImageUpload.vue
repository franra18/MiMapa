<template>
  <div class="image-upload">
    <label for="image-input" class="upload-label">
      <div v-if="!previewUrl" class="upload-placeholder">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <circle cx="8.5" cy="8.5" r="1.5"></circle>
          <polyline points="21 15 16 10 5 21"></polyline>
        </svg>
        <p>Seleccionar imagen</p>
        <span>JPG, PNG (máx. 5MB)</span>
      </div>
      <div v-else class="image-preview">
        <img :src="previewUrl" alt="Vista previa">
        <button @click.prevent="removeImage" class="remove-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </label>
    
    <input
      id="image-input"
      type="file"
      accept="image/jpeg,image/png,image/jpg"
      @change="handleFileSelect"
      ref="fileInput"
      style="display: none"
    />

    <div v-if="uploading" class="upload-progress">
      <div class="spinner"></div>
      <span>Subiendo imagen...</span>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['image-uploaded', 'image-removed']);

const fileInput = ref(null);
const previewUrl = ref('');
const uploading = ref(false);
const error = ref('');

async function handleFileSelect(event) {
  const file = event.target.files[0];
  if (!file) return;

  error.value = '';

  // Validar tamaño (5MB máximo)
  if (file.size > 5 * 1024 * 1024) {
    error.value = 'La imagen no puede superar los 5MB';
    return;
  }

  // Validar tipo
  if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
    error.value = 'Solo se permiten imágenes JPG o PNG';
    return;
  }

  // Mostrar preview
  const reader = new FileReader();
  reader.onload = (e) => {
    previewUrl.value = e.target.result;
  };
  reader.readAsDataURL(file);

  // Subir a Cloudinary
  await uploadToCloudinary(file);
}

async function uploadToCloudinary(file) {
  uploading.value = true;
  error.value = '';

  try {
    const cloudName = import.meta.env.VITE_CLOUDINARY_CLOUD_NAME;
    const uploadPreset = import.meta.env.VITE_CLOUDINARY_UPLOAD_PRESET;

    console.log('Cloudinary config:', { cloudName, uploadPreset });

    if (!cloudName || !uploadPreset) {
      throw new Error('Configuración de Cloudinary no encontrada. Verifica las variables de entorno.');
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', uploadPreset);

    const response = await fetch(
      `https://api.cloudinary.com/v1_1/${cloudName}/image/upload`,
      {
        method: 'POST',
        body: formData
      }
    );

    const data = await response.json();
    
    if (!response.ok) {
      console.error('Cloudinary error:', data);
      throw new Error(data.error?.message || 'Error al subir la imagen');
    }

    console.log('Upload successful:', data.secure_url);
    emit('image-uploaded', data.secure_url);
  } catch (err) {
    error.value = err.message || 'Error al subir la imagen. Intenta de nuevo.';
    console.error('Upload error:', err);
    previewUrl.value = '';
  } finally {
    uploading.value = false;
  }
}

function removeImage() {
  previewUrl.value = '';
  error.value = '';
  if (fileInput.value) {
    fileInput.value.value = '';
  }
  emit('image-removed');
}
</script>

<style scoped>
.image-upload {
  margin-bottom: 16px;
}

.upload-label {
  display: block;
  cursor: pointer;
}

.upload-placeholder {
  border: 2px dashed #d1d5db;
  border-radius: 8px;
  padding: 32px;
  text-align: center;
  transition: all 0.3s;
}

.upload-placeholder:hover {
  border-color: #3b82f6;
  background: #f9fafb;
}

.upload-placeholder svg {
  color: #9ca3af;
  margin-bottom: 12px;
}

.upload-placeholder p {
  margin: 8px 0 4px 0;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.upload-placeholder span {
  font-size: 12px;
  color: #6b7280;
}

.image-preview {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #d1d5db;
}

.image-preview img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.remove-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.7);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.3s;
}

.remove-btn:hover {
  background: rgba(0, 0, 0, 0.9);
}

.remove-btn svg {
  color: white;
}

.upload-progress {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
  padding: 12px;
  background: #f0f9ff;
  border-radius: 6px;
  border: 1px solid #bfdbfe;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #3b82f6;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.upload-progress span {
  font-size: 14px;
  color: #1e40af;
}

.error-message {
  margin-top: 12px;
  padding: 12px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  color: #dc2626;
  font-size: 14px;
}
</style>
