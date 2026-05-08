from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import Profile, SocialLink, SkillCategory, Skill, Experience, Education, Project, Certificate
import json


class SectionOrderWidget(forms.Widget):
    """Custom widget for drag-and-drop section ordering"""

    template_name = 'admin/widgets/section_order.html'

    class Media:
        css = {
            'all': ('admin/css/section_order.css',)
        }
        js = (
            'https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js',
            'admin/js/section_order.js',
        )

    def render(self, name, value, attrs=None, renderer=None):
        if value is None or value == '':
            sections = Profile.DEFAULT_SECTIONS
        elif isinstance(value, str):
            try:
                sections = json.loads(value)
            except json.JSONDecodeError:
                sections = Profile.DEFAULT_SECTIONS
        else:
            sections = value

        if not sections:
            sections = Profile.DEFAULT_SECTIONS

        html = f'''
        <div class="section-order-widget">
            <input type="hidden" name="{name}" id="id_{name}" value='{json.dumps(sections)}'>
            <div class="section-order-help">
                <p>Drag sections to reorder. Toggle visibility with the eye icon. Numbers update automatically.</p>
            </div>
            <ul class="section-order-list" id="section-order-list">
        '''

        for i, section in enumerate(sections):
            visible = section.get('visible', True)
            numbered = section.get('numbered', True)
            section_name = section.get('name', section['id'].title())

            html += f'''
                <li class="section-item {'visible' if visible else 'hidden'}"
                    data-id="{section['id']}"
                    data-visible="{str(visible).lower()}"
                    data-numbered="{str(numbered).lower()}">
                    <span class="drag-handle">
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                            <circle cx="4" cy="4" r="1.5"/>
                            <circle cx="4" cy="8" r="1.5"/>
                            <circle cx="4" cy="12" r="1.5"/>
                            <circle cx="10" cy="4" r="1.5"/>
                            <circle cx="10" cy="8" r="1.5"/>
                            <circle cx="10" cy="12" r="1.5"/>
                        </svg>
                    </span>
                    <span class="section-number"></span>
                    <input type="text" class="section-name-input" value="{section_name}" data-original="{section_name}">
                    <button type="button" class="visibility-toggle" title="Toggle visibility">
                        <svg class="eye-open" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                            <circle cx="12" cy="12" r="3"/>
                        </svg>
                        <svg class="eye-closed" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                            <line x1="1" y1="1" x2="23" y2="23"/>
                        </svg>
                    </button>
                </li>
            '''

        html += '''
            </ul>
            <button type="button" class="reset-sections-btn" id="reset-sections">Reset to Default</button>
        </div>
        '''

        return mark_safe(html)

    def value_from_datadict(self, data, files, name):
        return data.get(name)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'section_order': SectionOrderWidget(),
        }


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
    form = ProfileForm
    list_display = ['name', 'title', 'email']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'title', 'subtitle', 'bio')
        }),
        ('Contact', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Media', {
            'fields': ('profile_image', 'resume')
        }),
        ('Display Options', {
            'fields': ('show_calendly_cta', 'show_normal_theme'),
            'description': 'Control visibility of various page elements'
        }),
        ('Section Order', {
            'fields': ('section_order',),
            'description': 'Drag and drop to reorder sections. The numbers next to each section title on your site will update automatically.',
            'classes': ('wide',),
        }),
    )


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
