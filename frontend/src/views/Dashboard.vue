<template>
  <div class="dashboard-vue">
      Dashboards
      Возможности:
      Переход ко всем доскам
      управление досками
      список отфильтрованных по доскам задач, появление новых
  </div>
</template>

<script>
import useSideBar from '@/components/composables/useSideBar'


export default {
    name: 'Dashboards',
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