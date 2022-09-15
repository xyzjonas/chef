<template>
  <div>

    <nav class="navbar is-primary" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <router-link :to="{ name: 'home' }" class="navbar-item">
          <img src="../assets/favicon.png" alt="Logo"><span class="ml-2">
          <strong>CHEF</strong></span>
        </router-link>
      </div>

      <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <router-link :to="{ name: 'recipes'}" class="button is-primary mx-0">
            <span class="icon is-small">
              <i class="fas fa-list"></i>
            </span>
            <strong>All</strong>
          </router-link>
          <router-link :to="{ name: 'newcategory'}" class="button is-primary mx-0 pl-0">
            <strong>Add Category</strong>
          </router-link>
          <router-link :to="{ name: 'new'}" class="button is-light">
            <span class="icon is-small">
              <i class="fas fa-plus"></i>
            </span>
            <span>Recipe</span>
          </router-link>
        </div>
      </div>
      </div>
    </nav>

  </div>
</template>
