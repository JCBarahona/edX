"""
Django sudo utils.
"""

from django.conf import settings

from eventtracking import tracker
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey

from lms.djangoapps.courseware.access import get_user_role


def track_sudo_event(request, user, region, next_url, social_auth=False):
    """
    Track django sudo requests.
    """
    try:
        course_key = CourseKey.from_string(region)
    except InvalidKeyError:
        course_key = None

    user_role = None
    if region == "django_admin":
        user_role = region
    elif course_key:
        user_role = get_user_role(user, course_key)

    params = {
        "is_sudo": False,
        "success": False,
        "region": region,
        "user_id": user.id,
        "user_role": user_role,
        "next_url": next_url,
        "service": settings.SERVICE_VARIANT,
        "auth_type": "edx_login"
    }
    if social_auth:
        params["auth_type"] = "third_party_auth"

    if request.is_sudo(region):
        params['is_sudo'] = True
        params['success'] = True

    tracker.emit(
        "edx.user.sudo.reauthenticated",
        params

    )
