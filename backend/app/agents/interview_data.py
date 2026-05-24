"""
Complete interview question bank for AI-COS.
Covers HR, Technical, AI Engineering, DevOps, Freelance, and Storytelling.
"""

HR_QUESTIONS = [
    "Tell me about yourself.",
    "What are your greatest strengths?",
    "What is your biggest weakness?",
    "Where do you see yourself in 5 years?",
    "Why do you want to leave your current job?",
    "Why should we hire you?",
    "Tell me about a challenge you faced and how you handled it.",
    "What motivates you at work?",
    "How do you handle pressure and tight deadlines?",
    "Describe a time you worked in a team and had a conflict.",
    "What are your salary expectations?",
    "Tell me about a time you failed and what you learned.",
    "How do you prioritize your work?",
    "What do you know about our company?",
    "Do you have any questions for us?",
]

TECHNICAL_QUESTIONS = [
    "Explain what an API is and how REST works.",
    "What is the difference between SQL and NoSQL databases?",
    "How does Docker help in software development?",
    "What is CI/CD and why is it important?",
    "Explain microservices architecture.",
    "What is a database index and when would you use one?",
    "How would you debug a slow API endpoint?",
    "What is the difference between synchronous and asynchronous programming?",
    "Explain what a WebSocket is and when to use it over REST.",
    "What is version control and how do you use Git in a team?",
    "How do you ensure your code is secure?",
    "What is containerization and how does Kubernetes relate to Docker?",
    "Explain the difference between authentication and authorization.",
    "What is caching and when would you use Redis?",
    "How would you design a system that needs to handle 1 million requests per day?",
]

AI_ENGINEERING_QUESTIONS = [
    "What is a large language model and how does it work?",
    "Explain RAG — Retrieval Augmented Generation — and when to use it.",
    "What is the difference between fine-tuning and prompt engineering?",
    "How does a vector database work and why is it useful for AI?",
    "What is LangChain and what problems does it solve?",
    "Explain what an AI agent is and how multi-agent systems work.",
    "What is the difference between supervised and unsupervised learning?",
    "How would you reduce hallucinations in an LLM application?",
    "What is embeddings and how are they used in semantic search?",
    "Explain the transformer architecture in simple terms.",
    "How would you build a production-grade RAG pipeline?",
    "What is LangGraph and how does it differ from LangChain?",
    "How do you evaluate the quality of an LLM application?",
    "What is the role of temperature in LLM generation?",
    "How would you handle context window limitations in a chatbot?",
]

DEVOPS_QUESTIONS = [
    "What is Infrastructure as Code and which tools have you used?",
    "Explain the difference between Docker and a virtual machine.",
    "What is Kubernetes and what problem does it solve?",
    "How do you monitor a production system?",
    "What is a deployment pipeline and how would you set one up?",
    "Explain blue-green deployment.",
    "What is a load balancer and when do you need one?",
    "How do you handle secrets and environment variables securely?",
    "What is the difference between horizontal and vertical scaling?",
    "Describe your experience with cloud platforms like AWS, GCP, or Azure.",
]

FREELANCE_QUESTIONS = [
    "Tell me about yourself and your experience.",
    "Walk me through a project you are proud of.",
    "How do you handle client feedback and revisions?",
    "What is your development process from requirement to delivery?",
    "How do you estimate project timelines and costs?",
    "Tell me about a time you missed a deadline and how you handled it.",
    "How do you communicate project progress to clients?",
    "What tools do you use for project management?",
    "How do you handle a client who keeps changing requirements?",
    "What is your hourly rate and how do you justify it?",
    "Can you work with our existing codebase?",
    "How do you ensure code quality in your projects?",
]

PROJECT_PROMPTS = {
    "fastapi": [
        "Explain your FastAPI project — what problem does it solve?",
        "How did you design the API endpoints in your FastAPI project?",
        "How do you handle authentication in your FastAPI application?",
        "What database did you use and how does SQLAlchemy connect to it?",
        "How did you handle errors and validation in FastAPI?",
        "Explain the async architecture in your FastAPI project.",
    ],
    "ai_agent": [
        "Explain your AI agent project — what does it do?",
        "How did you design the multi-agent system?",
        "What LLM did you use and why did you choose it?",
        "How does the RAG system work in your project?",
        "What was the biggest technical challenge you faced?",
        "How do you evaluate the quality of your AI agent's responses?",
    ],
    "rag": [
        "Explain your RAG system — how does it work?",
        "What vector database did you choose and why?",
        "How do you chunk and embed documents?",
        "How do you measure retrieval quality?",
        "What was the hardest part of building the RAG pipeline?",
        "How do you handle cases where the context is not relevant?",
    ],
    "saas": [
        "Tell me about the SaaS product you built.",
        "How did you handle user authentication and authorization?",
        "How did you design the subscription and billing system?",
        "What was your deployment strategy?",
        "How do you handle scalability in your SaaS?",
        "What metrics do you track for your SaaS product?",
    ],
}

STORYTELLING_PROMPTS = [
    "Tell me a story about overcoming a technical challenge.",
    "Describe a project from start to finish as a story.",
    "Tell me about a time you learned something completely new.",
    "Share a story about a mistake you made and what you learned.",
    "Tell me about your journey into AI engineering.",
    "Describe a time you had to explain a technical concept to a non-technical person.",
    "Share a story about a team project that went really well.",
    "Tell me about the most interesting problem you have ever solved.",
]

CONFIDENCE_EXERCISES = [
    "Introduce yourself in 60 seconds as if you are at a networking event.",
    "Explain what you do to someone who knows nothing about technology.",
    "Pitch yourself to a recruiter in 30 seconds.",
    "Describe your strongest skill and why it makes you valuable.",
    "Tell me why you are the best person for this role.",
]

STAR_FRAMEWORK = """
The STAR method helps you answer behavioral questions clearly:

S — Situation: Set the scene. What was the context?
T — Task: What was your responsibility or challenge?
A — Action: What specific steps did YOU take?
R — Result: What was the outcome? Use numbers if possible.

Example:
Q: Tell me about a challenge you faced.
S: "At my previous job, our deployment pipeline was taking 2 hours..."
T: "I was asked to reduce deployment time by 50%..."
A: "I implemented Docker containers and set up a CI/CD pipeline..."
R: "Deployment time dropped from 2 hours to 20 minutes — a 83% improvement."
"""
