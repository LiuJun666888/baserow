<script>
export default {
  fetch({ store, redirect }) {
    // const name = store.getters['auth/isAuthenticated'] ? 'dashboard' : 'login'
    // redirect( {name} )
    const name = store.getters['auth/isAuthenticated'] ? 'dashboard' : 'https://passport.felo.me/oauth/authorize?response_type=code&client_id=ydFC1EF960E67640199449EB2C6A6F3921&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2FoauthLogin'
    redirect( name )
  },
}
</script>
