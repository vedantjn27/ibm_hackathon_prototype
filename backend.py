"""
ClimaX: AI + Quantum + Blockchain-Powered Climate Resilience OS
Backend Implementation with RAG, Agentic AI, Quantum Simulation, and Blockchain
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import requests
import asyncio
import json
import hashlib
import time
from datetime import datetime
import numpy as np
from dataclasses import dataclass
import logging
from enum import Enum
import uuid
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ClimaX Backend", description="Climate Resilience OS Backend")

# ==================== MODELS ====================

class DisasterType(str, Enum):
    FLOOD = "flood"
    HEATWAVE = "heatwave"
    CYCLONE = "cyclone"
    DROUGHT = "drought"
    EARTHQUAKE = "earthquake"

class AlertLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class WeatherData:
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    precipitation: float
    location: str
    timestamp: datetime

class CitizenReport(BaseModel):
    id: str
    location: Dict[str, float]  # {"lat": float, "lon": float}
    disaster_type: DisasterType
    severity: int  # 1-10 scale
    description: str
    image_url: Optional[str] = None
    timestamp: datetime
    verified: bool = False

class DisasterAlert(BaseModel):
    id: str
    region: str
    disaster_type: DisasterType
    alert_level: AlertLevel
    description: str
    affected_area: Dict[str, Any]
    evacuation_routes: List[Dict[str, Any]]
    resources_needed: Dict[str, int]
    timestamp: datetime
    blockchain_hash: str

class ResourceOptimization(BaseModel):
    region: str
    resources: Dict[str, int]
    demand: Dict[str, int]
    optimization_result: Dict[str, Any]
    quantum_runtime: float

# ==================== QUANTUM SIMULATION MODULE ====================

class QuantumResourceOptimizer:
    """Simulates Quantum Approximate Optimization Algorithm (QAOA) for resource allocation"""

    def __init__(self):
        self.name = "Quantum Resource Optimizer"
        logger.info("Initialized Quantum Resource Optimizer (Simulated)")

    async def optimize_resources(self, regions: List[str], resources: Dict[str, int],
                                demands: Dict[str, Dict[str, int]]) -> Dict[str, Any]:
        """
        Simulates quantum optimization for multi-region resource allocation
        In real implementation, this would use Qiskit with QAOA
        """
        start_time = time.time()

        # Simulate quantum computation delay
        await asyncio.sleep(0.1)

        # Simulate optimization results
        total_demand = sum(sum(region_demand.values()) for region_demand in demands.values())
        total_supply = sum(resources.values())

        optimization_result = {
            "status": "optimal" if total_supply >= total_demand else "suboptimal",
            "total_supply": total_supply,
            "total_demand": total_demand,
            "allocation": {},
            "efficiency_score": min(total_supply / total_demand, 1.0) * 100
        }

        # Distribute resources proportionally
        for region in regions:
            region_demand = demands.get(region, {})
            region_total = sum(region_demand.values())
            allocation_ratio = min(total_supply / total_demand, 1.0) if total_demand > 0 else 1.0

            optimization_result["allocation"][region] = {
                resource: int(demand * allocation_ratio)
                for resource, demand in region_demand.items()
            }

        runtime = time.time() - start_time
        optimization_result["quantum_runtime"] = runtime

        logger.info(f"Quantum optimization completed in {runtime:.3f}s")
        return optimization_result

# ==================== BLOCKCHAIN SIMULATION MODULE ====================

class BlockchainLedger:
    """Simulates blockchain-based disaster alert ledger"""

    def __init__(self):
        self.chain = []
        self.pending_alerts = []
        self.create_genesis_block()
        logger.info("Initialized Blockchain Ledger (Simulated)")

    def create_genesis_block(self):
        genesis_block = {
            "index": 0,
            "timestamp": datetime.now().isoformat(),
            "data": "Genesis Block",
            "previous_hash": "0",
            "hash": self.calculate_hash("0", "Genesis Block", datetime.now().isoformat())
        }
        self.chain.append(genesis_block)

    def calculate_hash(self, previous_hash: str, data: str, timestamp: str) -> str:
        """Calculate SHA-256 hash for blockchain"""
        block_string = f"{previous_hash}{data}{timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def add_alert_to_chain(self, alert: DisasterAlert) -> str:
        """Add disaster alert to blockchain"""
        previous_block = self.chain[-1]
        new_block = {
            "index": len(self.chain),
            "timestamp": datetime.now().isoformat(),
            "data": alert.dict(),
            "previous_hash": previous_block["hash"],
            "hash": ""
        }

        new_block["hash"] = self.calculate_hash(
            new_block["previous_hash"],
            json.dumps(new_block["data"]),
            new_block["timestamp"]
        )

        self.chain.append(new_block)
        logger.info(f"Alert {alert.id} added to blockchain with hash {new_block['hash']}")
        return new_block["hash"]

    def verify_chain(self) -> bool:
        """Verify blockchain integrity"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block["previous_hash"] != previous_block["hash"]:
                return False

            if current_block["hash"] != self.calculate_hash(
                current_block["previous_hash"],
                json.dumps(current_block["data"]),
                current_block["timestamp"]
            ):
                return False

        return True

