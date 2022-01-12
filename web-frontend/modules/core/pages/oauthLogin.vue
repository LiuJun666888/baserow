<!--<template>-->
<!--  <div>{{ title }}</div>-->

<!--</template>-->
<script>

export default {
  name: 'oauthLogin',
  data() {
    return {
      title: 'ok'//重定向时根据标题名调用
    }
  },
  //空页面，获得code后调用后端oauth接口
  mounted() {
    this.title = 'create'
    this.authLogin()

  },
  methods: {
    async authLogin() {
      const query = this.$route.query
      if (query.code) {
        this.title = 'get'
        await this.$store.dispatch('auth/oauthLogin', query.code)
        this.title = 'good'
        await this.$router.push({ path: '/' })
      } else {
        this.title = 'no code'
      }

    }
  },
  render: function (h) {
    return h() // 避免警告
  },

}
</script>

