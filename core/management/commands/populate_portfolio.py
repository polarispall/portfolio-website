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
        """Create project entries based on resume"""
        skills = {s.name: s for s in Skill.objects.all()}

        projects = [
            {
                'title': 'My Linux Journey',
                'slug': 'my-linux-journey',
                'short_description': 'Custom Arch Linux development environment built from scratch with Hyprland compositor, extensive Neovim IDE configuration, and comprehensive dotfiles management',
                'description': (
                    "## The Breaking Point\n\n"
                    "About two years ago, Windows finally pushed me over the edge. It wasn't one thing—it was "
                    "everything. Bluescreens once a week. System Explorer freezing my entire computer. The "
                    "moment I wanted keybinds to open specific applications and realized Windows couldn't do "
                    "it natively. The moment I wanted more than pressing the Windows key and picking from that "
                    "terrible start menu search.\n\n"

                    "![The Windows experience](/media/projects/gallery/windows-bsod.png)\n\n"

                    "I'd already spent countless hours making Windows work through sheer force of configuration—"
                    "PowerToys, AltDrag, AutoHotkey scripts for global keybindings. I even implemented my own "
                    "emacs-style movement bindings system-wide before I'd ever touched Emacs or Vim. But these "
                    "were all hacks fighting against the OS.\n\n"

                    "I wanted the real thing. I wanted to understand how an OS actually works. And honestly, "
                    "I was tired of the telemetry, the bloat, the feeling that my computer wasn't really mine.\n\n"

                    "## Going Straight to Arch\n\n"
                    "I skipped the beginner distros entirely. Manual Arch installation from the wiki, minimal "
                    "base system, build everything from there. People said it was crazy for a first Linux "
                    "install, but my Windows configuration experience taught me I learn best by understanding "
                    "every layer—if I was going to do this, I wanted to actually understand what was happening "
                    "underneath.\n\n"

                    "The installation itself was a learning experience. Partitioning with `fdisk`, formatting "
                    "filesystems, installing the base system with `pacstrap`, generating fstab, chrooting into "
                    "the new system. Each step required understanding rather than clicking 'Next'.\n\n"

                    "## The Pentaboot Nightmare (Worth It)\n\n"
                    "My first month was chaos. I set up a pentaboot system: Arch as my main, a second Arch "
                    "partition for testing and breaking things safely, Ubuntu to understand the Debian ecosystem, "
                    "Debian for comparison, Linux Mint XFCE to see what a \"beginner\" distro felt like, and "
                    "Windows for Office when absolutely necessary.\n\n"

                    "Getting this working meant reinstalling GRUB probably 20+ times per partition. Not an "
                    "exaggeration. Each distro wanted to overwrite the bootloader, partitions needed specific "
                    "flags, UUIDs had to be correct in every config. By the end I had a nice GRUB theme and "
                    "actually understood how bootloaders work. Worth the pain.\n\n"

                    "![My GRUB bootloader with all five operating systems](/media/projects/gallery/grub-pentaboot.png)\n\n"

                    "Same hardware, different philosophies. It became obvious quickly that Arch's approach—"
                    "explicit configuration, rolling releases, the wiki as documentation—matched how I think "
                    "about systems. The \"beginner\" distros felt like they were hiding things from me.\n\n"

                    "## Hyprland: My First Tiling WM\n\n"
                    "Hyprland wasn't a migration from i3 or bspwm—it was my first tiling window manager. But "
                    "the concept wasn't new. All those AutoHotkey scripts on Windows? They were building toward "
                    "keyboard-driven workflows. FancyZones for pseudo-tiling, custom hotkeys for everything. "
                    "I didn't want a \"normal\" window manager. Hyprland was just doing it properly.\n\n"

                    "Going straight to Wayland meant learning the modern stack from day one. Screen sharing "
                    "needed portal configs, clipboard worked differently, some apps needed workarounds. But "
                    "I was building from scratch anyway—no X11 habits to unlearn later.\n\n"

                    "The config grew to hundreds of lines: window rules for floating specific applications, "
                    "workspace assignments, animations tuned for responsiveness over flash, keybindings designed "
                    "around muscle memory from my Windows days. The entire system controllable without a mouse.\n\n"

                    "![My actual Hyprland workflow](/media/projects/gallery/hyprland-workflow.png)\n\n"

                    "## VS Code to Neovim\n\n"
                    "On Windows, I used VS Code for a long time. It worked, but I couldn't get into flow. I "
                    "kept implementing global hotkeys through AutoHotkey—emacs-style bindings mixed with custom "
                    "shortcuts for everything. `Ctrl+F` for forward, `Ctrl+B` for back, working across Discord, "
                    "Slack, Office, VS Code itself. This was before I'd ever used Emacs or Vim. I just kind of "
                    "landed on those movement patterns naturally from programming.\n\n"

                    "When I moved to Linux, I tried Neovim and something clicked. The workflow between terminal, "
                    "Yazi, and Neovim just made sense. Everything scriptable with Lua instead of fighting JSON "
                    "settings. VS Code works out of the box—I'll give it that—but it's not scriptable with "
                    "LuaJIT, not as powerful, not as integrated with the terminal workflow.\n\n"

                    "**My keybinding philosophy:** everything reachable without leaving home row. Leader key "
                    "combinations that make sense mnemonically. `<leader>ff` for find files, `<leader>fg` for "
                    "find grep, `<leader>gg` for git. Neogit handles Git operations without leaving the editor—"
                    "visual staging, interactive rebase that doesn't feel like editing a TODO file. Combined "
                    "with Diffview for side-by-side diffs, the entire Git workflow lives in Neovim.\n\n"

                    "![Neogit staging and committing](/media/projects/gallery/neovim-neogit.png)\n\n"

                    "## Practical Workflow Over Ricing\n\n"
                    "I've spent countless hours on this setup, but more on building a practical workflow than "
                    "pure ricing. The goal was never screenshots for r/unixporn—it was a development environment "
                    "where everything flows together.\n\n"

                    "- **Walker** for launching anything without touching the mouse\n"
                    "- **Telescope** for fuzzy finding files and grepping across projects\n"
                    "- **Yazi** for visual file browsing when I need to explore (miss Directory Opus sometimes)\n"
                    "- **tmux** for persistent sessions and splits\n"
                    "- **Zsh** as my main shell with custom config (Bash on some partitions)\n"
                    "- **Waybar** showing only what matters\n\n"

                    "The dotfiles repo is the single source of truth. Shell configs, Neovim, Hyprland, systemd "
                    "user services—everything version controlled and portable.\n\n"

                    "![My dotfiles repository structure](/media/projects/gallery/dotfiles-repo.png)\n\n"

                    "## What I Actually Learned\n\n"
                    "The biggest gain wasn't the desktop environment—it was understanding how computers actually "
                    "work. Linux runs on basically every server. Learning it meant learning devops, cloud "
                    "infrastructure, networking, deployment. Docker works so much better natively than through "
                    "WSL. No more pretending I'm on Linux through a compatibility layer.\n\n"

                    "I learned how the OS is actually built and used. Package management with pacman and the AUR. "
                    "Systemd for services and timers. How the graphics stack works. Filesystem permissions that "
                    "make sense. The stuff that actually matters when you're deploying real applications.\n\n"

                    "## What Transferred\n\n"
                    "All that time configuring Windows wasn't wasted. The skills transferred directly—understanding "
                    "systems deeply, scripting automation, building keyboard-driven workflows. Linux just lets me "
                    "do it properly instead of fighting the OS at every step.\n\n"

                    "Do I miss anything? Directory Opus was incredible for file management—nothing on Linux quite "
                    "matches it. Some proprietary tools don't have good alternatives. But the tradeoffs are worth "
                    "it. Two years of breaking things and fixing them taught me more than tutorials ever could. "
                    "When something breaks now, I know where to look. This environment is exactly what I want it "
                    "to be."
                ),
                'skills': ['Linux', 'Bash', 'Neovim', 'Git'],
                'custom_technologies': 'Arch Linux, Hyprland, Wayland, systemd, Lua, Zsh, tmux',
                'github_url': 'https://github.com/polarispall/dotfiles',
                'is_featured': True,
                'order': 1,
            },
            {
                'title': 'About This Website',
                'slug': 'this-website',
                'short_description': 'Full-stack Django portfolio with modular content-driven architecture, Docker containerization, and production deployment on AWS EC2',
                'description': (
                    "## Project Philosophy\n\n"
                    "This portfolio website demonstrates practical full-stack development—from database design "
                    "to production deployment. The core architecture is content-driven: every piece of content "
                    "lives in the database rather than hardcoded templates. I can update the entire site through "
                    "Django's admin interface without touching a single line of code.\n\n"

                    "![Portfolio Homepage](/media/projects/gallery/portfolio-home.png)\n\n"

                    "The site you're looking at right now is the result of this project. Every section, skill, "
                    "project description, and piece of content is managed through a custom Django admin interface. "
                    "This means I can add new projects, update my skills, or modify any text without deploying "
                    "new code—the database is the single source of truth.\n\n"

                    "## Modular Django Architecture\n\n"
                    "The backend follows Django best practices with models designed for maximum flexibility. "
                    "Rather than hardcoding content into templates, I built a comprehensive data model that "
                    "represents every aspect of the portfolio.\n\n"

                    "![Django Admin Interface](/media/projects/gallery/django-admin.png)\n\n"

                    "**Data Models Include:**\n"
                    "- **Profile** for personal information, bio, and site-wide settings\n"
                    "- **SkillCategory** and **Skill** for organized technology display with custom icons\n"
                    "- **Experience** for work history with linked skills and technologies\n"
                    "- **Education** for academic background\n"
                    "- **Project** with rich markdown descriptions and image galleries\n"
                    "- **SocialLink** for profile connections with custom or Font Awesome icons\n"
                    "- **SiteSettings** for global configuration like theme options\n\n"

                    "The Skill model is particularly flexible—it supports custom SVG icons, Font Awesome classes, "
                    "configurable glow colors for hover effects, and links to external documentation. Projects "
                    "reference skills through many-to-many relationships, automatically displaying appropriate "
                    "icons and creating a cohesive visual language across the site.\n\n"

                    "Custom model methods handle computed properties like combining linked skills with custom "
                    "technologies. Django admin customization includes inline editors, drag-and-drop ordering, "
                    "and custom widgets that make content editing intuitive.\n\n"

                    "## Frontend Development\n\n"
                    "The frontend uses semantic HTML5 with a custom CSS architecture built entirely on CSS "
                    "custom properties (variables). No CSS framework—everything is hand-crafted for this specific "
                    "design.\n\n"

                    "![Theme Switching Demo](/media/projects/gallery/theme-demo.png)\n\n"

                    "The theming system supports three modes: dark, light, and normal. Each theme defines its "
                    "own set of CSS variables, and switching themes is as simple as changing a data attribute "
                    "on the root element. Transitions are smooth, and the user's preference persists in "
                    "localStorage.\n\n"

                    "Responsive design handles everything from 375px mobile screens to ultrawide desktop displays. "
                    "The layout adapts using CSS Grid and Flexbox, with media queries at carefully chosen "
                    "breakpoints that correspond to actual content needs rather than arbitrary device sizes.\n\n"

                    "**Interactive Elements:**\n"
                    "- Typing animation on the hero section with cursor that fades after completion\n"
                    "- Smooth scrolling navigation with active section highlighting\n"
                    "- Theme toggling with visual feedback tooltip\n"
                    "- Mobile hamburger menu with slide-out animation\n"
                    "- Scroll-triggered animations for content sections\n"
                    "- Skill tags with hover effects showing brand colors\n\n"

                    "Dependencies are minimal—no jQuery, no CSS frameworks like Bootstrap or Tailwind, just "
                    "vanilla JavaScript and carefully architected CSS. The entire frontend weighs in at a "
                    "fraction of what a framework-heavy site would require.\n\n"

                    "## Docker Containerization\n\n"
                    "Docker provides consistency between development and production environments. The setup "
                    "ensures that what works on my laptop works identically in production.\n\n"

                    "![Docker Architecture](/media/projects/gallery/docker-setup.png)\n\n"

                    "The multi-stage Dockerfile creates optimized production images:\n"
                    "1. Build stage installs dependencies and collects static files\n"
                    "2. Production stage copies only what's needed for a minimal footprint\n"
                    "3. Non-root user for security\n"
                    "4. Health checks for container orchestration\n\n"

                    "Docker Compose defines the complete application stack with volume mounts for persistent "
                    "data (SQLite database, media uploads) and environment variables for configuration. "
                    "Development and production compose files share a base configuration with environment-specific "
                    "overrides.\n\n"

                    "## Production Deployment\n\n"
                    "The production stack runs on AWS EC2 with Debian as the base OS:\n\n"
                    "- **Cloudflare** handles DNS, provides CDN caching, and adds a security layer\n"
                    "- **Caddy** reverse proxy manages automatic HTTPS with Let's Encrypt\n"
                    "- **Gunicorn** serves the Django application with multiple workers\n"
                    "- **SQLite** provides file-based persistence perfect for portfolio scale\n"
                    "- **WhiteNoise** serves static files efficiently without a separate server\n\n"

                    "![Deployment Architecture](/media/projects/gallery/deployment-arch.png)\n\n"

                    "Caddy was chosen specifically for its automatic certificate management—it handles Let's "
                    "Encrypt issuance and renewal without any manual intervention, cron jobs, or certbot "
                    "configuration. The Caddyfile is remarkably simple compared to equivalent Nginx configs.\n\n"

                    "## Technical Challenges Solved\n\n"
                    "**Theme System:** CSS custom properties change based on a data-theme attribute, with "
                    "JavaScript handling toggle and localStorage persistence. Colors needed to work across "
                    "all themes while maintaining WCAG accessibility contrast ratios. The skill icons show "
                    "their brand colors on hover, requiring careful CSS filter calculations.\n\n"

                    "**Navigation Responsiveness:** With seven navigation items plus a theme toggle, the "
                    "horizontal nav overflowed on tablet-sized screens. The hamburger menu activates at 1100px "
                    "with careful attention to slide-out animation, proper z-index stacking, and body scroll "
                    "locking when the menu is open.\n\n"

                    "**Markdown Rendering:** Project descriptions support full markdown with syntax highlighting "
                    "for code blocks. This required a custom template filter using Python-Markdown with "
                    "extensions for fenced code blocks, tables, and table of contents. Comprehensive CSS "
                    "ensures markdown content looks consistent with the site's design.\n\n"

                    "**Section Ordering:** The admin interface allows drag-and-drop reordering of homepage "
                    "sections. This required a custom Django widget with JavaScript for the sortable interface "
                    "and JSON field storage for the order configuration.\n\n"

                    "## Lessons Learned\n\n"
                    "Planning data models before writing frontend code paid dividends throughout the project. "
                    "The time invested in designing flexible models meant adding new sections or modifying "
                    "content required no template changes—just database updates through the admin.\n\n"

                    "CSS architecture matters enormously. Starting with solid custom properties and consistent "
                    "naming conventions made the responsive design and theming work much smoother than previous "
                    "projects where I added styles ad-hoc. The BEM-ish naming pattern kept specificity manageable.\n\n"

                    "Choosing SQLite over PostgreSQL was the right call for this scale. No separate database "
                    "server to manage, backups are just file copies, and performance is more than adequate "
                    "for a portfolio site with low traffic."
                ),
                'skills': ['Django', 'Docker', 'AWS', 'SQLite', 'Python', 'HTML', 'CSS', 'Caddy', 'Gunicorn', 'Cloudflare'],
                'custom_technologies': '',
                'live_url': 'https://polarispall.com',
                'github_url': 'https://github.com/polarispall/portfolio',
                'is_featured': True,
                'order': 2,
            },
            {
                'title': 'Game Development',
                'slug': 'game-development',
                'short_description': '2D and 3D games in Unity with custom art, procedural generation, and component-based architecture',
                'description': (
                    "## The Game Development Journey\n\n"
                    "Multiple 2D and 3D games built in Unity, exploring everything from hand-crafted level "
                    "design to procedural generation. What started as curiosity about how games work under "
                    "the hood became a deep dive into game feel, systems design, and the intersection of "
                    "code and creativity.\n\n"

                    "![2D RPG in Unity](/media/projects/gallery/game-unity.png)\n\n"

                    "The main project is a 2D top-down RPG—tile-based world, NPC interactions, dialogue, "
                    "exploration between areas. But I've also built platformers, experimented with 3D, and "
                    "explored procedural content generation.\n\n"

                    "## Procedural Generation\n\n"
                    "One of the more interesting areas: creating content algorithmically rather than by hand. "
                    "The foundation is noise generation—Perlin noise, simplex noise—functions that produce "
                    "smooth, natural-looking randomness. Sample the noise at each point in a grid, and you "
                    "get terrain that looks organic rather than chaotic.\n\n"

                    "The challenge isn't generating random content—it's generating *playable* content. Pure "
                    "noise creates unusable garbage. The real work is constraining the randomness: ensuring "
                    "paths exist, difficulty ramps appropriately, and the result is actually fun. This meant "
                    "building validation systems, playtesting parameters, and iterating until procedural "
                    "levels felt designed rather than random.\n\n"

                    "## Game Architecture\n\n"
                    "Games are built using component-based architecture—Unity's core pattern. Rather than "
                    "monolithic scripts, functionality separates into discrete components: player controller, "
                    "enemy AI, collision handler, dialogue system, inventory. Compose them together to create "
                    "complex behaviors. Learning when to use composition vs. inheritance was key—inheritance "
                    "hierarchies become rigid, composition stays flexible.\n\n"

                    "![Dialogue and NPC interaction](/media/projects/gallery/game-dialogue.png)\n\n"

                    "State machines manage game states (menu, playing, paused) and entity states (idle, "
                    "moving, attacking, interacting). Each state defines allowed transitions, input handling, "
                    "and update logic. This prevents impossible states and makes adding new behaviors "
                    "straightforward—just add a new state and define its transitions.\n\n"

                    "## Art & Animation\n\n"
                    "Custom art created in Aseprite for pixel art and Moho for more complex animation. "
                    "Tiles for terrain, sprites for characters and objects, animations frame by frame.\n\n"

                    "![Creating assets in Aseprite](/media/projects/gallery/game-aseprite.png)\n\n"

                    "The workflow: design, block in colors, refine, export as sprite sheet. Unity imports "
                    "and slices into individual sprites. Animations are sequences played in order—walk "
                    "cycles, idle states, reactions. Unity's Animator state machine connects animations "
                    "to game states.\n\n"

                    "Understanding the relationship between art and gameplay matters:\n"
                    "- Sprite size affects hitbox design\n"
                    "- Animation frames communicate state to players\n"
                    "- Visual clarity impacts playability\n"
                    "- Color palettes establish mood and readability\n\n"

                    "## 2D vs 3D\n\n"
                    "**2D games** taught foundational concepts: tile-based worlds, camera systems, sprite "
                    "layering and sorting, simple physics. Problems are easier to visualize and debug.\n\n"

                    "**3D games** introduced spatial complexity that 2D never touches. Blender for modeling—"
                    "vertices, faces, UV unwrapping, rigging. In Unity: 3D camera control (third-person "
                    "cameras are harder than they look), perspective rendering, Z-fighting issues, more "
                    "expensive physics, lighting affecting gameplay readability. Learning to think in three "
                    "dimensions required a mental shift.\n\n"

                    "## Physics & Game Feel\n\n"
                    "Unity's physics provides the foundation, but good game feel requires custom tuning. "
                    "Player movement needs to feel responsive—not floaty, not sluggish. This means tweaking "
                    "gravity, acceleration curves, input buffering. Small changes dramatically affect how "
                    "the game feels.\n\n"

                    "Going beyond \"does it work\" to \"does it feel good\": screen shake on impacts, particle "
                    "effects on actions, camera smoothing, sound design for feedback. These polish elements "
                    "transform functional games into enjoyable ones.\n\n"

                    "Game development is different from web development. Everything runs in a loop, every "
                    "frame. Performance matters constantly—60fps means 16ms for everything. The intersection "
                    "of code and creativity is what makes it interesting."
                ),
                'skills': ['C#', 'Unity', 'Blender'],
                'custom_technologies': 'Aseprite, Moho, Procedural Generation, State Machines',
                'is_featured': True,
                'order': 3,
            },
            {
                'title': 'Windows Configuration for Powerusers',
                'slug': 'windows-configuration',
                'short_description': 'Custom keybind system and automation layer built with AutoHotkey, featuring Capslock modifier strategy and global mark mode for keyboard-driven workflows',
                'description': (
                    "## The Problem: Default Windows Friction\n\n"
                    "Before fully transitioning to Linux, I spent years as a Windows poweruser hitting constant "
                    "friction with the default OS experience. The default tools are functional but mediocre. "
                    "Window management is clunky, file exploration is limited, and keyboard-driven workflows "
                    "are an afterthought.\n\n"

                    "![Windows Desktop Setup](/media/projects/gallery/windows-desktop.png)\n\n"

                    "Discovered that productivity gains come not from fighting the system, but from building a "
                    "custom layer on top of it. Windows becomes a different operating system when you replace "
                    "the defaults with best-in-class tools and tie everything together with automation.\n\n"

                    "## The Tools Stack\n\n"
                    "Every default Windows tool can be replaced with something better. Here's the stack I "
                    "assembled over years of experimentation:\n\n"

                    "![PowerToys FancyZones](/media/projects/gallery/windows-powertoys.png)\n\n"

                    "**PowerToys** provided system-level utilities that Microsoft should have shipped:\n"
                    "- FancyZones for window snapping (far more flexible than built-in Snap)\n"
                    "- Text Extractor for OCR—select any region and extract text\n"
                    "- PowerRename for batch renaming with regex support\n"
                    "- Color Picker accessible anywhere with a hotkey\n"
                    "- File Locksmith to find what's locking a file\n"
                    "- Always On Top to pin windows above others\n\n"

                    "**Alt-Drag** enabled moving and resizing windows from anywhere by holding Alt—a tiny tweak "
                    "with massive impact. No more hunting for title bars or resize handles. Just Alt+drag to "
                    "move, Alt+right-drag to resize. This alone saves hundreds of mouse movements daily.\n\n"

                    "**Flow Launcher** became the application launcher and command runner, replacing Windows "
                    "Search and the Run dialog with something actually fast and extensible. Similar to Alfred "
                    "on macOS or rofi on Linux. Launch apps, search files, run calculations, convert units, "
                    "search the web—all from one hotkey.\n\n"

                    "![Flow Launcher](/media/projects/gallery/windows-flow.png)\n\n"

                    "**Directory Opus** replaced Windows Explorer entirely. A professional file manager with:\n"
                    "- Dual-pane view for easy file operations between locations\n"
                    "- Customizable columns and views per folder\n"
                    "- Saved search queries and folder presets\n"
                    "- Inline preview for images, documents, code\n"
                    "- Scripting support for custom commands\n"
                    "- Tabbed interface for multiple locations\n\n"

                    "**Windows Terminal** replaced the ancient cmd.exe and basic PowerShell window. Proper "
                    "tabs, GPU-accelerated rendering, customizable themes, and support for multiple shells "
                    "(PowerShell, WSL, Git Bash) in one interface.\n\n"

                    "## The AutoHotkey Revelation\n\n"
                    "These tools were good, but AutoHotkey was transformative. It's a scripting language that "
                    "remaps keys and creates custom hotkeys at the OS level—no privileged access required, "
                    "running entirely in userspace.\n\n"

                    "![AutoHotkey Script](/media/projects/gallery/windows-ahk.png)\n\n"

                    "Started with simple remaps:\n"
                    "- Capslock to Escape (essential for Vim users)\n"
                    "- Capslock held becomes Control\n"
                    "- Right Alt to Backspace for easier reach\n\n"

                    "Then realized the real power: Capslock as a completely custom modifier layer.\n\n"

                    "## The Capslock Modifier Strategy\n\n"
                    "Capslock is a prime piece of keyboard real estate—right where your pinky rests—but its "
                    "default function (toggle caps lock) is nearly useless. Made the strategic decision to "
                    "repurpose it entirely.\n\n"

                    "Disabled the native Capslock function completely and remapped it as a custom modifier key. "
                    "This essentially created a new tier of keybinds with zero conflicts—nothing in any "
                    "application uses Capslock as a modifier.\n\n"

                    "**Navigation Layer (Emacs-inspired):**\n"
                    "- `Capslock+F` → Forward (Right arrow)\n"
                    "- `Capslock+B` → Backward (Left arrow)\n"
                    "- `Capslock+N` → Next line (Down arrow)\n"
                    "- `Capslock+P` → Previous line (Up arrow)\n"
                    "- `Capslock+A` → Beginning of line (Home)\n"
                    "- `Capslock+E` → End of line (End)\n"
                    "- `Capslock+Alt+F` → Forward word (Ctrl+Right)\n"
                    "- `Capslock+Alt+B` → Backward word (Ctrl+Left)\n\n"

                    "**Editing Layer:**\n"
                    "- `Capslock+D` → Delete forward (Delete key)\n"
                    "- `Capslock+H` → Delete backward (Backspace)\n"
                    "- `Capslock+K` → Kill to end of line\n"
                    "- `Capslock+U` → Kill to beginning of line\n"
                    "- `Capslock+W` → Kill word backward\n\n"

                    "This created navigation semantics that feel like being inside a text editor everywhere—"
                    "browsers, Slack, GitHub forms, email, terminals. The hands never leave the home row.\n\n"

                    "## Mark Mode: Selection Without the Mouse\n\n"
                    "Implemented a global mark mode inspired by Emacs. In Emacs, you set a mark, move the "
                    "cursor, and the region between mark and cursor becomes selected. Replicated this system-wide.\n\n"

                    "![Mark Mode Demo](/media/projects/gallery/windows-mark.png)\n\n"

                    "`Capslock+Space` toggles mark mode with visual feedback (a small notification). Once "
                    "activated, any movement command extends the selection instead of moving the cursor.\n\n"

                    "**Example workflow - select three words:**\n"
                    "1. `Capslock+Space` (enable mark mode)\n"
                    "2. `Capslock+Alt+F` (forward one word, now selected)\n"
                    "3. `Capslock+Alt+F` (forward another word, selection extends)\n"
                    "4. `Capslock+Alt+F` (forward third word, selection extends)\n"
                    "5. `Ctrl+C` (copy) or `Capslock+W` (cut)\n\n"

                    "Works in every text field on the system—browsers, editors, chat apps, everywhere. "
                    "This alone eliminated a massive source of context-switching cost. No more reaching for "
                    "the mouse to select text.\n\n"

                    "## Application-Specific Hotkeys\n\n"
                    "AutoHotkey can detect which application is focused and apply different keybinds. Created "
                    "per-application customizations:\n\n"
                    "- Browser: hotkeys for tab management, history navigation\n"
                    "- VS Code: additional keybinds that don't conflict with built-in ones\n"
                    "- Discord/Slack: quick navigation between servers/channels\n"
                    "- File manager: custom commands for common operations\n\n"

                    "## The Workflow Payoff\n\n"
                    "The cumulative effect was profound. Context-switching costs dropped dramatically:\n"
                    "- No switching between keyboard and mouse for navigation/selection\n"
                    "- No hunting for windows—Flow Launcher brings anything up instantly\n"
                    "- No fumbling with window management—FancyZones + Alt-Drag handle it\n"
                    "- No leaving the home row for arrow keys or navigation\n\n"

                    "The muscle memory built up across tools created a coherent system where the entire OS "
                    "feels like a unified text editor. `Capslock+F` always means forward, whether in Chrome, "
                    "VS Code, Slack, or Notepad. Same language everywhere.\n\n"

                    "This project demonstrated the value of systems thinking—seeing the computer as a toolkit "
                    "where individual tools can be unified into a coherent whole. The willingness to invest "
                    "in automation pays dividends daily."
                ),
                'skills': ['Bash'],
                'custom_technologies': 'AutoHotkey, PowerToys, Flow Launcher, Directory Opus',
                'is_featured': True,
                'order': 4,
            },
            {
                'title': 'My Neovim Workflow - Git & IDE',
                'slug': 'neovim-workflow',
                'short_description': 'Full development workflow in Neovim—Git with Neogit/Diffview/Gitsigns, file navigation with Telescope/Yazi, and LSP-powered editing',
                'description': (
                    "## The Approach\n\n"
                    "I don't believe everything must live in one tool. If a dedicated app does something "
                    "better, I'll use it. But bringing Git and navigation into Neovim isn't about purity—"
                    "it's practical efficiency. The linkage between editing, version control, and file "
                    "navigation should be immediate. Context-switching costs time.\n\n"

                    "## Git: The Core of the Workflow\n\n"
                    "Git integration is where this setup really shines.\n\n"

                    "**Gitsigns** runs constantly, showing changes in the gutter. But the real power: "
                    "stage and unstage individual *lines*. Not files, not hunks—lines. Changed three things "
                    "but only one belongs in this commit? Stage just that line. Inline git blame shows who "
                    "wrote what and when. Navigate between changes with `]c` and `[c`.\n\n"

                    "![Neogit staging interface](/media/projects/gallery/neovim-neogit.png)\n\n"

                    "**Neogit** provides the full staging interface—Magit-inspired. Status view with staged, "
                    "unstaged, untracked files. Expand to see hunks. Stage/unstage with single keystrokes. "
                    "Commit, push, pull, branch management, stash—all visual.\n\n"

                    "**Diffview** handles deep comparison:\n\n"

                    "![Diffview side-by-side](/media/projects/gallery/neovim-diffview.png)\n\n"

                    "- Compare any two commits, branches, or working tree state\n"
                    "- Side-by-side diff with syntax highlighting\n"
                    "- File tree showing all changed files\n"
                    "- Navigate between changes with keybinds\n\n"

                    "Reviewing a PR? Open Diffview against main and see exactly what changed across every "
                    "file. Need to understand what a coworker's branch does before merging? Same thing. "
                    "The merge conflict resolution view is particularly useful—three-way diff showing "
                    "base, ours, and theirs.\n\n"

                    "## The Case for Rebase\n\n"
                    "Most people learn one Git workflow: branch, commit, commit, commit, merge. It works. "
                    "But it creates messy history. Every merge commit. Every \"fix typo\" and \"actually fix "
                    "it this time\" commit preserved forever. The log becomes noise.\n\n"

                    "**Rebase is underrated.** Interactive rebase lets you rewrite history before sharing it. "
                    "Clean up your commits. Squash the five \"WIP\" commits into one meaningful commit. "
                    "Reorder so the logical changes are in logical order. Edit commit messages to actually "
                    "describe what happened.\n\n"

                    "Why don't more people use it? The CLI interface is intimidating. `git rebase -i HEAD~5` "
                    "opens a TODO file where you edit words like `pick` and `squash`. Easy to mess up. "
                    "People learn to avoid it.\n\n"

                    "Neogit makes rebase visual:\n\n"

                    "![Interactive rebase in Neogit](/media/projects/gallery/neovim-rebase.png)\n\n"

                    "See your commits in a list. Move them up/down to reorder. Mark one as `squash` to fold "
                    "it into the previous. Mark as `edit` to stop and amend. Mark as `drop` to remove it "
                    "entirely. Edit messages inline. Execute with a keypress.\n\n"

                    "**Rebase before merging.** Before opening a PR, rebase and clean up. Squash the debug "
                    "commits. Make each commit a logical unit of change. Reviewers see a clear story: this "
                    "commit adds the feature, this commit adds tests, this commit updates docs. Not twenty "
                    "commits of stream-of-consciousness coding.\n\n"

                    "**Rebase onto main.** Instead of merging main into your branch (creating a merge commit), "
                    "rebase your branch onto main. Your commits replay on top of the latest main. Linear "
                    "history. No merge commits cluttering the log.\n\n"

                    "This isn't about dogma. Merge commits have their place. But rebase is a tool too many "
                    "people never learn because the interface is hostile. Making it visual and integrated "
                    "removes that barrier.\n\n"

                    "## The Full Workflow\n\n"
                    "Here's how all these pieces actually connect in a real development session.\n\n"

                    "### Starting Work\n\n"
                    "I open Neovim in the project root. First thing: `<leader>ff` to Telescope into the file "
                    "I need. Fuzzy matching means I type a few characters and it finds the file. If I don't "
                    "remember the exact name, `<leader>fg` lets me grep for content—search for a function "
                    "name, a string, anything. Results show in Telescope with preview. Enter to open.\n\n"

                    "If I need to explore the directory structure—maybe I'm new to the codebase or looking "
                    "for something I can't name—`<leader>e` opens Yazi in a floating window. Full directory "
                    "tree, preview pane showing file contents, vi-style navigation. I can browse, preview "
                    "files without opening them, then Enter to open what I need. Yazi also handles bulk "
                    "operations: rename, move, copy, delete. Sometimes that's faster than shell commands.\n\n"

                    "### Editing with LSP\n\n"
                    "Once I'm in a file, the LSP is always running. Completions appear as I type—nvim-cmp "
                    "pulls from multiple sources: the language server, buffer words, file paths, snippets. "
                    "Tab to accept, Ctrl-n/Ctrl-p to navigate options. Signature help shows function "
                    "parameters as I type them.\n\n"

                    "Errors and warnings appear inline as virtual text—I see the problem without opening "
                    "a separate panel. `]d` jumps to the next diagnostic, `[d` to previous. Hover over "
                    "something with `K` to see its type and documentation. `gd` goes to definition. `gr` "
                    "shows all references across the project. `<leader>rn` renames a symbol everywhere.\n\n"

                    "Code actions with `<leader>ca`—the LSP suggests fixes. Missing import? One keypress "
                    "adds it. Unused variable? Remove it. The language server knows the semantics; I just "
                    "approve the action.\n\n"

                    "Treesitter handles the syntax layer. Highlighting that understands code structure, not "
                    "just regex patterns. Incremental selection with `<C-space>`—select the inner node, "
                    "press again to expand to the outer node. Select a function body, then the whole "
                    "function, then the whole class. Text objects like `af` (around function) and `if` "
                    "(inside function) work because Treesitter understands the AST.\n\n"

                    "### Tracking Changes with Git\n\n"
                    "While I'm editing, Gitsigns shows what's changed in the gutter. Added lines get a "
                    "green bar. Modified lines yellow. Deleted lines a red triangle. I always know what "
                    "I've touched.\n\n"

                    "When I finish a logical piece of work—not the whole feature, just a coherent change—"
                    "I stage it. With Gitsigns, I can stage individual lines. `<leader>hs` stages the hunk "
                    "under cursor. But if I changed multiple things in one hunk and only want to commit "
                    "part of it, I visually select the lines and stage just those. This granularity matters "
                    "for clean commits.\n\n"

                    "I keep working. Stage more changes as I go. The staged changes accumulate while I "
                    "continue editing.\n\n"

                    "### Committing\n\n"
                    "When I'm ready to commit, `<leader>gg` opens Neogit. The status buffer shows everything: "
                    "staged changes at the top, unstaged below, untracked files at the bottom. I can expand "
                    "any file to see the diff. If I staged something I shouldn't have, `u` unstages it. If "
                    "I missed something, `s` stages it.\n\n"

                    "Press `c` to start a commit. A buffer opens for the commit message. Write the message, "
                    "`<C-c><C-c>` to confirm. The commit happens. I can immediately `p` to push, or keep "
                    "working.\n\n"

                    "If I've made several messy commits and want to clean up before pushing, I rebase. In "
                    "Neogit, `r` then `i` starts interactive rebase. I see my commits in a list. Move them "
                    "around, mark some to squash, edit messages. Execute the rebase. What would be scary "
                    "on the command line is visual and safe here.\n\n"

                    "### Comparing and Reviewing\n\n"
                    "Need to see what changed between branches? `<leader>dv` opens Diffview. Pick the "
                    "branches to compare. Side-by-side diff with full syntax highlighting. File tree on "
                    "the left shows all changed files—click through them to see each diff.\n\n"

                    "Reviewing a PR before merging? Diff against main. I see exactly what the branch "
                    "introduces. During merge conflicts, Diffview shows the three-way diff: base, ours, "
                    "theirs. Pick which changes to keep. Resolve conflicts visually instead of editing "
                    "conflict markers by hand.\n\n"

                    "### The Loop\n\n"
                    "This is the loop: Telescope/Yazi to navigate. LSP for intelligent editing. Gitsigns "
                    "for awareness and line-level staging. Neogit for commits and rebasing. Diffview for "
                    "comparison. Each tool does one thing well. They connect through keybinds and shared "
                    "context.\n\n"

                    "No alt-tabbing. No context switches. The version control, file navigation, and code "
                    "intelligence are all right there, connected to what I'm writing. That's the efficiency "
                    "gain—not doing everything in Neovim for purity, but reducing friction where friction "
                    "exists.\n\n"

                    "## Practical, Not Pure\n\n"
                    "I'll use `git log` in a terminal when that's easier. GitHub's web UI for some PR "
                    "reviews. The goal isn't Neovim for everything—it's removing friction where it exists. "
                    "Git's friction is mostly interface. The operations are powerful; the CLI makes them "
                    "awkward. Making them visual and integrated means actually using them."
                ),
                'skills': ['Neovim', 'Git', 'Linux'],
                'custom_technologies': 'Neogit, Diffview, Gitsigns, Telescope, Yazi, Treesitter, LSP',
                'is_featured': True,
                'order': 5,
            },
            {
                'title': 'My Homelab',
                'slug': 'homelab',
                'short_description': 'Self-hosted infrastructure running 24/7 on Debian with Docker, Cloudflare tunnels, and proper security hardening',
                'description': (
                    "## The Setup\n\n"
                    "A self-hosted server running 24/7 on Debian Stable. Old hardware—Core 2 Duo E8500, "
                    "4GB RAM, a couple hundred gigs of storage—but it handles everything I throw at it.\n\n"

                    "The server runs headless. No monitor, no desktop environment, just SSH access and "
                    "web interfaces. All management happens remotely.\n\n"

                    "![Server resource usage](/media/projects/gallery/homelab-btop.png)\n\n"

                    "## Design Choices\n\n"
                    "**Why Debian Stable?** When something runs 24/7, you want boring. Debian Stable's "
                    "packages are old but tested. Updates don't break things at 3am. Arch is great on my "
                    "desktop where I want the latest everything—on a server, I want reliability. Debian's "
                    "release cycle means I upgrade once every few years, not constantly.\n\n"

                    "**Why Docker?** Isolation and reproducibility. Each service runs in its own container "
                    "with explicit dependencies. No conflicts between services wanting different versions "
                    "of the same library. If something breaks, nuke the container and rebuild from the "
                    "image. The compose file *is* the documentation—it defines exactly what's running and "
                    "how it's configured.\n\n"

                    "**Why not bare metal services?** Tried it. Package management becomes a nightmare "
                    "when you have 10+ services with conflicting dependencies. Containers let me run "
                    "whatever versions each service needs without polluting the host system. Upgrades are "
                    "trivial—pull new image, recreate container, done.\n\n"

                    "**Why old hardware?** It's what I had. But also: constraints force efficiency. When "
                    "you only have 4GB RAM, you learn to pick lightweight alternatives, avoid bloated "
                    "images, and actually think about resource usage. Most services idle at near-zero CPU. "
                    "Memory stays under 50%. The E8500 handles it fine.\n\n"

                    "## The Two Stacks\n\n"
                    "Services split into two access patterns: public and private. Different security "
                    "models, different routing, same Docker infrastructure underneath.\n\n"

                    "### Public Stack (Cloudflare Tunnel)\n\n"
                    "For services that need internet access—like this portfolio website.\n\n"

                    "**Why Cloudflare Tunnel over port forwarding?** Traditional setup: open ports on "
                    "router, set up dynamic DNS, manage SSL certificates, hope your ISP doesn't block "
                    "ports or change your IP. Cloudflare Tunnel: outbound connection only, no ports open, "
                    "home IP hidden, SSL handled automatically, DDoS protection included. The tunnel "
                    "daemon connects *out* to Cloudflare—nothing needs to be open inbound.\n\n"

                    "The request flow:\n"
                    "1. DNS query hits Cloudflare (records managed in their dashboard)\n"
                    "2. Cloudflare routes through their network to my `cloudflared` daemon\n"
                    "3. `cloudflared` forwards to Nginx reverse proxy inside Docker\n"
                    "4. Nginx routes to the appropriate container based on hostname\n"
                    "5. Response flows back through the same chain\n\n"

                    "**Why Nginx between Cloudflare and containers?** Could skip it—cloudflared can route "
                    "directly to containers. But Nginx gives me one place to manage routing rules, add "
                    "headers, handle caching, configure rate limiting. If I add a new service, I update "
                    "Nginx config, not Cloudflare tunnel config. Separation of concerns.\n\n"

                    "Nginx and public containers share a Docker bridge network. Containers expose ports "
                    "only to that network, never to the host. A container compromise can't directly reach "
                    "the host or other networks.\n\n"

                    "### Private Stack (Tailscale)\n\n"
                    "For services that should never touch the public internet.\n\n"

                    "**Why Tailscale over traditional VPN?** OpenVPN or WireGuard manually configured "
                    "means managing keys, dealing with NAT, setting up a VPN server, opening ports. "
                    "Tailscale is WireGuard underneath but handles all the coordination. NAT traversal "
                    "just works. My laptop, phone, and server join the same mesh network. From anywhere, "
                    "I access internal services like I'm on the home network.\n\n"

                    "The server gets a stable Tailscale IP (100.x.x.x range). MagicDNS gives hostnames. "
                    "I access Syncthing, Filebrowser, SSH—all through the tailnet. No port forwarding, "
                    "no dynamic DNS, no exposed services.\n\n"

                    "Private services run on a separate Docker network, completely isolated from the "
                    "public stack. Not connected to Nginx. Not reachable except through Tailscale.\n\n"

                    "## Docker Architecture\n\n"
                    "Docker Compose orchestrates everything. The compose file defines:\n"
                    "- Named volumes for persistent data (database files, configs survive rebuilds)\n"
                    "- Custom bridge networks (public and private isolated from each other)\n"
                    "- Environment variables from `.env` files (secrets stay out of version control)\n"
                    "- Restart policies (`unless-stopped`—survives reboots, respects manual stops)\n"
                    "- Resource limits where needed (prevents runaway containers eating all RAM)\n\n"

                    "Network segmentation is key. A container can only reach what it's explicitly "
                    "networked with. Public containers can't see private containers. Private containers "
                    "can't reach the internet. The compose file defines these boundaries.\n\n"

                    "## Services\n\n"
                    "A few highlights—this is the tip of the iceberg:\n\n"
                    "**Forgejo** — Self-hosted Git. Lightweight Gitea fork. Some projects don't belong "
                    "on GitHub.\n\n"
                    "**Syncthing** — File sync across devices. Decentralized, encrypted, no cloud.\n\n"
                    "**Filebrowser** — Web file manager for quick access without SSH.\n\n"
                    "**Actual Budget** — Financial tracking. FOSS alternative to YNAB.\n\n"
                    "**Samba** — Local network file shares.\n\n"
                    "There's more running—various tools, experiments, automation. The infrastructure "
                    "supports spinning up new services quickly when I need them.\n\n"

                    "## Security\n\n"
                    "- **UFW firewall** — minimal ports open (SSH only, and even that's optional via Tailscale)\n"
                    "- **fail2ban** — monitors logs, auto-bans IPs after failed auth attempts\n"
                    "- **SSH key-only** — password auth disabled entirely\n"
                    "- **Non-root user** for daily operations\n"
                    "- **Containers with minimal privileges** — no unnecessary capabilities\n"
                    "- **Automatic security updates** via unattended-upgrades\n\n"

                    "## Running It\n\n"
                    "Systemd manages the Docker daemon and host-level services. Timer units handle "
                    "scheduled tasks. Journal logging centralizes everything for debugging.\n\n"

                    "29 days uptime at last check. Running infrastructure teaches things documentation "
                    "doesn't—Docker networking debugging, container startup failures, storage management, "
                    "recovering from failed updates. The homelab is where theory meets practice."
                ),
                'skills': ['Linux', 'Docker', 'Nginx', 'Bash', 'Cloudflare'],
                'custom_technologies': 'Debian, Docker Compose, Tailscale, Syncthing, Forgejo, fail2ban',
                'is_featured': True,
                'order': 6,
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
