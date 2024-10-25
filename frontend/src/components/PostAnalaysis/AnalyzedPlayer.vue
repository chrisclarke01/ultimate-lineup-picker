<template>
    <div>
        {{ player.position }}: {{ player.name }}, Projected Points: {{ player.points }}
    </div>
</template>

<script setup>
    import { defineProps } from 'vue';

    defineProps({
        player: {
            position: String,
            name: String,
            points: Number
        }
    });
</script>

<style scoped>
</style>