<template>
  <b-menu class="box">
    <b-menu-list label="Menu">
      <b-menu-item to="/user" tag="nuxt-link" label="Profile Settings" active-class="is-active" exact></b-menu-item>
      <b-menu-item to="/user/tokens" tag="nuxt-link" label="Tokens" active-class="is-active" exact></b-menu-item>
    </b-menu-list>
    <b-menu-list label="Actions">
      <b-menu-item to="/login" tag="nuxt-link" label="Login" active-class="is-active" exact></b-menu-item>
      <b-menu-item tag="a" href="http://localhost:8000/logout" label="Logout"></b-menu-item>
    </b-menu-list>
  </b-menu>
</template>

<script>
export default {
  data() {
    return {
      isActive: true
    }
  }
}
</script>