<template>
  <PlayerCard />
  <MainPage />
  <LineupPicker />
</template>

<script setup>
  import MainPage from '@/components/MainPage.vue'
  import LineupPicker from './components/LineupPicker.vue';
  import PlayerCard from './components/PlayerCard.vue';
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
