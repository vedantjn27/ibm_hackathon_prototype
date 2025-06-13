import React, { useState } from 'react';
import Header from './components/Layout/Header';
import SystemOverview from './components/Dashboard/SystemOverview';
import WeatherMonitor from './components/Weather/WeatherMonitor';
import AlertsPanel from './components/Alerts/AlertsPanel';
import CitizenReports from './components/Reports/CitizenReports';

function App() {
  const [activeSection, setActiveSection] = useState('dashboard');

  const renderSection = () => {
    switch (activeSection) {
      case 'dashboard':
        return <SystemOverview />;
      case 'weather':
        return <WeatherMonitor />;
      case 'alerts':
        return <AlertsPanel />;
      case 'reports':
        return <CitizenReports />;
      default:
        return <SystemOverview />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900">
      <Header 
        activeSection={activeSection} 
        onSectionChange={setActiveSection} 
      />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderSection()}
      </main>

      {/* Background Effects */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-0 w-1/3 h-1/3 bg-blue-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-0 w-1/3 h-1/3 bg-purple-500/10 rounded-full blur-3xl"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-1/4 h-1/4 bg-green-500/5 rounded-full blur-3xl"></div>
      </div>
    </div>
  );
}

export default App;