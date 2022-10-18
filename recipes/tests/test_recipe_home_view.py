
from unittest.mock import patch

from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewsTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_shows_no_recipes_fund_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            '<h1>No recipes found here</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        # need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # check if one recipe exist
        self.assertIn('Recipe title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipe_not_published(self):
        """Test recipe is_published False dont show"""
        # need a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        # check if one recipe exists
        self.assertIn(
            '<h1>No recipes found here</h1>',
            response.content.decode('utf-8')
        )

    def test_invalid_page_query_uses_page_one(self):  # noqa: E501
        # If it cannot convert query string to integer, set current_page as 1
        self.make_recipe_in_batch(qtd=8)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=<2>')

            self.assertEqual(
                response.context['recipes'].number, 1)

            response = self.client.get(reverse('recipes:home') + '?page=2')

            self.assertEqual(
                response.context['recipes'].number, 2)

    # @patch('recipes.views.PER_PAGE', new=4)
    def test_recipe_home_is_paginated(self):
        self.make_recipe_in_batch(qtd=8)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)
