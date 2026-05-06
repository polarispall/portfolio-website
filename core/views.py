from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from .models import Profile, SocialLink, SkillCategory, Skill, Experience, Education, Project, Certificate


class PortfolioView(TemplateView):
    template_name = 'portfolio/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        context['social_links'] = SocialLink.objects.filter(is_active=True)

        # Skills grouped by dynamic categories (only active skills and categories)
        context['skill_categories'] = SkillCategory.objects.filter(
            is_active=True
        ).prefetch_related('skills').all()
        context['skills'] = Skill.objects.filter(is_active=True)

        context['experiences'] = Experience.objects.filter(is_active=True)
        context['education'] = Education.objects.filter(is_active=True)
        context['projects'] = Project.objects.filter(is_active=True)
        context['featured_projects'] = Project.objects.filter(is_featured=True, is_active=True)
        context['certificates'] = Certificate.objects.all()
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/detail.html'
    slug_field = 'slug'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        context['social_links'] = SocialLink.objects.filter(is_active=True)
        return context

    def get_queryset(self):
        return Project.objects.filter(is_active=True)
