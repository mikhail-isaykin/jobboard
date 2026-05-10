from django.test import TestCase
from django.contrib.auth import get_user_model
from companies.models import Company, Vacancy, HiddenVacancy

User = get_user_model()


class VacancyQuerySetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.owner = User.objects.create_user(username='owner', password='pass')
        self.company = Company.objects.create(owner=self.owner, name='TestCo')
        self.vacancy = Vacancy.objects.create(
            company=self.company,
            title='Dev',
            city='Moscow',
            salary_type='monthly',
            description='Test',
        )

    def test_hidden_vacancy_excluded(self):
        HiddenVacancy.objects.create(user=self.user, vacancy=self.vacancy)
        qs = Vacancy.objects.visible_for_user(self.user)
        self.assertNotIn(self.vacancy, qs)

    def test_visible_vacancy_included(self):
        qs = Vacancy.objects.visible_for_user(self.user)
        self.assertIn(self.vacancy, qs)


def test_unauthenticated_user_sees_all(self):
    HiddenVacancy.objects.create(user=self.user, vacancy=self.vacancy)
    from django.contrib.auth.models import AnonymousUser
    qs = Vacancy.objects.visible_for_user(AnonymousUser())
    self.assertIn(self.vacancy, qs)

def test_multiple_hidden_vacancies_excluded(self):
    vacancy2 = Vacancy.objects.create(
        company=self.company,
        title='Designer',
        city='Moscow',
        salary_type='monthly',
        description='Test',
    )
    HiddenVacancy.objects.create(user=self.user, vacancy=self.vacancy)
    HiddenVacancy.objects.create(user=self.user, vacancy=vacancy2)
    qs = Vacancy.objects.visible_for_user(self.user)
    self.assertEqual(qs.count(), 0)

def test_hidden_vacancy_is_user_specific(self):
    """Vacancy hidden by one user remains visible to another."""
    other_user = User.objects.create_user(username='other', password='pass')
    vacancy2 = Vacancy.objects.create(
        company=self.company,
        title='Designer',
        city='SPb',
        salary_type='monthly',
        description='Test',
    )
    vacancy3 = Vacancy.objects.create(
        company=self.company,
        title='Manager',
        city='Kazan',
        salary_type='weekly',
        description='Test',
    )
        # self.user hides vacancy and vacancy2
    HiddenVacancy.objects.create(user=self.user, vacancy=self.vacancy)
    HiddenVacancy.objects.create(user=self.user, vacancy=vacancy2)

    # other_user hides only vacancy3
    HiddenVacancy.objects.create(user=other_user, vacancy=vacancy3)

    qs_user = Vacancy.objects.visible_for_user(self.user)
    qs_other = Vacancy.objects.visible_for_user(other_user)

    self.assertNotIn(self.vacancy, qs_user)
    self.assertNotIn(vacancy2, qs_user)
    self.assertIn(vacancy3, qs_user)

    self.assertIn(self.vacancy, qs_other)
    self.assertIn(vacancy2, qs_other)
    self.assertNotIn(vacancy3, qs_other)

    self.assertEqual(qs_user.count(), 1)
    self.assertEqual(qs_other.count(), 2)