import React, { useEffect, useState } from 'react';
import { Users, MapPin, Clock, CheckCircle, AlertCircle, Camera, Star } from 'lucide-react';
import { citizenService } from '../../services/api';
import type { CitizenReport } from '../../types';
import { format } from 'date-fns';
import ReportSubmissionForm from './ReportSubmissionForm';

const CitizenReports: React.FC = () => {
  const [reports, setReports] = useState<CitizenReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  const fetchReports = async () => {
    try {
      const data = await citizenService.getReports(20);
      setReports(data);
    } catch (error) {
      console.error('Failed to fetch citizen reports:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
    const interval = setInterval(fetchReports, 30000);

    return () => clearInterval(interval);
  }, []);

  const getSeverityColor = (severity: number) => {
    if (severity >= 8) return 'text-red-400 bg-red-500/20';
    if (severity >= 6) return 'text-orange-400 bg-orange-500/20';
    if (severity >= 4) return 'text-yellow-400 bg-yellow-500/20';
    return 'text-green-400 bg-green-500/20';
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

  const handleReportSubmitted = () => {
    setShowForm(false);
    fetchReports();
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
          <Users className="h-6 w-6 text-green-400 mr-2" />
          Citizen Reports & Community Intelligence
        </h2>
        <button
          onClick={() => setShowForm(true)}
          className="flex items-center space-x-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
        >
          <Users className="h-4 w-4" />
          <span>Submit Report</span>
        </button>
      </div>

      {showForm && (
        <ReportSubmissionForm 
          onClose={() => setShowForm(false)}
          onSubmitted={handleReportSubmitted}
        />
      )}

      {reports.length === 0 ? (
        <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-12 text-center">
          <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-white mb-2">No Citizen Reports</h3>
          <p className="text-gray-400 mb-4">Be the first to report a climate-related incident in your area.</p>
          <button
            onClick={() => setShowForm(true)}
            className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
          >
            Submit First Report
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {reports.map((report) => (
            <div
              key={report.id}
              className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-6 hover:bg-white/15 transition-all duration-300"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{getDisasterIcon(report.disaster_type)}</span>
                  <div>
                    <h3 className="text-lg font-semibold text-white capitalize flex items-center">
                      {report.disaster_type} Report
                      {report.verified && (
                        <CheckCircle className="h-4 w-4 text-green-400 ml-2" />
                      )}
                    </h3>
                    <div className="flex items-center space-x-2 mt-1">
                      <MapPin className="h-4 w-4 text-gray-400" />
                      <span className="text-sm text-gray-400">
                        {report.location.lat.toFixed(4)}, {report.location.lon.toFixed(4)}
                      </span>
                      <Clock className="h-4 w-4 text-gray-400 ml-4" />
                      <span className="text-sm text-gray-400">
                        {format(new Date(report.timestamp), 'MMM dd, yyyy HH:mm')}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <div className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(report.severity)}`}>
                    Severity: {report.severity}/10
                  </div>
                  {report.verified ? (
                    <div className="flex items-center space-x-1 text-green-400">
                      <CheckCircle className="h-4 w-4" />
                      <span className="text-xs">Verified</span>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-1 text-yellow-400">
                      <AlertCircle className="h-4 w-4" />
                      <span className="text-xs">Pending</span>
                    </div>
                  )}
                </div>
              </div>

              <p className="text-gray-300 mb-4">{report.description}</p>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  {report.image_url && (
                    <div className="flex items-center space-x-1 text-blue-400">
                      <Camera className="h-4 w-4" />
                      <span className="text-xs">Photo attached</span>
                    </div>
                  )}
                  <div className="flex items-center space-x-1">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`h-3 w-3 ${
                          i < Math.floor(report.severity / 2) ? 'text-yellow-400 fill-current' : 'text-gray-500'
                        }`}
                      />
                    ))}
                  </div>
                </div>
                
                <div className="text-xs text-gray-400 font-mono">
                  ID: {report.id.slice(0, 8)}...
                </div>
              </div>

              {report.verified && (
                <div className="mt-4 p-3 bg-green-500/10 border border-green-500/30 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-400" />
                    <span className="text-sm text-green-300 font-medium">AI Verification Complete</span>
                  </div>
                  <p className="text-xs text-green-400 mt-1">
                    Report has been verified and integrated into threat analysis system.
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CitizenReports;