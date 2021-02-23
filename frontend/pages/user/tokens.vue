<template>
<div class="container is-fluid box has-background-purp">
  <div class="columns">
    <div class="column is-1  " >
      <navmenu />
    </div>
    <div class="column">
      <table class="table">
  <thead>
    <tr>
      <th>Character Name</th>
      <th>Token Type</th>
      <th>Scopes</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="token in tokens" v-if="token.scopes.length > 1">
      <td>{{ token.character_name }}</td>
      <td>{{ token.token_type }}</td>
      <td><div class="tags"><span v-for="scope in token.scopes" class="tag is-primary is-light">{{ scope | cleanscopes | capitalize }}</span></div></td>
    </tr>
    <tr><a href="http://localhost:8000/link/trade_character" class="button">Trade Character</a></tr>
  </tbody>
</table>

    </div>
  </div>

</div>
</template>

<script>
import Nav from '~/components/user/nav.vue'

export default {
  data() {
    return {
      tokens: null
    }
  },
  components: {
    'navmenu': Nav
  },
  created() {
    this.getTokens()
  },
  methods: {
    getTokens()
    {
      this.$axios.get('http://localhost:8000/api/v1/tokens/').then(response => {
      this.tokens = response.data;
    }).catch(error => {
        
    });
    }
  }
}
</script>
