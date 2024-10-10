<template>
  <div class="frontpage">
    <h2>Input Team Below</h2>
      <div class="playerInput">
        <form @submit.prevent="addPlayer()">
          <input v-model="name" required placeholder="Type Player Name">
          <select v-model="position" name="position">
            <option value="QB">QB</option>
            <option value="WR">WR</option>
            <option value="RB">RB</option>
            <option value="TE">TE</option>
            <option value="DST">D/ST</option>
            <option value="K">K</option>
          </select>
          <select v-model="team" name="team">
            <option value="Arizona Cardinals">Arizona Cardinals</option>
            <option value="Atlanta Falcons">Atlanta Falcons</option>
            <option value="Baltimore Ravens">Baltimore Ravens</option>
            <option value="Buffalo Bills">Buffalo Bills</option>
            <option value="Carolina Panthers">Carolina Panthers</option>
            <option value="Chicago Bears">Chicago Bears</option>
            <option value="Cincinnati Bengals">Cincinnati Bengals</option>
            <option value="Cleveland Browns">Cleveland Browns</option>
            <option value="Dallas Cowboys">Dallas Cowboys</option>
            <option value="Denver Broncos">Denver Broncos</option>
            <option value="Detroit Lions">Detroit Lions</option>
            <option value="Green Bay Packers">Green Bay Packers</option>
            <option value="Houston Texans">Houston Texans</option>
            <option value="Indianapolis Colts">Indianapolis Colts</option>
            <option value="Jacksonville Jaguars">Jacksonville Jaguars</option>
            <option value="Kansas City Chiefs">Kansas City Chiefs</option>
            <option value="Las Vegas Raiders">Las Vegas Raiders</option>
            <option value="Los Angeles Chargers">Los Angeles Chargers</option>
            <option value="Los Angeles Rams">Los Angeles Rams</option>
            <option value="Miami Dolphins">Miami Dolphins</option>
            <option value="Minnesota Vikings">Minnesota Vikings</option>
            <option value="New England Patriots">New England Patriots</option>
            <option value="New Orleans Saints">New Orleans Saints</option>
            <option value="New York Giants">New York Giants</option>
            <option value="New York Jets">New York Jets</option>
            <option value="Philadelphia Eagles">Philadelphia Eagles</option>
            <option value="Pittsburgh Steelers">Pittsburgh Steelers</option>
            <option value="San Francisco 49ers">San Francisco 49ers</option>
            <option value="Seattle Seahawks">Seattle Seahawks</option>
            <option value="Tampa Bay Buccaneers">Tampa Bay Buccaneers</option>
            <option value="Tennessee Titans">Tennessee Titans</option>
            <option value="Washington Commanders">Washington Commanders</option>
          </select>
          <button>Submit Player to Roster</button>
        </form>
        <ul>
          <li v-for="player in players" :key="player.id">
            {{ player.position }}: {{ player.name }}, {{ player.team }}
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
import axios from 'axios'

// Give each player a unique ID
let id = 0

// Create a newPlayer variable and an empty list to contain passed in players
const name = ref('')
const position = ref('')
const team = ref('')
const players = ref([])

// Add a player to the list
function addPlayer() { // eslint-disable-line no-unused-vars
  players.value.push({ id: id++, name: name.value, position: position.value, team: team.value })
  name.value = ''
  position.value = ''
  team.value = ''
}

// Remove a player from the list
function removePlayer(player) { // eslint-disable-line no-unused-vars
  players.value = players.value.filter((t) => t !== player)
}

// Pass roster information for analysis
function analyzeRoster() { // eslint-disable-line no-unused-vars
  axios.post(
    'http://localhost:8080/players',
    JSON.stringify({
      name: name.value,
      position: position.value,
      team: team.value,
    }), {
      headers: {
        // Remove headers
      }
    }
  ).then(response => {
    console.log(response.data)
  }).catch(error => {
    console.log(error);
  });
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
ul {
  list-style-type: none;
}
</style>
