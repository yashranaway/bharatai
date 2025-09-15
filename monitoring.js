#!/usr/bin/env node

/**
 * Simple monitoring script for Mini Bharat AI Store
 * Checks the health of both frontend and backend services
 */

import http from 'http';

// Configuration
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:3001';
const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:8501';

// Health check function
async function checkHealth(url, serviceName) {
  try {
    const response = await fetch(`${url}/api/health`);
    if (response.ok) {
      const data = await response.json();
      console.log(`${serviceName} is running - ${data.message}`);
      return true;
    } else {
      console.log(`${serviceName} is unhealthy - HTTP ${response.status}`);
      return false;
    }
  } catch (error) {
    console.log(`${serviceName} is down - ${error.message}`);
    return false;
  }
}

// Main monitoring function
async function monitorServices() {
  console.log(`\nMonitoring Mini Bharat AI Store Services - ${new Date().toISOString()}`);
  console.log('=' .repeat(50));
  
  // Check backend
  const backendHealthy = await checkHealth(BACKEND_URL, 'Backend API');
  
  // Check frontend (Streamlit doesn't have a standard health endpoint, so we'll just check if it responds)
  try {
    const response = await fetch(FRONTEND_URL);
    if (response.ok) {
      console.log(`Frontend Interface is accessible`);
    } else {
      console.log(`Frontend Interface is not accessible - HTTP ${response.status}`);
    }
  } catch (error) {
    console.log(`Frontend Interface is down - ${error.message}`);
  }
  
  console.log('=' .repeat(50));
  
  if (backendHealthy) {
    console.log('All critical services are running!');
  } else {
    console.log('Some services require attention!');
  }
}

// Run monitoring
monitorServices();

// If running in continuous mode
if (process.argv.includes('--continuous')) {
  const interval = process.argv.includes('--interval') 
    ? parseInt(process.argv[process.argv.indexOf('--interval') + 1]) * 1000 
    : 30000; // Default 30 seconds
  
  console.log(`\nContinuous monitoring enabled (every ${interval/1000} seconds)`);
  console.log('Press Ctrl+C to stop\n');
  
  setInterval(monitorServices, interval);
}