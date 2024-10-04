<template>
  <div class="frontpage">
    <h1>Welcome to the Ultimate Lineup Picker</h1>
    <p>
      The Ultimate Lineup Picker is a tool that uses sportsbook player props to infer fantasy points for players.
    </p>
    <p>
      Using these inferred points, it will automatically set up the best lineup given a particular team.
    </p>
    <h2>Input Team Below</h2>
      <div class="playerInput">
        <form @submit.prevent="addPlayer">
          <input v-model="newPlayer" required placeholder="Type Player Name">
          <button>Submit Player to Roster</button>
        </form>
        <ul>
          <li v-for="player in players" :key="player.id">
            {{ player.name }}
            <button @click="removePlayer(player)">Remove Player</button>
          </li>
        </ul>
        <button @click="analyzeRoster">Analyze Roster</button>
      </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

let id = 0

const newPlayer = ref('')
const players = ref([])

function addPlayer() { // eslint-disable-line no-unused-vars
  players.value.push({ id: id++, name: newPlayer.value })
}

function removePlayer(player) { // eslint-disable-line no-unused-vars
  players.value = players.value.filter((t) => t !== player)
}

function analyzeRoster() { // eslint-disable-line no-unused-vars
  if (players.value.length < 1) {
    alert("Must input at least 1 player")
  } else {
    console.log(players.value)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
ul {
  list-style-type: none;
}
</style>
