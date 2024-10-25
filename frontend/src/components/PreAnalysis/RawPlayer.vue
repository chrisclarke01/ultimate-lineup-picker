<template>
    <div>
        {{ player.position }}: {{ player.name }}, {{ player.team }}
    <button @click="$emit('removePlayer', player)">Remove Player</button>
    </div>
</template>

<script setup>
    import { defineProps } from 'vue';

    defineProps({
        player: {
            name: String,
            position: String,
            team: String
        }
    });
</script>

<style scoped>
</style>