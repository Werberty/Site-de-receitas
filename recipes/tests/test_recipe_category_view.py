from django.urls import resolve, reverse
from recipes.views import site

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewsTest(RecipeTestBase):

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category',
                               kwargs={'category_id': 1000}))
        self.assertIs(view.func.view_class, site.RecipeListViewCategory)

    def test_recipe_category_returns_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        # need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        # check if one recipe exist
        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipe_not_published(self):
        """Test recipe is_published False dont show"""
        # need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse(
            'recipes:recipe',
            kwargs={'pk': recipe.category.id}
        ))

        self.assertEqual(response.status_code, 404)
