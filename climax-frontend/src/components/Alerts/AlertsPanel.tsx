import React, { useEffect, useState } from 'react';
import { AlertTriangle, MapPin, Users, Package, Clock, Shield, RefreshCw } from 'lucide-react';
import { alertService } from '../../services/api';
import type { DisasterAlert } from '../../types';
import { format } from 'date-fns';

const AlertsPanel: React.FC = () => {
  const [alerts, setAlerts] = useState<DisasterAlert[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  const fetchAlerts = async () => {
    try {
      const data = await alertService.getAlerts(20);
      setAlerts(data);
    } catch (error) {
      console.error('Failed to fetch alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateTestAlerts = async () => {
    setGenerating(true);
    try {
      await alertService.generateTestAlerts();
      await fetchAlerts(); // Refresh alerts after generation
    } catch (error) {
      console.error('Failed to generate test alerts:', error);
    } finally {
      setGenerating(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const getAlertLevelColor = (level: string) => {
    switch (level) {
      case 'critical': return 'bg-red-500/20 border-red-500 text-red-400';
      case 'high': return 'bg-orange-500/20 border-orange-500 text-orange-400';
      case 'medium': return 'bg-yellow-500/20 border-yellow-500 text-yellow-400';
      default: return 'bg-green-500/20 border-green-500 text-green-400';
    }
  };

  const getDisasterIcon = (type: string) => {
    switch (type) {
      case 'flood': return '🌊';
      case 'heatwave': return '🔥';
      case 'cyclone': return '🌪️';
      case 'drought': return '🏜️';
      case 'earthquake': return '🏔️';
      default: return '⚠️';
    }
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="bg-white/10 backdrop-blur-sm rounded-xl p-6 animate-pulse">
            <div className="h-4 bg-white/20 rounded mb-4"></div>
            <div className="h-8 bg-white/20 rounded mb-2"></div>
            <div className="h-4 bg-white/20 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-white flex items-center">
          <AlertTriangle className="h-6 w-6 text-red-400 mr-2" />
          Disaster Alerts & Blockchain Verification
        </h2>
        <div className="flex space-x-3">
          <button
            onClick={fetchAlerts}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          >
            <RefreshCw className="h-4 w-4" />
            <span>Refresh</span>
          </button>
          <button
            onClick={generateTestAlerts}
            disabled={generating}
            className="flex items-center space-x-2 px-4 py-2 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white rounded-lg transition-colors"
          >
            <Shield className={`h-4 w-4 ${generating ? 'animate-spin' : ''}`} />
            <span>Generate Test Alerts</span>
          </button>
        </div>
      </div>

      {alerts.length === 0 ? (
        <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-12 text-center">
          <AlertTriangle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-white mb-2">No Active Alerts</h3>
          <p className="text-gray-400 mb-4">System is monitoring all regions. Generate test alerts to see the interface in action.</p>
          <button
            onClick={generateTestAlerts}
            disabled={generating}
            className="px-6 py-2 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white rounded-lg transition-colors"
          >
            Generate Test Alerts
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-6 hover:bg-white/15 transition-all duration-300"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{getDisasterIcon(alert.disaster_type)}</span>
                  <div>
                    <h3 className="text-lg font-semibold text-white capitalize">
                      {alert.disaster_type} Alert - {alert.region}
                    </h3>
                    <div className="flex items-center space-x-2 mt-1">
                      <MapPin className="h-4 w-4 text-gray-400" />
                      <span className="text-sm text-gray-400">{alert.region}</span>
                      <Clock className="h-4 w-4 text-gray-400 ml-4" />
                      <span className="text-sm text-gray-400">
                        {format(new Date(alert.timestamp), 'MMM dd, yyyy HH:mm')}
                      </span>
                    </div>
                  </div>
                </div>
                <div className={`px-3 py-1 rounded-full border text-xs font-medium ${getAlertLevelColor(alert.alert_level)}`}>
                  {alert.alert_level.toUpperCase()}
                </div>
              </div>

              <p className="text-gray-300 mb-4">{alert.description}</p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div className="bg-white/5 rounded-lg p-3">
                  <div className="flex items-center space-x-2 mb-2">
                    <Users className="h-4 w-4 text-blue-400" />
                    <span className="text-sm font-medium text-white">Affected Area</span>
                  </div>
                  <p className="text-sm text-gray-300">{alert.affected_area.radius_km} km radius</p>
                  <p className="text-sm text-gray-300">{alert.affected_area.population.toLocaleString()} population</p>
                </div>

                <div className="bg-white/5 rounded-lg p-3">
                  <div className="flex items-center space-x-2 mb-2">
                    <Package className="h-4 w-4 text-green-400" />
                    <span className="text-sm font-medium text-white">Resources Needed</span>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm text-gray-300">Water: {alert.resources_needed.water}</p>
                    <p className="text-sm text-gray-300">Food: {alert.resources_needed.food}</p>
                    <p className="text-sm text-gray-300">Medical: {alert.resources_needed.medical}</p>
                  </div>
                </div>

                <div className="bg-white/5 rounded-lg p-3">
                  <div className="flex items-center space-x-2 mb-2">
                    <Shield className="h-4 w-4 text-purple-400" />
                    <span className="text-sm font-medium text-white">Blockchain</span>
                  </div>
                  <p className="text-xs text-purple-300 font-mono break-all">
                    {alert.blockchain_hash}
                  </p>
                  <div className="flex items-center space-x-1 mt-1">
                    <div className="h-2 w-2 bg-green-500 rounded-full"></div>
                    <span className="text-xs text-green-400">Verified</span>
                  </div>
                </div>
              </div>

              {alert.evacuation_routes.length > 0 && (
                <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-3">
                  <h4 className="text-sm font-medium text-blue-300 mb-2">Evacuation Routes</h4>
                  <div className="flex flex-wrap gap-2">
                    {alert.evacuation_routes.map((route, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-blue-500/20 text-blue-300 text-xs rounded-full"
                      >
                        {route.route_id}: {route.status}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AlertsPanel;