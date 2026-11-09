from django.shortcuts import render

from .models import Project


def project_list(request):
    return render(request, "projects/list.html", {"projects": Project.objects.filter(is_published=True)})
