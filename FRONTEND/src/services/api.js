// FRONTEND/src/services/api.js
const API_URL = 'http://localhost:5000/api';

export const fetchChartData = async () => {
  try {
    const response = await fetch(`${API_URL}/data`);
    if (!response.ok) throw new Error('Network response was not ok');
    return await response.json();
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
};

export const checkBackendHealth = async () => {
  try {
    const response = await fetch(`${API_URL}/health`);
    return await response.json();
  } catch (error) {
    console.error('Backend is not reachable:', error);
    return { status: 'Backend not connected' };
  }
};