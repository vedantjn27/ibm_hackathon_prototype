import React, { useEffect, useState } from 'react';
import { Activity, Users, AlertTriangle, Database, Cpu, Zap } from 'lucide-react';
import { dashboardService } from '../../services/api';
import type { DashboardData } from '../../types';

const SystemOverview: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const data = await dashboardService.getDashboardData();
        setDashboardData(data);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="bg-white/10 backdrop-blur-sm rounded-xl p-6 animate-pulse">
            <div className="h-4 bg-white/20 rounded mb-4"></div>
            <div className="h-8 bg-white/20 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'online':
      case 'verified':
      case 'ready':
      case 'active':
        return 'text-green-400';
      case 'error':
        return 'text-red-400';
      default:
        return 'text-yellow-400';
    }
  };

  const stats = [
    { 
      title: 'Active Alerts', 
      value: dashboardData?.total_alerts || 0, 
      icon: AlertTriangle, 
      color: 'text-red-400',
      bgColor: 'bg-red-500/10',
      change: '+12%'
    },
    { 
      title: 'Active Regions', 
      value: dashboardData?.active_regions || 0, 
      icon: Activity, 
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/10',
      change: 'Stable'
    },
    { 
      title: 'Citizen Reports', 
      value: dashboardData?.citizen_reports || 0, 
      icon: Users, 
      color: 'text-green-400',
      bgColor: 'bg-green-500/10',
      change: '+8%'
    },
    { 
      title: 'Blockchain Blocks', 
      value: dashboardData?.blockchain_blocks || 0, 
      icon: Database, 
      color: 'text-purple-400',
      bgColor: 'bg-purple-500/10',
      change: '+3%'
    },
    { 
      title: 'Quantum Optimizations', 
      value: dashboardData?.recent_optimizations || 0, 
      icon: Zap, 
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
      change: '+15%'
    },
    { 
      title: 'System Health', 
      value: '98.5%', 
      icon: Cpu, 
      color: 'text-emerald-400',
      bgColor: 'bg-emerald-500/10',
      change: 'Optimal'
    },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div
              key={index}
              className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-6 hover:bg-white/15 transition-all duration-300"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <span className="text-sm text-green-400 font-medium">{stat.change}</span>
              </div>
              <h3 className="text-lg font-semibold text-white mb-1">{stat.title}</h3>
              <p className={`text-3xl font-bold ${stat.color}`}>{stat.value}</p>
            </div>
          );
        })}
      </div>

      {/* System Health Details */}
      <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
          <Cpu className="h-5 w-5 text-blue-400 mr-2" />
          System Health Status
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {dashboardData?.system_health && Object.entries(dashboardData.system_health).map(([service, status]) => (
            <div key={service} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
              <span className="capitalize text-white text-sm">{service.replace('_', ' ')}</span>
              <span className={`text-sm font-medium ${getStatusColor(status)}`}>
                {status}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Real-time Activity Feed */}
      <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
          <Activity className="h-5 w-5 text-green-400 mr-2" />
          Real-time Activity
        </h3>
        <div className="space-y-3">
          <div className="flex items-center space-x-3 p-3 bg-green-500/10 rounded-lg">
            <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-green-300 text-sm">AI Agent Delhi: Threat analysis completed</span>
            <span className="text-gray-400 text-xs ml-auto">2 min ago</span>
          </div>
          <div className="flex items-center space-x-3 p-3 bg-blue-500/10 rounded-lg">
            <div className="h-2 w-2 bg-blue-500 rounded-full animate-pulse"></div>
            <span className="text-blue-300 text-sm">Quantum optimization: Resource allocation updated</span>
            <span className="text-gray-400 text-xs ml-auto">5 min ago</span>
          </div>
          <div className="flex items-center space-x-3 p-3 bg-purple-500/10 rounded-lg">
            <div className="h-2 w-2 bg-purple-500 rounded-full animate-pulse"></div>
            <span className="text-purple-300 text-sm">Blockchain: New alert block verified</span>
            <span className="text-gray-400 text-xs ml-auto">8 min ago</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SystemOverview;