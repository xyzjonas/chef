import Vue from "vue";
import VueRouter from "vue-router";
import History from "../views/History.vue";
import Home from "../views/Home.vue";
import Recipes from "../views/Recipes.vue";
import Recipe from "../views/Recipe.vue";
import NewRecipe from "../views/NewRecipe.vue";
import Ingredients from "../views/Ingredients.vue";
import Ingredient from "../views/Ingredient.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/recipes",
    name: "Recipes",
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
    name: "NewRecipe",
    component: NewRecipe
  },
  {
    path: "/recipes/:id",
    name: "Recipe",
    component: Recipe
  },
  {
    path: "/",
    name: "Roulette",
    component: History
  },
  {
    path: "/",
    name: "History",
    component: History
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
