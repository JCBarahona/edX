import factory
from factory.fuzzy import FuzzyText

from openedx.core.djangoapps.credit.models import CreditProvider, CreditEligibility, CreditCourse


class CreditCourseFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = CreditCourse

    course_key = FuzzyText(prefix='fake.org/', suffix='/fake.run')


class CreditProviderFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = CreditProvider

    provider_id = FuzzyText(length=5)


class CreditEligibilityFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = CreditEligibility

    course = factory.SubFactory(CreditCourseFactory)
