<template>
  <div class="roadmap-view">
    <h2 style="margin-top: 15px;">Roadmap</h2>
    <hr>
      <div class="roadmap" v-for="roadmap in roadmaps" :key="roadmap">
        <div class="roadmap__project_title">
          <h4 style="padding-bottom: 10px; margin-bottom: 10px; border-bottom: 1px solid black" class="roadmap__project__title">Проект: {{roadmap.project.title}}</h4>
          <h4>Менеджер: {{roadmap.project.manager_name}}</h4>
        </div>
        <h4>Тип: {{roadmap.project.type}}</h4>
        <h4>Дедлайн: {{roadmap.deadline}}</h4>
        <h5>Задач: {{roadmap.project.tasks}}</h5>
        <button v-if="roadmap.project.tasks !== 0" style="margin-top: 10px; margin-bottom: 20px;" class="btn btn-outline-primary" @click="showRoadmap($event)">Показать</button>
        <div class="roadmap_tasks">
          <div class="roadmap_task" v-for="task in roadmap.roadmaptasks" :key="task">
            <h5 style="padding-bottom: 10px; margin-bottom: 10px; border-bottom: 1px solid black;">Задача: {{task.task.title}}</h5>
            <h4>{{task.content}}</h4>
            <h6>Пользователь: {{task.task.developer}}</h6>
          </div>
        </div>
        
      </div>
      
      
  </div>
</template>

<script>
import useSideBar from '@/components/composables/useSideBar'
import axios from 'axios'
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
      this.getRoadMaps()
        
    },
    data(){
      return {
        roadmaps: []
      }
    },
    methods:{
      get(){
        this.$emit('selectSideBarLine', this.$route.name)
      },
      getRoadMaps(){
        axios({
                method: "get",
                url: `http://localhost:8000/api/roadmaps/`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
                })
                .then((responce) => {
                  this.roadmaps = responce.data                  
                })
                .catch((err) => {
                console.log(err);
                })
      },
      showRoadmap(elem){
        let panel = elem.target.nextElementSibling
        if (panel.style.maxHeight) {
          panel.style.maxHeight = null;
        } else {
          panel.style.maxHeight = panel.scrollHeight + "px";
        }
      }
    }

}
</script>

<style>
  .roadmap{
    border: 1px solid black;
    padding: 10px;
    border-radius: 7px;
    margin-bottom: 30px;
  }
  .roadmap:hover{
    background: rgb(231, 231, 231);
  }
  .roadmap_task{
    border: 1px solid rgb(116, 116, 255);
    border-radius: 7px;
    padding: 10px;

  }
  .roadmap_tasks{
    display: flex;
    flex-direction: column;
    gap: 20px;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.2s ease-out;
  }
</style>