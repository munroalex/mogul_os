import Vue from 'vue'

Vue.filter('capitalize', function (value) {
  if (!value) return ''
  value = value.toString()
  return value.charAt(0).toUpperCase() + value.slice(1)
})

Vue.filter('cleanscopes', function (value) {
  if (!value) return ''
  value = value.toString()
  value = value.split(".")
  return value[1];
})