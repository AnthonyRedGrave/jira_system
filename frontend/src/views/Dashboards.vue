<template>
  <div class="dashboards-vue">
      <span class="your_projects_span">Ваши проекты</span>
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
            <div v-if="project.last_task.title">
              <span>Новых задач</span>
            </div>
            <hr>
            <button type="button" @click="toDashboard(project.id)" class="btn btn-primary action-dashboard">
              Доска проекта
            </button>
            <button type="button" @click="toProjectPage(project.id)" class="btn btn-primary action-detail">
              Страница проекта
            </button>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboards',
  data(){
    return{
      projects: []
    }
  },
  created(){
    this.getProjectList()
  },
  methods:{
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
      toProjectPage(id){
        this.$router.push({ path: 'project-detail', query: {'id': id }})
      },
      toDashboard(id){
        this.$router.push({ path: 'dashboard', query: {'id': id }})
      }
  }
}
</script>

<style scoped>

.dashboards-vue{
  width: 1200px;
}

.project_block{
  min-height: 240px;
}
.your_projects_span{
  font-size: 32px;
}

.projects_list{
  display: flex;
  /* max-width: 1000px; */
  margin-right: 0;
  flex-direction: row;
}

.project_block{
  width: 450px;
}

.action-dashboard{
  margin-top: 15px;
  margin-bottom: 15px;
}

.action-detail{
  margin-bottom: 15px;
}

.dashboards-vue{
  margin-top: 10px;
}
</style>