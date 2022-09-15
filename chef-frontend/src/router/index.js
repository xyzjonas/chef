import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Recipes from "../views/Recipes.vue";
import Recipe from "../views/Recipe.vue";
import CategoryView from "../views/CategoryView.vue";
import NewCategoryView from "../views/NewCategoryView.vue";
import NewRecipe from "../views/NewRecipe.vue";
import Ingredients from "../views/Ingredients.vue";
import Ingredient from "../views/Ingredient.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/recipes",
    name: "recipes",
    component: Recipes
  },
  {
    path: "/ingredients",
    name: "Ingredients",
    component: Ingredients
  },
  {
    path: "/ingredients/:id",
    name: "Ingredient",
    component: Ingredient
  },
  {
    path: "/recipes/new",
    name: "new",
    component: NewRecipe
  },
  {
    path: "/recipes/newcategory",
    name: "newcategory",
    component: NewCategoryView
  },
  {
    path: "/recipes/:id",
    name: "recipe",
    component: Recipe
  },
  {
    path: "/categories/:id",
    name: "category",
    component: CategoryView
  },
];

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes
});

export default router;