# ==================== RAG SYSTEM MODULE ====================

class ClimateKnowledgeBase:
    """RAG-based climate knowledge system"""

    def __init__(self):
        self.documents = []
        self.embeddings = {}
        self.load_climate_knowledge()
        logger.info("Initialized Climate Knowledge Base with RAG")

    def load_climate_knowledge(self):
        """Load climate disaster knowledge base"""
        knowledge_base = [
            {
                "id": "flood_001",
                "content": "Floods are caused by heavy rainfall, dam failures, or coastal storm surges. Early warning signs include rapid water level rise, heavy continuous rainfall for 24+ hours, and upstream dam alerts.",
                "disaster_type": "flood",
                "region": "general"
            },
            {
                "id": "heatwave_001",
                "content": "Heatwaves are prolonged periods of excessively hot weather. In India, temperatures above 40°C for 3+ days constitute a heatwave. Vulnerable populations include elderly, children, and outdoor workers.",
                "disaster_type": "heatwave",
                "region": "india"
            },
            {
                "id": "cyclone_001",
                "content": "Cyclones in the Bay of Bengal typically occur between April-June and October-December. Warning signs include sudden drop in barometric pressure, increasing wind speeds, and heavy cloud formation.",
                "disaster_type": "cyclone",
                "region": "coastal_india"
            },
            {
                "id": "drought_001",
                "content": "Droughts occur when rainfall is significantly below normal for extended periods. Agricultural drought affects crop production, while meteorological drought refers to precipitation deficits.",
                "disaster_type": "drought",
                "region": "general"
            }
        ]

        self.documents = knowledge_base
        # In real implementation, you'd use sentence transformers for embeddings
        for doc in knowledge_base:
            # Simulate embedding with simple hash for demo
            self.embeddings[doc["id"]] = hash(doc["content"]) % 1000

    def query_knowledge(self, query: str, disaster_type: str = None) -> List[Dict]:
        """Query knowledge base using RAG"""
        # Simple similarity search simulation
        # In real implementation, use FAISS or similar vector DB
        relevant_docs = []

        for doc in self.documents:
            if disaster_type and doc["disaster_type"] != disaster_type:
                continue

            # Simple keyword matching for demo
            if any(word.lower() in doc["content"].lower() for word in query.split()):
                relevant_docs.append(doc)

        return relevant_docs[:3]  # Return top 3 relevant documents

# ==================== AGENTIC AI MODULE ====================

