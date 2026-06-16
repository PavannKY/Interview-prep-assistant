"""
Skill bank for dataset generation.
Covers: Web Development, Data Science/ML, DevOps/Cloud
"""

SKILL_BANK = {

    # ─── Web Development ──────────────────────────────────────────────────────
    "web_dev": {
        "frontend": [
            "React", "Vue.js", "Angular", "Next.js", "TypeScript", "JavaScript",
            "HTML", "CSS", "Tailwind CSS", "Redux", "GraphQL", "REST APIs",
            "Webpack", "Vite", "Jest", "Cypress"
        ],
        "backend": [
            "FastAPI", "Django", "Flask", "Node.js", "Express.js", "Spring Boot",
            "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLAlchemy", "Prisma",
            "JWT", "OAuth2", "WebSockets", "Celery", "RabbitMQ"
        ],
        "fullstack": [
            "Docker", "Nginx", "CI/CD", "REST API design", "Microservices",
            "System Design", "Database Design", "Caching", "Authentication"
        ]
    },

    # ─── Data Science / ML ────────────────────────────────────────────────────
    "data_ml": {
        "core": [
            "Python", "NumPy", "Pandas", "Matplotlib", "Seaborn",
            "Scikit-learn", "Statsmodels", "SciPy"
        ],
        "ml": [
            "Machine Learning", "Deep Learning", "Neural Networks",
            "Random Forest", "XGBoost", "LightGBM", "Linear Regression",
            "Logistic Regression", "SVM", "K-Means", "PCA",
            "Feature Engineering", "Cross Validation", "Hyperparameter Tuning"
        ],
        "dl_nlp": [
            "PyTorch", "TensorFlow", "Keras", "Transformers", "BERT", "GPT",
            "Fine-tuning", "LoRA", "NLP", "Computer Vision", "CNN", "RNN", "LSTM",
            "Attention Mechanism", "Embeddings", "RAG", "LangChain", "LlamaIndex"
        ],
        "data_eng": [
            "SQL", "Spark", "Airflow", "dbt", "ETL pipelines",
            "Data Warehousing", "Snowflake", "BigQuery", "Kafka",
            "Data Cleaning", "EDA", "A/B Testing", "Statistics"
        ]
    },

    # ─── DevOps / Cloud ───────────────────────────────────────────────────────
    "devops": {
        "containers": [
            "Docker", "Kubernetes", "Helm", "Docker Compose",
            "Container Registry", "Podman"
        ],
        "cloud": [
            "AWS", "GCP", "Azure", "EC2", "S3", "Lambda", "RDS",
            "Cloud Functions", "Cloud Run", "Azure Functions",
            "IAM", "VPC", "Load Balancers", "Auto Scaling"
        ],
        "cicd": [
            "GitHub Actions", "Jenkins", "GitLab CI", "CircleCI",
            "ArgoCD", "Terraform", "Ansible", "Pulumi",
            "Infrastructure as Code", "Blue-Green Deployment"
        ],
        "monitoring": [
            "Prometheus", "Grafana", "ELK Stack", "Datadog",
            "CloudWatch", "Distributed Tracing", "OpenTelemetry",
            "SRE", "SLO", "SLA", "Incident Management"
        ]
    }
}


