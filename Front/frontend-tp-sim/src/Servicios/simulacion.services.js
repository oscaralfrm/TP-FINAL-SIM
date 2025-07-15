// src/Servicios/simulacion.services.js
import axios from 'axios';

const API_URL = 'http://localhost:5000/simular';

export const ejecutarSimulacion = async (parametros) => {
  try {
    const response = await axios.post(API_URL, parametros);
    return response.data;
  } catch (error) {
    console.error('Error en la simulación:', error);
    throw error;
  }
};
