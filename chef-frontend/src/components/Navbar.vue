<template>
  <div>

    <nav class="navbar is-dark is-fixed-top">
      <div class="container">
        <div class="navbar-brand">
          <a href="/" class="navbar-item">
            <img src="../assets/favicon.png" alt="Logo"><span class="ml-2"><strong>CHEF</strong></span>
          </a>
          <a v-on:click="toggleMenu" ref="nav-burger" class="navbar-burger" data-target="navbarMenuHeroB">
            <span></span>
            <span></span>
            <span></span>
          </a>
        </div>
        <div ref="nav-menu" class="navbar-menu is-dark">
          <div class="navbar-end" style="text-align: center;">
            <router-link v-on:click.native="closeMenu" :to="{ name: 'Home' }" class="navbar-item">Home</router-link>
            <router-link :to="{ name: 'Recipes' }" v-on:click.native="closeMenu" class="navbar-item">All recipes</router-link>
            <router-link :to="{ name: 'Roulette' }" v-on:click.native="closeMenu" class="navbar-item">Roulette</router-link>
            <router-link :to="{ name: 'History' }" v-on:click.native="closeMenu" class="navbar-item">History</router-link>
            <router-link :to="{ name: 'NewRecipe' }" v-on:click.native="closeMenu" class="navbar-item">New</router-link>
          </div>
        </div>
      </div>
    </nav>

  </div>
</template>


<script>
export default {
  data() {
    return {
      heroTitles: {
        Home: { title: 'Chef', subtitle: '...only the best recipes manager' },
        Recipes: { title: 'Recipe finder', subtitle: '' },
        Roulette: { title: 'Roulette', subtitle: '' },
        History: { title: 'History', subtitle: '' },
        NewRecipe: { title: 'New', subtitle: '' },
        Recipe: { title: 'Recipe detail', subtitle: '' },
      }
    }
  },
  methods : {
    openMenu() {
      console.log("opening menu...")
      this.$refs["nav-burger"].classList.add("is-active");
      this.$refs["nav-menu"].classList.add("is-active");
    },
    closeMenu() {
      console.log("closing menu...")
      this.$refs["nav-burger"].classList.remove("is-active");
      this.$refs["nav-menu"].classList.remove("is-active");
    },
    toggleMenu() {
      console.log("toggled");
      if (this.$refs["nav-burger"].classList.contains("is-active")) {
        this.$refs["nav-burger"].classList.remove("is-active");
        this.$refs["nav-menu"].classList.remove("is-active");
      } else {
        this.$refs["nav-burger"].classList.add("is-active");
        this.$refs["nav-menu"].classList.add("is-active");
      }
    }
  },
  updated() {
    this.closeMenu();
  }
}
</script>