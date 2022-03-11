<template>
  <div class="side-bar">
    <side-bar/>
    
  </div>
  <div class="router">
    <router-view/>
  </div>
</template>

<script>
import SideBar from '@/components/SideBar.vue'

export default {
  components: {
    SideBar
  }
}
</script>

<style>
  #app{
    display: flex;
  }
</style>
