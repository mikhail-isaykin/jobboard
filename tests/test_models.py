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
