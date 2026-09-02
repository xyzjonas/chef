import {
  createRouter,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import Recipes from "@/views/Recipes.vue";
import Recipe from "@/views/Recipe.vue";
import RecipeEditView from "@/views/RecipeEditView.vue";
import Ingredients from "@/views/Ingredients.vue";
import Ingredient from "@/views/Ingredient.vue";
import TagsView from "@/views/TagsView.vue";
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
      path: "/tags",
      name: "tags",
      component: TagsView,
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
