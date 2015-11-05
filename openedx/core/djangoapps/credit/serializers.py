""" Credit API Serializers """

from rest_framework import serializers
from opaque_keys.edx.keys import CourseKey
from opaque_keys import InvalidKeyError

from openedx.core.djangoapps.credit.models import CreditCourse, CreditProvider, CreditEligibility


class CourseKeyField(serializers.Field):
    """
    Serializer field for a model CourseKey field.
    """

    def to_representation(self, data):
        """Convert a course key to unicode. """
        return unicode(data)

    def to_internal_value(self, data):
        """Convert unicode to a course key. """
        try:
            return CourseKey.from_string(data)
        except InvalidKeyError as ex:
            raise serializers.ValidationError("Invalid course key: {msg}".format(msg=ex.msg))


class CreditCourseSerializer(serializers.ModelSerializer):
    """ CreditCourse Serializer """

    course_key = CourseKeyField()

    class Meta(object):
        model = CreditCourse
        exclude = ('id',)


class CreditProviderSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='provider_id')
    description = serializers.CharField(source='provider_description')
    status_url = serializers.URLField(source='provider_status_url')
    url = serializers.URLField(source='provider_url')

    class Meta(object):
        model = CreditProvider
        fields = ('id', 'display_name', 'url', 'status_url', 'description', 'enable_integration',
                  'fulfillment_instructions', 'thumbnail_url',)


class CreditEligibilitySerializer(serializers.ModelSerializer):
    course_key = serializers.SerializerMethodField()

    def get_course_key(self, obj):
        return unicode(obj.course.course_key)

    class Meta(object):
        model = CreditEligibility
        fields = ('username', 'course_key', 'deadline',)
