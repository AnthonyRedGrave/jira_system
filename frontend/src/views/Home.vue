<template>
  <div class="home">
    ГЛАВНАЯ
    Возможности: 
    Создание проекта Dashboard
    Просмотр всех проектов
    Назначение
    Какие задачи уже просмотрел программист
    Просмотр последних изменений от команды (для менеджера)
    Ответы на сообщения

  </div>
</template>

<script>
import useSideBar from '@/components/composables/useSideBar'

export default {
  name: 'Home',
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