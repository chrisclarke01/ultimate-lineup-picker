<template>
  <div class="frontpage">
    <h2>Input Team Below</h2>
      <div class="playerInput">
        <form @submit.prevent="addPlayer()">
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

<script>
// https://stackoverflow.com/questions/71819204/how-do-i-change-a-boolean-variables-value-from-a-grandchild-component-in-this-v
// for when conditional rendering needs to happen
  export default {
    name: 'MyButton',
    props: {
      label: String,
      isVisible: Boolean
    },

    emits: [
      'toggleVisibility',
    ],

    methods: {
      handleClick() {
        this.$emit('toggleVisibility')
      }
    }
  }
</script>

<script setup>
import { ref } from 'vue'

// Give each player a unique ID
let id = 0

// Create a newPlayer variable and an empty list to contain passed in players
const newPlayer = ref('')
const players = ref([])

// Add a player to the list
function addPlayer() { // eslint-disable-line no-unused-vars
  players.value.push({ id: id++, name: newPlayer.value })
  newPlayer.value = ''
}

// Remove a player from the list
function removePlayer(player) { // eslint-disable-line no-unused-vars
  players.value = players.value.filter((t) => t !== player)
}

// Pass roster information for analysis
function analyzeRoster() { // eslint-disable-line no-unused-vars
  if (players.value.length < 9) {
    alert("Must input at least 9 players")
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
