import {
  createRouter,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import CategoryListingView from "@/views/CategoryListingView.vue";
import Recipes from "@/views/Recipes.vue";
import Recipe from "@/views/Recipe.vue";
import RecipeEditView from "@/views/RecipeEditView.vue";
import CategoryView from "@/views/CategoryView.vue";
import CategoryNewView from "@/views/CategoryNewView.vue";
import CategoryEditView from "@/views/CategoryEditView.vue";
import NewRecipe from "@/views/NewRecipe.vue";
import Ingredients from "@/views/Ingredients.vue";
import Ingredient from "@/views/Ingredient.vue";
import NotFoundView from "@/views/NotFoundView.vue";

const router = createRouter({
  // history: createWebHashHistory(import.meta.env.BASE_URL),
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "recipes",
      component: Recipes,
    },
    {
      path: "/ingredients",
      name: "ingredients",
      component: Ingredients,
    },
    {
      path: "/ingredients/:id",
      name: "ingredient",
      component: Ingredient,
    },
    {
      path: "/recipes/new",
      name: "new",
      component: NewRecipe,
    },
    {
      path: "/recipes/:id",
      name: "recipe",
      component: Recipe,
    },
    {
      path: "/recipes/:id/edit",
      name: "editrecipe",
      component: RecipeEditView,
    },
    {
      path: "/categories",
      name: "categories",
      component: CategoryListingView,
    },
    {
      path: "/categories/:id",
      name: "category",
      component: CategoryView,
    },
    {
      path: "/recipes/newcategory",
      name: "newcategory",
      component: CategoryNewView,
    },
    {
      path: "/categories/:id/edit",
      name: "editcategory",
      component: CategoryEditView,
    },
    {
      path: "/404",
      name: "notfound",
      component: NotFoundView,
    },
    {
      path: '/:catchAll(.*)',
      component: NotFoundView,
    }
  ],
});

export default router;
