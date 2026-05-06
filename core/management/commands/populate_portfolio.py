import shutil
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from datetime import date
from core.models import Profile, SocialLink, SkillCategory, Skill, Experience, Education, Project


class Command(BaseCommand):
    help = 'Populates the portfolio with Polaris Pall data'

    def handle(self, *args, **options):
        self.stdout.write('Populating portfolio data...')

        # Clear existing data
        Profile.objects.all().delete()
        SocialLink.objects.all().delete()
        Skill.objects.all().delete()
        Experience.objects.all().delete()
        Education.objects.all().delete()
        Project.objects.all().delete()

        # Create Profile
        profile = Profile.objects.create(
            name='Polaris Pall',
            title='Full Stack Developer',
            subtitle='Building and deploying web applications across the entire stack',
            bio='''Full stack developer with hands-on experience building and deploying web applications across the entire stack. Proficient in Python, JavaScript/TypeScript, and modern frameworks including Django and React.

Strong background in Linux systems, containerization, and cloud deployment. I'm passionate about clean code, efficient systems, and creating seamless user experiences.

Currently studying Computer Science and always eager to learn new technologies and tackle challenging problems.''',
            email='pallpolaris@gmail.com',
            phone='+1 343 202 3493',
            location='Canada',
        )

        # Copy and attach resume PDF
        resume_source = Path('/home/polaris/EternalSync/documents/work/resumes/resume-v7.pdf')
        if resume_source.exists():
            resume_dir = settings.MEDIA_ROOT / 'resume'
            resume_dir.mkdir(parents=True, exist_ok=True)
            resume_dest = resume_dir / 'polaris-pall-resume.pdf'
            shutil.copy2(resume_source, resume_dest)
            profile.resume.name = 'resume/polaris-pall-resume.pdf'
            profile.save()
            self.stdout.write(self.style.SUCCESS(f'Copied resume to {resume_dest}'))
        else:
            self.stdout.write(self.style.WARNING(f'Resume not found at {resume_source}'))

        self.stdout.write(self.style.SUCCESS(f'Created profile: {profile.name}'))

        # Create Social Links
        social_links = [
            {'platform': 'GitHub', 'url': 'https://github.com/polarispall', 'icon_class': 'fab fa-github', 'use_font_awesome': True, 'order': 1},
        ]
        for link in social_links:
            SocialLink.objects.create(**link)
        self.stdout.write(self.style.SUCCESS(f'Created {len(social_links)} social links'))

        # Create Skill Categories
        categories_data = [
            {'name': 'Languages', 'slug': 'languages', 'icon': 'fas fa-code', 'order': 1},
            {'name': 'Frameworks', 'slug': 'frameworks', 'icon': 'fas fa-layer-group', 'order': 2},
            {'name': 'Databases', 'slug': 'databases', 'icon': 'fas fa-database', 'order': 3},
            {'name': 'DevTools', 'slug': 'devtools', 'icon': 'fas fa-terminal', 'order': 4},
            {'name': 'Tools', 'slug': 'tools', 'icon': 'fas fa-tools', 'order': 5},
            {'name': 'Cloud & DevOps', 'slug': 'cloud-devops', 'icon': 'fas fa-cloud', 'order': 6},
        ]
        categories = {}
        for cat_data in categories_data:
            cat, _ = SkillCategory.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)
            categories[cat_data['slug']] = cat
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} skill categories'))

        # Create Skills with proper icons and brand colors
        skills_data = [
            # Languages - Blue tones
            {'name': 'Python', 'category': 'languages', 'icon_class': 'fab fa-python', 'use_font_awesome': True, 'url': 'https://python.org', 'glow_color': '#FFD700', 'order': 1},
            {'name': 'JavaScript', 'category': 'languages', 'icon_class': 'fab fa-js', 'use_font_awesome': True, 'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript', 'glow_color': '#F7DF1E', 'order': 2},
            {'name': 'TypeScript', 'category': 'languages', 'icon_class': 'fab fa-js', 'use_font_awesome': True, 'url': 'https://www.typescriptlang.org', 'glow_color': '#3178C6', 'order': 3},
            {'name': 'C#', 'category': 'languages', 'icon_class': 'fab fa-windows', 'use_font_awesome': True, 'url': 'https://learn.microsoft.com/en-us/dotnet/csharp/', 'glow_color': '#239120', 'order': 4},
            {'name': 'Java', 'category': 'languages', 'icon_class': 'fab fa-java', 'use_font_awesome': True, 'url': 'https://www.java.com', 'glow_color': '#ED8B00', 'order': 5},

            # Frameworks - Cyan/Green tones
            {'name': 'Django', 'category': 'frameworks', 'icon_class': 'fab fa-python', 'use_font_awesome': True, 'url': 'https://www.djangoproject.com', 'glow_color': '#092E20', 'order': 1},
            {'name': 'React', 'category': 'frameworks', 'icon_class': 'fab fa-react', 'use_font_awesome': True, 'url': 'https://react.dev', 'glow_color': '#61DAFB', 'order': 2},
            {'name': 'Tailwind CSS', 'category': 'frameworks', 'icon_class': 'fab fa-css3', 'use_font_awesome': True, 'url': 'https://tailwindcss.com', 'glow_color': '#06B6D4', 'order': 3},
            {'name': 'Flutter', 'category': 'frameworks', 'icon_class': 'fab fa-flutter', 'use_font_awesome': True, 'url': 'https://flutter.dev', 'glow_color': '#02569B', 'order': 4},
            {'name': 'Webflow', 'category': 'frameworks', 'icon_class': 'fas fa-palette', 'use_font_awesome': True, 'url': 'https://webflow.com', 'glow_color': '#4353FF', 'order': 5},
            {'name': 'REST APIs', 'category': 'frameworks', 'icon_class': 'fas fa-plug', 'use_font_awesome': True, 'url': 'https://restfulapi.net', 'glow_color': '#00D9FF', 'order': 6},

            # Databases - Green tones
            {'name': 'PostgreSQL', 'category': 'databases', 'icon_class': 'fas fa-database', 'use_font_awesome': True, 'url': 'https://www.postgresql.org', 'glow_color': '#336791', 'order': 1},
            {'name': 'MySQL', 'category': 'databases', 'icon_class': 'fas fa-database', 'use_font_awesome': True, 'url': 'https://www.mysql.com', 'glow_color': '#00758F', 'order': 2},
            {'name': 'SQLite', 'category': 'databases', 'icon_class': 'fas fa-database', 'use_font_awesome': True, 'url': 'https://www.sqlite.org', 'glow_color': '#003B57', 'order': 3},

            # DevTools - Purple tones
            {'name': 'Git', 'category': 'devtools', 'icon_class': 'fab fa-git-alt', 'use_font_awesome': True, 'url': 'https://git-scm.com', 'glow_color': '#F1502F', 'order': 1},
            {'name': 'Neovim', 'category': 'devtools', 'icon_class': 'fas fa-terminal', 'use_font_awesome': True, 'url': 'https://neovim.io', 'glow_color': '#57CB86', 'order': 2},
            {'name': 'Pytest', 'category': 'devtools', 'icon_class': 'fas fa-vial', 'use_font_awesome': True, 'url': 'https://pytest.org', 'glow_color': '#0A9ED9', 'order': 3},
            {'name': 'Zapier', 'category': 'tools', 'icon_class': 'fas fa-zap', 'use_font_awesome': True, 'url': 'https://zapier.com', 'glow_color': '#FF5C35', 'order': 4},
            {'name': 'Unity', 'category': 'tools', 'icon_class': 'fab fa-unity', 'use_font_awesome': True, 'url': 'https://unity.com', 'glow_color': '#FFFFFF', 'order': 5},

            # Cloud & DevOps - Red/Warm tones
            {'name': 'Docker', 'category': 'cloud-devops', 'icon_class': 'fab fa-docker', 'use_font_awesome': True, 'url': 'https://www.docker.com', 'glow_color': '#2496ED', 'order': 1},
            {'name': 'AWS', 'category': 'cloud-devops', 'icon_class': 'fab fa-aws', 'use_font_awesome': True, 'url': 'https://aws.amazon.com', 'glow_color': '#FF9900', 'order': 2},
            {'name': 'Nginx', 'category': 'cloud-devops', 'icon_class': 'fas fa-server', 'use_font_awesome': True, 'url': 'https://nginx.org', 'glow_color': '#009639', 'order': 3},
            {'name': 'Linux', 'category': 'cloud-devops', 'icon_class': 'fab fa-linux', 'use_font_awesome': True, 'url': 'https://www.linux.org', 'glow_color': '#FCC624', 'order': 4},
            {'name': 'CI/CD', 'category': 'cloud-devops', 'icon_class': 'fas fa-sync', 'use_font_awesome': True, 'url': 'https://en.wikipedia.org/wiki/CI/CD', 'glow_color': '#9C3EE0', 'order': 5},
        ]
        for skill in skills_data:
            category_slug = skill.pop('category')
            Skill.objects.create(category=categories[category_slug], **skill)
        self.stdout.write(self.style.SUCCESS(f'Created {len(skills_data)} skills'))

        # Create Experience
        exp = Experience.objects.create(
            company='Phzio',
            position='Frontend Developer',
            work_type='remote',
            work_type_visible=True,
            start_date=date(2025, 1, 1),
            end_date=None,
            is_current=True,
            description='''• Contributed to frontend development for a healthcare platform using Webflow
• Built and maintained UI components using modern JavaScript practices
• Automated internal workflows and integrations using Zapier
• Collaborated with the development team to implement new features''',
            custom_technologies='HTML, CSS',
            company_url='https://phzio.com',
            is_active=True,
        )

        # Link skills to experience
        webflow_skill = Skill.objects.filter(name='Webflow').first()
        javascript_skill = Skill.objects.filter(name='JavaScript').first()
        zapier_skill = Skill.objects.filter(name='Zapier').first()

        if webflow_skill:
            exp.skills.add(webflow_skill)
        if javascript_skill:
            exp.skills.add(javascript_skill)
        if zapier_skill:
            exp.skills.add(zapier_skill)

        self.stdout.write(self.style.SUCCESS('Created experience entries'))

        # Create Education
        Education.objects.create(
            institution='',
            degree='Computer Science',
            field_of_study='',
            start_date=date(2024, 9, 1),
            end_date=None,
            is_current=True,
            description='Currently studying Computer Science with focus on software development, algorithms, and systems programming.',
            is_active=True,
        )
        self.stdout.write(self.style.SUCCESS('Created education entries'))

        # Create Projects
        projects_data = [
            {
                'title': 'Ski Resort Booking System',
                'slug': 'ski-resort-booking',
                'short_description': 'Full-stack booking application for managing room reservations and appointments',
                'description': '''Developed a comprehensive booking system for a ski resort, handling room reservations and appointment scheduling.

Key features:
• User authentication using Django's built-in auth system
• Admin panel for managing bookings, rooms, and availability
• Optimized PostgreSQL database schema for efficient queries
• Deployed to AWS using EC2, Elastic Beanstalk, and RDS''',
                'custom_technologies': 'EC2, RDS',
                'skills': ['Django', 'PostgreSQL', 'Tailwind CSS', 'AWS'],
                'is_featured': True,
                'is_active': True,
                'order': 1,
            },
            {
                'title': 'Game Development Projects',
                'slug': 'game-development',
                'short_description': '2D platformers and games featuring procedural generation built with Unity',
                'description': '''Built various 2D games using Unity and C#, focusing on procedural generation and engaging gameplay mechanics.

Key features:
• Procedural level generation for infinite replayability
• Custom physics and player interaction systems
• Game mechanics including combat, movement, and puzzle elements
• Optimized performance for smooth gameplay''',
                'custom_technologies': 'Game Design, Procedural Generation',
                'skills': ['Unity', 'C#'],
                'is_featured': True,
                'is_active': True,
                'order': 2,
            },
            {
                'title': 'Homelab Infrastructure',
                'slug': 'homelab-infrastructure',
                'short_description': 'Personal server infrastructure with containerized services and automation',
                'description': '''Configured and maintain personal server infrastructure for development and self-hosted services.

Key features:
• Nginx reverse proxy with SSL certificates for secure access
• Containerized services using Docker and Docker Compose
• System automation with shell scripts and cron jobs
• SSH-based remote management and monitoring''',
                'custom_technologies': 'SSH, Systemd',
                'skills': ['Linux', 'Nginx', 'Docker'],
                'is_featured': True,
                'is_active': True,
                'order': 3,
            },
        ]
        for project_data in projects_data:
            skills = project_data.pop('skills')
            project = Project.objects.create(**project_data)

            # Link skills to project
            for skill_name in skills:
                skill = Skill.objects.filter(name=skill_name).first()
                if skill:
                    project.skills.add(skill)
        self.stdout.write(self.style.SUCCESS(f'Created {len(projects_data)} projects'))

        self.stdout.write(self.style.SUCCESS('\nPortfolio data populated successfully!'))
        self.stdout.write('Run the server and visit http://127.0.0.1:8000/ to see your portfolio')
