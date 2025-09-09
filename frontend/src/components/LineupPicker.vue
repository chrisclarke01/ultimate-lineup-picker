<template>
  <h2 @click='settingsChosen = !settingsChosen;' id='settingsButton'>
    Settings
  </h2>
  <div class='settings' v-if='settingsChosen'>
    <hr/>
    <label>
      Use Test Data Instead of Live Data
      <input type='checkbox' v-model='useTestData'>
      
      <br />
      QB Amount<input type='radio' value='1' name='qb' v-model='minQbNum'>1
      <input type='radio' value='2' name='qb' v-model='minQbNum'>2
      <input type='radio' value='3' name='qb' v-model='minQbNum'>3
      
      <br />
      RB Amount<input type='radio' value='1' name='rb' v-model='minRbNum'>1
      <input type='radio' value='2' name='rb' v-model='minRbNum'>2
      <input type='radio' value='3' name='rb' v-model='minRbNum'>3
      
      <br />
      WR Amount<input type='radio' value='1' name='wr' v-model='minWrNum'>1
      <input type='radio' value='2' name='wr' v-model='minWrNum'>2
      <input type='radio' value='3' name='wr' v-model='minWrNum'>3
      
      <br />
      TE Amount<input type='radio' value='1' name='te' v-model='minTeNum'>1
      <input type='radio' value='2' name='te' v-model='minTeNum'>2
      <input type='radio' value='3' name='te' v-model='minTeNum'>3

      <br />
      FLEX Amount<input type='radio' value='1' name='flex' v-model='minFlexNum'>1
      <input type='radio' value='2' name='flex' v-model='minFlexNum'>2
      <input type='radio' value='3' name='flex' v-model='minFlexNum'>3

      <br />
      DST Amount<input type='radio' value='1' name='dst' v-model='minDstNum'>1
      <input type='radio' value='2' name='dst' v-model='minDstNum'>2
      <input type='radio' value='3' name='dst' v-model='minDstNum'>3
      
      <br />
      K Amount<input type='radio' value='1' name='k' v-model='minKNum'>1
      <input type='radio' value='2' name='k' v-model='minKNum'>2
      <input type='radio' value='3' name='k' v-model='minKNum'>3
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
  import { ref, onMounted } from 'vue'
  import DefenseRoster from '../assets/defenses.json'
  import PlayerCard from './PlayerCard.vue';

  // Player data API Key
  const PLAYER_DATA_API_KEY = process.env.VUE_APP_PLAYER_DATA_API_KEY;
  let playerData = null;

  // Flag to display the settings
  const settingsChosen = ref(false);

  // Flag to display a loading animation during backend calculation
  const loading = ref(false);

  // Minimum required amounts of every position
  let minQbNum = ref(1);
  let minRbNum = ref(2);
  let minWrNum = ref(2);
  let minTeNum = ref(1);
  let minFlexNum = ref(1);
  let minDstNum = ref(1);
  let minKNum = ref(1);

  // Track whether test or live data is to be used
  let useTestData = ref(false);
  
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

  /**
   * Functions to be run on page load
   */
  onMounted(() => {
    // Immediately upon page load, load player data
    loadPlayerData();
  })
  
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
      for (const key in playerData) {
        const curr = playerData[key];
        if (curr['Status'] === 'Active' && (curr['FantasyPosition'] === 'QB' || curr['FantasyPosition'] === 'WR' || curr['FantasyPosition'] === 'RB' || curr['FantasyPosition'] === 'TE' || curr['FantasyPosition'] === 'DST' || curr['FantasyPosition'] === 'K')) {
          const fullName = curr['Name'].split('.').join('').split('\'').join('').substring(0, name.length);
          const firstName = curr['FirstName'].split('.').join('').split('\'').join('').substring(0, name.length);
          const lastName = curr['LastName'].split('.').join('').split('\'').join('').substring(0, name.length);
          if ((fullName.toUpperCase() === name.toUpperCase() || firstName.toUpperCase() === name.toUpperCase() || lastName.toUpperCase() === name.toUpperCase()) && playerOptions.value.length <= 5) {
            playerOptions.value.push({
              name: curr['Name'],
              position: curr['FantasyPosition'],
              team: curr['Team']
            });
          }
        }
      }
    }
  }
  
  /**
   * Loads player data by accessing SportsDataIO API and returning a JSON list of all NFL players.
   * Specifically modifies to only include active players in positions we care about, for speed.
   */
  async function loadPlayerData() {
    if (playerData == null) {
      // Create variable to house only players
      let roster = null;

      // URL of the SportsDataIO API
      const url = 'https://api.sportsdata.io/v3/nfl/scores/json/Players?key=' + PLAYER_DATA_API_KEY;

      // Format to send the message.
      const options = {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type':'application/json'
        }
      }
      
      // Hit API, and receive response.
      // Store response in playerData.
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
        roster = data;
      })
      .catch(error => {
        console.log('Fetch error: ', error);
      });

      // Combine team defenses with actual players
      playerData = [ ...DefenseRoster, ...roster ];

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
        if (rbNum == minRbNum.value) {
          flexNum++;
        } else {
          rbNum++;
        }
      } else if (position == 'WR') {
        if (wrNum == minWrNum.value) {
          flexNum++;
        } else {
          wrNum++;
        }
      } else if (position == 'TE') {
        if (teNum == minTeNum.value) {
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
    if (qbNum < minQbNum.value) {
      missingPlayers.push(minQbNum.value - qbNum + ' QB');
    } if (rbNum < minRbNum.value) {
      missingPlayers.push(minRbNum.value - rbNum + ' RB');
    } if (wrNum < minWrNum.value) {
      missingPlayers.push(minWrNum.value - wrNum + ' WR');
    } if (teNum < minTeNum.value) {
      missingPlayers.push(minTeNum.value - teNum + ' TE');
    } if (flexNum < minFlexNum.value) {
      missingPlayers.push(minFlexNum.value - flexNum + ' extra Flex');
    } if (dstNum < minDstNum.value) {
      missingPlayers.push(minDstNum.value - dstNum + ' D/ST');
    } if (kNum < minKNum.value) {
      missingPlayers.push(minKNum.value - kNum + ' K');
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