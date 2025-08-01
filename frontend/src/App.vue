<template>
  <div class="container mx-auto p-4 text-center">
    <h1 class="text-4xl text-white mb-4">Self-Balancing Task Manager</h1>
    <div v-for="category in taskCategories" :key="category.name" class="task-card card-glass p-4 mb-4">
      <h2 class="text-xl" :class="category.scoreClass">{{ category.name }}: {{ category.score }}</h2>
      <button class="btn btn-primary" @click="completeTask(category)">Complete Task</button>
    </div>
    <div>
      <h3 class="text-2xl text-white">Neutrality Score: <span :class="neutralityClass">{{ totalScore }}</span></h3>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      taskCategories: [
        { name: 'Design Pattern', score: 4 },
        { name: 'GFG, TUF', score: 11 },
        { name: 'GitHub Recap', score: -4 },
        { name: 'Duolingo', score: -13 },
        { name: 'Pushups', score: 29 }
      ],
    };
  },
  computed: {
    totalScore() {
      return this.taskCategories.reduce((acc, category) => acc + category.score, 0);
    },
    neutralityClass() {
      return this.totalScore > 0 ? 'score-positive' : this.totalScore < 0 ? 'score-negative' : 'score-zero';
    }
  },
  methods: {
    completeTask(category) {
      category.score--;
    }
  }
};
</script>

<style>
@import 'bootstrap/dist/css/bootstrap.css';
@import 'tailwindcss/tailwind.css';
</style>
