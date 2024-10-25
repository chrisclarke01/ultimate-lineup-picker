<template>
    <div v-if="analyzedPlayers.length !== 0">
        <h2>Your Ideal Lineup</h2>
        <AnalyzedPlayer v-for="player in analyzedPlayers" :key="player.id" :player="player" />
        <button @click="restart">Clear All Players & Lineup</button>
    </div>
</template>

<script setup>
    import { defineProps } from 'vue';

    defineProps({
        analyzedPlayers: Array
    });
    
    // Clears all data
    function restart() {
        // players.value = [];
        this.analyzedPlayers = [];
    }
</script>

<style scoped>
</style>