import os
import sys

# Ensure project root is in sys.path when running standalone
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.db_config import get_connection

SAMPLE_JOBS = [
    {
        "title": "Software Engineer",
        "company": "Tata Consultancy Services (TCS)",
        "location": "Bengaluru, Karnataka",
        "job_type": "Full-time",
        "experience_level": "Entry Level",
        "category": "Software Engineering",
        "description": "We are seeking a proactive Software Engineer to join our core development team. You will build and maintain backend web services and collaborate with cross-functional teams to deliver scalable enterprise solutions. Freshers and early career engineers with strong problem-solving abilities are encouraged to apply.",
        "responsibilities": "- Develop high-performance backend modules and REST APIs using Python and Flask.\n- Write clean, maintainable, and well-tested code following industry standards.\n- Manage database schemas, write optimized queries in MySQL, and ensure data integrity.\n- Collaborate with team members using Git for version control and participate in code reviews.",
        "required_skills": "python, flask, mysql, git",
        "preferred_skills": "docker, rest api, linux, agile",
        "salary_lpa": 6.50,
        "salary_range": "₹5 - ₹8 LPA"
    },
    {
        "title": "Frontend Developer",
        "company": "Infosys",
        "location": "Pune, Maharashtra",
        "job_type": "Full-time",
        "experience_level": "Mid Level",
        "category": "Frontend Development",
        "description": "Join our digital experience studio as a Frontend Developer building dynamic and responsive web applications. You will translate wireframes into interactive user interfaces and enhance performance across modern browsers. The ideal candidate has deep expertise in modern JavaScript frameworks.",
        "responsibilities": "- Build reusable UI components and pages using React, JavaScript, HTML, and CSS.\n- Optimize web applications for maximum speed, scalability, and cross-browser responsiveness.\n- Integrate frontend components with backend RESTful APIs and handle asynchronous state management.\n- Work closely with UI/UX designers to translate Figma mockups into pixel-perfect web pages.",
        "required_skills": "react, javascript, html, css",
        "preferred_skills": "typescript, bootstrap, figma, git",
        "salary_lpa": 9.50,
        "salary_range": "₹8 - ₹12 LPA"
    },
    {
        "title": "Data Scientist",
        "company": "Wipro",
        "location": "Hyderabad, Telangana",
        "job_type": "Full-time",
        "experience_level": "Mid Level",
        "category": "Data Science",
        "description": "We are looking for an analytical Data Scientist to unlock valuable insights from large and complex datasets. You will formulate predictive models, conduct exploratory data analysis, and translate business questions into machine learning solutions. This role offers strong opportunities to work with state-of-the-art predictive architectures.",
        "responsibilities": "- Conduct exploratory data analysis and data preprocessing using Python, Pandas, and NumPy.\n- Develop, validate, and tune predictive and classification machine learning models.\n- Build deep learning prototypes using TensorFlow for structured and unstructured data analysis.\n- Present findings and model metrics to business stakeholders through clear visualizations.",
        "required_skills": "python, pandas, numpy, machine learning, tensorflow",
        "preferred_skills": "scikit-learn, sql, tableau, r",
        "salary_lpa": 14.00,
        "salary_range": "₹12 - ₹18 LPA"
    },
    {
        "title": "Full Stack Developer",
        "company": "Flipkart",
        "location": "Bengaluru, Karnataka",
        "job_type": "Full-time",
        "experience_level": "Senior Level",
        "category": "Full Stack Development",
        "description": "Flipkart is seeking a Full Stack Developer to spearhead core product features across both client and server layers. You will drive architecture decisions, build robust backend services, and craft seamless user interfaces. We value engineers with strong end-to-end ownership and passion for high-scale e-commerce systems.",
        "responsibilities": "- Architect and implement end-to-end web features using Python, Flask, React, and MySQL.\n- Design robust database schemas and optimize query execution for high-throughput traffic.\n- Ensure tight integration between frontend state management and backend microservices.\n- Mentor junior developers and enforce rigorous testing and code quality practices.",
        "required_skills": "python, javascript, flask, react, mysql",
        "preferred_skills": "docker, redis, git, microservices",
        "salary_lpa": 18.50,
        "salary_range": "₹16 - ₹24 LPA"
    },
    {
        "title": "DevOps Engineer",
        "company": "Tech Mahindra",
        "location": "Chennai, Tamil Nadu",
        "job_type": "Full-time",
        "experience_level": "Mid Level",
        "category": "DevOps & Cloud",
        "description": "Tech Mahindra is hiring a DevOps Engineer to automate and streamline our operations and processes. You will build and maintain CI/CD pipelines, containerize applications, and manage cloud infrastructure. This role is key to ensuring reliable, zero-downtime application deployments across hybrid environments.",
        "responsibilities": "- Build, maintain, and optimize automated CI/CD deployment pipelines using Jenkins and Git.\n- Containerize multi-tier applications using Docker and support cloud deployments.\n- Provision and monitor scalable cloud infrastructure on AWS.\n- Automate routine server maintenance tasks and configuration scripts with Python.",
        "required_skills": "docker, aws, git, python",
        "preferred_skills": "kubernetes, terraform, linux, jenkins",
        "salary_lpa": 11.00,
        "salary_range": "₹9 - ₹14 LPA"
    },
    {
        "title": "Machine Learning Engineer",
        "company": "Zoho Corporation",
        "location": "Chennai, Tamil Nadu",
        "job_type": "Full-time",
        "experience_level": "Mid Level",
        "category": "Artificial Intelligence",
        "description": "Zoho is seeking an innovative Machine Learning Engineer to design, train, and deploy intelligent algorithms into production SaaS software. You will work on real-time recommendation, NLP, and predictive pipelines. Ideal candidates understand both mathematical foundations and practical deployment engineering.",
        "responsibilities": "- Build, train, and evaluate production-ready machine learning models with scikit-learn and TensorFlow.\n- Develop scalable data pipelines to clean, transform, and aggregate data using Pandas and NumPy.\n- Package models as low-latency microservices with REST endpoints for live product integration.\n- Monitor model drift and continuously retrain models using automated pipelines.",
        "required_skills": "python, tensorflow, scikit-learn, pandas",
        "preferred_skills": "nlp, deep learning, docker, mysql",
        "salary_lpa": 13.50,
        "salary_range": "₹11 - ₹17 LPA"
    },
    {
        "title": "Web Developer",
        "company": "HCL Technologies",
        "location": "Noida, Uttar Pradesh",
        "job_type": "Full-time",
        "experience_level": "Entry Level",
        "category": "Web Development",
        "description": "HCL Technologies is seeking a Web Developer to build, maintain, and enhance corporate client portals and modern web platforms. You will work with clean markup, modular stylesheets, and lightweight backend services. Great career accelerator for enthusiastic developers looking for hands-on web development experience.",
        "responsibilities": "- Develop responsive and mobile-first web pages using HTML, CSS, Bootstrap, and JavaScript.\n- Build simple, lightweight backend routing and form processing handlers with Python and Flask.\n- Perform cross-browser compatibility testing and ensure accessibility compliance.\n- Troubleshoot layout bugs and optimize image and asset loading times.",
        "required_skills": "html, css, javascript, bootstrap, flask",
        "preferred_skills": "python, git, mysql, rest api",
        "salary_lpa": 5.50,
        "salary_range": "₹4.5 - ₹7 LPA"
    },
    {
        "title": "Data Analyst",
        "company": "Swiggy",
        "location": "Bengaluru, Karnataka",
        "job_type": "Full-time",
        "experience_level": "Entry Level",
        "category": "Data & Analytics",
        "description": "Swiggy is looking for a Data Analyst to translate raw operational data into actionable business intelligence. You will partner with operations and marketing teams to evaluate KPIs and spot emerging trends. This role requires sharp analytical curiosity and hands-on proficiency with relational databases and dashboards.",
        "responsibilities": "- Write complex SQL queries to extract, aggregate, and validate metrics from multi-table databases.\n- Clean, manipulate, and analyze structured datasets using Python and Pandas.\n- Build interactive dashboards, visualizations, and tracking reports in Power BI and Excel.\n- Formulate data-driven hypotheses to optimize consumer delivery experiences.",
        "required_skills": "python, sql, excel, power bi, pandas",
        "preferred_skills": "mysql, tableau, statistics, git",
        "salary_lpa": 7.00,
        "salary_range": "₹6 - ₹9 LPA"
    },
    {
        "title": "Cloud Engineer",
        "company": "Larsen & Toubro Infotech (LTIMindtree)",
        "location": "Mumbai, Maharashtra",
        "job_type": "Full-time",
        "experience_level": "Mid Level",
        "category": "DevOps & Cloud",
        "description": "LTIMindtree is hiring a Cloud Engineer to architect, implement, and maintain resilient cloud environments. You will automate workload deployments and configure network security on AWS. Candidates should have a strong grasp of container management and automation scripting.",
        "responsibilities": "- Deploy and administer scalable compute, storage, and networking resources on AWS.\n- Containerize application workloads using Docker and configure local test environments.\n- Write Python automation scripts for cloud backup, metric polling, and resource management.\n- Maintain version control for infrastructure configurations and code using Git.",
        "required_skills": "aws, docker, python, git",
        "preferred_skills": "azure, terraform, linux, kubernetes",
        "salary_lpa": 12.00,
        "salary_range": "₹10 - ₹15 LPA"
    },
    {
        "title": "Backend Developer",
        "company": "Razorpay",
        "location": "Bengaluru, Karnataka",
        "job_type": "Full-time",
        "experience_level": "Mid Level",
        "category": "Backend Development",
        "description": "Razorpay is seeking an experienced Backend Developer to power our financial payment workflows and transaction engines. You will design ultra-reliable APIs that process millions of transactions securely each day. We offer a high-trust, fast-paced environment where your engineering decisions directly impact scale.",
        "responsibilities": "- Build secure, high-throughput RESTful APIs with Python and Flask.\n- Design resilient relational database schemas and optimize complex queries in MySQL.\n- Implement caching, rate limiting, and defensive validation across API endpoints.\n- Collaborate across engineering teams using Git, code reviews, and CI testing.",
        "required_skills": "python, flask, mysql, git",
        "preferred_skills": "redis, rest api, docker, microservices",
        "salary_lpa": 16.00,
        "salary_range": "₹14 - ₹20 LPA"
    },
    {
        "title": "Mobile App Developer",
        "company": "Zomato",
        "location": "Gurugram, Haryana",
        "job_type": "Full-time",
        "experience_level": "Mid Level",
        "category": "Mobile Development",
        "description": "Zomato is seeking a Mobile App Developer to build seamless user journeys on mobile platforms. You will work on cross-platform and native features that delight millions of food lovers every day. We value clean code, buttery 60fps animations, and relentless focus on user delight.",
        "responsibilities": "- Develop and maintain mobile features using React Native and modern JavaScript.\n- Write native bridge components and Android integrations in Java when necessary.\n- Connect mobile client applications with backend REST APIs and secure token handling.\n- Profile mobile memory usage, frame rendering, and optimize offline-first storage.",
        "required_skills": "java, javascript, react native",
        "preferred_skills": "android, ios, git, rest api",
        "salary_lpa": 13.00,
        "salary_range": "₹11 - ₹17 LPA"
    },
    {
        "title": "Database Administrator",
        "company": "Cognizant",
        "location": "Kolkata, West Bengal",
        "job_type": "Full-time",
        "experience_level": "Senior Level",
        "category": "Database & Systems",
        "description": "Cognizant is hiring a Database Administrator to safeguard enterprise data platforms and optimize database performance. You will oversee clustering, backup schedules, database replication, and query performance tuning. Ideal candidate has strong mastery of MySQL and automation scripting.",
        "responsibilities": "- Install, configure, monitor, and patch production MySQL database instances.\n- Analyze slow queries, maintain proper indexes, and tune database configuration parameters.\n- Develop automated database backup, replication, and disaster recovery scripts in Python.\n- Establish user roles, permission policies, and data security compliance measures.",
        "required_skills": "mysql, sql, python",
        "preferred_skills": "postgresql, linux, docker, git",
        "salary_lpa": 12.50,
        "salary_range": "₹10 - ₹16 LPA"
    },
    {
        "title": "QA Engineer",
        "company": "Capgemini",
        "location": "Hyderabad, Telangana",
        "job_type": "Full-time",
        "experience_level": "Entry Level",
        "category": "Quality Assurance",
        "description": "Capgemini is looking for a detail-oriented QA Engineer to validate software quality and execute automated testing suites. You will design test cases, execute regressions, and identify software defects early in the release cycle. A fantastic opportunity to learn automation testing in an enterprise environment.",
        "responsibilities": "- Design and execute automated test scripts for APIs and web apps using Python.\n- Maintain test repositories, branches, and version control using Git.\n- Run test environments in isolated Docker containers for reproducible test suites.\n- Document defect reports and track resolution with engineering development teams.",
        "required_skills": "python, git, docker",
        "preferred_skills": "selenium, jenkins, linux, rest api",
        "salary_lpa": 6.00,
        "salary_range": "₹5 - ₹8 LPA"
    },
    {
        "title": "UI/UX Developer",
        "company": "Freshworks",
        "location": "Chennai, Tamil Nadu",
        "job_type": "Full-time",
        "experience_level": "Mid Level",
        "category": "Frontend Development",
        "description": "Freshworks is looking for a creative UI/UX Developer who bridges the gap between visual design and technical front-end implementation. You will turn wireframes and prototypes into accessible, responsive web interfaces. If you obsess over micro-interactions and clean front-end structure, we want to talk to you.",
        "responsibilities": "- Build responsive, modern interfaces utilizing HTML, CSS, JavaScript, and Bootstrap.\n- Collaborate closely with product design teams to prototype user interfaces in Figma.\n- Implement fluid animations, layout responsiveness, and accessibility guidelines (WCAG).\n- Maintain a cohesive front-end design system across multiple product lines.",
        "required_skills": "html, css, javascript, bootstrap",
        "preferred_skills": "figma, react, git, photoshop",
        "salary_lpa": 8.50,
        "salary_range": "₹7 - ₹11 LPA"
    },
    {
        "title": "Systems Engineer",
        "company": "Persistent Systems",
        "location": "Pune, Maharashtra",
        "job_type": "Full-time",
        "experience_level": "Mid Level",
        "category": "DevOps & Cloud",
        "description": "Persistent Systems is hiring a Systems Engineer to design, deploy, and maintain robust infrastructure systems. You will automate system provisioning, monitor server health, and troubleshoot Linux and cloud environments. This role requires practical scripting proficiency and strong knowledge of containerization.",
        "responsibilities": "- Configure and maintain cloud infrastructure on AWS and virtualized environments.\n- Write Python scripts to automate system health monitoring, backups, and alerting.\n- Deploy containerized services using Docker and manage container lifecycles.\n- Manage code repositories, system configs, and operational runbooks using Git.",
        "required_skills": "python, docker, aws, git",
        "preferred_skills": "linux, bash, kubernetes, nginx",
        "salary_lpa": 9.00,
        "salary_range": "₹7.5 - ₹12 LPA"
    }
]

