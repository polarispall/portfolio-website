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

        # Skills with Font Awesome icons
        fa_skills = [
            # Languages
            {'name': 'Python', 'category': 'languages', 'icon': 'fab fa-python', 'color': '#4584b6', 'url': 'https://python.org', 'order': 1},
            {'name': 'JavaScript', 'category': 'languages', 'icon': 'fab fa-js', 'color': '#f7df1e', 'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript', 'order': 2},
            {'name': 'C#', 'category': 'languages', 'icon': 'fas fa-hashtag', 'color': '#9b4993', 'url': 'https://docs.microsoft.com/en-us/dotnet/csharp/', 'order': 4},
            {'name': 'Java', 'category': 'languages', 'icon': 'fab fa-java', 'color': '#f89820', 'url': 'https://java.com', 'order': 5},
            {'name': 'Bash', 'category': 'languages', 'icon': 'fas fa-terminal', 'color': '#4eaa25', 'url': 'https://www.gnu.org/software/bash/', 'order': 6},

            # Backend & Frameworks
            {'name': 'Node.js', 'category': 'backend', 'icon': 'fab fa-node-js', 'color': '#68a063', 'url': 'https://nodejs.org', 'order': 2},

            # Frontend
            {'name': 'React', 'category': 'frontend', 'icon': 'fab fa-react', 'color': '#61dafb', 'url': 'https://react.dev', 'order': 1},
            {'name': 'HTML', 'category': 'frontend', 'icon': 'fab fa-html5', 'color': '#e34f26', 'url': 'https://developer.mozilla.org/en-US/docs/Web/HTML', 'order': 3},
            {'name': 'CSS', 'category': 'frontend', 'icon': 'fab fa-css3-alt', 'color': '#264de4', 'url': 'https://developer.mozilla.org/en-US/docs/Web/CSS', 'order': 4},
            {'name': 'Flutter', 'category': 'frontend', 'icon': 'fab fa-flutter', 'color': '#54c5f8', 'url': 'https://flutter.dev', 'order': 5},

            # DevOps & Infrastructure
            {'name': 'Docker', 'category': 'devops', 'icon': 'fab fa-docker', 'color': '#2496ed', 'url': 'https://docker.com', 'order': 1},
            {'name': 'AWS', 'category': 'devops', 'icon': 'fab fa-aws', 'color': '#ff9900', 'url': 'https://aws.amazon.com', 'order': 2},
            {'name': 'Nginx', 'category': 'devops', 'icon': 'fas fa-server', 'color': '#009639', 'url': 'https://nginx.org', 'order': 3},
            {'name': 'Linux', 'category': 'devops', 'icon': 'fab fa-linux', 'color': '#fcc624', 'url': 'https://kernel.org', 'order': 4},
            {'name': 'Cloudflare', 'category': 'devops', 'icon': 'fab fa-cloudflare', 'color': '#f38020', 'url': 'https://cloudflare.com', 'order': 6},

            # DevTools
            {'name': 'Git', 'category': 'devtools', 'icon': 'fab fa-git-alt', 'color': '#f05032', 'url': 'https://git-scm.com', 'order': 1},
            {'name': 'GitHub', 'category': 'devtools', 'icon': 'fab fa-github', 'color': '#6e5494', 'url': 'https://github.com', 'order': 2},
            {'name': 'MCP', 'category': 'devtools', 'icon': 'fas fa-plug', 'color': '#d97706', 'url': 'https://modelcontextprotocol.io', 'order': 5},

            # Tools
            {'name': 'Unity', 'category': 'tools', 'icon': 'fab fa-unity', 'color': '#96a7b8', 'url': 'https://unity.com', 'order': 1},
            {'name': 'Zapier', 'category': 'tools', 'icon': 'fas fa-bolt', 'color': '#ff4a00', 'url': 'https://zapier.com', 'order': 3},
        ]

        # Skills with custom SVG icons (from Simple Icons)
        custom_skills = [
            # Languages
            {'name': 'TypeScript', 'category': 'languages', 'icon_file': 'skill_icons/typescript.svg', 'color': '#3178c6', 'url': 'https://typescriptlang.org', 'order': 3},

            # Backend & Frameworks
            {'name': 'Django', 'category': 'backend', 'icon_file': 'skill_icons/django.svg', 'color': '#44b78b', 'url': 'https://djangoproject.com', 'order': 1},
            {'name': '.NET', 'category': 'backend', 'icon_file': 'skill_icons/dotnet.svg', 'color': '#512bd4', 'url': 'https://dotnet.microsoft.com', 'order': 3},
            {'name': 'Gunicorn', 'category': 'backend', 'icon_file': 'skill_icons/gunicorn.svg', 'color': '#499848', 'url': 'https://gunicorn.org', 'order': 4},

            # Databases
            {'name': 'PostgreSQL', 'category': 'databases', 'icon_file': 'skill_icons/postgresql.svg', 'color': '#4169e1', 'url': 'https://postgresql.org', 'order': 1},
            {'name': 'MySQL', 'category': 'databases', 'icon_file': 'skill_icons/mysql.svg', 'color': '#00758f', 'url': 'https://mysql.com', 'order': 2},
            {'name': 'SQLite', 'category': 'databases', 'icon_file': 'skill_icons/sqlite.svg', 'color': '#0ea5e9', 'url': 'https://sqlite.org', 'order': 3},

            # Frontend
            {'name': 'Tailwind CSS', 'category': 'frontend', 'icon_file': 'skill_icons/tailwindcss.svg', 'color': '#38bdf8', 'url': 'https://tailwindcss.com', 'order': 2},
            {'name': 'Webflow', 'category': 'frontend', 'icon_file': 'skill_icons/webflow.svg', 'color': '#4353ff', 'url': 'https://webflow.com', 'order': 6},

            # DevOps & Infrastructure
            {'name': 'Caddy', 'category': 'devops', 'icon_file': 'skill_icons/caddy.svg', 'color': '#22d3ee', 'url': 'https://caddyserver.com', 'order': 5},

            # DevTools
            {'name': 'Neovim', 'category': 'devtools', 'icon_file': 'skill_icons/neovim.svg', 'color': '#57a143', 'url': 'https://neovim.io', 'order': 3},
            {'name': 'pytest', 'category': 'devtools', 'icon_file': 'skill_icons/pytest.svg', 'color': '#009fe3', 'url': 'https://pytest.org', 'order': 4},

            # Tools
            {'name': 'Blender', 'category': 'tools', 'icon_file': 'skill_icons/blender.svg', 'color': '#ea7600', 'url': 'https://blender.org', 'order': 2},
        ]

        # Create Font Awesome skills
        for skill_data in fa_skills:
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
                    'custom_icon': '',
                    'order': skill_data['order'],
                    'is_active': True,
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} skill: {skill.name}')

        # Create custom icon skills
        for skill_data in custom_skills:
            category = categories.get(skill_data['category'])
            if not category:
                self.stdout.write(self.style.WARNING(f'  Category not found: {skill_data["category"]}'))
                continue

            skill, created = Skill.objects.update_or_create(
                name=skill_data['name'],
                category=category,
                defaults={
                    'icon_class': '',
                    'glow_color': skill_data['color'],
                    'url': skill_data.get('url', ''),
                    'use_font_awesome': False,
                    'custom_icon': skill_data['icon_file'],
                    'order': skill_data['order'],
                    'is_active': True,
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} skill: {skill.name} (custom icon)')

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
                    "## Project Overview\n\n"
                    "This portfolio website represents the culmination of my full-stack development journey, "
                    "built from the ground up using Django as the backend framework. The project showcases "
                    "not just my work, but demonstrates practical implementation of modern web development "
                    "practices, from database design to production deployment.\n\n"

                    "## Architecture & Design Philosophy\n\n"
                    "The core philosophy behind this project was to create a completely content-driven "
                    "architecture where every piece of content - from skills and projects to experience "
                    "entries - lives in the database rather than being hardcoded in templates. This means "
                    "I can update my entire portfolio through Django's admin interface without touching "
                    "a single line of code.\n\n"

                    "I designed the data models with flexibility in mind. The Skill model, for example, "
                    "supports custom SVG icons, Font Awesome classes, glow colors for visual effects, "
                    "and even links to external documentation. Projects can reference skills through "
                    "many-to-many relationships, automatically displaying the appropriate icons and "
                    "creating a cohesive visual language across the site.\n\n"

                    "## Technical Implementation\n\n"
                    "### Backend Development\n"
                    "The Django application follows a modular structure with a single 'core' app handling "
                    "all portfolio-related models: Profile, Skill, SkillCategory, Experience, Education, "
                    "Project, Section, SocialLink, and SiteSettings. Each model is carefully designed with "
                    "appropriate field types, validators, and help text for the admin interface.\n\n"

                    "I implemented custom model methods for computed properties, such as generating "
                    "technology displays that combine linked skills with custom technologies. The ordering "
                    "system uses django-ordered-model for drag-and-drop reordering in the admin.\n\n"

                    "### Frontend Development\n"
                    "The frontend uses semantic HTML5 with a custom CSS architecture. I built a comprehensive "
                    "design system with CSS custom properties for theming, supporting both dark and light "
                    "modes with smooth transitions. The responsive design handles everything from mobile "
                    "(375px) to large desktop displays without breakpoint issues.\n\n"

                    "JavaScript handles interactive elements: the typing animation on the hero section, "
                    "smooth scrolling navigation, theme toggling with localStorage persistence, and the "
                    "mobile hamburger menu. I kept dependencies minimal - no jQuery, no CSS frameworks.\n\n"

                    "### Containerization & DevOps\n"
                    "Docker plays a central role in both development and production. The multi-stage "
                    "Dockerfile creates optimized production images, while docker-compose.yml defines "
                    "the complete application stack. I use volume mounts for persistent data (SQLite "
                    "database, media uploads) and environment variables for configuration.\n\n"

                    "## Production Deployment\n\n"
                    "The production environment runs on an AWS EC2 instance with Debian. I chose Caddy "
                    "as the reverse proxy for its automatic HTTPS capabilities - it handles Let's Encrypt "
                    "certificate issuance and renewal without any manual intervention.\n\n"

                    "The deployment architecture:\n"
                    "- Cloudflare handles DNS and provides an additional security/caching layer\n"
                    "- Caddy reverse proxy manages SSL termination and routes requests\n"
                    "- Gunicorn serves the Django application with multiple workers\n"
                    "- Docker containers ensure consistent environments\n"
                    "- SQLite provides simple, file-based persistence perfect for a portfolio site\n\n"

                    "## Challenges & Solutions\n\n"
                    "One interesting challenge was implementing the theme system. I needed colors to "
                    "work across both themes while maintaining accessibility. The solution involved "
                    "CSS custom properties that change based on a data-theme attribute, with JavaScript "
                    "handling the toggle and persistence.\n\n"

                    "Another challenge was the navigation responsiveness. With seven navigation items "
                    "plus a theme toggle, the horizontal nav overflowed on tablet-sized screens. I solved "
                    "this by implementing a hamburger menu that activates at 1100px, with careful attention "
                    "to the slide-out animation and proper z-index stacking.\n\n"

                    "## Lessons Learned\n\n"
                    "Building this portfolio reinforced the value of planning data models before writing "
                    "any frontend code. The time invested in designing flexible models paid dividends when "
                    "I could add new sections or modify content without template changes.\n\n"

                    "I also gained deeper appreciation for CSS architecture. Starting with a solid foundation "
                    "of custom properties and consistent naming conventions made the responsive design work "
                    "much smoother than previous projects where I'd added styles ad-hoc."
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
                    "## Introduction to Game Development\n\n"
                    "My journey into game development began with a simple question: how do games actually "
                    "work under the hood? This curiosity led me down a fascinating path of learning Unity, "
                    "C#, and the fundamental principles that make interactive entertainment possible. What "
                    "started as experimentation evolved into building complete 2D platformer games with "
                    "procedurally generated levels.\n\n"

                    "## Why Unity and C#?\n\n"
                    "I chose Unity for several reasons. Its component-based architecture teaches good "
                    "software design patterns that transfer to other domains. The visual editor provides "
                    "immediate feedback while still requiring real programming for anything beyond basic "
                    "prototypes. C# is a mature, statically-typed language that enforces discipline while "
                    "offering modern features like LINQ, async/await, and powerful generics.\n\n"

                    "The Unity ecosystem also offers extensive documentation and a massive community. When "
                    "I encountered challenges - and there were many - I could usually find solutions through "
                    "official docs, forum posts, or tutorial videos.\n\n"

                    "## Core Game Systems\n\n"
                    "### Physics and Movement\n"
                    "The foundation of any platformer is responsive movement. I implemented a custom "
                    "character controller that provides tight, predictable controls. This involved:\n\n"
                    "- Ground detection using raycasts to determine when the player can jump\n"
                    "- Variable jump height based on button hold duration\n"
                    "- Coyote time (brief window to jump after leaving a platform)\n"
                    "- Jump buffering (registering jump input slightly before landing)\n"
                    "- Smooth acceleration and deceleration curves\n\n"

                    "Getting movement to feel right required extensive iteration. Small changes to values "
                    "like gravity scale, jump force, or acceleration rates dramatically affect how the "
                    "game feels to play.\n\n"

                    "### Collision Detection\n"
                    "Unity's built-in physics handles basic collision, but platformers need precise control. "
                    "I implemented custom collision resolution for specific scenarios:\n\n"
                    "- One-way platforms the player can jump through from below\n"
                    "- Slope handling to prevent sliding and maintain consistent speed\n"
                    "- Corner correction to prevent frustrating near-misses on jumps\n"
                    "- Trigger zones for hazards, collectibles, and level transitions\n\n"

                    "### State Management\n"
                    "Player behavior is managed through a finite state machine. States include Idle, "
                    "Running, Jumping, Falling, WallSliding, and Dashing. Each state defines allowed "
                    "transitions and handles input differently. This architecture prevents impossible "
                    "states (like jumping while already jumping) and makes adding new abilities straightforward.\n\n"

                    "## Procedural Level Generation\n\n"
                    "The most technically challenging aspect was procedural generation. Rather than "
                    "hand-designing every level, the game creates unique layouts each playthrough.\n\n"

                    "### The Algorithm\n"
                    "I implemented a chunk-based system where levels are composed of pre-designed room "
                    "templates connected procedurally. The algorithm:\n\n"
                    "1. Starts with an entrance chunk\n"
                    "2. Selects compatible chunks based on exit/entrance points\n"
                    "3. Validates that the path remains completable\n"
                    "4. Places enemies and collectibles based on difficulty curves\n"
                    "5. Ensures the exit is reachable through pathfinding validation\n\n"

                    "### Balancing Randomness\n"
                    "Pure randomness creates frustrating or boring levels. I implemented constraints:\n"
                    "- Difficulty ramping (easier chunks early, harder chunks later)\n"
                    "- Guaranteed safe zones after challenging sections\n"
                    "- Minimum and maximum distances between checkpoints\n"
                    "- Seed-based generation for reproducible levels\n\n"

                    "## Animation and Visual Polish\n\n"
                    "### Sprite Animation\n"
                    "I created sprite sheets for all character states and implemented Unity's Animator "
                    "system with blend trees for smooth transitions. Animation events trigger sound "
                    "effects and particle systems at precise moments (footstep sounds, dust clouds on "
                    "landing, etc.).\n\n"

                    "### Juice and Game Feel\n"
                    "Making a game feel satisfying requires attention to small details:\n"
                    "- Screen shake on impacts (with configurable intensity and duration)\n"
                    "- Hit pause (brief freeze frames on significant events)\n"
                    "- Particle effects for movement, damage, and collectibles\n"
                    "- Squash and stretch on the player sprite\n"
                    "- Camera smoothing with look-ahead in the movement direction\n\n"

                    "## Audio Implementation\n\n"
                    "Sound design significantly impacts game feel. I implemented an audio manager that "
                    "handles:\n"
                    "- Spatial audio for environmental sounds\n"
                    "- Music layers that change based on game state\n"
                    "- Sound pooling to prevent audio source exhaustion\n"
                    "- Volume mixing and audio ducking during important events\n\n"

                    "## Performance Optimization\n\n"
                    "Games require consistent frame rates. I learned to profile and optimize:\n"
                    "- Object pooling for frequently spawned objects (bullets, particles, enemies)\n"
                    "- Hybrid culling strategies for off-screen entities\n"
                    "- Texture atlasing to reduce draw calls\n"
                    "- Efficient collision layers to minimize physics calculations\n"
                    "- Coroutines and async patterns to spread heavy operations across frames\n\n"

                    "## What I Learned\n\n"
                    "Game development taught me skills that extend beyond games:\n\n"
                    "- **State machines** are useful anywhere you have complex object behavior\n"
                    "- **Component architecture** promotes reusable, testable code\n"
                    "- **Performance profiling** is essential for any application\n"
                    "- **User experience** details matter enormously (the 'feel' of interactions)\n"
                    "- **Iteration** is key - the first implementation is rarely the best\n\n"

                    "Most importantly, I learned that making something fun requires constant playtesting "
                    "and willingness to throw away code that isn't working, no matter how clever it seemed."
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
                    "## The Homelab Journey\n\n"
                    "What started as a spare computer running a Minecraft server has evolved into a "
                    "comprehensive home infrastructure project. My homelab serves as both a learning "
                    "environment and a practical solution for self-hosting services I use daily. This "
                    "project encompasses hardware selection, operating system configuration, networking, "
                    "containerization, and ongoing maintenance.\n\n"

                    "## Hardware Evolution\n\n"
                    "The current setup runs on repurposed enterprise hardware - specifically a Dell "
                    "OptiPlex that offers excellent performance-per-dollar. Key specifications:\n"
                    "- Intel Core i5 processor (enough for my workloads)\n"
                    "- 32GB RAM (containers are memory-hungry)\n"
                    "- 500GB NVMe SSD for the OS and containers\n"
                    "- 4TB HDD for media and backups\n"
                    "- Gigabit ethernet connection\n\n"

                    "I chose this approach over cloud hosting for several reasons: no recurring costs "
                    "beyond electricity, complete control over the hardware, no bandwidth limitations, "
                    "and the educational value of managing physical infrastructure.\n\n"

                    "## Operating System: Debian Linux\n\n"
                    "After experimenting with Ubuntu Server, Proxmox, and even TrueNAS, I settled on "
                    "Debian Stable for its rock-solid reliability. The system runs headless (no GUI) "
                    "with SSH as the primary management interface.\n\n"

                    "Key system configurations:\n"
                    "- Unattended security updates via unattended-upgrades\n"
                    "- SSH hardened with key-only authentication\n"
                    "- fail2ban protecting against brute force attempts\n"
                    "- Custom MOTD showing system status on login\n"
                    "- Zsh with Oh My Zsh for a better shell experience\n\n"

                    "## Container Architecture\n\n"
                    "Everything runs in Docker containers orchestrated by Docker Compose. This approach "
                    "provides isolation, reproducibility, and easy updates. My compose file defines "
                    "the entire application stack declaratively.\n\n"

                    "### Current Services\n\n"
                    "**Media & Entertainment:**\n"
                    "- Jellyfin for media streaming (self-hosted Netflix alternative)\n"
                    "- Navidrome for music streaming\n"
                    "- Calibre-web for ebook management\n\n"

                    "**Productivity:**\n"
                    "- Nextcloud for file sync and sharing\n"
                    "- Vaultwarden (Bitwarden-compatible password manager)\n"
                    "- Bookstack for documentation and notes\n\n"

                    "**Infrastructure:**\n"
                    "- Nginx Proxy Manager for reverse proxy and SSL\n"
                    "- Portainer for container management GUI\n"
                    "- Watchtower for automatic container updates\n"
                    "- Uptime Kuma for service monitoring\n\n"

                    "**Development:**\n"
                    "- Gitea for self-hosted Git repositories\n"
                    "- Code-server (VS Code in the browser)\n\n"

                    "## Networking Configuration\n\n"
                    "### Internal Network\n"
                    "The homelab exists on a dedicated VLAN, isolated from IoT devices and guest "
                    "networks. This provides security boundaries while allowing controlled access.\n\n"

                    "### Reverse Proxy Setup\n"
                    "Nginx Proxy Manager handles all incoming requests:\n"
                    "- Routes requests to appropriate containers based on subdomain\n"
                    "- Terminates SSL/TLS with Let's Encrypt certificates\n"
                    "- Provides access control for sensitive services\n"
                    "- Enables WebSocket proxying for real-time applications\n\n"

                    "### DNS Configuration\n"
                    "I use a combination of:\n"
                    "- Public DNS (Cloudflare) for externally-accessible services\n"
                    "- Pi-hole for internal DNS and ad-blocking\n"
                    "- Local DNS entries for .local domain resolution\n\n"

                    "## Security Measures\n\n"
                    "Running services accessible from the internet requires security consciousness:\n\n"
                    "**Network Security:**\n"
                    "- UFW firewall allowing only necessary ports\n"
                    "- Cloudflare proxy hiding the actual IP\n"
                    "- VPN (WireGuard) for accessing internal-only services remotely\n"
                    "- Fail2ban monitoring logs for suspicious activity\n\n"

                    "**Application Security:**\n"
                    "- Strong, unique passwords via Vaultwarden\n"
                    "- Two-factor authentication where supported\n"
                    "- Regular security updates via Watchtower\n"
                    "- Principle of least privilege for container permissions\n\n"

                    "## Backup Strategy\n\n"
                    "Data loss would be catastrophic, so I implemented a 3-2-1 backup strategy:\n"
                    "- 3 copies of important data\n"
                    "- 2 different storage media\n"
                    "- 1 offsite backup\n\n"

                    "Implementation:\n"
                    "- Automated daily backups via cron scripts\n"
                    "- Restic for encrypted, deduplicated backups\n"
                    "- Local backup to the secondary HDD\n"
                    "- Remote backup to Backblaze B2 (cheap cloud storage)\n"
                    "- Database dumps before container backups\n\n"

                    "## Monitoring and Maintenance\n\n"
                    "### Monitoring Stack\n"
                    "- Uptime Kuma checks all services every minute\n"
                    "- Notifications via Discord webhook on failures\n"
                    "- Grafana dashboards for system metrics (CPU, RAM, disk, network)\n"
                    "- Prometheus collecting metrics from node_exporter\n\n"

                    "### Regular Maintenance\n"
                    "- Weekly review of logs and alerts\n"
                    "- Monthly security audit of exposed services\n"
                    "- Quarterly hardware inspection and cleaning\n"
                    "- Annual review of backup restoration procedures\n\n"

                    "## Lessons Learned\n\n"
                    "Running a homelab has taught me invaluable lessons:\n\n"
                    "**Technical Skills:**\n"
                    "- Linux system administration at a deeper level\n"
                    "- Networking concepts (DNS, SSL, reverse proxies, VLANs)\n"
                    "- Docker and container orchestration\n"
                    "- Backup strategies and disaster recovery\n\n"

                    "**Soft Skills:**\n"
                    "- Documentation is essential (future me forgets everything)\n"
                    "- Start simple, add complexity gradually\n"
                    "- Automation saves time in the long run\n"
                    "- Security is not optional\n\n"

                    "The homelab continues to evolve as I discover new services to self-host and "
                    "better ways to manage the infrastructure. It's become an essential part of both "
                    "my learning journey and daily digital life."
                ),
                'skills': ['Linux', 'Docker', 'Nginx', 'Bash', 'SQLite'],
                'custom_technologies': 'systemd, ufw, cron',
                'is_featured': True,
                'order': 3,
            },
            {
                'title': 'My Linux Journey',
                'slug': 'linux-journey',
                'short_description': 'From Windows power user to Linux enthusiast - a complete transition story',
                'description': (
                    "## The Beginning: Why Linux?\n\n"
                    "My journey to Linux began not with ideology, but with frustration. Windows updates "
                    "interrupting work, telemetry concerns, and the inability to truly customize my "
                    "computing environment pushed me to explore alternatives. What I found was far more "
                    "than an operating system - it was a philosophy of computing that aligned with how "
                    "I wanted to interact with technology.\n\n"

                    "## First Steps: Ubuntu and the Learning Curve\n\n"
                    "Like many newcomers, I started with Ubuntu. The initial experience was humbling. "
                    "Simple tasks I'd done for years on Windows suddenly required research. Installing "
                    "software, managing files, configuring hardware - everything had a learning curve.\n\n"

                    "The terminal intimidated me at first. Coming from a GUI-centric Windows experience, "
                    "typing commands felt archaic. But gradually, I began to appreciate the power and "
                    "precision of the command line. Tasks that required multiple clicks and window "
                    "navigations in Windows became single commands.\n\n"

                    "### Early Challenges\n"
                    "- Graphics drivers were a constant battle (Nvidia on Linux was notoriously painful)\n"
                    "- Gaming seemed impossible (this was before Proton matured)\n"
                    "- Some hardware simply didn't work (webcams, specific printers)\n"
                    "- Professional software I relied on had no Linux versions\n\n"

                    "## Distribution Hopping: Finding My Fit\n\n"
                    "The Linux world offers hundreds of distributions, each with different philosophies. "
                    "I tried many:\n\n"

                    "**Ubuntu/Linux Mint:** Great for beginners, but felt bloated. Snap packages caused "
                    "frustrations with startup times and theming issues.\n\n"

                    "**Fedora:** Cutting-edge software, excellent defaults. Taught me about SELinux and "
                    "introduced me to GNOME in its pure form.\n\n"

                    "**Manjaro/Arch:** Rolling release model appealed to me. Access to the AUR (Arch User "
                    "Repository) was game-changing. Eventually moved to pure Arch for the learning experience.\n\n"

                    "**Debian:** Rock-solid stability. Became my choice for servers after experiencing "
                    "the chaos of running bleeding-edge software on production systems.\n\n"

                    "Currently, I run Arch Linux on my desktop (I use Arch btw) and Debian on servers. "
                    "This combination gives me the latest software for daily use and stability where "
                    "it matters most.\n\n"

                    "## The Desktop Environment Quest\n\n"
                    "Linux offers unprecedented desktop customization. I've extensively used:\n\n"

                    "**GNOME:** Clean, modern, opinionated. Works great out of the box but fights you "
                    "on customization. The workflow is unique but efficient once learned.\n\n"

                    "**KDE Plasma:** The most customizable full desktop. Sometimes overwhelming in options. "
                    "Resource usage has improved dramatically in recent versions.\n\n"

                    "**i3/Sway (Tiling WMs):** Completely changed how I use computers. Mouse becomes "
                    "optional. Keyboard-driven workflows are incredibly efficient for development.\n\n"

                    "**Hyprland:** My current choice. A modern Wayland compositor with beautiful animations "
                    "and powerful tiling. Configuring it taught me about display protocols, GPU rendering, "
                    "and the Wayland ecosystem.\n\n"

                    "## Terminal Mastery\n\n"
                    "The terminal went from intimidating to indispensable. Key developments:\n\n"

                    "**Shell Evolution:**\n"
                    "Started with Bash, moved to Zsh with Oh My Zsh for plugins and themes. Now use "
                    "Fish for its intelligent autosuggestions and user-friendly defaults. Each transition "
                    "taught me more about how shells work.\n\n"

                    "**Essential Tools I Use Daily:**\n"
                    "- `ripgrep` (rg) - faster grep, respects .gitignore\n"
                    "- `fd` - user-friendly find alternative\n"
                    "- `bat` - cat with syntax highlighting\n"
                    "- `exa`/`eza` - modern ls replacement\n"
                    "- `fzf` - fuzzy finder for everything\n"
                    "- `tmux` - terminal multiplexer for session management\n"
                    "- `neovim` - my text editor of choice after the Vim learning curve\n\n"

                    "**Scripting:**\n"
                    "Bash scripting became second nature. Automating repetitive tasks, creating custom "
                    "tools, and gluing programs together. The Unix philosophy of small, composable tools "
                    "clicked into place.\n\n"

                    "## System Administration Skills\n\n"
                    "Running Linux as a daily driver forced me to learn administration:\n\n"

                    "**Package Management:**\n"
                    "Understanding apt, dnf, pacman, and the AUR. Learning to resolve dependency conflicts, "
                    "manage repositories, and even build packages from source.\n\n"

                    "**Service Management:**\n"
                    "Systemd became familiar territory. Writing unit files, managing services, analyzing "
                    "boot times, and debugging service failures.\n\n"

                    "**Filesystem Knowledge:**\n"
                    "Understanding the Linux filesystem hierarchy, mount points, permissions (including "
                    "the intricacies of user/group/other and special bits like setuid).\n\n"

                    "**Networking:**\n"
                    "Configuring network interfaces, understanding NetworkManager vs systemd-networkd, "
                    "setting up firewalls, SSH configuration and key management.\n\n"

                    "## Gaming on Linux\n\n"
                    "This deserves special mention because it was my biggest concern. The situation has "
                    "transformed dramatically:\n\n"

                    "**Steam and Proton:**\n"
                    "Valve's Proton compatibility layer runs most Windows games flawlessly. The Steam Deck "
                    "accelerated Linux gaming development. Games that seemed impossible to run now work "
                    "out of the box.\n\n"

                    "**Native Games:**\n"
                    "More developers release Linux versions. The indie scene especially embraces Linux.\n\n"

                    "**Wine and Lutris:**\n"
                    "For games outside Steam, Wine (and its gaming-focused derivatives) handle most cases. "
                    "Lutris provides easy installation scripts for popular titles.\n\n"

                    "I now game exclusively on Linux with minimal friction.\n\n"

                    "## The Philosophy Shift\n\n"
                    "Beyond technical skills, Linux changed how I think about computing:\n\n"

                    "**Ownership:** I control my computer, not the operating system vendor. No forced "
                    "updates, no telemetry I can't disable, no artificial limitations.\n\n"

                    "**Transparency:** Open source means I can inspect how things work. When something "
                    "breaks, I can often understand why and fix it myself.\n\n"

                    "**Community:** The Linux community, despite stereotypes, is incredibly helpful. "
                    "Forums, wikis (especially the Arch Wiki), and IRC/Matrix channels provide support "
                    "that commercial software can't match.\n\n"

                    "**Efficiency:** My workflow is faster and more keyboard-driven. Tiling window "
                    "managers, terminal-based tools, and scripting automation save significant time.\n\n"

                    "## Current Setup\n\n"
                    "My daily driver configuration:\n"
                    "- **OS:** Arch Linux (btw)\n"
                    "- **WM:** Hyprland (Wayland compositor)\n"
                    "- **Terminal:** Kitty with Fish shell\n"
                    "- **Editor:** Neovim with extensive configuration\n"
                    "- **Browser:** Firefox (Librewolf for privacy)\n"
                    "- **File Manager:** ranger (terminal) + Thunar (GUI when needed)\n\n"

                    "## Advice for Beginners\n\n"
                    "If you're considering the switch:\n\n"
                    "1. **Start with a user-friendly distro** - Linux Mint or Fedora are excellent choices\n"
                    "2. **Dual boot first** - Keep Windows as a safety net\n"
                    "3. **Learn the terminal gradually** - Don't force it, let curiosity guide you\n"
                    "4. **Embrace the learning process** - Frustration is part of growth\n"
                    "5. **Join communities** - Reddit, Discord, forums are incredibly helpful\n"
                    "6. **Document your setup** - Future you will thank present you\n\n"

                    "The Linux journey never really ends. There's always more to learn, configure, and "
                    "optimize. And that's exactly what makes it rewarding."
                ),
                'skills': ['Linux', 'Bash', 'Docker', 'Nginx'],
                'custom_technologies': 'Arch Linux, Hyprland, Neovim, systemd',
                'is_featured': True,
                'order': 4,
            },
            {
                'title': 'Configuring Windows',
                'slug': 'configuring-windows',
                'short_description': 'Optimizing Windows for development and power users',
                'description': (
                    "## Why This Guide Exists\n\n"
                    "Despite my preference for Linux, Windows remains necessary for certain tasks - "
                    "specific software requirements, gaming compatibility, or professional environments "
                    "that mandate it. Over years of use, I've developed a comprehensive approach to "
                    "configuring Windows that minimizes frustrations while maximizing productivity.\n\n"

                    "This isn't about making Windows into Linux (though WSL helps). It's about working "
                    "with Windows effectively while addressing its common pain points.\n\n"

                    "## Initial Setup: The First Hour\n\n"
                    "A fresh Windows installation requires immediate attention to several areas:\n\n"

                    "### Privacy and Telemetry\n"
                    "Windows 10/11 collects extensive telemetry by default. During OOBE (Out-of-Box "
                    "Experience), decline all optional data collection. Post-installation:\n\n"
                    "- Settings → Privacy & Security: Review every category\n"
                    "- Disable advertising ID, activity history, and tailored experiences\n"
                    "- Limit diagnostic data to 'Required' only\n"
                    "- Disable 'Improve inking and typing'\n"
                    "- Review app permissions (camera, microphone, location)\n\n"

                    "For thorough debloating, tools like O&O ShutUp10++ provide granular control over "
                    "hundreds of telemetry settings. Document changes for reproducibility.\n\n"

                    "### Removing Bloatware\n"
                    "Fresh Windows installations include unwanted apps. PowerShell removes them:\n\n"
                    "```powershell\n"
                    "Get-AppxPackage *Xbox* | Remove-AppxPackage\n"
                    "Get-AppxPackage *Zune* | Remove-AppxPackage\n"
                    "Get-AppxPackage *bing* | Remove-AppxPackage\n"
                    "# Continue for other unwanted packages\n"
                    "```\n\n"

                    "Be cautious - some packages have dependencies. Research before removing.\n\n"

                    "## Package Management: WinGet and Beyond\n\n"
                    "Windows finally has a decent package manager. WinGet (built into Windows 11, "
                    "available for Windows 10) enables command-line software installation:\n\n"

                    "```powershell\n"
                    "# Install essential development tools\n"
                    "winget install Microsoft.VisualStudioCode\n"
                    "winget install Git.Git\n"
                    "winget install Python.Python.3.11\n"
                    "winget install Microsoft.WindowsTerminal\n"
                    "```\n\n"

                    "Export your installed packages for easy restoration:\n"
                    "```powershell\n"
                    "winget export -o packages.json\n"
                    "winget import -i packages.json  # On new installation\n"
                    "```\n\n"

                    "For applications not in WinGet, Chocolatey provides broader coverage. I maintain "
                    "a script that installs my complete software stack on fresh installations.\n\n"

                    "## Development Environment Setup\n\n"
                    "### Windows Terminal\n"
                    "The default command prompt is painful. Windows Terminal is essential:\n"
                    "- Multiple tabs and panes\n"
                    "- GPU-accelerated rendering\n"
                    "- Customizable themes and fonts\n"
                    "- Profiles for different shells (PowerShell, CMD, WSL, Git Bash)\n\n"

                    "My configuration uses a Nerd Font for icon support and a custom color scheme "
                    "matching my Linux setup. Settings sync via JSON export.\n\n"

                    "### WSL 2 (Windows Subsystem for Linux)\n"
                    "WSL 2 transforms Windows development. It runs a real Linux kernel, enabling:\n"
                    "- Native Linux tools and workflows\n"
                    "- Docker with Linux containers\n"
                    "- Proper filesystem performance for Linux-native projects\n"
                    "- Access to Windows files from Linux and vice versa\n\n"

                    "Setup:\n"
                    "```powershell\n"
                    "wsl --install -d Ubuntu\n"
                    "# Or for Arch enthusiasts:\n"
                    "# wsl --import Arch C:\\WSL\\Arch archlinux.tar\n"
                    "```\n\n"

                    "I configure WSL with the same dotfiles as my Linux systems, maintaining consistent "
                    "tooling across environments.\n\n"

                    "### Git Configuration\n"
                    "Git on Windows has quirks. Essential configuration:\n"
                    "```bash\n"
                    "git config --global core.autocrlf true  # Handle line endings\n"
                    "git config --global credential.helper manager  # Windows credential manager\n"
                    "git config --global init.defaultBranch main\n"
                    "```\n\n"

                    "For WSL integration, configure Git to use Windows credentials:\n"
                    "```bash\n"
                    "git config --global credential.helper '/mnt/c/Program\\ Files/Git/mingw64/bin/git-credential-manager.exe'\n"
                    "```\n\n"

                    "## System Optimization\n\n"
                    "### Startup Programs\n"
                    "Windows accumulates startup programs that slow boot times. Task Manager's Startup "
                    "tab shows impact ratings. Disable unnecessary entries. For stubborn programs, "
                    "check Task Scheduler and Registry run keys.\n\n"

                    "### Virtual Memory\n"
                    "For systems with ample RAM (32GB+), I configure a fixed pagefile size rather than "
                    "system-managed. This prevents fragmentation and provides predictable behavior.\n\n"

                    "### Power Settings\n"
                    "Default power plans throttle performance. For desktops:\n"
                    "- Use 'High Performance' or create a custom plan\n"
                    "- Disable USB selective suspend (prevents peripheral issues)\n"
                    "- Set 'Turn off hard disk' to Never for SSDs\n\n"

                    "### Storage Optimization\n"
                    "- Disable hibernation if not needed (`powercfg /h off`) - reclaims RAM-sized space\n"
                    "- Configure Storage Sense for automatic cleanup\n"
                    "- Move default user folders to secondary drive if applicable\n"
                    "- Disable Search indexing for development directories (massive I/O reduction)\n\n"

                    "## Keyboard and Navigation\n\n"
                    "### Essential Shortcuts\n"
                    "Windows has powerful built-in shortcuts often overlooked:\n"
                    "- `Win + V`: Clipboard history (must enable in settings)\n"
                    "- `Win + Shift + S`: Screenshot tool\n"
                    "- `Win + .`: Emoji picker\n"
                    "- `Ctrl + Shift + Esc`: Direct to Task Manager\n"
                    "- `Win + Number`: Launch/switch to taskbar programs\n\n"

                    "### PowerToys\n"
                    "Microsoft's PowerToys fills functionality gaps:\n"
                    "- **FancyZones**: Window management with custom layouts\n"
                    "- **PowerToys Run**: Superior application launcher (Alt+Space)\n"
                    "- **Keyboard Manager**: Remap keys (I swap Caps Lock to Escape)\n"
                    "- **File Locksmith**: Find what's locking a file\n"
                    "- **Always On Top**: Pin windows above others\n\n"

                    "### AutoHotkey Scripts\n"
                    "For custom shortcuts and text expansion, AutoHotkey is invaluable. Example scripts:\n"
                    "- Text expansion for common phrases and code snippets\n"
                    "- Custom window management hotkeys\n"
                    "- Application-specific shortcuts\n\n"

                    "## Security Configuration\n\n"
                    "### Windows Security\n"
                    "Built-in Windows Defender is sufficient for most users. Ensure:\n"
                    "- Real-time protection enabled\n"
                    "- Cloud-delivered protection enabled\n"
                    "- Controlled folder access for ransomware protection\n"
                    "- Regular definition updates\n\n"

                    "### Firewall Rules\n"
                    "Windows Firewall is capable but has a terrible interface. Use Windows Firewall "
                    "Control (free) for easier rule management. Block unnecessary outbound connections "
                    "for telemetry-heavy applications.\n\n"

                    "### BitLocker\n"
                    "Enable BitLocker for drive encryption, especially on laptops. Backup recovery "
                    "keys to multiple locations.\n\n"

                    "## Maintenance Automation\n\n"
                    "### Scheduled Tasks\n"
                    "Automate maintenance with Task Scheduler:\n"
                    "- Weekly disk cleanup\n"
                    "- Monthly Windows Update check (if updates are paused)\n"
                    "- Regular backup scripts\n\n"

                    "### Backup Strategy\n"
                    "- File History for document versioning\n"
                    "- System Image for full recovery capability\n"
                    "- Cloud sync for critical files (OneDrive, Syncthing)\n"
                    "- Regular export of application settings\n\n"

                    "## Quality of Life Improvements\n\n"
                    "### File Explorer Tweaks\n"
                    "- Show file extensions (critical for security and development)\n"
                    "- Show hidden files\n"
                    "- Disable 'Quick Access' if preferred\n"
                    "- Add 'Open in Terminal' context menu\n\n"

                    "### Fonts\n"
                    "Install a proper programming font. I use JetBrains Mono Nerd Font for terminal "
                    "and editor consistency with Linux systems.\n\n"

                    "### Dark Mode\n"
                    "Enable system-wide dark mode in Personalization settings. Most modern applications "
                    "respect this setting.\n\n"

                    "## Conclusion\n\n"
                    "A well-configured Windows installation can be a productive environment. The key "
                    "is taking control during initial setup, automating maintenance, and using tools "
                    "that bridge functionality gaps. While I prefer Linux, these configurations make "
                    "Windows bearable - and sometimes even pleasant - when it's required.\n\n"

                    "Document your configuration. Future you, reinstalling after a drive failure, will "
                    "be grateful for a setup script and settings export."
                ),
                'skills': ['Bash', 'Docker'],
                'custom_technologies': 'PowerShell, WSL 2, WinGet, PowerToys',
                'is_featured': True,
                'order': 5,
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
