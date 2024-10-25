<template>
  <div class="frontpage">
    <img alt="ULP logo" :src='logo'>
    <h1>Welcome to the Ultimate Lineup Picker</h1>
    <p>
      The Ultimate Lineup Picker is a tool that uses sportsbook player props to infer fantasy points for players.
      <br>
      Using these inferred points, it will automatically set up the best lineup given a particular team.
    </p>
  </div>
</template>

<script setup>
  import logo from '@/assets/logo.png'
</script>