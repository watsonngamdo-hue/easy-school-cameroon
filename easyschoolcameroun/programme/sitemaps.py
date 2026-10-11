# programme/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Matiere, Lesson


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            'programme:programme',
            "programme:about",
            "programme:level",
            "programme:contact",
            "programme:billing",
        ]

    def location(self, item):
        return reverse(item)


class CourseSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Matiere.objects.all()

    def location(self, obj):
        return f"/courses/{obj.slug}"
  
class MatiereSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Matiere.objects.all()

    def location(self, obj):
        return f"/courses/{obj.slug}"   
    

class LessonSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Lesson.objects.all()

    def location(self, obj):
        return f"/lecon_detail/{obj.niveau.slug}/{obj.matiere.slug}/{obj.slug}"    