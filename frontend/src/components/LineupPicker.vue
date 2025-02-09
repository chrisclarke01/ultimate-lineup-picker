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

  <!-- Input section. User inputs name, position, and team, and from this, a player object is created and binded. -->
  <form id='playerInputForm' @submit.prevent='addPlayer()'>
    <input required id='nameInput' v-model="name"  placeholder='Type Player Name' >
    <select required id='positionInput' v-model='position' name='position'>
      <option value='QB'>QB</option>
      <option value='WR'>WR</option>
      <option value='RB'>RB</option>
      <option value='TE'>TE</option>
      <option value='DST'>D/ST</option>
      <option value='K'>K</option>
    </select>
    <select required id='teamInput' v-model='team' name='team'>
      <option value='Arizona Cardinals'>Arizona Cardinals</option>
      <option value='Atlanta Falcons'>Atlanta Falcons</option>
      <option value='Baltimore Ravens'>Baltimore Ravens</option>
      <option value='Buffalo Bills'>Buffalo Bills</option>
      <option value='Carolina Panthers'>Carolina Panthers</option>
      <option value='Chicago Bears'>Chicago Bears</option>
      <option value='Cincinnati Bengals'>Cincinnati Bengals</option>
      <option value='Cleveland Browns'>Cleveland Browns</option>
      <option value='Dallas Cowboys'>Dallas Cowboys</option>
      <option value='Denver Broncos'>Denver Broncos</option>
      <option value='Detroit Lions'>Detroit Lions</option>
      <option value='Green Bay Packers'>Green Bay Packers</option>
      <option value='Houston Texans'>Houston Texans</option>
      <option value='Indianapolis Colts'>Indianapolis Colts</option>
      <option value='Jacksonville Jaguars'>Jacksonville Jaguars</option>
      <option value='Kansas City Chiefs'>Kansas City Chiefs</option>
      <option value='Las Vegas Raiders'>Las Vegas Raiders</option>
      <option value='Los Angeles Chargers'>Los Angeles Chargers</option>
      <option value='Los Angeles Rams'>Los Angeles Rams</option>
      <option value='Miami Dolphins'>Miami Dolphins</option>
      <option value='Minnesota Vikings'>Minnesota Vikings</option>
      <option value='New England Patriots'>New England Patriots</option>
      <option value='New Orleans Saints'>New Orleans Saints</option>
      <option value='New York Giants'>New York Giants</option>
      <option value='New York Jets'>New York Jets</option>
      <option value='Philadelphia Eagles'>Philadelphia Eagles</option>
      <option value='Pittsburgh Steelers'>Pittsburgh Steelers</option>
      <option value='San Francisco 49ers'>San Francisco 49ers</option>
      <option value='Seattle Seahawks'>Seattle Seahawks</option>
      <option value='Tampa Bay Buccaneers'>Tampa Bay Buccaneers</option>
      <option value='Tennessee Titans'>Tennessee Titans</option>
      <option value='Washington Commanders'>Washington Commanders</option>
    </select>
    <button>Submit Player to Roster</button>
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
  const useTestData = ref(false)
  
  // Give each player a unique ID, name, position, and team
  let id = 0
  const name = ref('')
  const position = ref('')
  const team = ref('')

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
  ])
  let remainingRequests = ref([])
  let analyzedPlayers = ref([])
  
  // Add a player to the input list
  function addPlayer() {
    players.value.push({
      id: id++,
      name: name.value,
      position: position.value,
      team: team.value
    });
    name.value = '';
    position.value = '';
    team.value = '';
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
    width:33%;
  }

  #settingsButton {
    cursor: pointer;
    color: royalblue;
  }

  .nameInput {
    border-radius: 2px;
    margin-left: 20px;
  }

  .positionInput {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 4%;
    padding: 14px 16px;
    border: none;
    border-radius: 4px;
    background-color: #f1f1f1;
    font-size: medium;
    margin-left: 20px;
  }

  .teamInput {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20%;
    padding: 14px 16px;
    border: none;
    border-radius: 4px;
    background-color: #f1f1f1;
    font-size: medium;
    margin-left: 20px;
  }

  .playerInputForm {
    display: flex;
    align-items: center;
    justify-content: center;
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