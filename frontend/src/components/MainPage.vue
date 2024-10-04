<template>
  <div class="frontpage">
    <h1>{{ msg }}</h1>
    <p>
      The Ultimate Lineup Picker is a tool that uses sportsbook player props to infer fantasy points for players.
    </p>
    <p>
      Using these inferred points, it will automatically set up the best lineup given a particular team.
    </p>
    <h2>Input Team Below</h2>
    <div class="inputSection">
      <div class="playerInput" id="qb">
          <label>Quarterback: </label>
          <input type="text">
      </div>
      <div class="playerInput" id="rb">
          <label>Running Back 1: </label>
          <input type="text">
      </div>
      <div class="playerInput" id="rb">
          <label>Running Back 2: </label>
          <input type="text">
      </div>
      <div class="playerInput" id="wr">
          <label>Wide Receiver 1: </label>
          <input type="text">
      </div>
      <div class="playerInput" id="wr">
          <label>Wide Receiver 2: </label>
          <input type="text">
      </div>
      <div class="playerInput" id="te">
          <label>Tight End: </label>
          <input type="text">
      </div>
      <div class="playerInput" id="flex">
          <label>Flex: </label>
          <input type="text">
      </div>
      <div class="playerInput" id="dst">
          <label>Defense/Special Teams: </label>
          <input type="text">
      </div>
      <div class="playerInput" id="k">
          <label>Kicker: </label>
          <input type="text">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.playerInput {
  padding: 5px;
  border-radius: 5px;
  margin-bottom: 5px;
}

.playerInput>label {
  display: inline-block;
  width: 200px;
}
</style>
