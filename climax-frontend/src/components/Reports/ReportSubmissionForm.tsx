import React, { useState } from 'react';
import { X, MapPin, Upload, Send } from 'lucide-react';
import { citizenService } from '../../services/api';

interface ReportSubmissionFormProps {
  onClose: () => void;
  onSubmitted: () => void;
}

const ReportSubmissionForm: React.FC<ReportSubmissionFormProps> = ({ onClose, onSubmitted }) => {
  const [formData, setFormData] = useState({
    disaster_type: 'flood' as const,
    severity: 5,
    description: '',
    location: {
      lat: 28.6139,
      lon: 77.2090
    },
    verified: false // 🔧 Add this line
  });
  const [submitting, setSubmitting] = useState(false);

  const disasterTypes = [
    { value: 'flood', label: 'Flood', icon: '🌊' },
    { value: 'heatwave', label: 'Heatwave', icon: '🔥' },
    { value: 'cyclone', label: 'Cyclone', icon: '🌪️' },
    { value: 'drought', label: 'Drought', icon: '🏜️' },
    { value: 'earthquake', label: 'Earthquake', icon: '🏔️' }
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      await citizenService.submitReport(formData);
      onSubmitted();
    } catch (error) {
      console.error('Failed to submit report:', error);
    } finally {
      setSubmitting(false);
    }
  };

  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setFormData(prev => ({
            ...prev,
            location: {
              lat: position.coords.latitude,
              lon: position.coords.longitude
            }
          }));
        },
        (error) => {
          console.error('Error getting location:', error);
        }
      );
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div className="bg-slate-900 border border-white/20 rounded-xl p-6 w-full max-w-md">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-white">Submit Disaster Report</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Disaster Type
            </label>
            <div className="grid grid-cols-2 gap-2">
              {disasterTypes.map((type) => (
                <button
                  key={type.value}
                  type="button"
                  onClick={() => setFormData(prev => ({ ...prev, disaster_type: type.value as any }))}
                  className={`flex items-center space-x-2 p-3 rounded-lg border transition-colors ${
                    formData.disaster_type === type.value
                      ? 'bg-blue-600 border-blue-500 text-white'
                      : 'bg-white/5 border-white/20 text-gray-300 hover:bg-white/10'
                  }`}
                >
                  <span>{type.icon}</span>
                  <span className="text-sm">{type.label}</span>
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Severity (1-10)
            </label>
            <input
              type="range"
              min="1"
              max="10"
              value={formData.severity}
              onChange={(e) => setFormData(prev => ({ ...prev, severity: parseInt(e.target.value) }))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
            <div className="flex justify-between text-xs text-gray-400 mt-1">
              <span>Low</span>
              <span className="text-white font-medium">{formData.severity}</span>
              <span>Critical</span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
              placeholder="Describe what you're witnessing..."
              className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Location
            </label>
            <div className="flex space-x-2">
              <input
                type="number"
                value={formData.location.lat}
                onChange={(e) => setFormData(prev => ({ 
                  ...prev, 
                  location: { ...prev.location, lat: parseFloat(e.target.value) }
                }))}
                placeholder="Latitude"
                className="flex-1 px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                step="any"
                required
              />
              <input
                type="number"
                value={formData.location.lon}
                onChange={(e) => setFormData(prev => ({ 
                  ...prev, 
                  location: { ...prev.location, lon: parseFloat(e.target.value) }
                }))}
                placeholder="Longitude"
                className="flex-1 px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                step="any"
                required
              />
              <button
                type="button"
                onClick={getCurrentLocation}
                className="px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
              >
                <MapPin className="h-4 w-4" />
              </button>
            </div>
          </div>

          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="flex-1 flex items-center justify-center space-x-2 px-4 py-2 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white rounded-lg transition-colors"
            >
              <Send className="h-4 w-4" />
              <span>{submitting ? 'Submitting...' : 'Submit Report'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ReportSubmissionForm;