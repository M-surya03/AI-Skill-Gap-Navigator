"""
Skill Gap Navigator — Skills Taxonomy
Curated database of 150+ skills with metadata, resources, and prerequisites.
"""

from typing import Dict, List, Any

SKILLS_TAXONOMY: Dict[str, Dict[str, Any]] = {
    # ─── Programming Languages ─────────────────────────────────────────────
    "python": {
        "canonical": "Python",
        "category": "Programming Languages",
        "aliases": ["python3", "python programming", "py", "python developer", "python scripting"],
        "difficulty": 2,
        "avg_weeks_to_learn": 8,
        "prerequisites": [],
        "resources": [
            {"title": "Python Official Tutorial", "url": "https://docs.python.org/3/tutorial/", "type": "documentation"},
            {"title": "CS50P – Harvard Python Course", "url": "https://cs50.harvard.edu/python/2022/", "type": "course"},
            {"title": "Automate the Boring Stuff", "url": "https://automatetheboringstuff.com/", "type": "book"},
        ],
        "related_jobs": ["Data Scientist", "Backend Developer", "ML Engineer", "Data Analyst"],
    },
    "javascript": {
        "canonical": "JavaScript",
        "category": "Programming Languages",
        "aliases": ["js", "javascript programming", "ecmascript", "es6", "es2015"],
        "difficulty": 2,
        "avg_weeks_to_learn": 8,
        "prerequisites": ["html", "css"],
        "resources": [
            {"title": "The Odin Project", "url": "https://www.theodinproject.com/", "type": "course"},
            {"title": "javascript.info", "url": "https://javascript.info/", "type": "tutorial"},
            {"title": "MDN Web Docs", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "type": "documentation"},
        ],
        "related_jobs": ["Frontend Developer", "Full Stack Developer", "Web Developer"],
    },
    "typescript": {
        "canonical": "TypeScript",
        "category": "Programming Languages",
        "aliases": ["ts", "typescript programming"],
        "difficulty": 2,
        "avg_weeks_to_learn": 4,
        "prerequisites": ["javascript"],
        "resources": [
            {"title": "TypeScript Official Handbook", "url": "https://www.typescriptlang.org/docs/handbook/", "type": "documentation"},
            {"title": "Total TypeScript", "url": "https://www.totaltypescript.com/", "type": "course"},
        ],
        "related_jobs": ["Frontend Developer", "Full Stack Developer"],
    },
    "java": {
        "canonical": "Java",
        "category": "Programming Languages",
        "aliases": ["java programming", "core java", "java developer"],
        "difficulty": 3,
        "avg_weeks_to_learn": 10,
        "prerequisites": [],
        "resources": [
            {"title": "Java Programming MOOC", "url": "https://java-programming.mooc.fi/", "type": "course"},
            {"title": "Effective Java", "url": "https://www.oreilly.com/library/view/effective-java/9780134686097/", "type": "book"},
        ],
        "related_jobs": ["Backend Developer", "Android Developer", "Enterprise Developer"],
    },
    "c++": {
        "canonical": "C++",
        "category": "Programming Languages",
        "aliases": ["cpp", "c plus plus", "cplusplus"],
        "difficulty": 4,
        "avg_weeks_to_learn": 14,
        "prerequisites": ["c"],
        "resources": [
            {"title": "learncpp.com", "url": "https://www.learncpp.com/", "type": "tutorial"},
            {"title": "C++ Primer", "url": "https://www.oreilly.com/library/view/c-primer-fifth/9780133053043/", "type": "book"},
        ],
        "related_jobs": ["Systems Engineer", "Game Developer", "Embedded Developer"],
    },
    "c": {
        "canonical": "C",
        "category": "Programming Languages",
        "aliases": ["c programming", "c language"],
        "difficulty": 3,
        "avg_weeks_to_learn": 10,
        "prerequisites": [],
        "resources": [
            {"title": "CS50 – Harvard", "url": "https://cs50.harvard.edu/x/", "type": "course"},
        ],
        "related_jobs": ["Systems Engineer", "Embedded Developer"],
    },
    "go": {
        "canonical": "Go",
        "category": "Programming Languages",
        "aliases": ["golang", "go programming"],
        "difficulty": 2,
        "avg_weeks_to_learn": 6,
        "prerequisites": ["programming_basics"],
        "resources": [
            {"title": "A Tour of Go", "url": "https://go.dev/tour/welcome/1", "type": "tutorial"},
            {"title": "Go by Example", "url": "https://gobyexample.com/", "type": "tutorial"},
        ],
        "related_jobs": ["Backend Developer", "DevOps Engineer", "Cloud Engineer"],
    },
    "rust": {
        "canonical": "Rust",
        "category": "Programming Languages",
        "aliases": ["rust programming", "rust lang"],
        "difficulty": 4,
        "avg_weeks_to_learn": 14,
        "prerequisites": ["programming_basics"],
        "resources": [
            {"title": "The Rust Book", "url": "https://doc.rust-lang.org/book/", "type": "book"},
        ],
        "related_jobs": ["Systems Engineer", "WebAssembly Developer"],
    },
    "r": {
        "canonical": "R",
        "category": "Programming Languages",
        "aliases": ["r programming", "r language", "rlang"],
        "difficulty": 2,
        "avg_weeks_to_learn": 6,
        "prerequisites": ["statistics"],
        "resources": [
            {"title": "R for Data Science", "url": "https://r4ds.had.co.nz/", "type": "book"},
        ],
        "related_jobs": ["Data Analyst", "Statistician", "Data Scientist"],
    },
    "scala": {
        "canonical": "Scala",
        "category": "Programming Languages",
        "aliases": ["scala programming"],
        "difficulty": 3,
        "avg_weeks_to_learn": 10,
        "prerequisites": ["java"],
        "resources": [
            {"title": "Scala Exercises", "url": "https://www.scala-exercises.org/", "type": "tutorial"},
        ],
        "related_jobs": ["Data Engineer", "Big Data Developer"],
    },

    # ─── Web Frameworks ────────────────────────────────────────────────────
    "react": {
        "canonical": "React.js",
        "category": "Web Frameworks",
        "aliases": ["reactjs", "react.js", "react js", "react framework"],
        "difficulty": 3,
        "avg_weeks_to_learn": 8,
        "prerequisites": ["javascript", "html", "css"],
        "resources": [
            {"title": "React Official Docs", "url": "https://react.dev/", "type": "documentation"},
            {"title": "Full Stack Open", "url": "https://fullstackopen.com/en/", "type": "course"},
        ],
        "related_jobs": ["Frontend Developer", "Full Stack Developer"],
    },
    "nextjs": {
        "canonical": "Next.js",
        "category": "Web Frameworks",
        "aliases": ["next.js", "next js", "nextjs framework"],
        "difficulty": 3,
        "avg_weeks_to_learn": 6,
        "prerequisites": ["react", "javascript"],
        "resources": [
            {"title": "Next.js Official Docs", "url": "https://nextjs.org/docs", "type": "documentation"},
            {"title": "Next.js Tutorial", "url": "https://nextjs.org/learn", "type": "course"},
        ],
        "related_jobs": ["Full Stack Developer", "Frontend Developer"],
    },
    "vue": {
        "canonical": "Vue.js",
        "category": "Web Frameworks",
        "aliases": ["vuejs", "vue.js", "vue js"],
        "difficulty": 2,
        "avg_weeks_to_learn": 6,
        "prerequisites": ["javascript", "html", "css"],
        "resources": [
            {"title": "Vue.js Official Docs", "url": "https://vuejs.org/guide/introduction.html", "type": "documentation"},
        ],
        "related_jobs": ["Frontend Developer", "Full Stack Developer"],
    },
    "angular": {
        "canonical": "Angular",
        "category": "Web Frameworks",
        "aliases": ["angular.js", "angularjs", "angular framework"],
        "difficulty": 4,
        "avg_weeks_to_learn": 10,
        "prerequisites": ["typescript", "javascript"],
        "resources": [
            {"title": "Angular Official Docs", "url": "https://angular.io/docs", "type": "documentation"},
        ],
        "related_jobs": ["Frontend Developer", "Full Stack Developer"],
    },
    "fastapi": {
        "canonical": "FastAPI",
        "category": "Web Frameworks",
        "aliases": ["fast api", "fastapi framework"],
        "difficulty": 2,
        "avg_weeks_to_learn": 4,
        "prerequisites": ["python"],
        "resources": [
            {"title": "FastAPI Official Docs", "url": "https://fastapi.tiangolo.com/", "type": "documentation"},
        ],
        "related_jobs": ["Backend Developer", "ML Engineer", "API Developer"],
    },
    "django": {
        "canonical": "Django",
        "category": "Web Frameworks",
        "aliases": ["django framework", "django rest framework", "drf"],
        "difficulty": 3,
        "avg_weeks_to_learn": 8,
        "prerequisites": ["python"],
        "resources": [
            {"title": "Django Official Docs", "url": "https://docs.djangoproject.com/", "type": "documentation"},
            {"title": "Django Girls Tutorial", "url": "https://tutorial.djangogirls.org/", "type": "tutorial"},
        ],
        "related_jobs": ["Backend Developer", "Full Stack Developer"],
    },
    "flask": {
        "canonical": "Flask",
        "category": "Web Frameworks",
        "aliases": ["flask framework", "flask python"],
        "difficulty": 2,
        "avg_weeks_to_learn": 4,
        "prerequisites": ["python"],
        "resources": [
            {"title": "Flask Official Docs", "url": "https://flask.palletsprojects.com/", "type": "documentation"},
        ],
        "related_jobs": ["Backend Developer", "API Developer"],
    },
    "node": {
        "canonical": "Node.js",
        "category": "Web Frameworks",
        "aliases": ["nodejs", "node.js", "node js"],
        "difficulty": 3,
        "avg_weeks_to_learn": 6,
        "prerequisites": ["javascript"],
        "resources": [
            {"title": "Node.js Official Docs", "url": "https://nodejs.org/en/docs/", "type": "documentation"},
        ],
        "related_jobs": ["Backend Developer", "Full Stack Developer"],
    },
    "express": {
        "canonical": "Express.js",
        "category": "Web Frameworks",
        "aliases": ["expressjs", "express.js", "express js"],
        "difficulty": 2,
        "avg_weeks_to_learn": 4,
        "prerequisites": ["node", "javascript"],
        "resources": [
            {"title": "Express.js Official Docs", "url": "https://expressjs.com/", "type": "documentation"},
        ],
        "related_jobs": ["Backend Developer", "Full Stack Developer"],
    },
    "spring": {
        "canonical": "Spring Boot",
        "category": "Web Frameworks",
        "aliases": ["spring boot", "spring framework", "springboot"],
        "difficulty": 4,
        "avg_weeks_to_learn": 10,
        "prerequisites": ["java"],
        "resources": [
            {"title": "Spring Boot Official Docs", "url": "https://spring.io/projects/spring-boot", "type": "documentation"},
        ],
        "related_jobs": ["Backend Developer", "Enterprise Developer"],
    },

    # ─── Web Basics ────────────────────────────────────────────────────────
    "html": {
        "canonical": "HTML",
        "category": "Web Basics",
        "aliases": ["html5", "hypertext markup language"],
        "difficulty": 1,
        "avg_weeks_to_learn": 2,
        "prerequisites": [],
        "resources": [
            {"title": "MDN HTML Guide", "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML", "type": "documentation"},
        ],
        "related_jobs": ["Frontend Developer", "Web Designer"],
    },
    "css": {
        "canonical": "CSS",
        "category": "Web Basics",
        "aliases": ["css3", "cascading style sheets", "tailwind", "tailwindcss", "sass", "scss"],
        "difficulty": 1,
        "avg_weeks_to_learn": 3,
        "prerequisites": ["html"],
        "resources": [
            {"title": "MDN CSS Guide", "url": "https://developer.mozilla.org/en-US/docs/Learn/CSS", "type": "documentation"},
            {"title": "CSS Tricks", "url": "https://css-tricks.com/", "type": "tutorial"},
        ],
        "related_jobs": ["Frontend Developer", "Web Designer"],
    },
    "graphql": {
        "canonical": "GraphQL",
        "category": "Web Basics",
        "aliases": ["graph ql", "graphql api"],
        "difficulty": 3,
        "avg_weeks_to_learn": 4,
        "prerequisites": ["api_design"],
        "resources": [
            {"title": "GraphQL Official Docs", "url": "https://graphql.org/learn/", "type": "documentation"},
        ],
        "related_jobs": ["Full Stack Developer", "Backend Developer"],
    },
    "rest_api": {
        "canonical": "REST API",
        "category": "Web Basics",
        "aliases": ["rest", "restful", "restful api", "api design", "api_design", "web api"],
        "difficulty": 2,
        "avg_weeks_to_learn": 3,
        "prerequisites": ["http"],
        "resources": [
            {"title": "REST API Tutorial", "url": "https://restfulapi.net/", "type": "tutorial"},
        ],
        "related_jobs": ["Backend Developer", "Full Stack Developer"],
    },

    # ─── Data Science & ML ─────────────────────────────────────────────────
    "machine_learning": {
        "canonical": "Machine Learning",
        "category": "AI/ML",
        "aliases": ["ml", "machine learning algorithms", "supervised learning", "unsupervised learning"],
        "difficulty": 4,
        "avg_weeks_to_learn": 16,
        "prerequisites": ["python", "statistics", "linear_algebra"],
        "resources": [
            {"title": "Andrew Ng's ML Course (Coursera)", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "type": "course"},
            {"title": "fast.ai Practical Deep Learning", "url": "https://course.fast.ai/", "type": "course"},
            {"title": "Hands-On ML – Aurélien Géron", "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/", "type": "book"},
        ],
        "related_jobs": ["ML Engineer", "Data Scientist", "AI Engineer"],
    },
    "deep_learning": {
        "canonical": "Deep Learning",
        "category": "AI/ML",
        "aliases": ["dl", "neural networks", "deep neural network", "dnn", "ann"],
        "difficulty": 5,
        "avg_weeks_to_learn": 16,
        "prerequisites": ["machine_learning", "python", "linear_algebra"],
        "resources": [
            {"title": "Deep Learning Specialization – Coursera", "url": "https://www.coursera.org/specializations/deep-learning", "type": "course"},
            {"title": "Deep Learning Book", "url": "https://www.deeplearningbook.org/", "type": "book"},
        ],
        "related_jobs": ["ML Engineer", "AI Researcher", "Computer Vision Engineer"],
    },
    "tensorflow": {
        "canonical": "TensorFlow",
        "category": "AI/ML",
        "aliases": ["tensorflow 2", "tf", "keras", "tensorflow/keras"],
        "difficulty": 3,
        "avg_weeks_to_learn": 6,
        "prerequisites": ["python", "machine_learning"],
        "resources": [
            {"title": "TensorFlow Official Tutorials", "url": "https://www.tensorflow.org/tutorials", "type": "documentation"},
        ],
        "related_jobs": ["ML Engineer", "Data Scientist"],
    },
    "pytorch": {
        "canonical": "PyTorch",
        "category": "AI/ML",
        "aliases": ["torch", "pytorch framework"],
        "difficulty": 3,
        "avg_weeks_to_learn": 6,
        "prerequisites": ["python", "machine_learning"],
        "resources": [
            {"title": "PyTorch Official Tutorials", "url": "https://pytorch.org/tutorials/", "type": "documentation"},
            {"title": "Deep Learning with PyTorch", "url": "https://pytorch.org/deep-learning-with-pytorch", "type": "book"},
        ],
        "related_jobs": ["ML Engineer", "AI Researcher"],
    },
    "nlp": {
        "canonical": "Natural Language Processing",
        "category": "AI/ML",
        "aliases": ["natural language processing", "text mining", "text analytics", "language models", "llm"],
        "difficulty": 4,
        "avg_weeks_to_learn": 12,
        "prerequisites": ["machine_learning", "python"],
        "resources": [
            {"title": "Hugging Face NLP Course", "url": "https://huggingface.co/learn/nlp-course", "type": "course"},
            {"title": "Stanford NLP (CS224N)", "url": "https://web.stanford.edu/class/cs224n/", "type": "course"},
        ],
        "related_jobs": ["NLP Engineer", "AI Researcher", "Data Scientist"],
    },
    "computer_vision": {
        "canonical": "Computer Vision",
        "category": "AI/ML",
        "aliases": ["cv", "image processing", "object detection", "image recognition"],
        "difficulty": 4,
        "avg_weeks_to_learn": 12,
        "prerequisites": ["deep_learning", "python"],
        "resources": [
            {"title": "Stanford CS231n", "url": "http://cs231n.stanford.edu/", "type": "course"},
            {"title": "OpenCV Official Docs", "url": "https://docs.opencv.org/", "type": "documentation"},
        ],
        "related_jobs": ["Computer Vision Engineer", "ML Engineer"],
    },
    "scikit_learn": {
        "canonical": "Scikit-Learn",
        "category": "AI/ML",
        "aliases": ["sklearn", "scikit learn", "sci-kit learn"],
        "difficulty": 2,
        "avg_weeks_to_learn": 4,
        "prerequisites": ["python", "statistics"],
        "resources": [
            {"title": "Scikit-learn Official Docs", "url": "https://scikit-learn.org/stable/", "type": "documentation"},
        ],
        "related_jobs": ["Data Scientist", "ML Engineer"],
    },
    "llm": {
        "canonical": "Large Language Models",
        "category": "AI/ML",
        "aliases": ["llms", "large language models", "gpt", "chatgpt", "openai", "gemini", "claude", "generative ai", "gen ai", "langchain"],
        "difficulty": 4,
        "avg_weeks_to_learn": 10,
        "prerequisites": ["nlp", "machine_learning", "python"],
        "resources": [
            {"title": "LLM University – Cohere", "url": "https://llm.university/", "type": "course"},
            {"title": "Hugging Face Transformers", "url": "https://huggingface.co/docs/transformers", "type": "documentation"},
        ],
        "related_jobs": ["AI Engineer", "ML Engineer", "Prompt Engineer"],
    },

    # ─── Data Engineering ──────────────────────────────────────────────────
    "sql": {
        "canonical": "SQL",
        "category": "Databases",
        "aliases": ["mysql", "postgresql", "postgres", "sqlite", "relational database", "rdbms", "database"],
        "difficulty": 2,
        "avg_weeks_to_learn": 6,
        "prerequisites": [],
        "resources": [
            {"title": "SQLZoo", "url": "https://sqlzoo.net/", "type": "tutorial"},
            {"title": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "type": "tutorial"},
        ],
        "related_jobs": ["Data Analyst", "Data Engineer", "Backend Developer"],
    },
    "mongodb": {
        "canonical": "MongoDB",
        "category": "Databases",
        "aliases": ["mongo", "mongodb database", "nosql", "no-sql"],
        "difficulty": 2,
        "avg_weeks_to_learn": 4,
        "prerequisites": [],
        "resources": [
            {"title": "MongoDB University", "url": "https://university.mongodb.com/", "type": "course"},
        ],
        "related_jobs": ["Backend Developer", "Full Stack Developer", "Data Engineer"],
    },
    "spark": {
        "canonical": "Apache Spark",
        "category": "Data Engineering",
        "aliases": ["pyspark", "apache spark", "spark framework"],
        "difficulty": 4,
        "avg_weeks_to_learn": 10,
        "prerequisites": ["python", "sql"],
        "resources": [
            {"title": "Spark Official Docs", "url": "https://spark.apache.org/docs/latest/", "type": "documentation"},
        ],
        "related_jobs": ["Data Engineer", "Big Data Engineer"],
    },
    "kafka": {
        "canonical": "Apache Kafka",
        "category": "Data Engineering",
        "aliases": ["apache kafka", "kafka streaming", "event streaming"],
        "difficulty": 4,
        "avg_weeks_to_learn": 8,
        "prerequisites": ["distributed_systems"],
        "resources": [
            {"title": "Kafka Official Docs", "url": "https://kafka.apache.org/documentation/", "type": "documentation"},
        ],
        "related_jobs": ["Data Engineer", "Backend Developer", "Platform Engineer"],
    },
    "airflow": {
        "canonical": "Apache Airflow",
        "category": "Data Engineering",
        "aliases": ["apache airflow", "airflow orchestration", "workflow orchestration"],
        "difficulty": 3,
        "avg_weeks_to_learn": 6,
        "prerequisites": ["python", "sql"],
        "resources": [
            {"title": "Airflow Official Docs", "url": "https://airflow.apache.org/docs/", "type": "documentation"},
        ],
        "related_jobs": ["Data Engineer", "ML Ops Engineer"],
    },
    "data_visualization": {
        "canonical": "Data Visualization",
        "category": "Data Science",
        "aliases": ["visualization", "matplotlib", "seaborn", "plotly", "tableau", "power bi", "powerbi", "dashboards", "charts"],
        "difficulty": 2,
        "avg_weeks_to_learn": 4,
        "prerequisites": ["python", "statistics"],
        "resources": [
            {"title": "Matplotlib Tutorials", "url": "https://matplotlib.org/stable/tutorials/index.html", "type": "documentation"},
            {"title": "Plotly Python Docs", "url": "https://plotly.com/python/", "type": "documentation"},
        ],
        "related_jobs": ["Data Analyst", "Data Scientist", "BI Developer"],
    },
    "data_analysis": {
        "canonical": "Data Analysis",
        "category": "Data Science",
        "aliases": ["data analytics", "pandas", "numpy", "data wrangling", "eda", "exploratory data analysis"],
        "difficulty": 2,
        "avg_weeks_to_learn": 6,
        "prerequisites": ["python", "statistics"],
        "resources": [
            {"title": "Pandas Official Docs", "url": "https://pandas.pydata.org/docs/", "type": "documentation"},
            {"title": "Kaggle Learn – Data Analysis", "url": "https://www.kaggle.com/learn", "type": "course"},
        ],
        "related_jobs": ["Data Analyst", "Data Scientist"],
    },

    # ─── Cloud & DevOps ────────────────────────────────────────────────────
    "aws": {
        "canonical": "AWS",
        "category": "Cloud",
        "aliases": ["amazon web services", "amazon aws", "ec2", "s3", "lambda", "cloud computing"],
        "difficulty": 3,
        "avg_weeks_to_learn": 10,
        "prerequisites": ["networking_basics", "linux"],
        "resources": [
            {"title": "AWS Free Tier", "url": "https://aws.amazon.com/free/", "type": "platform"},
            {"title": "AWS Skill Builder", "url": "https://skillbuilder.aws/", "type": "course"},
        ],
        "related_jobs": ["Cloud Engineer", "DevOps Engineer", "Solutions Architect"],
    },
    "azure": {
        "canonical": "Microsoft Azure",
        "category": "Cloud",
        "aliases": ["azure cloud", "microsoft azure", "azure devops"],
        "difficulty": 3,
        "avg_weeks_to_learn": 10,
        "prerequisites": ["networking_basics"],
        "resources": [
            {"title": "Microsoft Learn", "url": "https://learn.microsoft.com/en-us/training/", "type": "course"},
        ],
        "related_jobs": ["Cloud Engineer", "DevOps Engineer"],
    },
    "gcp": {
        "canonical": "Google Cloud Platform",
        "category": "Cloud",
        "aliases": ["google cloud", "gcp", "google cloud platform", "bigquery"],
        "difficulty": 3,
        "avg_weeks_to_learn": 10,
        "prerequisites": ["networking_basics"],
        "resources": [
            {"title": "Google Cloud Skills Boost", "url": "https://cloudskillsboost.google/", "type": "course"},
        ],
        "related_jobs": ["Cloud Engineer", "Data Engineer"],
    },
    "docker": {
        "canonical": "Docker",
        "category": "DevOps",
        "aliases": ["containerization", "containers", "dockerfile"],
        "difficulty": 2,
        "avg_weeks_to_learn": 4,
        "prerequisites": ["linux"],
        "resources": [
            {"title": "Docker Official Docs", "url": "https://docs.docker.com/get-started/", "type": "documentation"},
        ],
        "related_jobs": ["DevOps Engineer", "Platform Engineer", "SRE"],
    },
    "kubernetes": {
        "canonical": "Kubernetes",
        "category": "DevOps",
        "aliases": ["k8s", "kubernetes orchestration", "container orchestration"],
        "difficulty": 4,
        "avg_weeks_to_learn": 10,
        "prerequisites": ["docker"],
        "resources": [
            {"title": "Kubernetes Official Docs", "url": "https://kubernetes.io/docs/home/", "type": "documentation"},
        ],
        "related_jobs": ["DevOps Engineer", "Platform Engineer", "SRE"],
    },
    "git": {
        "canonical": "Git",
        "category": "DevOps",
        "aliases": ["git version control", "github", "gitlab", "version control", "bitbucket"],
        "difficulty": 2,
        "avg_weeks_to_learn": 3,
        "prerequisites": [],
        "resources": [
            {"title": "Pro Git Book", "url": "https://git-scm.com/book/en/v2", "type": "book"},
            {"title": "Learn Git Branching", "url": "https://learngitbranching.js.org/", "type": "tutorial"},
        ],
        "related_jobs": ["All Software Roles"],
    },
    "ci_cd": {
        "canonical": "CI/CD",
        "category": "DevOps",
        "aliases": ["cicd", "continuous integration", "continuous deployment", "github actions", "jenkins", "gitlab ci"],
        "difficulty": 3,
        "avg_weeks_to_learn": 6,
        "prerequisites": ["git", "docker"],
        "resources": [
            {"title": "GitHub Actions Docs", "url": "https://docs.github.com/en/actions", "type": "documentation"},
        ],
        "related_jobs": ["DevOps Engineer", "Platform Engineer"],
    },
    "linux": {
        "canonical": "Linux",
        "category": "DevOps",
        "aliases": ["unix", "bash", "shell scripting", "command line", "terminal", "bash scripting"],
        "difficulty": 2,
        "avg_weeks_to_learn": 5,
        "prerequisites": [],
        "resources": [
            {"title": "The Linux Command Line", "url": "https://linuxcommand.org/tlcl.php", "type": "book"},
        ],
        "related_jobs": ["DevOps Engineer", "Systems Engineer", "SRE"],
    },

    # ─── Core CS Concepts ──────────────────────────────────────────────────
    "statistics": {
        "canonical": "Statistics",
        "category": "Mathematics",
        "aliases": ["statistical analysis", "probability", "bayesian", "statistical modeling"],
        "difficulty": 3,
        "avg_weeks_to_learn": 10,
        "prerequisites": [],
        "resources": [
            {"title": "Khan Academy Statistics", "url": "https://www.khanacademy.org/math/statistics-probability", "type": "course"},
            {"title": "Think Stats", "url": "https://greenteapress.com/thinkstats2/", "type": "book"},
        ],
        "related_jobs": ["Data Scientist", "Data Analyst", "ML Engineer"],
    },
    "linear_algebra": {
        "canonical": "Linear Algebra",
        "category": "Mathematics",
        "aliases": ["matrix operations", "vectors", "matrices", "linear algebra for ml"],
        "difficulty": 3,
        "avg_weeks_to_learn": 8,
        "prerequisites": [],
        "resources": [
            {"title": "3Blue1Brown – Essence of Linear Algebra", "url": "https://www.3blue1brown.com/topics/linear-algebra", "type": "tutorial"},
        ],
        "related_jobs": ["ML Engineer", "Data Scientist"],
    },
    "data_structures": {
        "canonical": "Data Structures & Algorithms",
        "category": "Computer Science",
        "aliases": ["dsa", "algorithms", "data structures", "problem solving", "leetcode", "competitive programming"],
        "difficulty": 3,
        "avg_weeks_to_learn": 14,
        "prerequisites": ["programming_basics"],
        "resources": [
            {"title": "NeetCode", "url": "https://neetcode.io/", "type": "course"},
            {"title": "Introduction to Algorithms (CLRS)", "url": "https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/", "type": "book"},
        ],
        "related_jobs": ["Software Engineer", "Backend Developer"],
    },
    "system_design": {
        "canonical": "System Design",
        "category": "Computer Science",
        "aliases": ["distributed systems", "scalability", "microservices", "architecture"],
        "difficulty": 5,
        "avg_weeks_to_learn": 16,
        "prerequisites": ["data_structures", "networking_basics"],
        "resources": [
            {"title": "System Design Primer", "url": "https://github.com/donnemartin/system-design-primer", "type": "book"},
            {"title": "ByteByteGo", "url": "https://bytebytego.com/", "type": "course"},
        ],
        "related_jobs": ["Senior Engineer", "Solutions Architect"],
    },
    "networking_basics": {
        "canonical": "Computer Networking",
        "category": "Computer Science",
        "aliases": ["networking", "tcp/ip", "http", "http", "dns", "protocols"],
        "difficulty": 2,
        "avg_weeks_to_learn": 6,
        "prerequisites": [],
        "resources": [
            {"title": "Computer Networking: A Top-Down Approach", "url": "https://gaia.cs.umass.edu/kurose_ross/", "type": "book"},
        ],
        "related_jobs": ["Network Engineer", "DevOps Engineer", "Backend Developer"],
    },
    "programming_basics": {
        "canonical": "Programming Fundamentals",
        "category": "Computer Science",
        "aliases": ["programming fundamentals", "coding basics", "programming basics", "oop", "object oriented programming"],
        "difficulty": 1,
        "avg_weeks_to_learn": 6,
        "prerequisites": [],
        "resources": [
            {"title": "CS50 – Harvard", "url": "https://cs50.harvard.edu/x/", "type": "course"},
        ],
        "related_jobs": ["All Software Roles"],
    },
    "agile": {
        "canonical": "Agile & Scrum",
        "category": "Project Management",
        "aliases": ["scrum", "agile methodology", "sprint", "kanban", "jira"],
        "difficulty": 1,
        "avg_weeks_to_learn": 2,
        "prerequisites": [],
        "resources": [
            {"title": "Scrum Guide", "url": "https://scrumguides.org/scrum-guide.html", "type": "documentation"},
        ],
        "related_jobs": ["All Software Roles"],
    },

    # ─── Security ──────────────────────────────────────────────────────────
    "cybersecurity": {
        "canonical": "Cybersecurity",
        "category": "Security",
        "aliases": ["security", "ethical hacking", "penetration testing", "infosec", "information security", "network security"],
        "difficulty": 4,
        "avg_weeks_to_learn": 20,
        "prerequisites": ["networking_basics", "linux"],
        "resources": [
            {"title": "TryHackMe", "url": "https://tryhackme.com/", "type": "platform"},
            {"title": "HackTheBox", "url": "https://www.hackthebox.com/", "type": "platform"},
        ],
        "related_jobs": ["Security Engineer", "Penetration Tester", "SOC Analyst"],
    },
    "blockchain": {
        "canonical": "Blockchain",
        "category": "Distributed Systems",
        "aliases": ["web3", "solidity", "ethereum", "smart contracts", "defi", "nft"],
        "difficulty": 4,
        "avg_weeks_to_learn": 12,
        "prerequisites": ["programming_basics", "cryptography"],
        "resources": [
            {"title": "CryptoZombies", "url": "https://cryptozombies.io/", "type": "tutorial"},
        ],
        "related_jobs": ["Blockchain Developer", "Web3 Developer"],
    },
    "mlops": {
        "canonical": "MLOps",
        "category": "AI/ML",
        "aliases": ["ml ops", "ml operations", "model deployment", "model monitoring", "feature store"],
        "difficulty": 4,
        "avg_weeks_to_learn": 12,
        "prerequisites": ["machine_learning", "docker", "ci_cd"],
        "resources": [
            {"title": "MLflow Official Docs", "url": "https://mlflow.org/docs/latest/index.html", "type": "documentation"},
            {"title": "Made With ML", "url": "https://madewithml.com/", "type": "course"},
        ],
        "related_jobs": ["MLOps Engineer", "ML Platform Engineer"],
    },
}


def get_all_skill_keys() -> List[str]:
    """Return all canonical skill keys."""
    return list(SKILLS_TAXONOMY.keys())


def get_skill(skill_key: str) -> Dict[str, Any]:
    """Get skill metadata by canonical key."""
    return SKILLS_TAXONOMY.get(skill_key, {})


def build_alias_index() -> Dict[str, str]:
    """Build a reverse lookup: alias → canonical key."""
    index = {}
    for key, meta in SKILLS_TAXONOMY.items():
        # Add the key itself
        index[key.lower()] = key
        index[meta["canonical"].lower()] = key
        for alias in meta.get("aliases", []):
            index[alias.lower()] = key
    return index


ALIAS_INDEX = build_alias_index()