# ─── Skill Combinations ───────────────────────────────────────────────────────
# Each entry = a realistic candidate skill set (2-5 skills)
SKILL_COMBINATIONS = [

    # Web Dev combos
    ["React", "TypeScript", "Node.js"],
    ["React", "Redux", "REST APIs", "Jest"],
    ["Vue.js", "Django", "PostgreSQL"],
    ["Next.js", "TypeScript", "Tailwind CSS", "GraphQL"],
    ["FastAPI", "PostgreSQL", "Redis", "Docker"],
    ["Django", "Celery", "RabbitMQ", "PostgreSQL"],
    ["Node.js", "Express.js", "MongoDB", "JWT"],
    ["React", "FastAPI", "SQLAlchemy", "Docker"],
    ["Angular", "Spring Boot", "MySQL"],
    ["Flask", "Redis", "REST APIs", "OAuth2"],
    ["Next.js", "Prisma", "PostgreSQL", "TypeScript"],
    ["WebSockets", "FastAPI", "Redis", "Docker"],
    ["React", "GraphQL", "Node.js", "MongoDB"],
    ["Django", "PostgreSQL", "Nginx", "CI/CD"],
    ["Microservices", "Docker", "FastAPI", "RabbitMQ"],
    ["System Design", "Caching", "Database Design", "REST API design"],
    ["Authentication", "JWT", "OAuth2", "FastAPI"],

    # Data Science / ML combos
    ["Python", "Pandas", "Scikit-learn", "Matplotlib"],
    ["Machine Learning", "XGBoost", "Feature Engineering", "Cross Validation"],
    ["Deep Learning", "PyTorch", "CNN", "Computer Vision"],
    ["NLP", "Transformers", "BERT", "Fine-tuning"],
    ["Python", "NumPy", "Pandas", "EDA"],
    ["Random Forest", "XGBoost", "Hyperparameter Tuning", "Scikit-learn"],
    ["TensorFlow", "Keras", "Neural Networks", "Deep Learning"],
    ["RAG", "LangChain", "Embeddings", "LlamaIndex"],
    ["SQL", "Spark", "ETL pipelines", "Airflow"],
    ["Statistics", "A/B Testing", "Python", "Pandas"],
    ["LightGBM", "XGBoost", "Feature Engineering", "Cross Validation"],
    ["PyTorch", "LoRA", "Fine-tuning", "Transformers"],
    ["Data Warehousing", "BigQuery", "dbt", "SQL"],
    ["Kafka", "Spark", "Airflow", "ETL pipelines"],
    ["PCA", "K-Means", "Scikit-learn", "Python"],
    ["LSTM", "RNN", "PyTorch", "NLP"],
    ["BERT", "Transformers", "NLP", "Fine-tuning"],
    ["EDA", "Seaborn", "Pandas", "Statistics"],

    # DevOps / Cloud combos
    ["Docker", "Kubernetes", "Helm", "CI/CD"],
    ["AWS", "EC2", "S3", "Lambda"],
    ["Terraform", "AWS", "IAM", "VPC"],
    ["GitHub Actions", "Docker", "Kubernetes"],
    ["Prometheus", "Grafana", "Kubernetes", "SRE"],
    ["GCP", "Cloud Run", "Cloud Functions", "BigQuery"],
    ["Azure", "Azure Functions", "IAM", "CI/CD"],
    ["ArgoCD", "Kubernetes", "Helm", "GitLab CI"],
    ["ELK Stack", "Grafana", "Prometheus", "Datadog"],
    ["Ansible", "Terraform", "Infrastructure as Code", "AWS"],
    ["Docker Compose", "Nginx", "CI/CD", "GitHub Actions"],
    ["Blue-Green Deployment", "Kubernetes", "ArgoCD"],
    ["Auto Scaling", "Load Balancers", "AWS", "EC2"],
    ["OpenTelemetry", "Distributed Tracing", "Prometheus"],
    ["Jenkins", "Docker", "Kubernetes", "CI/CD"],
    ["Pulumi", "AWS", "Infrastructure as Code"],
    ["SLO", "SLA", "Incident Management", "SRE"],

    # Cross-domain combos (realistic full-stack / MLOps profiles)
    ["Python", "FastAPI", "Docker", "PostgreSQL"],
    ["Machine Learning", "Docker", "AWS", "FastAPI"],
    ["PyTorch", "Docker", "Kubernetes", "CI/CD"],
    ["React", "FastAPI", "PostgreSQL", "Docker", "AWS"],
    ["Airflow", "Spark", "AWS", "Docker"],
    ["MLOps", "Docker", "Kubernetes", "Prometheus"] if True else [],
    ["NLP", "FastAPI", "Docker", "PostgreSQL"],
    ["Data Warehousing", "Airflow", "AWS", "SQL"],
]

# Remove empty combos
SKILL_COMBINATIONS = [s for s in SKILL_COMBINATIONS if s]
