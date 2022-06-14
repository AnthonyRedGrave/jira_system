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
              <span v-if="managerProjects() == 0">
                <h2>У Вас нет проектов</h2>
              </span>
              <span v-else v-for="proj in managerProjectsList" :key="proj.id">
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
              <span v-if="developerProjects() == 0">
                <h2>У Вас нет проектов</h2>
              </span>
              
              <span v-else v-for="proj in developerProjectsList" :key="proj.id">
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
        <div v-for="project in projects" :key="project.id" @click="toProjectDashboard(project.id)" class="project_block">
          <div class="project_title">
            Проект {{project.title}}
          </div>
          <hr>
          <div class="project_description">
            <span>Тип {{project.type}}</span> 
            <span>Менеджер {{project.manager_name}}</span>
          </div>
          <hr>
          <div class="notific_block">
            <button type="button" class="btn btn-primary notific_butt">
              Уведомления <span class="badge bg-secondary">{{project.notifications.length}}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="create_project_block">
  
      <button type="button" class="btn btn-outline-primary accordion_show_form" @click="showCreateProjectForm($event)">Создать проект</button>
      <div class="errors__block" style="margin-top:15px;" v-if="errorList">
        <div v-for="error in errorList" :key="error" class="alert alert-danger" role="alert">
          {{error[0]}}:{{error[1][0]}}
        </div>
      </div>
      <div class="panel">
        <form @submit.prevent="createProject">
          <div class="mb-3">
            <label class="form-label">Название проекта</label>
            <input class="form-control" v-model="titleProject">
          </div>
          <div class="mb-3">
            <label class="form-label">Тип проекта</label>
            <select v-model="typeProject" class="form-select" aria-label="Default select example">
              <option selected>Выберите тип проекта</option>
              <option value="software">Разработка программного обеспечения</option>
              <option value="service_management">Управление услугами</option>
              <option value="work_management">Управление работой</option>
              <option value="marketing">Маркетинг</option>
              <option value="work_with_personnel">Работа с кадрами</option>
              <option value="finance">Финансы</option>
              <option value="design">Проектирование</option>
              <option value="personal">Личные</option>
            </select>
          </div>
          <div class="mb-3">
            <label class="form-label">Дедлайн проекта</label>
            <input class="form-control" v-model="deadline">
          </div>
          <div class="mb-3">
            <label class="form-label">Разработчики</label>
            <input class="form-control" v-model="username_search" @input="seachDevelopers" placeholder="Введите имена разработчиков для проекта">
            <div v-if="developers" class="developers_block">
                <div v-for="developer in developers" :key="developer.id" class="developer_block">
                  <div class="developer_avatar">
                    <img v-bind:src="developer.image" class="developer_image" alt="...">
                  </div>
                  <div class="developer_username">
                    <span>{{developer.username}}</span>
                  </div>
                  <div class="developer_username">
                    <span>{{developer.first_name}}</span>
                    <span>{{developer.last_name}}</span>
                  </div>
                  <div class="action_buttons">
                    <button type="button" class="btn btn-outline-danger" style="height: 40px;" @click="removeFromDevelopers(developer)">Убрать приглашение</button>
                  </div>
                </div>
                <hr>
                <div v-for="developer in developers_list" :key="developer.id" class="developer_block">
                  <div class="developer_avatar">
                    <img v-bind:src="developer.image" class="developer_image" alt="...">
                  </div>
                  <div class="developer_username">
                    <span>{{developer.username}}</span>
                  </div>
                  <div class="developer_username">
                    <span>{{developer.first_name}}</span>
                    <span>{{developer.last_name}}</span>
                  </div>
                  <div class="action_buttons">
                    <button type="button" class="btn btn-outline-primary" style="height: 40px;" @click="addToDevelopers(developer)">Отправить приглашение</button>
                  </div>
                </div>
            </div>
            <button type="submit" class="btn btn-outline-primary">Создать проект</button>
          </div>
        </form>
      </div>
    </div>
    
  </div>
