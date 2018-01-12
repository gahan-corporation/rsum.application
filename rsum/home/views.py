#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Views for the rsum home application."""
import datetime
import json
from collections import OrderedDict

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from home.export.word import ExportDocument

from home.models.section import Section
from home.models.profile import Profile


def index(request):
    """Load the index page of the rsum application.

    :param request: `django.http.HttpRequest` object for index page.
    :type request: object
    :return: HttpResponse object resulting from execution of render method.
    :rtype: object
    """
    profile = Profile.objects.get(name=settings.OWNER)

    sections = OrderedDict()
    sections_query = Section.objects.values()
    for section_item in sections_query:
        sections.update({
            section_item.get('name'): json.loads(section_item.get('content'))
        })

    skills = sections.get('skills')

    sections.update({'skills': calculate_skills(skills)})

    context = {
        'profile': profile,
        'sections': sections,
        'dir': settings.DIR,
    }

    return render(request, 'home/index.html', context)


def calculate_skills(skills):
    """Calculate necessary values for the skills progress bars.

    :param skills: The unmodified skills section.
    :type skills: OrderedDict
    :return: An updated Skills section with missing values filled in.
    :rtype: OrderedDict
    :raises: ValueError
    """
    begin = skills.get('start')
    current_year = float(datetime.date.today().strftime("%Y"))
    career_length = float(current_year) - float(begin)

    for name, skill in skills.items():
        if name != 'start':
            start_skill = float(skill.get('start'))
            years_skill = current_year - start_skill
            experience_value = years_skill / career_length * 100
            experience_string = "{0} year(s)".format(int(years_skill))

            skills.update({
                name: {
                    'name': skills.get(name).get('name'),
                    'start': skills.get(name).get('start'),
                    'experience_value': experience_value,
                    'experience_string': experience_string,
                }
            })

            # I don't much like nested for loops, but it's the only way.
            for sub_name, sub_skill in skill.items():
                if (
                        not isinstance(sub_skill, str) and
                        not isinstance(sub_skill, int)
                ):
                    start_sub = float(sub_skill.get('start'))
                    years_sub = current_year - start_sub
                    sub_experience_value = years_sub / career_length * 100
                    sub_experience_string = (
                        "{0} year(s)".format(int(years_sub))
                    )

                    skills.get(name).update({
                        sub_name: {
                            'name': sub_skill.get('name'),
                            'start': sub_skill.get('start'),
                            'experience_value': sub_experience_value,
                            'experience_string': sub_experience_string,
                        }
                    })
    return skills
