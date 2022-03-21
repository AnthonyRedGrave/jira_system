<template>
  <div class="backlog-view">
    Backlog
  </div>
</template>

<script>
import useSideBar from '@/components/composables/useSideBar'

export default {
  name: 'Backlog',
  setup(){

      const {menu, selectSideBarLine} = useSideBar()
      return {
        selectSideBarLine,
        menu
      }
    },
    created(){
      this.get()
        
    },
    methods:{
      get(){
        this.$emit('selectSideBarLine', this.$route.name)
      }
    }

}
</script>

<style>

</style>