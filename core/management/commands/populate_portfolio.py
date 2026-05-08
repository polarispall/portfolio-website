"""
Portfolio Data Population Script
Based on Polaris Pall's resume (v4.1/v4.2)

Run with: uv run python manage.py populate_portfolio
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from datetime import date
from core.models import (
    Profile, SocialLink, SkillCategory, Skill,
    Experience, Education, Project, Certificate
)


class Command(BaseCommand):
    help = 'Populate portfolio with data from resume'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()

        self.stdout.write('Populating portfolio data...')

        self.create_profile()
        self.create_social_links()
        self.create_skill_categories()
        self.create_skills()
        self.create_experience()
        self.create_education()
        self.create_projects()

        self.stdout.write(self.style.SUCCESS('Portfolio data populated successfully!'))

    def clear_data(self):
        """Clear all portfolio data"""
        models = [Certificate, Project, Education, Experience, Skill, SkillCategory, SocialLink, Profile]
        for model in models:
            count = model.objects.count()
            model.objects.all().delete()
            self.stdout.write(f'  Deleted {count} {model.__name__} records')

    def create_profile(self):
        """Create or update the main profile"""
        profile, created = Profile.objects.update_or_create(
            defaults={
                'name': 'Polaris Pall',
                'title': 'Full Stack Developer',
                'subtitle': 'Building and deploying web applications across the entire stack',
                'bio': (
                    "Full stack developer with hands-on experience building and deploying web applications "
                    "across the entire stack. Proficient in Python, JavaScript/TypeScript, and modern "
                    "frameworks including Django and React.\n\n"
                    "Strong background in Linux systems, containerization, and cloud deployment. "
                    "I'm passionate about clean code, efficient systems, and creating seamless user experiences.\n\n"
                    "Currently studying Computer Science and always eager to learn new technologies "
                    "and take on challenging problems."
                ),
                'email': 'polaris@polarispall.com',
                'phone': '(343) 202-3493',
                'location': 'Ontario, Canada',
                'show_calendly_cta': True,
                'show_normal_theme': False,
            }
        )
        action = 'Created' if created else 'Updated'
        self.stdout.write(f'  {action} profile: {profile.name}')
        return profile

    def create_social_links(self):
        """Create social media links"""
        links = [
            {
                'platform': 'GitHub',
                'url': 'https://github.com/polarispall',
                'icon_class': 'fab fa-github',
                'order': 1,
            },
            {
                'platform': 'LinkedIn',
                'url': 'https://linkedin.com/in/polarispall',
                'icon_class': 'fab fa-linkedin',
                'order': 2,
            },
            {
                'platform': 'Email',
                'url': 'mailto:polaris@polarispall.com',
                'icon_class': 'fas fa-envelope',
                'order': 3,
            },
        ]

        for link_data in links:
            link, created = SocialLink.objects.update_or_create(
                platform=link_data['platform'],
                defaults={
                    'url': link_data['url'],
                    'icon_class': link_data['icon_class'],
                    'use_font_awesome': True,
                    'order': link_data['order'],
                    'is_active': True,
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} social link: {link.platform}')

    def create_skill_categories(self):
        """Create skill categories"""
        categories = [
            {'name': 'Languages', 'slug': 'languages', 'icon': 'fas fa-code', 'order': 1},
            {'name': 'Backend & Frameworks', 'slug': 'backend', 'icon': 'fas fa-server', 'order': 2},
            {'name': 'Databases', 'slug': 'databases', 'icon': 'fas fa-database', 'order': 3},
            {'name': 'Frontend', 'slug': 'frontend', 'icon': 'fas fa-palette', 'order': 4},
            {'name': 'DevOps & Infrastructure', 'slug': 'devops', 'icon': 'fas fa-cloud', 'order': 5},
            {'name': 'DevTools', 'slug': 'devtools', 'icon': 'fas fa-terminal', 'order': 6},
            {'name': 'Tools', 'slug': 'tools', 'icon': 'fas fa-wrench', 'order': 7},
        ]

        for cat_data in categories:
            category, created = SkillCategory.objects.update_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'icon': cat_data['icon'],
                    'order': cat_data['order'],
                    'is_active': True,
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} category: {category.name}')

    def create_skills(self):
        """Create skills with proper icons and colors"""
        # Get categories
        categories = {cat.slug: cat for cat in SkillCategory.objects.all()}

        skills_data = [
            # Languages - core programming languages that deserve individual recognition
            {'name': 'Python', 'category': 'languages', 'icon': 'fab fa-python', 'color': '#3776ab', 'url': 'https://python.org', 'order': 1},
            {'name': 'JavaScript', 'category': 'languages', 'icon': 'fab fa-js', 'color': '#f7df1e', 'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript', 'order': 2},
            {'name': 'TypeScript', 'category': 'languages', 'icon': 'fab fa-js', 'color': '#3178c6', 'url': 'https://typescriptlang.org', 'order': 3},
            {'name': 'C#', 'category': 'languages', 'icon': 'fas fa-hashtag', 'color': '#239120', 'url': 'https://docs.microsoft.com/en-us/dotnet/csharp/', 'order': 4},
            {'name': 'Java', 'category': 'languages', 'icon': 'fab fa-java', 'color': '#ed8b00', 'url': 'https://java.com', 'order': 5},
            {'name': 'Bash', 'category': 'languages', 'icon': 'fas fa-terminal', 'color': '#4eaa25', 'url': 'https://www.gnu.org/software/bash/', 'order': 6},

            # Backend & Frameworks - major frameworks people search for
            {'name': 'Django', 'category': 'backend', 'icon': 'fab fa-python', 'color': '#092e20', 'url': 'https://djangoproject.com', 'order': 1},
            {'name': 'Node.js', 'category': 'backend', 'icon': 'fab fa-node-js', 'color': '#339933', 'url': 'https://nodejs.org', 'order': 2},
            {'name': '.NET', 'category': 'backend', 'icon': 'fab fa-microsoft', 'color': '#512bd4', 'url': 'https://dotnet.microsoft.com', 'order': 3},
            {'name': 'Gunicorn', 'category': 'backend', 'icon': 'fab fa-python', 'color': '#499848', 'url': 'https://gunicorn.org', 'order': 4},

            # Databases
            {'name': 'PostgreSQL', 'category': 'databases', 'icon': 'fas fa-database', 'color': '#336791', 'url': 'https://postgresql.org', 'order': 1},
            {'name': 'MySQL', 'category': 'databases', 'icon': 'fas fa-database', 'color': '#4479a1', 'url': 'https://mysql.com', 'order': 2},
            {'name': 'SQLite', 'category': 'databases', 'icon': 'fas fa-database', 'color': '#003b57', 'url': 'https://sqlite.org', 'order': 3},

            # Frontend
            {'name': 'React', 'category': 'frontend', 'icon': 'fab fa-react', 'color': '#61dafb', 'url': 'https://react.dev', 'order': 1},
            {'name': 'Tailwind CSS', 'category': 'frontend', 'icon': 'fab fa-css3-alt', 'color': '#06b6d4', 'url': 'https://tailwindcss.com', 'order': 2},
            {'name': 'HTML', 'category': 'frontend', 'icon': 'fab fa-html5', 'color': '#e34f26', 'url': 'https://developer.mozilla.org/en-US/docs/Web/HTML', 'order': 3},
            {'name': 'CSS', 'category': 'frontend', 'icon': 'fab fa-css3-alt', 'color': '#1572b6', 'url': 'https://developer.mozilla.org/en-US/docs/Web/CSS', 'order': 4},
            {'name': 'Flutter', 'category': 'frontend', 'icon': 'fas fa-mobile-alt', 'color': '#02569B', 'url': 'https://flutter.dev', 'order': 5},
            {'name': 'Webflow', 'category': 'frontend', 'icon': 'fas fa-globe', 'color': '#4353FF', 'url': 'https://webflow.com', 'order': 6},

            # DevOps & Infrastructure
            {'name': 'Docker', 'category': 'devops', 'icon': 'fab fa-docker', 'color': '#2496ed', 'url': 'https://docker.com', 'order': 1},
            {'name': 'AWS', 'category': 'devops', 'icon': 'fab fa-aws', 'color': '#ff9900', 'url': 'https://aws.amazon.com', 'order': 2},
            {'name': 'Nginx', 'category': 'devops', 'icon': 'fas fa-server', 'color': '#009639', 'url': 'https://nginx.org', 'order': 3},
            {'name': 'Linux', 'category': 'devops', 'icon': 'fab fa-linux', 'color': '#fcc624', 'url': 'https://kernel.org', 'order': 4},
            {'name': 'Caddy', 'category': 'devops', 'icon': 'fas fa-shield-alt', 'color': '#00ADD8', 'url': 'https://caddyserver.com', 'order': 5},
            {'name': 'Cloudflare', 'category': 'devops', 'icon': 'fab fa-cloudflare', 'color': '#F38020', 'url': 'https://cloudflare.com', 'order': 6},

            # DevTools - developer-focused tools
            {'name': 'Git', 'category': 'devtools', 'icon': 'fab fa-git-alt', 'color': '#f05032', 'url': 'https://git-scm.com', 'order': 1},
            {'name': 'GitHub', 'category': 'devtools', 'icon': 'fab fa-github', 'color': '#ffffff', 'url': 'https://github.com', 'order': 2},
            {'name': 'Neovim', 'category': 'devtools', 'icon': 'fas fa-edit', 'color': '#57a143', 'url': 'https://neovim.io', 'order': 3},
            {'name': 'pytest', 'category': 'devtools', 'icon': 'fas fa-vial', 'color': '#0A9EDC', 'url': 'https://pytest.org', 'order': 4},
            {'name': 'MCP', 'category': 'devtools', 'icon': 'fas fa-plug', 'color': '#8B5CF6', 'url': 'https://modelcontextprotocol.io', 'order': 5},

            # Tools - creative/productivity tools
            {'name': 'Unity', 'category': 'tools', 'icon': 'fab fa-unity', 'color': '#ffffff', 'url': 'https://unity.com', 'order': 1},
            {'name': 'Blender', 'category': 'tools', 'icon': 'fas fa-cube', 'color': '#F5792A', 'url': 'https://blender.org', 'order': 2},
            {'name': 'Zapier', 'category': 'tools', 'icon': 'fas fa-bolt', 'color': '#FF4A00', 'url': 'https://zapier.com', 'order': 3},
        ]

        for skill_data in skills_data:
            category = categories.get(skill_data['category'])
            if not category:
                self.stdout.write(self.style.WARNING(f'  Category not found: {skill_data["category"]}'))
                continue

            skill, created = Skill.objects.update_or_create(
                name=skill_data['name'],
                category=category,
                defaults={
                    'icon_class': skill_data['icon'],
                    'glow_color': skill_data['color'],
                    'url': skill_data.get('url', ''),
                    'use_font_awesome': True,
                    'order': skill_data['order'],
                    'is_active': True,
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} skill: {skill.name}')

    def create_experience(self):
        """Create work experience"""
        # Get skills for linking
        skills = {s.name: s for s in Skill.objects.all()}

        experiences = [
            {
                'company': 'Phzio',
                'position': 'Frontend Developer',
                'work_type': 'remote',
                'start_date': date(2025, 1, 1),
                'is_current': True,
                'description': (
                    "• Built and maintained UI components for healthcare platform using Webflow\n"
                    "• Automated internal workflows and integrations using Zapier for operational efficiency\n"
                    "• Collaborated with development team on feature implementation and design feedback"
                ),
                'skills': ['JavaScript', 'HTML', 'CSS', 'Webflow', 'Zapier'],
                'custom_technologies': '',
                'company_url': 'https://phzio.com',
            },
        ]

        for exp_data in experiences:
            exp, created = Experience.objects.update_or_create(
                company=exp_data['company'],
                position=exp_data['position'],
                defaults={
                    'work_type': exp_data['work_type'],
                    'work_type_visible': True,
                    'start_date': exp_data['start_date'],
                    'end_date': exp_data.get('end_date'),
                    'is_current': exp_data.get('is_current', False),
                    'description': exp_data['description'],
                    'custom_technologies': exp_data.get('custom_technologies', ''),
                    'company_url': exp_data.get('company_url', ''),
                    'is_active': True,
                }
            )

            # Link skills
            exp.skills.clear()
            for skill_name in exp_data.get('skills', []):
                if skill_name in skills:
                    exp.skills.add(skills[skill_name])

            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} experience: {exp.position} at {exp.company}')

    def create_education(self):
        """Create education entries - kept ambiguous as requested"""
        education_data = [
            {
                'degree': '',  # Intentionally blank
                'field_of_study': 'Computer Science',
                'institution': '',  # Intentionally ambiguous
                'start_date': date(2023, 9, 1),
                'is_current': True,
                'description': 'Currently studying Computer Science with focus on software development and systems.',
            },
        ]

        for edu_data in education_data:
            edu, created = Education.objects.update_or_create(
                field_of_study=edu_data['field_of_study'],
                start_date=edu_data['start_date'],
                defaults={
                    'degree': edu_data.get('degree', ''),
                    'institution': edu_data.get('institution', ''),
                    'end_date': edu_data.get('end_date'),
                    'is_current': edu_data.get('is_current', False),
                    'description': edu_data.get('description', ''),
                    'is_active': True,
                }
            )
            action = 'Created' if created else 'Updated'
            display_name = edu_data['field_of_study'] or edu_data['degree'] or 'Education'
            self.stdout.write(f'  {action} education: {display_name}')

    def create_projects(self):
        """Create project entries"""
        skills = {s.name: s for s in Skill.objects.all()}

        projects = [
            {
                'title': 'Portfolio Website',
                'slug': 'portfolio-website',
                'short_description': 'Full-stack portfolio with Django admin and Docker deployment',
                'description': (
                    "Built a full-stack portfolio website showcasing projects and technical work. "
                    "Designed modular Django architecture with content-driven models allowing editorial "
                    "updates through Django admin without template changes.\n\n"
                    "Containerized application using Docker and Docker Compose for local development and "
                    "production parity. Deployed to AWS EC2 running Debian with Caddy reverse proxy for "
                    "automatic HTTPS and Let's Encrypt certificate renewal.\n\n"
                    "Configured Cloudflare for DNS management. Used Gunicorn as application server."
                ),
                'skills': ['Django', 'Docker', 'AWS', 'SQLite', 'Python', 'HTML', 'CSS', 'Caddy', 'Gunicorn', 'Cloudflare'],
                'custom_technologies': '',
                'live_url': 'https://polarispall.com',
                'github_url': 'https://github.com/polarispall/portfolio',
                'is_featured': True,
                'order': 1,
            },
            {
                'title': 'Game Development',
                'slug': 'game-development',
                'short_description': '2D platformer games with procedural generation',
                'description': (
                    "Built 2D platformer games with procedural generation for dynamic level creation. "
                    "Implemented core gameplay systems including physics integration (gravity, collision "
                    "detection, rigidbody dynamics), player input handling, and game state management.\n\n"
                    "Designed game architecture using component-based patterns to organize code and systems. "
                    "Optimized rendering and memory usage for consistent performance. Integrated animation "
                    "systems and audio playback."
                ),
                'skills': ['C#', 'Unity'],
                'custom_technologies': 'Game Physics, Procedural Generation',
                'is_featured': True,
                'order': 2,
            },
            {
                'title': 'Homelab Infrastructure',
                'slug': 'homelab-infrastructure',
                'short_description': 'Personal server infrastructure with containerized applications',
                'description': (
                    "Built and maintain personal server infrastructure running multiple containerized "
                    "applications. Designed Docker images and Docker Compose for service orchestration.\n\n"
                    "Configured Nginx reverse proxy for routing and SSL/TLS termination. Created systemd "
                    "service units for application lifecycle management and automatic startup on boot.\n\n"
                    "Implemented firewall rules with ufw for network security. Automated system maintenance "
                    "using cron jobs for backups and log rotation."
                ),
                'skills': ['Linux', 'Docker', 'Nginx', 'Bash', 'SQLite'],
                'custom_technologies': 'systemd, ufw, cron',
                'is_featured': True,
                'order': 3,
            },
        ]

        for proj_data in projects:
            proj, created = Project.objects.update_or_create(
                slug=proj_data['slug'],
                defaults={
                    'title': proj_data['title'],
                    'short_description': proj_data['short_description'],
                    'description': proj_data['description'],
                    'custom_technologies': proj_data.get('custom_technologies', ''),
                    'live_url': proj_data.get('live_url', ''),
                    'github_url': proj_data.get('github_url', ''),
                    'is_featured': proj_data.get('is_featured', False),
                    'is_active': True,
                    'order': proj_data.get('order', 0),
                }
            )

            # Link skills
            proj.skills.clear()
            for skill_name in proj_data.get('skills', []):
                if skill_name in skills:
                    proj.skills.add(skills[skill_name])

            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} project: {proj.title}')
