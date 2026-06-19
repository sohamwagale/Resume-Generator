#!/usr/bin/env python3
"""
Test script to verify resume PDF generation works correctly
"""

from app import create_ats_resume

# Sample resume data
sample_data = {
    'full_name': 'Arjun Sharma',
    'job_title': 'Software Engineer',
    'email': 'arjun.sharma@gmail.com',
    'phone': '+91 98765 43210',
    'location': 'Bangalore, Karnataka, India',
    'linkedin': 'linkedin.com/in/arjunsharma',
    'website': 'arjunsharma.dev',
    'leetcode': 'leetcode.com/u/arjun_sharma',
    'summary': (
        'Computer Science graduate with a strong foundation in algorithms, system design, and distributed systems. '
        'Solved 500+ LeetCode problems (Top 5%, Knight badge). Experienced in building high-performance, '
        'fault-tolerant backend systems and scalable full-stack applications. '
        'Interned at a product-based company working on real-world, high-traffic systems. '
        'Passionate about open-source, low-level optimizations, and engineering at scale.'
    ),
    'skills': (
        'Technical Skills: Python, C++, Java, JavaScript (ES6+), TypeScript, Go (Basics), SQL, '
        'Data Structures & Algorithms (Advanced), System Design (LLD + HLD), '
        'React.js, Node.js, Spring Boot, REST APIs, gRPC, GraphQL\n'
        'Databases & Storage: PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, '
        'DynamoDB (Basics), Cassandra (Concepts)\n'
        'DevOps & Cloud: AWS (EC2, S3, Lambda, RDS, SQS, CloudWatch), Docker, Kubernetes (Basics), '
        'Terraform (Basics), CI/CD (GitHub Actions, Jenkins), Linux, Bash Scripting\n'
        'CS Fundamentals: Operating Systems, Computer Networks, DBMS, OOP, '
        'Distributed Systems, Concurrency & Multithreading, Memory Management\n'
        'AI & Tools: OpenAI API, LangChain, Git, Postman, Jira, Figma, IntelliJ, VS Code\n'
        'Soft Skills: First-Principles Thinking, Ownership Mindset, Clear Technical Communication, '
        'Collaborative Problem Solving, Handling Ambiguity, Attention to Scale'
    ),

    # Work Experience
    'experience_count': '2',

    'experience_0_title': 'Software Engineering Intern',
    'experience_0_company': 'Google (via STEP Internship Program), Bangalore',
    'experience_0_dates': 'May 2024 – Aug 2024',
    'experience_0_description': (
        '• Owned and shipped a latency optimization for an internal data pipeline (Google-scale), '
        'reducing P99 latency by 42% using batching and async processing in Go.\n'
        '• Designed and implemented a new caching layer using Redis that cut redundant DB reads by 60% '
        'across 3 downstream services.\n'
        '• Wrote comprehensive unit and integration tests (95%+ coverage) and passed code reviews '
        'with L5/L6 engineers.\n'
        '• Presented findings to a cross-functional team of 15 engineers; solution was adopted into production.'
    ),

    'experience_1_title': 'Backend Engineering Intern',
    'experience_1_company': 'Razorpay, Bangalore',
    'experience_1_dates': 'Nov 2023 – Jan 2024',
    'experience_1_description': (
        '• Built a real-time webhook retry mechanism using AWS SQS + Lambda, handling 1M+ events/day '
        'with 99.98% delivery reliability.\n'
        '• Refactored legacy monolith endpoints into microservices (Spring Boot), cutting response time by 28%.\n'
        '• Identified and fixed a race condition in concurrent payment state updates using optimistic locking; '
        'prevented ~$12K/month in duplicate charge errors.\n'
        '• Wrote runbooks and internal documentation adopted by 4 team members.'
    ),

    # Education
    'education_count': '1',
    'education_0_degree': 'B.Tech in Computer Science and Engineering',
    'education_0_school': 'Indian Institute of Technology (IIT) Bombay',
    'education_0_year': '2021 – 2025',
    'education_0_details': (
        'CGPA: 9.2 / 10 | Dean\'s List (All Semesters) | '
        'Relevant Coursework: Advanced Algorithms, Operating Systems, Distributed Systems, '
        'Database Internals, Computer Architecture, Compiler Design, Computer Networks'
    ),

    # Projects
    'projects': (
        'Distributed Key-Value Store | C++, Raft Consensus, gRPC, Docker | Mar 2025\n'
        '• Built a fault-tolerant, distributed KV store from scratch implementing the Raft consensus algorithm '
        'with leader election, log replication, and snapshotting.\n'
        '• Achieved linearizable reads/writes with <10ms latency under 10K concurrent clients in benchmarks.\n'
        '• Inspired by MIT 6.824 (Distributed Systems); passed all 50 provided test cases including network partitions.\n'
        'GitHub: github.com/arjunsharma/raft-kv-store\n\n'

        'Mini Search Engine | Python, Inverted Index, TF-IDF, FastAPI, React.js | Dec 2024\n'
        '• Designed and built a full-text search engine from scratch with web crawling, '
        'tokenization, inverted indexing, and TF-IDF ranking over 100K+ documents.\n'
        '• Achieved sub-50ms query response time; deployed on AWS EC2 with load balancing.\n'
        'GitHub: github.com/arjunsharma/mini-search-engine\n\n'

        'URL Shortener at Scale | Go, Redis, PostgreSQL, Docker, Kubernetes | Sep 2024\n'
        '• Designed a system capable of handling 100K redirects/second using consistent hashing, '
        'Redis caching, and horizontal scaling via Kubernetes.\n'
        '• Wrote a detailed HLD/LLD document covering capacity estimation, DB sharding, and CDN integration '
        '(received 400+ stars on GitHub).\n'
        'GitHub: github.com/arjunsharma/url-shortener-scale'
    ),

    # Additional Information
    'additional': (
        'Languages: English (Fluent), Hindi (Native), Marathi (Native)\n'
        'Competitive Programming: LeetCode – 500+ solved, Knight Badge, Top 5% globally | '
        'Codeforces – Specialist (1450+) | '
        'Google Kickstart 2024 – Global Rank 312 | '
        'ICPC Regionals 2023 – Qualified & Ranked Top 50 (Asia-West)\n'
        'Certifications: AWS Solutions Architect – Associate (2024), '
        'Meta Backend Developer Certificate (Coursera, 2024)\n'
        'Open Source: Contributor to facebook/react (2 merged PRs – performance fix & docs), '
        'redis/redis (issue triage & fix)\n'
        'Achievements: Smart India Hackathon 2024 – National Winner | '
        'Institute Technical Council – Core Team Lead | '
        'Published research paper on "Optimizing Cold Start Latency in Serverless Architectures" – '
        'IEEE Xplore 2025\n'
        'Interests: Systems Programming, Open Source, Competitive Programming, Tech Writing (Medium – 5K followers)'
    )
}
def test_pdf_generation():
    print("Testing PDF generation...")
    print("-" * 50)
    
    try:
        # Generate PDF
        pdf_buffer = create_ats_resume(sample_data)
        
        # Save to file
        with open('test_resume.pdf', 'wb') as f:
            f.write(pdf_buffer.read())
        
        print("✓ PDF generated successfully!")
        print("✓ Saved to: /home/claude/test_resume.pdf")
        print("-" * 50)
        print("Test Summary:")
        print(f"  - Name: {sample_data['full_name']}")
        print(f"  - Email: {sample_data['email']}")
        print(f"  - Experiences: {sample_data['experience_count']}")
        print(f"  - Education: {sample_data['education_count']}")
        print("-" * 50)
        return True
        
    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_pdf_generation()
    exit(0 if success else 1)