</template>

<script>
import useSideBar from '@/components/composables/useSideBar'
import axios from 'axios'

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
        username: JSON.parse(localStorage.getItem('username')),
        username_search: null,
        titleProject: null,
        typeProject: null,

        errorList: [],

        developers: [],
        developers_usernames:[],
        developers_list_username: [],
        developers_list: [],
        deadline: null
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
      createProject(){
        let data = {
                  title: this.titleProject,
                  type: this.typeProject,
                  developers: this.developers_usernames.join(","),
                  deadline: this.deadline
            }
        axios({
              method: "post",
              url: `http://localhost:8000/api/projects/`,
              data: data,
              headers: {
              Authorization: `Bearer ${this.$store.state.accessToken}`,
              },
              })
              .then((response) => {
                  console.log(response.data)
                  this.$router.push({ path: 'Dashboards'})

              })
              .catch((err) => {
              
              Object.entries(err.response.data).forEach((element)=>{
                this.errorList.push(element)

              })
              });
      },
      seachDevelopers(){
        if (this.username_search){
          axios
                .get(`http://localhost:8000/api/users`, {
                headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
                params: {
                    username: this.username_search
                },
                })
                .then((response) => {
                  response.data.forEach(element => {
                    if (!this.developers_list_username.includes(element.username) && !this.developers_usernames.includes(element.username)){
                      console.log(element)
                      this.developers_list.push(element)
                      this.developers_list_username.push(element.username)                    
                    }
                  });
                  
                })
                .catch((err) => {
                    console.log(err);
                });
        }
        else{
          this.developers_list = []
          this.developers_list_username = []

        }
          
      },
      addToDevelopers(developer){
        this.developers.push(developer)
        this.developers_usernames.push(developer.username)
        this.username_search = null
        this.developers_list = []
        this.developers_list_username = []
        
        
      },
      showCreateProjectForm(element){
        let panel = element.target.nextElementSibling.nextElementSibling
        this.errorList = []
        if (panel.style.maxHeight) {
          panel.style.maxHeight = null;
        } else {
          panel.style.maxHeight = panel.scrollHeight + "px";
        }

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
      toProjectDashboard(project_id){
        this.$router.push({ path: 'dashboard', query: {'id': project_id }})
      }
      
    }

}
</script>

<style>
.home{
  margin-left: 50px;
  width: 800px;
  margin-top: 10px;
}

.your_work_span{
  font-size: 32px;
  
}

.accordion_show_form{
  background-color: #eee;
  color: #444;
  cursor: pointer;
  padding: 18px;
  width: 100%;
  text-align: left;
  border: none;
  outline: none;
  transition: 0.4s;
}

.panel {
  margin-top: 20px;
  padding: 0 18px;
  background-color: white;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.2s ease-out;
}

.developers_block{
  padding: 0 18px;
  margin-top: 25px;
  border: 3px solid #78aeff;
  height: auto;
  max-height: auto;
  min-height: 500px;
  border-radius: 15px;
  margin-bottom: 50px;
  
}

.developer_block{
  display: flex;
  justify-content: space-between;
  border: 1px solid black;
  border-radius: 5px;
  background: rgb(243, 243, 243);
  margin: 15px 0px;
  padding: 15px;
}

.developer_image{
  width: 100px;
  height: 100px;

}

.action_buttons{
  display: flex;

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
  border-radius: 5px;
  padding: 15px;
  font-size: 22px;
  box-shadow: 0 0 5px rgba(0,0,0,0.5);
  min-width: 300px;
  max-width: 350px;
  margin-right: 20px;
  margin-bottom: 20px;
  transition: background .35s;


}

.project_block:hover{
  background: rgb(228, 228, 228);
  box-shadow: 0 0 10px rgba(0,0,0,0.5);

}

.notific_block{
  display: flex;
}

.project_description{
  display: flex;
  flex-direction: column;
  height: 50px;
  margin-bottom: 150px;
}
</style>