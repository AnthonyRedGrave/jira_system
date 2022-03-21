<template>
  <div class="side-bar">
    <side-bar :menu=menu @selectSideBarLine="selectSideBarLine($event)"/>
    
  </div>
  <div class="router">
    <router-view @selectSideBarLine="selectSideBarLine($event)"/>
  </div>
</template>

<script>
import SideBar from '@/components/SideBar.vue'
import useSideBar from '@/components/composables/useSideBar'
// import router from '@/router'

export default {
  components: {
    SideBar
  },
  data(){
    return{
      currentRoute: ""
    }
  },
  setup(){
      // const { currentRoute } = router
      const { menu, selectSideBarLine } = useSideBar()

      

      return {
        menu,
        selectSideBarLine
      }
    },
}
</script>

<style>
  #app{
    display: flex;
  }
</style>
