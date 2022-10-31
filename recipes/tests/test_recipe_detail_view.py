from django.urls import resolve, reverse
from recipes.views import site

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewsTest(RecipeTestBase):

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, site.RecipeDetail)

    def test_recipe_detail_returns_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page -It load one recipe'

        # need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse(
            'recipes:recipe',
            kwargs={'pk': 1}
        ))
        content = response.content.decode('utf-8')

        # check if one recipe exist
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Test recipe is_published False dont show"""
        # need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse(
            'recipes:recipe',
            kwargs={'pk': recipe.id}
        ))

        self.assertEqual(response.status_code, 404)
