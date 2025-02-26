<template>
  <h2 @click='settingsChosen = !settingsChosen;' id='settingsButton'>
    Settings
  </h2>
  <div class='settings' v-if='settingsChosen'>
    <hr/>
    <label>
      Use Test Data Instead of Live Data
      <input type='checkbox' v-model='useTestData'>
    </label>
    <hr />
  </div>
  <h2>
    Input Team Below
  </h2>

  <!-- Input section -->
  <form id='playerInput' @submit.prevent='addPlayer()'>
    <input required id='nameInput' v-model='name' @input='generateCards(name)' placeholder='Type Player Name' >
    <ul id='playerOptions' v-for='player in playerOptions' :key='player.name'>
      <PlayerCard :name='player.name' :position='player.position' :team='player.team' @click='addPlayer(player)' />
    </ul>
  </form>

  <!-- Display all the players by using an unordered list. Dynamically renders based on the amount of players entered. -->
  <ul>
    <li v-for='player in players' :key='player.id'>
      {{ player.position }}: {{ player.name }}, {{ player.team }}
      <button @click='removePlayer(player)'>Remove Player</button>
    </li>
  </ul>
  <button @click='analyzeRoster'>Analyze Roster</button>
  <br/>
  <button @click='restart'>Clear All Players & Lineup</button>

  <div v-if='loading' class="spinner" />

  <!-- Only show the ideal lineup of players if the server response has been received. -->
  <div v-if='analyzedPlayers.length !== 0'>
    <h2>
      Your Ideal Lineup
    </h2>
    <ul>
      <li v-for='player in analyzedPlayers' :key="player.id">
        {{ player.position }}: {{ player.name }}, Projected Points: {{ player.points }}
      </li>
    </ul>
    <p>
      Remaining API Requests: {{ remainingRequests }}
    </p>
  </div>
</template>
  
