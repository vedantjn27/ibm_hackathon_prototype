import React, { useEffect, useState } from 'react';
import { Cloud, Thermometer, Droplets, Wind, Gauge, MapPin, RefreshCw } from 'lucide-react';
import { weatherService, threatService } from '../../services/api';
import type { WeatherData, ThreatAnalysis } from '../../types';

const WeatherMonitor: React.FC = () => {
  const [weatherData, setWeatherData] = useState<Record<string, WeatherData>>({});
  const [threatAnalyses, setThreatAnalyses] = useState<Record<string, ThreatAnalysis>>({});
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const regions = ['delhi', 'mumbai', 'bangalore', 'chennai', 'kolkata'];

  const fetchWeatherData = async () => {
    setRefreshing(true);
    try {
      const weatherPromises = regions.map(region => 
        weatherService.getWeather(region).then(data => ({ region, data }))
      );
      const threatPromises = regions.map(region => 
        threatService.analyzeThreat(region).then(data => ({ region, data }))
      );

      const weatherResults = await Promise.all(weatherPromises);
      const threatResults = await Promise.all(threatPromises);

      const newWeatherData: Record<string, WeatherData> = {};
      const newThreatData: Record<string, ThreatAnalysis> = {};

      weatherResults.forEach(({ region, data }) => {
        newWeatherData[region] = data;
      });

      threatResults.forEach(({ region, data }) => {
        newThreatData[region] = data;
      });

      setWeatherData(newWeatherData);
      setThreatAnalyses(newThreatData);
    } catch (error) {
      console.error('Failed to fetch weather data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchWeatherData();
    const interval = setInterval(fetchWeatherData, 60000); // Update every minute

    return () => clearInterval(interval);
  }, []);

  const getThreatLevelColor = (level: string) => {
    switch (level) {
      case 'critical': return 'bg-red-500/20 border-red-500 text-red-400';
      case 'high': return 'bg-orange-500/20 border-orange-500 text-orange-400';
      case 'medium': return 'bg-yellow-500/20 border-yellow-500 text-yellow-400';
      default: return 'bg-green-500/20 border-green-500 text-green-400';
    }
  };

  if (loading) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {regions.map((region) => (
          <div key={region} className="bg-white/10 backdrop-blur-sm rounded-xl p-6 animate-pulse">
            <div className="h-6 bg-white/20 rounded mb-4"></div>
            <div className="space-y-3">
              <div className="h-4 bg-white/20 rounded"></div>
              <div className="h-4 bg-white/20 rounded"></div>
              <div className="h-4 bg-white/20 rounded"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-white flex items-center">
          <Cloud className="h-6 w-6 text-blue-400 mr-2" />
          Weather Monitoring & Threat Analysis
        </h2>
        <button
          onClick={fetchWeatherData}
          disabled={refreshing}
          className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-lg transition-colors"
        >
          <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {regions.map((region) => {
          const weather = weatherData[region];
          const threat = threatAnalyses[region];

          if (!weather || !threat) return null;

          return (
            <div
              key={region}
              className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-6 hover:bg-white/15 transition-all duration-300"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <MapPin className="h-5 w-5 text-blue-400" />
                  <h3 className="text-lg font-semibold text-white capitalize">{region}</h3>
                </div>
                <div className={`px-3 py-1 rounded-full border text-xs font-medium ${getThreatLevelColor(threat.threat_level)}`}>
                  {threat.threat_level.toUpperCase()}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="flex items-center space-x-2">
                  <Thermometer className="h-4 w-4 text-red-400" />
                  <div>
                    <p className="text-xs text-gray-400">Temperature</p>
                    <p className="text-sm font-semibold text-white">{weather.temperature.toFixed(1)}°C</p>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <Droplets className="h-4 w-4 text-blue-400" />
                  <div>
                    <p className="text-xs text-gray-400">Humidity</p>
                    <p className="text-sm font-semibold text-white">{weather.humidity.toFixed(0)}%</p>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <Wind className="h-4 w-4 text-gray-400" />
                  <div>
                    <p className="text-xs text-gray-400">Wind Speed</p>
                    <p className="text-sm font-semibold text-white">{weather.wind_speed.toFixed(1)} km/h</p>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <Gauge className="h-4 w-4 text-green-400" />
                  <div>
                    <p className="text-xs text-gray-400">Pressure</p>
                    <p className="text-sm font-semibold text-white">{weather.pressure.toFixed(0)} hPa</p>
                  </div>
                </div>
              </div>

              {threat.predicted_disasters.length > 0 && (
                <div className="mb-4">
                  <p className="text-xs text-gray-400 mb-2">Predicted Disasters:</p>
                  <div className="flex flex-wrap gap-1">
                    {threat.predicted_disasters.map((disaster, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-red-500/20 text-red-400 text-xs rounded-full"
                      >
                        {disaster}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {threat.recommendations.length > 0 && (
                <div>
                  <p className="text-xs text-gray-400 mb-2">AI Recommendations:</p>
                  <ul className="space-y-1">
                    {threat.recommendations.slice(0, 2).map((recommendation, index) => (
                      <li key={index} className="text-xs text-blue-300 flex items-start">
                        <span className="text-blue-500 mr-1">•</span>
                        {recommendation}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {threat.alert_generated && (
                <div className="mt-4 p-3 bg-red-500/20 border border-red-500/50 rounded-lg">
                  <p className="text-xs text-red-300 font-medium">🚨 Alert Generated</p>
                  <p className="text-xs text-red-400">ID: {threat.alert_id}</p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default WeatherMonitor;