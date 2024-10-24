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
      <div class="frontpage">
        <h2>Your Ideal Lineup</h2>
        <div class="results">
          <ul>
            <li v-for="player in analyzedPlayers" :key="player">
              {{ player.position }}: {{ player.name }}, Projected Points: {{ player.points }}
            </li>
          </ul>
        </div>
      <button @click="restart">Clear All Players & Lineup</button>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import axios from 'axios'

// Give each player a unique ID
let id = 0

// Create a newPlayer variable and an empty list to contain passed in players
const name = ref('')
const position = ref('')
const team = ref('')
let players = ref([
  // Temporary testing data
  {'id':'0', 'name':'Spencer Rattler', 'position':'QB', 'team':'New Orleans Saints'},
  {'id':'1', 'name':'Javonte Williams', 'position':'RB', 'team':'Denver Broncos'},
  {'id':'2', 'name':'Jaleel Mclaughlin', 'position':'RB', 'team':'Denver Broncos'},
  {'id':'3', 'name':'Alvin Kamara', 'position':'RB', 'team':'New Orleans Saints'},
  {'id':'4', 'name':'Jamaal Williams', 'position':'RB', 'team':'New Orleans Saints'},
  {'id':'5', 'name':'Courtland Sutton', 'position':'WR', 'team':'Denver Broncos'},
  {'id':'6', 'name':'Devaughn Vele', 'position':'WR', 'team':'Denver Broncos'},
  {'id':'7', 'name':'Bub Means', 'position':'WR', 'team':'New Orleans Saints'},
  {'id':'8', 'name':'Juwan Johnson', 'position':'TE', 'team':'New Orleans Saints'},
  {'id':'9', 'name':'Blake Grupe', 'position':'K', 'team':'New Orleans Saints'},
  {'id':'10', 'name':'Wil Lutz', 'position':'K', 'team':'Denver Broncos'},
  {'id':'11', 'name':'Denver Broncos', 'position':'DST', 'team':'Denver Broncos'},
  {'id':'12', 'name':'New Orleans Saints', 'position':'DST', 'team':'New Orleans Saints'},
  {'id':'13', 'name':'Bo Nix', 'position':'QB', 'team':'Denver Broncos'},
])

let analyzedPlayers = ref([])

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

// Clears all data
function restart() {
  players.value = [];
  analyzedPlayers.value = [];
}

// Pass roster information for analysis
function analyzeRoster() { // eslint-disable-line no-unused-vars
  axios.post(
    'http://localhost:5000/api/players',
    JSON.stringify({
      players: players.value
    }), {
      headers: {
        'Content-Type': 'application/json'
      }
    }
  ).then(response => {
    analyzedPlayers.value = response.data;
    console.log(analyzedPlayers.value);
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
