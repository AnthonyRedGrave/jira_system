<template>
  <div class="roadmap-view">
    Roadmap
    Просмотр хода процесса выполнения заданий на проекте
    указание времени, дедлайнов
  </div>
</template>

<script>
import useSideBar from '@/components/composables/useSideBar'

export default {
  name: 'Roadmap',
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