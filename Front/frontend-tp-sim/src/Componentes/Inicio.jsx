// src/Componentes/Inicio.jsx
import React, { useState } from 'react';
import { ejecutarSimulacion } from '../Servicios/simulacion.services';
import 'bootstrap/dist/css/bootstrap.min.css';

const Inicio = () => {
  const [formulario, setFormulario] = useState({
    media_llegada: '',
    tiempo_reparacion: '',
    trabajos_a_completar: '',
    iteraciones: ''
  });

  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormulario({ ...formulario, [e.target.name]: e.target.value });
  };

  const handleSimulacion = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const datos = {
        media_llegada: parseFloat(formulario.media_llegada),
        tiempo_reparacion: parseFloat(formulario.tiempo_reparacion),
        trabajos_a_completar: parseInt(formulario.trabajos_a_completar),
        iteraciones: parseInt(formulario.iteraciones)
      };
      const res = await ejecutarSimulacion(datos);
      setResultado(res);
    } catch (err) {
      setError('Ocurrió un error al ejecutar la simulación.');
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4">Simulación de Mecanógrafa</h2>
      <form onSubmit={handleSimulacion}>
        <div className="mb-3">
          <label className="form-label">Media de llegada (min)</label>
          <input type="number" step="0.1" className="form-control" name="media_llegada" value={formulario.media_llegada} onChange={handleChange} required min={0.1} />
        </div>
        <div className="mb-3">
          <label className="form-label">Tiempo de reparación (min)</label>
          <input type="number" step="0.1" className="form-control" name="tiempo_reparacion" value={formulario.tiempo_reparacion} onChange={handleChange} required min={0} />
        </div>
        <div className="mb-3">
          <label className="form-label">Trabajos a completar</label>
          <input type="number" className="form-control" name="trabajos_a_completar" value={formulario.trabajos_a_completar} onChange={handleChange} required min={1} />
        </div>
        <div className="mb-3">
          <label className="form-label">Iteraciones</label>
          <input type="number" className="form-control" name="iteraciones" value={formulario.iteraciones} onChange={handleChange} required min={1} />
        </div>
        <button type="submit" className="btn btn-primary">Ejecutar Simulación</button>
      </form>

      {error && <div className="alert alert-danger mt-3">{error}</div>}

      {resultado && (
        <div className="mt-4">
          <h4>Resultado</h4>
          {resultado.length === 1 ? (
            <pre>{JSON.stringify(resultado[0], null, 2)}</pre>
          ) : (
            resultado.map((r, i) => (
              <div key={i}>
                <h5>Corrida {i + 1}</h5>
                <pre>{JSON.stringify(r, null, 2)}</pre>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default Inicio;