<script setup>
  import { ref } from 'vue'
  import playerJson from '../assets/players.json';
  import PlayerCard from './PlayerCard.vue';

  // Flag to display the settings
  const settingsChosen = ref(false);

  // Flag to display a loading animation during backend calculation
  const loading = ref(false);

  // Minimum required amounts of every position
  const minQbNum = 1;
  const minRbNum = 2;
  const minWrNum = 2;
  const minTeNum = 1;
  const minFlexNum = 1;
  const minDstNum = 1;
  const minKNum = 1;

  // Track whether test or live data is to be used
  const useTestData = ref(false);
  
  // Give each player a unique ID, name, position, and team
  let id = 0;
  const name = ref('');
  const position = ref('');
  const team = ref('');

  // Store the input list of players and the output received from server.
  let players = ref([
    // Temporary testing data
    {'id':'0', 'name':'Spencer Rattler', 'position':'QB', 'team':'New Orleans Saints'},
    {'id':'13', 'name':'Bo Nix', 'position':'QB', 'team':'Denver Broncos'},
    {'id':'1', 'name':'Javonte Williams', 'position':'RB', 'team':'Denver Broncos'},
    {'id':'2', 'name':'Jaleel Mclaughlin', 'position':'RB', 'team':'Denver Broncos'},
    {'id':'3', 'name':'Alvin Kamara', 'position':'RB', 'team':'New Orleans Saints'},
    {'id':'4', 'name':'Jamaal Williams', 'position':'RB', 'team':'New Orleans Saints'},
    {'id':'5', 'name':'Courtland Sutton', 'position':'WR', 'team':'Denver Broncos'},
    {'id':'6', 'name':'Devaughn Vele', 'position':'WR', 'team':'Denver Broncos'},
    {'id':'7', 'name':'Bub Means', 'position':'WR', 'team':'New Orleans Saints'},
    {'id':'8', 'name':'Juwan Johnson', 'position':'TE', 'team':'New Orleans Saints'},
    {'id':'11', 'name':'Denver Broncos', 'position':'DST', 'team':'Denver Broncos'},
    {'id':'12', 'name':'New Orleans Saints', 'position':'DST', 'team':'New Orleans Saints'},
    {'id':'9', 'name':'Blake Grupe', 'position':'K', 'team':'New Orleans Saints'},
    {'id':'10', 'name':'Wil Lutz', 'position':'K', 'team':'Denver Broncos'},
  ]);
  let remainingRequests = ref([]);
  let analyzedPlayers = ref([]);

  // List of up to 5 potential players to display
  let playerOptions = ref([]);
  
  // Add a player to the input list
  function addPlayer(player) {
    if (players.value.some(e => e.name === player.name)) {
      // Do nothing - don't want to add duplicate players
    } else {
        players.value.push({
        id: id++,
        name: player.name,
        position: player.position,
        team: player.team
      });
    }

    name.value = '';
    position.value = '';
    team.value = '';
    playerOptions = ref([]);
  }

  // Generate player cards based on substring of typed name
  function generateCards(name) {
    playerOptions = ref([]);
    if (name.length > 2) {
      for (const key in playerJson) {
        const curr = playerJson[key];
        const currName = curr['PlayerName'].split('.').join('').substring(0, name.length);
        if (currName.toUpperCase() === name.toUpperCase() && playerOptions.value.length <= 5) {
          playerOptions.value.push({
            name: curr['PlayerName'],
            position: curr['Pos'],
            team: curr['Team']
          });
        }
      }
    }
  }
  
  // Remove a player from the input list
  function removePlayer(player) {
    players.value = players.value.filter((t) => t !== player);
  }
  
  /**
   * Clears all player data, both input and analyzed.
   * Functionally, clears the screen.
   */
  function restart() {
    players.value = [];
    analyzedPlayers.value = [];
  }
  
  /**
   * Wrapper method to call performRosterAnalysis
   * while also allowing loading animation
   */
  async function analyzeRoster() {
    loading.value = true;
    await performRosterAnalysis();
    loading.value = false;
  }

  /**
   * Queries the backend by sending players as a JSON to
   * the backend, and receiving the response as a JSON
   * stored in analyzedPlayers.
   */
  const performRosterAnalysis = async () => {
    // Clear existing Analyzed Players, starting fresh
    analyzedPlayers.value = [];

    // Ensure data is valid and the correct amount of players have been input.
    let qbNum = 0;
    let rbNum = 0;
    let wrNum = 0;
    let teNum = 0;
    let flexNum = 0;
    let dstNum = 0;
    let kNum = 0;

    for (const player of players.value) {
      let position = player['position'];
      if (position == 'QB') {
        qbNum++;
      } else if (position == 'RB') {
        if (rbNum == minRbNum) {
          flexNum++;
        } else {
          rbNum++;
        }
      } else if (position == 'WR') {
        if (wrNum == minWrNum) {
          flexNum++;
        } else {
          wrNum++;
        }
      } else if (position == 'TE') {
        if (teNum == minTeNum) {
          flexNum++;
        } else {
          teNum++;
        }
      } else if (position == 'DST') {
        dstNum++;
      } else if (position == 'K') {
        kNum++;
      }
    }

    let missingPlayers = [];
    if (qbNum < minQbNum) {
      missingPlayers.push(minQbNum - qbNum + ' QB');
    } if (rbNum < minRbNum) {
      missingPlayers.push(minRbNum - rbNum + ' RB');
    } if (wrNum < minWrNum) {
      missingPlayers.push(minWrNum - wrNum + ' WR');
    } if (teNum < minTeNum) {
      missingPlayers.push(minTeNum - teNum + ' TE');
    } if (flexNum < minFlexNum) {
      missingPlayers.push(minFlexNum - flexNum + ' extra Flex');
    } if (dstNum < minDstNum) {
      missingPlayers.push(minDstNum - dstNum + ' D/ST');
    } if (kNum < minKNum) {
      missingPlayers.push(minKNum - kNum + ' K');
    }
    
    if (missingPlayers.length > 0) {
      alert('Need more players: \n' + missingPlayers.join('\n'))
    } else {
      // URL of the backend
      const url = 'http://localhost:5000/api/players';

      // Format to send the message.
      const options = {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type':'application/json'
        },
        body: JSON.stringify({
          usingTestData: useTestData.value,
          players: players.value,
        })
      }
      
      // Hit backend, and receive response.
      // Store response in analyzedPlayers.
      await fetch(url, options)
      .then(response => {
        if (!response.ok) {
          response.json()
          .then(data => {
            alert(data['message']);
          });
          throw new Error('Could not communicate with server.');
        }
        return response.json();
      })
      .then(data => {
        remainingRequests.value = data['remaining-requests'];
        analyzedPlayers.value = data['player-data'];
      })
      .catch(error => {
        console.log('Fetch error: ', error);
      });
    }
  }
</script>
  
<style scoped>
  ul {
    list-style-type: none;
  }

  hr {
    width: 33%;
  }

  #settingsButton {
    cursor: pointer;
    color: royalblue;
  }

  #playerInput{
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
  }

  #nameInput {
    border-radius: 2px;
    margin-left: 20px;
    width: 300px;
    font-size: medium;
    margin-bottom: 3px;
  }

  #playerOptions {
    cursor: pointer;
    margin: 0px;
  }

  .spinner {
    border: 16px solid #f3f3f3;
    border-top: 16px solid #3498db;
    margin: auto;
    margin-top: 20px;
    border-radius: 50%;
    width: 120px;
    height: 120px;
    animation: spin 2s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>