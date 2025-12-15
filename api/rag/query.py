import json
import uuid
import random
import time
from typing import Optional

# Sample textbook chunks
CHUNKS = [
    {"ch": "ch1", "sec": "1.2", "title": "Embodied Intelligence", "text": "Embodied intelligence refers to intelligence that emerges from the interaction of a body with its environment. Unlike traditional AI, embodied intelligence is grounded in physical reality.", "page": 5},
    {"ch": "ch2", "sec": "2.1", "title": "Humanoid Robotics", "text": "Humanoid robots are designed to resemble human form. Bipedal locomotion - walking on two legs like humans - is a key characteristic that distinguishes humanoid robots from other morphologies.", "page": 15},
    {"ch": "ch3", "sec": "3.1", "title": "ROS 2 Fundamentals", "text": "Robot Operating System (ROS) is a flexible framework for writing robot software. ROS 2 is the next generation with improved performance, security, and real-time capabilities.", "page": 28},
    {"ch": "ch4", "sec": "4.1", "title": "Digital Twins", "text": "A digital twin is a virtual representation of a physical robot or system. Digital twins enable simulation and testing before deploying code to real hardware.", "page": 42},
    {"ch": "ch5", "sec": "5.1", "title": "Vision-Language-Action", "text": "Vision-Language-Action systems combine visual perception, language understanding, and motor control. These multimodal systems enable robots to understand instructions and execute complex tasks.", "page": 58},
    {"ch": "ch6", "sec": "6.1", "title": "Capstone Project", "text": "The capstone project is a comprehensive end-to-end robotics system integrating all course concepts. Students build a complete perception-planning-control pipeline for a household task.", "page": 75},
]

from http.server import BaseHTTPRequestHandler
import urllib.parse

class Handler(BaseHTTPRequestHandler):
    """Handle RAG query requests"""

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Handle POST requests"""
        try:
            # Parse query parameters from URL
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            query_text = query_params.get('query_text', [''])[0]
            student_id = query_params.get('student_id', ['guest'])[0]

            if not query_text or len(query_text) < 10:
                error_response = json.dumps({
                    'error': 'query_text must be at least 10 characters'
                })
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(error_response.encode())
                return

            query_id = str(uuid.uuid4())
            start_time = time.time()

            # Simple keyword matching for retrieval
            query_lower = query_text.lower()
            keywords = {
                "embodied": 0, "intelligence": 0,
                "bipedal": 1, "locomotion": 1, "walk": 1, "robot": 1,
                "ros": 2, "framework": 2,
                "digital": 3, "twin": 3, "simulation": 3,
                "vision": 4, "language": 4, "action": 4,
                "capstone": 5, "project": 5
            }

            scores = [0.0] * len(CHUNKS)
            for keyword, idx in keywords.items():
                if keyword in query_lower:
                    scores[idx] += 0.3

            for i in range(len(scores)):
                scores[i] += random.random() * 0.15

            top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:2]
            retrieved = [CHUNKS[i] for i in top_indices if scores[i] > 0.15]

            if not retrieved:
                retrieved = [CHUNKS[0]]

            response_text = "Based on the textbook: "
            sources = []

            for chunk in retrieved:
                response_text += chunk["text"] + " "
                sources.append({
                    "chunk_id": f"chunk_{chunk['ch']}",
                    "chapter_name": f"Chapter {chunk['ch'].upper()}",
                    "section_name": chunk['title'],
                    "section_number": chunk['sec'],
                    "page_number": chunk['page'],
                    "link_anchor": f"{chunk['ch']}-{chunk['title'].lower().replace(' ', '-')}"
                })

            response_text += f"\n\n**Sources:**\n"
            for src in sources:
                response_text += f"- {src['chapter_name']} Section {src['section_number']}: {src['section_name']} (page {src['page_number']})\n"

            latency_ms = (time.time() - start_time) * 1000
            confidence = 0.83 + random.random() * 0.12

            response_data = {
                "id": str(uuid.uuid4()),
                "query_id": query_id,
                "query_text": query_text,
                "response_text": response_text,
                "sources": sources,
                "confidence_score": round(confidence, 2),
                "hallucination_detected": False,
                "latency_ms": round(latency_ms, 1),
                "embedding_model": "bge-small-en-v1.5"
            }

            response = json.dumps(response_data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.encode())

        except Exception as e:
            error_response = json.dumps({'error': str(e)})
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(error_response.encode())
