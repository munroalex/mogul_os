export const state = () => ({
  counter: 0,
  lastUri: '/',
})

export const mutations = {
  increment(state) {
    state.counter++
  },
  setUri(state, payload)
  {
  	state.lastUri = payload
  }
}
