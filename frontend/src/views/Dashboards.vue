<template>
  <div class="dashboards-vue">
      <span class="your_projects_span">Ваши проекты</span>
      <hr>
      <div class="projects_list">
        <div v-for="project in projects" :key="project.id" class="project_block" @click="toDashboard(project.id)">
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
      toDashboard(id){
        this.$router.push({ path: 'Dashboard', query: {'id': id }})
      }
  }
}
</script>

<style>
.project_block{
  min-height: 240px;
}
.your_projects_span{
  font-size: 32px;
}

.projects_list{
  margin-top: 10px;
}


.dashboards-vue{
  margin-top: 10px;
}
</style>