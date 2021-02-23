import http from 'http'

export default function ({ route , store}) {
	// Let's figure out how to store the current uri here
	var newuri = route.path
	
	store.commit('setUri', newuri)
}