def seed_jobs():
    """Seeds sample jobs into MySQL database idempotently."""
    print("Connecting to database...")
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return

    try:
        print("Checking existing jobs in database...")
        cursor.execute("SELECT COUNT(*) AS cnt FROM jobs")
        result = cursor.fetchone()
        existing_count = result["cnt"] if result else 0

        if existing_count > 0:
            print(f"Found {existing_count} existing jobs in database.")
            print("Clearing existing jobs to ensure a fresh, consistent seed...")
            # Note: Disable foreign key checks momentarily if saved_jobs or recommendations reference jobs
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("TRUNCATE TABLE recommendations")
            cursor.execute("TRUNCATE TABLE saved_jobs")
            cursor.execute("TRUNCATE TABLE jobs")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            conn.commit()
            print("Existing jobs cleared successfully.")

        print(f"Inserting {len(SAMPLE_JOBS)} sample jobs...")
        insert_query = """
            INSERT INTO jobs (
                title, company, location, job_type, experience_level,
                category, description, responsibilities, required_skills,
                preferred_skills, salary_lpa, salary_range, is_active
            ) VALUES (
                %(title)s, %(company)s, %(location)s, %(job_type)s, %(experience_level)s,
                %(category)s, %(description)s, %(responsibilities)s, %(required_skills)s,
                %(preferred_skills)s, %(salary_lpa)s, %(salary_range)s, 1
            )
        """

        for job in SAMPLE_JOBS:
            cursor.execute(insert_query, job)
            print(f" - Inserted: {job['title']} at {job['company']}")

        conn.commit()
        print(f"\nSuccessfully seeded {len(SAMPLE_JOBS)} jobs into the database!")

    except Exception as e:
        conn.rollback()
        print(f"Error while seeding jobs: {e}")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    seed_jobs()
