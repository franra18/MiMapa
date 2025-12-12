import api from './api';

export const markerService = {
  async getAll() {
    const { data } = await api.get('/markers');
    return data;
  },

  async create(markerData) {
    const { data } = await api.post('/markers', markerData);
    return data;
  },

  async delete(id) {
    await api.delete(`/markers/${id}`);
  }
};

export const geocodingService = {
  async searchPlace(query) {
    const url = `https://nominatim.openstreetmap.org/search?format=jsonv2&q=${encodeURIComponent(query)}&limit=5`;
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'VueMapApp/1.0'
      }
    });
    return await response.json();
  }
};
