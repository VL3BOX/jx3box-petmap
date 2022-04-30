<template>
  <div id="app">
    <!-- <pet-map :pet-id="244"/> -->
    <pet-map :pet-id="98"/>
    <!-- <pet-map :pet-id="339"/> -->
    <!-- <pet-map :pet-id="385"/> -->
  </div>
</template>

<script>
import PetMap from './components/PetMap.vue'

export default {
  name: 'App',
  components: {
    PetMap
  }
}
</script>

<style lang="less">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