class RegionalAIAgent:
    """Agentic AI for regional climate intelligence"""

    def __init__(self, region: str):
        self.region = region
        self.knowledge_base = ClimateKnowledgeBase()
        self.alert_history = []
        logger.info(f"Initialized Regional AI Agent for {region}")

    def analyze_threat(self, weather_data: WeatherData) -> Dict[str, Any]:
        """Analyze climate threat using AI agent"""

        # Simulate AI analysis
        threat_analysis = {
            "region": self.region,
            "current_conditions": {
                "temperature": weather_data.temperature,
                "humidity": weather_data.humidity,
                "precipitation": weather_data.precipitation,
                "wind_speed": weather_data.wind_speed
            },
            "threat_level": "low",
            "predicted_disasters": [],
            "recommendations": []
        }

        # Simple rule-based threat detection (simulate AI)
        if weather_data.temperature > 40:
            threat_analysis["threat_level"] = "high"
            threat_analysis["predicted_disasters"].append("heatwave")
            threat_analysis["recommendations"].append("Stay indoors during peak hours")

        if weather_data.precipitation > 50:
            threat_analysis["threat_level"] = "medium"
            threat_analysis["predicted_disasters"].append("flood")
            threat_analysis["recommendations"].append("Avoid low-lying areas")

        if weather_data.wind_speed > 60:
            threat_analysis["threat_level"] = "critical"
            threat_analysis["predicted_disasters"].append("cyclone")
            threat_analysis["recommendations"].append("Evacuate to higher ground")

        return threat_analysis

    def generate_alert(self, threat_analysis: Dict[str, Any]) -> Optional[DisasterAlert]:
        """Generate disaster alert based on threat analysis"""

        if threat_analysis["threat_level"] in ["medium", "high", "critical"]:
            alert = DisasterAlert(
                id=str(uuid.uuid4()),
                region=self.region,
                disaster_type=threat_analysis["predicted_disasters"][0] if threat_analysis["predicted_disasters"] else "flood",
                alert_level=AlertLevel(threat_analysis["threat_level"]),
                description=f"AI-detected threat in {self.region}: {', '.join(threat_analysis['predicted_disasters'])}",
                affected_area={"radius_km": 50, "population": 100000},
                evacuation_routes=[{"route_id": "R1", "status": "open"}],
                resources_needed={"water": 1000, "food": 500, "medical": 100},
                timestamp=datetime.now(),
                blockchain_hash=""
            )

            self.alert_history.append(alert)
            return alert

        return None

# ==================== WEATHER DATA SERVICE ====================

class WeatherService:
    """Weather data service using OpenWeatherMap API"""

    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY", "demo_key")
        self.base_url = "http://api.openweathermap.org/data/2.5"

    async def get_weather_data(self, city: str) -> WeatherData:
        """Fetch weather data from OpenWeatherMap"""

        if self.api_key == "demo_key":
            # Return mock data for demo
            return WeatherData(
                temperature=np.random.uniform(25, 45),
                humidity=np.random.uniform(40, 90),
                pressure=np.random.uniform(990, 1020),
                wind_speed=np.random.uniform(5, 25),
                precipitation=np.random.uniform(0, 20),
                location=city,
                timestamp=datetime.now()
            )

        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            return WeatherData(
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                pressure=data["main"]["pressure"],
                wind_speed=data["wind"]["speed"],
                precipitation=data.get("rain", {}).get("1h", 0),
                location=city,
                timestamp=datetime.now()
            )

        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            raise HTTPException(status_code=500, detail="Weather service unavailable")

# ==================== GLOBAL INSTANCES ====================

weather_service = WeatherService()
blockchain = BlockchainLedger()
quantum_optimizer = QuantumResourceOptimizer()

# Regional AI Agents
regional_agents = {
    "delhi": RegionalAIAgent("Delhi"),
    "bangalore": RegionalAIAgent("Bangalore"),
    "mumbai": RegionalAIAgent("Mumbai"),
    "chennai": RegionalAIAgent("Chennai"),
    "kolkata": RegionalAIAgent("Kolkata")
}

# In-memory storage (use database in production)
citizen_reports = []
disaster_alerts = []
resource_optimizations = []

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ClimaX Backend - Climate Resilience OS",
        "version": "1.0.0",
        "modules": ["AI Agents", "Quantum Optimizer", "Blockchain", "RAG", "Weather Service"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "blockchain_integrity": blockchain.verify_chain(),
        "active_agents": len(regional_agents)
    }

@app.get("/weather/{city}")
async def get_weather(city: str):
    """Get weather data for a city"""
    weather_data = await weather_service.get_weather_data(city)
    return weather_data.__dict__

@app.post("/analyze-threat/{region}")
async def analyze_threat(region: str):
    """Analyze climate threat for a region"""
    if region.lower() not in regional_agents:
        raise HTTPException(status_code=404, detail="Regional agent not found")

    agent = regional_agents[region.lower()]
    weather_data = await weather_service.get_weather_data(region)

    threat_analysis = agent.analyze_threat(weather_data)

    # Generate alert if threat level is significant
    alert = agent.generate_alert(threat_analysis)
    if alert:
        # Add to blockchain
        blockchain_hash = blockchain.add_alert_to_chain(alert)
        alert.blockchain_hash = blockchain_hash
        disaster_alerts.append(alert)

        threat_analysis["alert_generated"] = True
        threat_analysis["alert_id"] = alert.id
        threat_analysis["blockchain_hash"] = blockchain_hash

    return threat_analysis

