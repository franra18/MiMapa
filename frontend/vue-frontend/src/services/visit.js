import api from './api';

export const visitService = {
  async getUserMarkers(email) {
    const { data } = await api.get(`/visits/user/${encodeURIComponent(email)}`);
    return data;
  },

  async getReceivedVisits() {
    const { data } = await api.get('/visits/received');
    return data;
  }
};
