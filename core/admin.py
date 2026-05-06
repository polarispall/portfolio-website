from django.contrib import admin
from django import forms
from .models import Profile, SocialLink, SkillCategory, Skill, Experience, Education, Project, Certificate


class SkillForm(forms.ModelForm):
    glow_color = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color'}),
        required=False
    )

    class Meta:
        model = Skill
        fields = '__all__'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email']


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    ordering = ['order']

    fieldsets = (
        (None, {
            'fields': ('platform', 'url', 'is_active', 'order')
        }),
        ('Icon Configuration', {
            'fields': ('use_font_awesome', 'icon_class', 'custom_icon'),
            'description': 'Choose either Font Awesome OR upload a custom SVG/PNG icon'
        }),
    )

    class Media:
        js = ('admin/js/social_admin.js',)


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    ordering = ['order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    form = SkillForm
    list_display = ['name', 'category', 'is_active', 'use_font_awesome', 'order']
    list_filter = ['category', 'is_active', 'use_font_awesome']
    list_editable = ['is_active', 'order']
    ordering = ['category__order', 'order']
    search_fields = ['name']

    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'is_active', 'order', 'url')
        }),
        ('Icon Configuration', {
            'fields': ('use_font_awesome', 'icon_class', 'custom_icon'),
            'description': 'Choose either Font Awesome OR upload a custom icon'
        }),
        ('Hover Effect', {
            'fields': ('glow_color',),
            'description': 'Choose the color for the glow effect when hovering'
        }),
    )

    class Media:
        js = ('admin/js/skill_admin.js',)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'start_date', 'is_current', 'is_active']
    list_filter = ['is_current', 'is_active']
    list_editable = ['is_active']
    ordering = ['-start_date']
    search_fields = ['position', 'company']

    fieldsets = (
        ('Position Details', {
            'fields': ('position', 'company', 'company_url', 'company_logo')
        }),
        ('Dates & Status', {
            'fields': ('start_date', 'end_date', 'is_current'),
            'description': 'Check "is_current" if this is your current position (end date will show as "Present")'
        }),
        ('Work Type', {
            'fields': ('work_type', 'work_type_visible'),
            'description': 'Uncheck "work_type_visible" to hide the work type on the website'
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Technologies & Skills', {
            'fields': ('skills', 'custom_technologies'),
            'description': 'Select skills from the list (they will display with icons and links). Use "custom_technologies" for anything else (e.g., "Agile, Scrum, Customer Service")'
        }),
        ('Visibility', {
            'fields': ('is_active',),
            'description': 'Uncheck to hide this experience from the website'
        }),
    )

    class Media:
        js = ('admin/js/experience_admin.js',)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'start_date', 'is_current', 'is_active']
    list_filter = ['is_current', 'is_active']
    list_editable = ['is_active']
    ordering = ['-start_date']
    search_fields = ['degree', 'institution', 'field_of_study']

    fieldsets = (
        ('Education Details', {
            'fields': ('institution', 'degree', 'field_of_study'),
            'description': 'All fields are optional - leave blank to stay ambiguous about where you studied'
        }),
        ('Dates & Status', {
            'fields': ('start_date', 'end_date', 'is_current'),
            'description': 'Check "is_current" if currently studying (end date will hide and show "Present")'
        }),
        ('Additional Info', {
            'fields': ('gpa', 'description', 'institution_url', 'institution_logo'),
        }),
        ('Visibility', {
            'fields': ('is_active',),
            'description': 'Uncheck to hide this education from the website'
        }),
    )

    class Media:
        js = ('admin/js/education_admin.js',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'is_active', 'order', 'created_at']
    list_filter = ['is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active', 'order']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order']
    search_fields = ['title', 'short_description']

    fieldsets = (
        ('Project Details', {
            'fields': ('title', 'slug', 'short_description', 'description', 'image')
        }),
        ('Links', {
            'fields': ('live_url', 'github_url'),
            'description': 'Links to live demo and source code'
        }),
        ('Technologies & Skills', {
            'fields': ('skills', 'custom_technologies'),
            'description': 'Select skills from the list (they will display with icons and links). Use "custom_technologies" for anything else.'
        }),
        ('Organization', {
            'fields': ('order', 'created_at'),
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_active'),
            'description': 'is_featured controls if shown on portfolio. is_active toggles visibility entirely.'
        }),
    )

    readonly_fields = ['created_at']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuer', 'issue_date']
    ordering = ['-issue_date']
