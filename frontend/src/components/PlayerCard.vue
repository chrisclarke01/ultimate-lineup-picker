<template>
    <div class='player-card'>
        <span>
            {{ name }}: {{ position }}, {{ team }}
        </span>
    </div>
</template>
  
<script setup>
    import { defineProps } from 'vue';

    defineProps({
        name: String,
        position: String,
        team: String
    });
</script>

<style scoped>
    .player-card {
        width: 300px;
        padding: 14px 16px;
        border: none;
        border-radius: 4px;
        background-color: #f1f1f1;
        font-size: medium;
        text-align: left;
    }
</style>