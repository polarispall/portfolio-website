from django.db import models


# Abstract Base Models
class OrderedModel(models.Model):
    """Abstract base for models that need ordering"""
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ['order']


class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True)
    resume = models.FileField(upload_to='resume/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Profile"


class SocialLink(OrderedModel):
    platform = models.CharField(max_length=50, help_text="Platform name (e.g., 'GitHub', 'Twitter')")
    url = models.URLField()
    use_font_awesome = models.BooleanField(
        default=True,
        help_text="Use Font Awesome icon? If unchecked, upload custom SVG/PNG"
    )
    icon_class = models.CharField(max_length=50, blank=True, help_text="Font Awesome class (e.g., 'fab fa-github'). Only used if Font Awesome is enabled")
    custom_icon = models.FileField(
        upload_to='social_icons/',
        blank=True,
        help_text="Upload custom SVG/PNG icon. Only used if Font Awesome is disabled"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this social link from the website"
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.platform


class SkillCategory(OrderedModel):
    """Dynamic skill categories managed through admin"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Font Awesome class for category icon (e.g., 'fas fa-code')"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this entire category from the website"
    )

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.name


class Skill(OrderedModel):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name='skills'
    )

    # Visibility toggle
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this skill from the website"
    )

    # Icon handling - either Font Awesome OR custom upload
    use_font_awesome = models.BooleanField(
        default=True,
        help_text="Use Font Awesome icon? If unchecked, upload custom SVG/PNG"
    )
    icon_class = models.CharField(
        max_length=50,
        blank=True,
        help_text="Font Awesome class (e.g., 'fab fa-python'). Only used if Font Awesome is enabled"
    )
    custom_icon = models.FileField(
        upload_to='skill_icons/',
        blank=True,
        help_text="Upload custom icon (SVG/PNG/JPG). Only used if Font Awesome is disabled"
    )

    # Optional link to skill homepage/docs
    url = models.URLField(
        blank=True,
        help_text="Link to homepage, documentation, or GitHub repo"
    )

    # Hover glow color
    glow_color = models.CharField(
        max_length=7,
        default='#ec4899',
        help_text="Hex color for hover glow effect (e.g., #ec4899)"
    )

    class Meta:
        ordering = ['category__order', 'order']

    def __str__(self):
        return self.name


class Experience(models.Model):
    WORK_TYPE_CHOICES = [
        ('semi_remote', 'Semi-Remote'),
        ('remote', 'Remote'),
        ('in_person', 'In-Person'),
    ]

    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    work_type = models.CharField(
        max_length=20,
        choices=WORK_TYPE_CHOICES,
        default='remote'
    )
    work_type_visible = models.BooleanField(
        default=True,
        help_text="Uncheck to hide work type from the website"
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(
        default=False,
        help_text="Check if this is your current position (hides end date field, shows 'Present' on website)"
    )
    description = models.TextField()

    # Many-to-many relationship with skills
    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name='experiences',
        help_text="Select skills used in this role (shows with icons and links)"
    )

    # Custom technologies field for anything not in the skills list
    custom_technologies = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated custom technologies/skills not in the skills list (e.g., 'Customer Service, Agile, Scrum')"
    )

    company_logo = models.ImageField(upload_to='companies/', blank=True)
    company_url = models.URLField(blank=True)

    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this experience from the website"
    )

    class Meta:
        ordering = ['-is_current', '-start_date']
        verbose_name_plural = "Experience"

    def custom_tech_list(self):
        """Return custom technologies as a list of stripped strings"""
        if self.custom_technologies:
            return [tech.strip() for tech in self.custom_technologies.split(',')]
        return []

    def __str__(self):
        return f"{self.position} at {self.company}"


class Education(models.Model):
    institution = models.CharField(max_length=150, blank=True, help_text="School/University name (optional - leave blank to stay ambiguous)")
    degree = models.CharField(max_length=150, blank=True, help_text="Degree name (e.g., 'Bachelor of Science', 'Diploma')")
    field_of_study = models.CharField(max_length=150, blank=True, help_text="Major/Field (e.g., 'Computer Science')")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(
        default=False,
        help_text="Check if currently studying (hides end date field, shows 'Present' on website)"
    )
    description = models.TextField(blank=True, help_text="Additional notes, coursework, achievements, etc.")
    gpa = models.CharField(max_length=20, blank=True, help_text="GPA or other metrics")
    institution_logo = models.ImageField(upload_to='education/', blank=True)
    institution_url = models.URLField(blank=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this education from the website"
    )

    class Meta:
        ordering = ['-is_current', '-start_date']
        verbose_name_plural = "Education"

    def __str__(self):
        parts = []
        if self.degree:
            parts.append(self.degree)
        if self.field_of_study:
            parts.append(f"in {self.field_of_study}")
        if self.institution:
            parts.append(f"at {self.institution}")
        return " ".join(parts) if parts else f"Education ({self.start_date.year})"


class Project(OrderedModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=200)
    description = models.TextField()

    # Many-to-many relationship with skills
    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name='projects',
        help_text="Select skills used in this project (shows with icons and links)"
    )

    # Custom technologies field for anything not in the skills list
    custom_technologies = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated custom technologies not in the skills list"
    )

    image = models.ImageField(upload_to='projects/', blank=True)
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this project from the website"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def custom_tech_list(self):
        """Return custom technologies as a list of stripped strings"""
        if self.custom_technologies:
            return [tech.strip() for tech in self.custom_technologies.split(',')]
        return []


class Certificate(models.Model):
    name = models.CharField(max_length=150)
    issuer = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='certificates/', blank=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return self.name
