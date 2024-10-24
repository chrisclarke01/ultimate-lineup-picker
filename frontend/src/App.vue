<template>
  <img alt="ULP logo" src="./assets/logo.png">
  <MainPage />
  <PlayerInput />
</template>

<script>
import PlayerInput from './components/PlayerInput.vue'
import MainPage from './components/MainPage.vue'
//import AnalyzedRoster from './components/AnalyzedRoster.vue'

export default {
  name: 'App',
  components: {
    MainPage,
    PlayerInput,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
