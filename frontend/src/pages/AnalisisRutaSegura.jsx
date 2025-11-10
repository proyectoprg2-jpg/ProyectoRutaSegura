import { useState, useEffect } from 'react';
import { getIndiceSeguridadAvenidas, getRutasMasSeguras, getZonasMasPeligrosas } from '../services/api';
import { Shield, AlertTriangle, TrendingUp, MapPin, Award } from 'lucide-react';

export default function AnalisisRutaSegura() {
  const [indiceSeguridad, setIndiceSeguridad] = useState([]);
  const [rutasSeguras, setRutasSeguras] = useState([]);
  const [zonasPeligrosas, setZonasPeligrosas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    setLoading(true);
    setError(null);
    try {
      const [indiceResp, segurasResp, peligrosasResp] = await Promise.all([
        getIndiceSeguridadAvenidas(),
        getRutasMasSeguras(5),
        getZonasMasPeligrosas(5)
      ]);

      setIndiceSeguridad(indiceResp.data || []);
      setRutasSeguras(segurasResp.data || []);
      setZonasPeligrosas(peligrosasResp.data || []);
    } catch (err) {
      console.error('Error cargando análisis:', err);
      setError(err.message || 'Error al cargar el análisis');
    } finally {
      setLoading(false);
    }
  };

  const obtenerColorNivel = (nivel) => {
    switch (nivel) {
      case 'Muy Segura':
        return 'bg-green-100 text-green-800';
      case 'Segura':
        return 'bg-blue-100 text-blue-800';
      case 'Moderada':
        return 'bg-yellow-100 text-yellow-800';
      case 'Peligrosa':
        return 'bg-orange-100 text-orange-800';
      case 'Muy Peligrosa':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Calculando índice de seguridad...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Error al cargar análisis</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={cargarDatos}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Análisis Ruta Segura</h1>
          <p className="text-gray-600 mt-1">Índice de seguridad por avenida considerando siniestros y delitos</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Avenidas</p>
              <p className="text-2xl font-bold text-blue-600">{indiceSeguridad.length}</p>
            </div>
            <MapPin className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Rutas Seguras</p>
              <p className="text-2xl font-bold text-green-600">{rutasSeguras.length}</p>
            </div>
            <Shield className="w-8 h-8 text-green-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Zonas Peligrosas</p>
              <p className="text-2xl font-bold text-red-600">{zonasPeligrosas.length}</p>
            </div>
            <AlertTriangle className="w-8 h-8 text-red-500" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow">
          <div className="p-4 border-b border-gray-200 flex items-center gap-2">
            <Award className="w-5 h-5 text-green-600" />
            <h2 className="text-lg font-semibold text-gray-800">Top 5 Rutas Más Seguras</h2>
          </div>
          <div className="p-4">
            {rutasSeguras.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No hay datos suficientes</p>
            ) : (
              <div className="space-y-3">
                {rutasSeguras.map((ruta, index) => (
                  <div key={ruta.avenida_id} className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="bg-green-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold">
                        {index + 1}
                      </div>
                      <div>
                        <p className="font-semibold text-gray-800">{ruta.avenida_nombre}</p>
                        <p className="text-sm text-gray-600">{ruta.zona}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-semibold text-green-700">
                        Índice: {ruta.indice_peligrosidad}
                      </p>
                      <p className="text-xs text-gray-600">
                        {ruta.total_siniestros} siniestros / {ruta.total_delitos} delitos
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow">
          <div className="p-4 border-b border-gray-200 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-red-600" />
            <h2 className="text-lg font-semibold text-gray-800">Top 5 Zonas Más Peligrosas</h2>
          </div>
          <div className="p-4">
            {zonasPeligrosas.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No hay zonas identificadas como peligrosas</p>
            ) : (
              <div className="space-y-3">
                {zonasPeligrosas.map((zona, index) => (
                  <div key={zona.avenida_id} className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="bg-red-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold">
                        {index + 1}
                      </div>
                      <div>
                        <p className="font-semibold text-gray-800">{zona.avenida_nombre}</p>
                        <p className="text-sm text-gray-600">{zona.zona}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-semibold text-red-700">
                        Índice: {zona.indice_peligrosidad}
                      </p>
                      <p className="text-xs text-gray-600">
                        {zona.total_siniestros} siniestros / {zona.total_delitos} delitos
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-800">Índice de Seguridad - Todas las Avenidas</h2>
          <p className="text-sm text-gray-600 mt-1">
            Fórmula: (3 × Siniestros) + (2 × Delitos) × (Factor Fallecidos)
          </p>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Avenida</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Zona</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Siniestros</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Delitos</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fallecidos</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Índice</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nivel</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {indiceSeguridad.map((avenida) => (
                <tr key={avenida.avenida_id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {avenida.avenida_nombre}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {avenida.zona}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {avenida.total_siniestros}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {avenida.total_delitos}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {avenida.total_fallecidos}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                    {avenida.indice_peligrosidad}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${obtenerColorNivel(avenida.nivel_seguridad)}`}>
                      {avenida.nivel_seguridad}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