@app.post("/citizen-report")
async def submit_citizen_report(report: CitizenReport):
    """Submit citizen disaster report"""
    report.id = str(uuid.uuid4())
    report.timestamp = datetime.now()

    # Simple verification simulation (in real app, use AI for verification)
    if len(report.description) > 10:
        report.verified = True

    citizen_reports.append(report)
    logger.info(f"Citizen report submitted: {report.id}")

    return {"status": "success", "report_id": report.id, "verified": report.verified}

@app.get("/citizen-reports")
async def get_citizen_reports(limit: int = 10):
    """Get recent citizen reports"""
    return citizen_reports[-limit:]

@app.post("/optimize-resources")
async def optimize_resources(regions: List[str], resources: Dict[str, int],
                           demands: Dict[str, Dict[str, int]]):
    """Optimize resource allocation using quantum computing"""

    optimization_result = await quantum_optimizer.optimize_resources(regions, resources, demands)

    # Store optimization result
    resource_opt = ResourceOptimization(
        region=",".join(regions),
        resources=resources,
        demand=demands,
        optimization_result=optimization_result,
        quantum_runtime=optimization_result["quantum_runtime"]
    )

    resource_optimizations.append(resource_opt)

    return optimization_result

@app.get("/alerts")
async def get_alerts(limit: int = 10):
    """Get recent disaster alerts"""
    return disaster_alerts[-limit:]

@app.get("/alerts/{region}")
async def get_regional_alerts(region: str, limit: int = 10):
    """Get alerts for specific region"""
    regional_alerts = [alert for alert in disaster_alerts if alert.region.lower() == region.lower()]
    return regional_alerts[-limit:]

@app.get("/blockchain/verify")
async def verify_blockchain():
    """Verify blockchain integrity"""
    is_valid = blockchain.verify_chain()
    return {
        "valid": is_valid,
        "blocks": len(blockchain.chain),
        "last_block_hash": blockchain.chain[-1]["hash"] if blockchain.chain else None
    }

@app.get("/blockchain/chain")
async def get_blockchain():
    """Get full blockchain"""
    return blockchain.chain

@app.get("/knowledge/query")
async def query_knowledge(query: str, disaster_type: Optional[str] = None):
    """Query climate knowledge base using RAG"""
    kb = ClimateKnowledgeBase()
    results = kb.query_knowledge(query, disaster_type)
    return {"query": query, "results": results}

@app.get("/simulation/dashboard")
async def get_dashboard_data():
    """Get dashboard data for simulation"""
    return {
        "total_alerts": len(disaster_alerts),
        "active_regions": len(regional_agents),
        "citizen_reports": len(citizen_reports),
        "blockchain_blocks": len(blockchain.chain),
        "recent_optimizations": len(resource_optimizations),
        "system_health": {
            "weather_service": "online",
            "blockchain": "verified" if blockchain.verify_chain() else "error",
            "quantum_optimizer": "ready",
            "ai_agents": "active"
        }
    }

@app.post("/test/generate-alerts")
async def generate_test_alerts():
    """Generate test alerts for demonstration"""
    test_regions = ["delhi", "mumbai", "bangalore"]
    generated_alerts = []

    for region in test_regions:
        weather_data = await weather_service.get_weather_data(region)
        agent = regional_agents[region]

        # Force high threat for demo
        weather_data.temperature = 42
        weather_data.precipitation = 60

        threat_analysis = agent.analyze_threat(weather_data)
        alert = agent.generate_alert(threat_analysis)

        if alert:
            blockchain_hash = blockchain.add_alert_to_chain(alert)
            alert.blockchain_hash = blockchain_hash
            disaster_alerts.append(alert)
            generated_alerts.append(alert)

    return {"generated_alerts": len(generated_alerts), "alerts": generated_alerts}

# ==================== STARTUP EVENT ====================

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    logger.info("🚀 ClimaX Backend Starting Up...")
    logger.info("🤖 AI Agents: Initialized")
    logger.info("⚛️ Quantum Optimizer: Ready")
    logger.info("🔗 Blockchain: Genesis block created")
    logger.info("🧠 RAG System: Knowledge base loaded")
    logger.info("🌤️ Weather Service: Connected")
    logger.info("✅ ClimaX Backend Ready!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
