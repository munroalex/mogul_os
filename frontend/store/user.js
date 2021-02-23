import axios from 'axios'

const api = axios.create({
  withCredentials: true
})

export const state = () => ({
  username: "Testing123",
  object: {},
  logged_in: false,

})

export const mutations = {
  SET_USER(state, payload) {
    state.username = payload.username
    state.object = payload
    state.logged_in = true
  },
  UNSET_USER(state) {
    state.username = null,
    state.object = {},
    state.logged_in = false
  }
}

export const actions = {
  getUserDetails({commit}) {
    api.get('http://localhost:8000/api/v1/user/')
    .then(response => {
      commit('SET_USER', response.data)
    }).catch(error => {
        console.log(error)
    });
  },
  checkAuthStatus({commit})
  {
    api.get('http://localhost:8000/api/v1/user/')
    .then(response => {
      // We're good
    }).catch(error => {
        commit('UNSET_USER')
    });
  }
}

