<template>
  <section>
    <div
      class="card container"
      @submit="login">
      <img
        alt="Logo"
        class="logo"
        src="@/assets/ankh.png"
        style="opacity: 1.0"
      >
      <form>
        <b-field
          :type="message ? 'is-danger' : 'is-primary'">
          <b-input
            v-model="username"
            placeholder="username"
            required/>
        </b-field>
        <b-field
          :message="message"
          :type="message ? 'is-danger' : 'is-primary'">
          <b-input
            v-model="password"
            password-reveal
            required
            icon-pack="fas"
            placeholder="Password"
            type="password"/>
        </b-field>
        <b-button
          native-type="submit"
          type="is-primary">
          <b-icon
            icon="sign-in-alt"
            pack="fas"/>
          <span>Login</span>
        </b-button>
      </form>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      username: '',
      password: '',
      message: ''
    }
  },
  mounted () {
    console.log('Vue code mounted in login()')
  },
  methods: {
    async login () {
      let data = {
        username: this.username,
        password: this.password
      }

      const response = await this.$http.post('login', data)
      if (response.data.error) {
        this.message = JSON.stringify(response.data.error)
      } else {
        this.$http.defaults.headers.common['Authorization'] = response.data.token
        this.$store.commit('login', {
          token: response.data.token,
          username: data.username,
          isAdmin: response.data.admin
        })
      }
      this.$router.push('/')
    },
    login2: function () {
      let data = {
        username: this.username,
        password: this.password
      }

      this.$http.post('login', data)
        .then(response => {
          console.log('entry of login response')
          if (response.data.error) {
            this.message = JSON.stringify(response.data.error)
            return
          }
          this.$http.defaults.headers.common['Authorization'] = response.data.token
          console.log('is admin: ', response.data.admin)
          this.$store.commit('login', {
            token: response.data.token,
            username: data.username,
            isAdmin: response.data.admin
          })

          this.$router.push('/')
        })
        .catch(error => {
          this.message = error.data.message || JSON.stringify(error)
          console.log('error of login response', this.message)
        })
        .finally(result => {
          console.log('hiero', result)
        })
    }
  }
}
</script>

<style>
.card {
  max-width: 500px;
  padding: 20px;
  background: rgba(255,255,255,0.3);
}

.logo {
  width: 150px;
}

body {
  background-image: url('~@/assets/background.jpg');
  background-size: cover;
  min-width: 100%;
  background-repeat: no-repeat;
  background-position: center center;
}
</style>
