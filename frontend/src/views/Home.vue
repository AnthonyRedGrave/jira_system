<template>
  <div class="home">
    <span class="your_work_span">Ваша работа</span>
    <hr>
    <div class="your_work_block">
      <div class="accordion accordion-flush" id="accordionFlushExample">
        <div class="accordion-item">
          <h2 class="accordion-header" id="flush-headingOne">
            <button class="accordion-button collapsed" style="font-size: 20px; padding-left: 2px;" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
              Как менеджера: {{managerProjects()}}
            </button>
          </h2>
          <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlushExample">
            <div class="accordion-body">
              <span v-for="proj in managerProjectsList" :key="proj.id">
                Проект {{proj.title}}
              </span>
            </div>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header" id="flush-headingTwo">
            <button class="accordion-button collapsed" style="font-size: 20px; padding-left: 2px;" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseTwo">
              Как разработчика: {{developerProjects()}}
            </button>
          </h2>
          <div id="flush-collapseTwo" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo" data-bs-parent="#accordionFlushExample">
            <div class="accordion-body">
              <span v-for="proj in developerProjectsList" :key="proj.id">
                Проект {{proj.title}}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <br>
    <br>
    <div class="recent_projects">
      <span class="recent_projects_title">
        Недавние проекты
      </span>
      <hr>
      <div class="projects_list">
        <div v-for="project in projects" :key="project.id" class="project_block">
          <div class="project_title">
            Проект {{project.title}}
          </div>
          <hr>
          <div class="project_description">
            <span>Тип {{project.type}}</span> 
            <span>Менеджер {{project.manager_name}}</span>
            <br>
            <button type="button" class="btn btn-primary">
              Уведомления <span class="badge bg-secondary">{{project.notifications}}</span>
            </button>
          </div>

        </div>
      </div>
    </div>
    <div class="create_project_block">
      <button type="button" class="btn btn-outline-primary">Create project</button>
    </div>
    
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
    data(){
      return{
        projects: [],
        tasks: [],
        managerProjectsList: [],
        developerProjectsList: [],
        username: JSON.parse(localStorage.getItem('username'))
      }
    },
    created(){
      this.get()
      this.getProjectList()
        
    },
    methods:{
      get(){
        this.$emit('selectSideBarLine', this.$route.name)
      },
      managerProjects(){
        this.managerProjectsList = this.projects.filter(el => el.manager_name === this.username)
        return this.projects.filter(el => el.manager_name === this.username).length
      },
      developerProjects(){
        this.developerProjectsList = this.projects.filter(el => el.developers.includes(this.username))
        return this.projects.filter(el => el.developers.includes(this.username)).length
      },
      getProjectList(){
        this.$store.dispatch("getProjects", {
          token: this.$store.state.accessToken,
        })
        .then((response) => {
          this.projects = response.data
        })
          .catch((err) => {
            console.log(err);
          });
      },
      
    }

}
</script>

<style>
.home{
  margin-left: 50px;
}

.your_work_span{
  font-size: 32px;

}

.recent_projects_title{
  font-size: 32px;

}

.your_work_block{
  font-size: 32px;
  display: flex;
  flex-direction: column;
}

.accordion-body{
  display: flex;
  flex-direction: column;
}

.projects_list{
  display: flex;
  max-width: 1000px;
  flex-wrap: wrap
}

.project_block{
  border:1px solid #0d6efd;
  padding: 15px;
  font-size: 22px;
  box-shadow: 0 0 5px rgba(0,0,0,0.5);
  min-width: 300px;
  margin-right: 20px;
  margin-bottom: 20px;
  transition: background .35s;


}

.project_block:hover{
  background: rgb(228, 228, 228);
  box-shadow: 0 0 10px rgba(0,0,0,0.5);

}

.project_description{
  display: flex;
  flex-direction: column;
}
</style>