import axios from 'axios';
import type { 
  WeatherData, 
  DisasterAlert, 
  CitizenReport, 
  ThreatAnalysis, 
  ResourceOptimization,
  DashboardData,
  KnowledgeResult 
} from '../types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const weatherService = {
  getWeather: async (city: string): Promise<WeatherData> => {
    const response = await api.get(`/weather/${city}`);
    return response.data;
  }
};

export const threatService = {
  analyzeThreat: async (region: string): Promise<ThreatAnalysis> => {
    const response = await api.post(`/analyze-threat/${region}`);
    return response.data;
  }
};

export const alertService = {
  getAlerts: async (limit: number = 10): Promise<DisasterAlert[]> => {
    const response = await api.get(`/alerts?limit=${limit}`);
    return response.data;
  },
  
  getRegionalAlerts: async (region: string, limit: number = 10): Promise<DisasterAlert[]> => {
    const response = await api.get(`/alerts/${region}?limit=${limit}`);
    return response.data;
  },

  generateTestAlerts: async () => {
    const response = await api.post('/test/generate-alerts');
    return response.data;
  }
};

export const citizenService = {
  submitReport: async (report: Omit<CitizenReport, 'id' | 'timestamp'>): Promise<any> => {
    const response = await api.post('/citizen-report', report);
    return response.data;
  },
  
  getReports: async (limit: number = 10): Promise<CitizenReport[]> => {
    const response = await api.get(`/citizen-reports?limit=${limit}`);
    return response.data;
  }
};

export const resourceService = {
  optimizeResources: async (
    regions: string[], 
    resources: Record<string, number>, 
    demands: Record<string, Record<string, number>>
  ): Promise<ResourceOptimization> => {
    const response = await api.post('/optimize-resources', { regions, resources, demands });
    return response.data;
  }
};

export const blockchainService = {
  verifyChain: async () => {
    const response = await api.get('/blockchain/verify');
    return response.data;
  },
  
  getChain: async () => {
    const response = await api.get('/blockchain/chain');
    return response.data;
  }
};

export const knowledgeService = {
  queryKnowledge: async (query: string, disaster_type?: string): Promise<{ query: string; results: KnowledgeResult[] }> => {
    const params: any = { query };
    if (disaster_type) params.disaster_type = disaster_type;
    
    const response = await api.get('/knowledge/query', { params });
    return response.data;
  }
};

export const dashboardService = {
  getDashboardData: async (): Promise<DashboardData> => {
    const response = await api.get('/simulation/dashboard');
    return response.data;
  }
};