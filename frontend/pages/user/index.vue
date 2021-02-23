<template>
<div class="container is-fluid box has-background-purp">
  <div class="columns">
    <div class="column is-1  " >
      <navmenu />
    </div>
    <div class="column">

    </div>
  </div>

</div>
</template>

<script>
import Nav from '~/components/user/nav.vue'

export default {
  data() {
    return {
      isActive: true
    }
  },
  components: {
    'navmenu': Nav
  }
}
</script>
