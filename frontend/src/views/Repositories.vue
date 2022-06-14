<template>
  <div class="repositories-view">
    <!-- https://bitbucket.org/dashboard/overview -->
    <h2 style="margin-top: 15px;">Репозитории</h2>
    <hr>
    <div class="repositories__projects">
      <div class="repositories__project" v-for="project in projects" :key="project.id">
        <div class="repos__project_title">
          <h4>{{project.title}}</h4>
        </div>
        <div class="repos__project_manager_name">
          Менеджер: {{project.manager_name}}
        </div>
        <div class="repos__project_type">
          {{project.type}}
        </div>
        <button class="btn btn-outline-primary">
          <a href="https://bitbucket.org/dashboard/repositories">Добавить репозиторий</a>
          
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import useSideBar from '@/components/composables/useSideBar'

export default {
  name: 'Repositories',
  setup(){

      const {menu, selectSideBarLine} = useSideBar()
      return {
        selectSideBarLine,
        menu
      }
  },
  data(){
    return{
      projects: []
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

<style scoped>
  .repositories-view{
    width: 1200px;
  }
  .repositories__project{
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    gap: 20px;
    border: 1px solid black;
    width: 950px;
    padding: 15px;
    border-radius: 10px;
  }
  .repositories__projects{
    display: flex;
    flex-direction: column;
    gap: 20px;

  }
</style>