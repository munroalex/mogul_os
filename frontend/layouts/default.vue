<template>
  <div class="has-navbar-fixed-top">
    <div id="pageloader" class="pageloader is-left-to-right is-theme"></div>  
    <nav x-data="initNavbar()" class="hero navbar is-fixed-top is-transparent">
        <div class="container is-fluid">
            <!-- Brand -->
            <div class="navbar-brand" >
                <a href="/" class="navbar-item">
                    <img src="https://www.eve-mogul.com/assets/images/happyyeti.png" alt="">&nbsp;
                    <b style="color: #fff;">Mogul OS</b>
                </a>
                <!-- Responsive toggle -->
                <div class="navbar-burger" @click="openMobileMenu()">
                    <div class="menu-toggle">
                        <span class="icon-box-toggle">
                            <span class="rotate">
                                <i class="icon-line-top"></i>
                                <i class="icon-line-center"></i>
                                <i class="icon-line-bottom"></i>
                            </span>
                        </span>
                    </div>
                </div>
                <!-- Menu item -->
                <div class="navbar-item is-nav-link">
                    <NuxtLink  class="is-centered-responsive" active-class="button is-link is-outlined" to="/hangar">Trading Tools</NuxtLink >
                </div>
                <!-- Menu item -->
                <div class="navbar-item is-nav-link">
                    <a class="is-centered-responsive" href="ico.html">Tools</a>
                </div>
                <!-- Menu item -->
                <div class="navbar-item is-nav-link">
                    <a class="is-centered-responsive" href="ico.html">Exchange</a>
                </div>
                <!-- Menu item -->
                <div class="navbar-item is-nav-link">
                    <a class="is-centered-responsive" href="roadmap.html">Leaderboards {{ last_uri }}</a>
                </div>
            </div>
            <!-- Menu -->
            <div id="navbarMenu" class="navbar-menu light-menu">
                <div class="navbar-end">
                    <!-- Menu item -->
                    <div class="navbar-item is-nav-link subscribe-block">
                        <div class="field has-addons">
                          <div class="control">
                            <input class="input" style="background: #0f0330; color: #fff; border: 0px;" placeholder="Tritanium..." type="text">
                          </div>
                          <div class="control">
                            <a class="button k-button k-primary raised has-gradient">
                              Search
                            </a>
                          </div>
                        </div>
                    </div>
                    <!-- Sign up -->
                    <div class="navbar-item">
                        <a href="/user" class="button k-button k-primary raised has-gradient" v-show="logged_in">
                            <span class="text">{{ username }}</span>
                            <span class="front-gradient"></span>
                        </a>

                        <a href="http://localhost:8000/login" class="button k-button k-primary raised has-gradient slanted" v-show="!logged_in">
                            <span class="text">Login/Register</span>
                            <span class="front-gradient"></span>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </nav>
    <div class="dark-wrapper has-navbar-fixed-top" style="padding-top: 4rem;">
      <Nuxt />
    </div>
    
    <footer class="krypton-footer">
      This is a footer
    </footer>    <!-- Back To Top Button -->
    
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  data() {
    return {
      'test': true
    }
  },
  head() {
    return {
      htmlAttrs: {
          style: ''
      }
    }
  },
  computed: {
    // mix the getters into computed with object spread operator
    todos () {
      return this.$store.state.todos.list
    },
    username()
    {
      return this.$store.state.user.username
    },
    logged_in()
    {
      return this.$store.state.user.logged_in
    },
    last_uri()
    {
      return this.$store.state.lastUri
    }
  },
  methods: {
    ...mapActions({
      getUserDetails: 'user/getUserDetails', // map `this.increment()` to `this.$store.dispatch('increment')`
      checkAuthStatus: 'user/checkAuthStatus', // map `this.increment()` to `this.$store.dispatch('increment')`
    }
    ),

  },
  components: {

  },
  created() {
    if(!this.logged_in)
    {
      this.getUserDetails()
      
    }
    this.checkAuthStatus()

  }
}
</script>
<style>
.krypton-subscribe-input::placeholder {
  color: #fff !important;
}
.input::placeholder {
  color: #fff !important;
}
::placeholder { 
color: #fff !important;
}
</style>