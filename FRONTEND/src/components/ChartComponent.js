// FRONTEND/src/components/ChartComponent.js
import React, { useState, useEffect } from 'react';
import { fetchChartData, checkBackendHealth } from '../services/api';

function ChartComponent() {
  const [chartData, setChartData] = useState([]);
  const [backendStatus, setBackendStatus] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check backend connection first
    checkBackendHealth().then(status => {
      setBackendStatus(status.status);
    });

    // Fetch chart data
    fetchChartData()
      .then(data => {
        setChartData(data.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Failed to fetch chart data:', error);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading data from chartitze backend...</div>;

  return (
    <div>
      <h2>Backend Status: {backendStatus}</h2>
      <h3>Chart Data from Backend:</h3>
      <ul>
        {chartData.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default ChartComponent;