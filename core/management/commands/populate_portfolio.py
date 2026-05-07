import shutil
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from datetime import date
from core.models import Profile, SocialLink, SkillCategory, Skill, Experience, Education, Project


class Command(BaseCommand):
    help = 'Populates the portfolio with Polaris Pall resume data'

    def handle(self, *args, **options):
        self.stdout.write('Populating portfolio data from resume...')

        # Clear existing data
        Profile.objects.all().delete()
        SocialLink.objects.all().delete()
        SkillCategory.objects.all().delete()
        Skill.objects.all().delete()
        Experience.objects.all().delete()
        Education.objects.all().delete()
        Project.objects.all().delete()

        # Create Profile (from resume header and summary)
        profile = Profile.objects.create(
            name='Polaris Pall',
            title='Full Stack Developer',
            subtitle='Building and deploying web applications across the entire stack',
            bio='''Full stack developer with hands-on experience building and deploying web applications across the entire stack. Proficient in Python, JavaScript/TypeScript, and modern frameworks including Django and React.

Strong background in Linux systems, containerization, and cloud deployment. Passionate about clean code, efficient systems, and creating seamless user experiences.

Currently studying Computer Science and always eager to learn new technologies and tackle challenging problems.''',
            email='polaris@polarispall.com',
            phone='(343) 202 3493',
            location='Canada',
        )

        # Copy and attach resume PDF
        resume_source = Path(settings.BASE_DIR) / 'resume' / 'resume-v2.pdf'
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

        # Create Skill Categories (matching resume sections)
        categories_data = [
            {'name': 'Languages & Runtime', 'slug': 'languages', 'icon': 'fas fa-code', 'order': 1},
            {'name': 'Backend & Frameworks', 'slug': 'backend', 'icon': 'fas fa-server', 'order': 2},
            {'name': 'Databases', 'slug': 'databases', 'icon': 'fas fa-database', 'order': 3},
            {'name': 'DevOps & Infrastructure', 'slug': 'devops', 'icon': 'fas fa-cloud', 'order': 4},
            {'name': 'Linux & Systems', 'slug': 'linux', 'icon': 'fab fa-linux', 'order': 5},
            {'name': 'Frontend', 'slug': 'frontend', 'icon': 'fas fa-palette', 'order': 6},
            {'name': 'Mobile & Game Dev', 'slug': 'mobile-game', 'icon': 'fas fa-gamepad', 'order': 7},
            {'name': 'Tools & Workflow', 'slug': 'tools', 'icon': 'fas fa-tools', 'order': 8},
        ]
        categories = {}
        for cat_data in categories_data:
            cat = SkillCategory.objects.create(**cat_data)
            categories[cat_data['slug']] = cat
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} skill categories'))

        # Create Skills (from resume)
        skills_data = [
            # Languages & Runtime
            {'name': 'Python', 'category': 'languages', 'icon_class': 'fab fa-python', 'url': 'https://python.org', 'glow_color': '#3776AB', 'order': 1},
            {'name': 'JavaScript', 'category': 'languages', 'icon_class': 'fab fa-js', 'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript', 'glow_color': '#F7DF1E', 'order': 2},
            {'name': 'TypeScript', 'category': 'languages', 'icon_class': 'fab fa-js', 'url': 'https://www.typescriptlang.org', 'glow_color': '#3178C6', 'order': 3},
            {'name': 'C#', 'category': 'languages', 'icon_class': 'fas fa-hashtag', 'url': 'https://learn.microsoft.com/en-us/dotnet/csharp/', 'glow_color': '#239120', 'order': 4},
            {'name': 'Java', 'category': 'languages', 'icon_class': 'fab fa-java', 'url': 'https://www.java.com', 'glow_color': '#ED8B00', 'order': 5},
            {'name': 'Bash', 'category': 'languages', 'icon_class': 'fas fa-terminal', 'url': 'https://www.gnu.org/software/bash/', 'glow_color': '#4EAA25', 'order': 6},
            {'name': 'Dart', 'category': 'languages', 'icon_class': 'fas fa-bullseye', 'url': 'https://dart.dev', 'glow_color': '#0175C2', 'order': 7},

            # Backend & Frameworks
            {'name': 'Django', 'category': 'backend', 'icon_class': 'fab fa-python', 'url': 'https://www.djangoproject.com', 'glow_color': '#092E20', 'order': 1},
            {'name': 'REST APIs', 'category': 'backend', 'icon_class': 'fas fa-plug', 'url': 'https://restfulapi.net', 'glow_color': '#00D9FF', 'order': 2},
            {'name': 'Node.js', 'category': 'backend', 'icon_class': 'fab fa-node-js', 'url': 'https://nodejs.org', 'glow_color': '#339933', 'order': 3},
            {'name': '.NET', 'category': 'backend', 'icon_class': 'fab fa-microsoft', 'url': 'https://dotnet.microsoft.com', 'glow_color': '#512BD4', 'order': 4},

            # Databases
            {'name': 'PostgreSQL', 'category': 'databases', 'icon_class': 'fas fa-database', 'url': 'https://www.postgresql.org', 'glow_color': '#336791', 'order': 1},
            {'name': 'MySQL', 'category': 'databases', 'icon_class': 'fas fa-database', 'url': 'https://www.mysql.com', 'glow_color': '#4479A1', 'order': 2},
            {'name': 'SQLite', 'category': 'databases', 'icon_class': 'fas fa-database', 'url': 'https://www.sqlite.org', 'glow_color': '#003B57', 'order': 3},

            # DevOps & Infrastructure
            {'name': 'Docker', 'category': 'devops', 'icon_class': 'fab fa-docker', 'url': 'https://www.docker.com', 'glow_color': '#2496ED', 'order': 1},
            {'name': 'Nginx', 'category': 'devops', 'icon_class': 'fas fa-server', 'url': 'https://nginx.org', 'glow_color': '#009639', 'order': 2},
            {'name': 'AWS', 'category': 'devops', 'icon_class': 'fab fa-aws', 'url': 'https://aws.amazon.com', 'glow_color': '#FF9900', 'order': 3},
            {'name': 'CI/CD', 'category': 'devops', 'icon_class': 'fas fa-sync', 'url': '', 'glow_color': '#9C3EE0', 'order': 4},

            # Linux & Systems
            {'name': 'Linux', 'category': 'linux', 'icon_class': 'fab fa-linux', 'url': 'https://www.linux.org', 'glow_color': '#FCC624', 'order': 1},
            {'name': 'Shell Scripting', 'category': 'linux', 'icon_class': 'fas fa-terminal', 'url': '', 'glow_color': '#4EAA25', 'order': 2},
            {'name': 'Neovim', 'category': 'linux', 'icon_class': 'fas fa-edit', 'url': 'https://neovim.io', 'glow_color': '#57A143', 'order': 3},
            {'name': 'SSH', 'category': 'linux', 'icon_class': 'fas fa-key', 'url': '', 'glow_color': '#000000', 'order': 4},
            {'name': 'Systemd', 'category': 'linux', 'icon_class': 'fas fa-cog', 'url': '', 'glow_color': '#00A98F', 'order': 5},

            # Frontend
            {'name': 'React', 'category': 'frontend', 'icon_class': 'fab fa-react', 'url': 'https://react.dev', 'glow_color': '#61DAFB', 'order': 1},
            {'name': 'Tailwind CSS', 'category': 'frontend', 'icon_class': 'fab fa-css3', 'url': 'https://tailwindcss.com', 'glow_color': '#06B6D4', 'order': 2},
            {'name': 'HTML5', 'category': 'frontend', 'icon_class': 'fab fa-html5', 'url': '', 'glow_color': '#E34F26', 'order': 3},
            {'name': 'CSS3', 'category': 'frontend', 'icon_class': 'fab fa-css3-alt', 'url': '', 'glow_color': '#1572B6', 'order': 4},
            {'name': 'Webflow', 'category': 'frontend', 'icon_class': 'fas fa-palette', 'url': 'https://webflow.com', 'glow_color': '#4353FF', 'order': 5},

            # Mobile & Game Dev
            {'name': 'Flutter', 'category': 'mobile-game', 'icon_class': 'fas fa-mobile-alt', 'url': 'https://flutter.dev', 'glow_color': '#02569B', 'order': 1},
            {'name': 'Unity', 'category': 'mobile-game', 'icon_class': 'fab fa-unity', 'url': 'https://unity.com', 'glow_color': '#FFFFFF', 'order': 2},
            {'name': 'Arduino', 'category': 'mobile-game', 'icon_class': 'fas fa-microchip', 'url': 'https://www.arduino.cc', 'glow_color': '#00979D', 'order': 3},

            # Tools & Workflow
            {'name': 'Git', 'category': 'tools', 'icon_class': 'fab fa-git-alt', 'url': 'https://git-scm.com', 'glow_color': '#F05032', 'order': 1},
            {'name': 'pytest', 'category': 'tools', 'icon_class': 'fas fa-vial', 'url': 'https://pytest.org', 'glow_color': '#0A9ED9', 'order': 2},
            {'name': 'MCP', 'category': 'tools', 'icon_class': 'fas fa-robot', 'url': '', 'glow_color': '#8B5CF6', 'order': 3},
            {'name': 'Zapier', 'category': 'tools', 'icon_class': 'fas fa-bolt', 'url': 'https://zapier.com', 'glow_color': '#FF4A00', 'order': 4},
            {'name': 'Blender', 'category': 'tools', 'icon_class': 'fas fa-cube', 'url': 'https://www.blender.org', 'glow_color': '#F5792A', 'order': 5},
        ]

        skill_objects = {}
        for skill_data in skills_data:
            category_slug = skill_data.pop('category')
            skill_data['use_font_awesome'] = True
            skill = Skill.objects.create(category=categories[category_slug], **skill_data)
            skill_objects[skill.name] = skill
        self.stdout.write(self.style.SUCCESS(f'Created {len(skills_data)} skills'))

        # Create Experience (from resume)
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
            company_url='https://phzio.com',
            is_active=True,
        )

        # Link skills to experience
        exp_skills = ['JavaScript', 'Webflow', 'Zapier']
        for skill_name in exp_skills:
            if skill_name in skill_objects:
                exp.skills.add(skill_objects[skill_name])

        self.stdout.write(self.style.SUCCESS('Created experience entries'))

        # Create Education (from resume)
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

        # Create Projects (from resume)
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
                'custom_technologies': 'EC2, RDS, Elastic Beanstalk',
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
                'custom_technologies': 'Docker Compose, SSL, Cron',
                'skills': ['Linux', 'Nginx', 'Docker', 'SSH'],
                'is_featured': True,
                'is_active': True,
                'order': 3,
            },
        ]

        for project_data in projects_data:
            skills_list = project_data.pop('skills')
            project = Project.objects.create(**project_data)

            for skill_name in skills_list:
                if skill_name in skill_objects:
                    project.skills.add(skill_objects[skill_name])

        self.stdout.write(self.style.SUCCESS(f'Created {len(projects_data)} projects'))

        self.stdout.write(self.style.SUCCESS('\n✓ Portfolio data populated from resume successfully!'))
        self.stdout.write('Visit your site to see the updated portfolio')
