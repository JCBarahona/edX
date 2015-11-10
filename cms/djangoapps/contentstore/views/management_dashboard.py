"""
These views handle all actions in Studio related to management commands
"""
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods, require_GET

from edxmako.shortcuts import render_to_response
from opaque_keys.edx.keys import CourseKey

from contentstore.models import ManagementCommand
from contentstore.views.item import orphan_handler

__all__ = [
    'dashboard',
]


log = logging.getLogger(__name__)



def get_management_commands():
    """
    Fetches all management commands.
    """
    commands = ManagementCommand.objects.all()
    return commands


# pylint: disable=unused-argument
@login_required
@ensure_csrf_cookie
@require_http_methods(("GET"))
def dashboard(request, course_key_string):
    """
    Escalate All commands dashboard.
    """
    course_usage_key = CourseKey.from_string(course_key_string)
    all_commands = get_management_commands()
    return render_to_response('management_dashboard.html', {
            'commands': all_commands
        })


# pylint: disable=unused-argument
@login_required
@require_http_methods(("GET"))
def print_draft_orphans(request, course_key_string):
    """
    Print orphans
    """
    orphans = orphan_handler(request, course_key_string)
    return render_to_response('management_command.html', {
            'command_output': orphans,
            'command_name' : 'draft_orphans'
        })


# pylint: disable=unused-argument
@login_required
@require_http_methods(("GET"))
def print_published_orphans(request, course_key_string):
    """
    Print publish orphans
    """
    course_key_string = course_key_string + '+branch@published-branch'
    orphans = orphan_handler(request, course_key_string)
    return render_to_response('management_command.html', {
            'command_output': orphans,
            'command_name' : 'published_orphans'
        })


# pylint: disable=unused-argument
@login_required
@require_http_methods(("GET"))
def force_publish_course(request, course_key_string):
    """
    Force publish a course
    """
    output = 'Not yet implemented.'
    return render_to_response('management_command.html', {
            'command_output': output,
            'command_name': 'force_publish'
        })