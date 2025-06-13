export interface WeatherData {
  temperature: number;
  humidity: number;
  pressure: number;
  wind_speed: number;
  precipitation: number;
  location: string;
  timestamp: string;
}

export interface DisasterAlert {
  id: string;
  region: string;
  disaster_type: 'flood' | 'heatwave' | 'cyclone' | 'drought' | 'earthquake';
  alert_level: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  affected_area: {
    radius_km: number;
    population: number;
  };
  evacuation_routes: Array<{
    route_id: string;
    status: string;
  }>;
  resources_needed: {
    water: number;
    food: number;
    medical: number;
  };
  timestamp: string;
  blockchain_hash: string;
}

export interface CitizenReport {
  id: string;
  location: {
    lat: number;
    lon: number;
  };
  disaster_type: 'flood' | 'heatwave' | 'cyclone' | 'drought' | 'earthquake';
  severity: number;
  description: string;
  image_url?: string;
  timestamp: string;
  verified: boolean;
}

export interface ThreatAnalysis {
  region: string;
  current_conditions: {
    temperature: number;
    humidity: number;
    precipitation: number;
    wind_speed: number;
  };
  threat_level: 'low' | 'medium' | 'high' | 'critical';
  predicted_disasters: string[];
  recommendations: string[];
  alert_generated?: boolean;
  alert_id?: string;
  blockchain_hash?: string;
}

export interface ResourceOptimization {
  status: string;
  total_supply: number;
  total_demand: number;
  allocation: Record<string, Record<string, number>>;
  efficiency_score: number;
  quantum_runtime: number;
}

export interface DashboardData {
  total_alerts: number;
  active_regions: number;
  citizen_reports: number;
  blockchain_blocks: number;
  recent_optimizations: number;
  system_health: {
    weather_service: string;
    blockchain: string;
    quantum_optimizer: string;
    ai_agents: string;
  };
}

export interface KnowledgeResult {
  id: string;
  content: string;
  disaster_type: string;
  region: string;
}