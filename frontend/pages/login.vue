<template>
  <div class="container">
    <center>

        <!-- Landing page Hero -->

        <section class="hero is-transparent">
            <!-- Hero Image and Title -->
            <div class="hero-body">
                <div class="container">
                    <div class="columns is-vcentered">
    
                        <!-- Landing page Title -->
                        <div class="column is-5 landing-caption">
                            <h1 class="title is-1 is-light is-semibold is-spaced main-title">Mogul OS</h1>
                            <h2 class="subtitle is-5 is-light is-thin">
                                Finishing up...<br>
                                <i>Redirecting you to {{ last_uri }}</i>
                            </h2>
                        </div>
                        <!-- Hero image -->
                        <div class="column is-7">
                            <figure class="image">
                                <img src="https://www.eve-mogul.com/assets/images/yetismirk.png" style="width: 317px; height: 578px;" alt="">
                            </figure>
                        </div>
                    </div>
                </div>
            </div>
    
        </section>
        <!-- /Landing page Hero -->
      </center>
      </div>
</template>

<script>
export default {
  components: {

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
  watch: {
    logged_in() {
      if(this.logged_in)
      {
        return this.$router.push(this.last_uri);
      }
    }
  }
}
</script>