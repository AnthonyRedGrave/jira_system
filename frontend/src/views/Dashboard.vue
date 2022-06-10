<template>
  <div class="dashboard-vue">
    <div v-if="projectInfo.manager_name == this.$store.state.username" class="tasks_form-block">
      <h2>Панель менеджера проекта</h2>
      <div class="btn btn-outline-secondary add_type_btn" @click="showCreateTypeTaskForm($event)" style="margin-right: 15px;">Добавить тип для задач</div>
      
      <div class="btn btn-outline-secondary add_developer" @click="showAddDeveloper($event)" style="margin-right: 15px">Добавить разработчика</div>
      <div class="type_task_title" style="margin-top: 0px;">
        <input class="form-control type_task_title_input" placeholder="Новый тип задач" v-model="newTypeTaskTitle" type="text">
        <button class="btn btn-outline-secondary" @click="createTypeTask()">Добавить</button>
      </div>
      <div class="add_new_developer_block" style="margin-top: 0px;">
        <input class="form-control developer_name" placeholder="Имя разработчика" @input="seachDevelopers" v-model="developer_name" type="text">
        <div class="block-developers">
          <div v-for="dev in found_developers" :key="dev.id" class="devel-block">
            <div class="developer-name" @click="findDeveloper(dev.username)">
              {{dev.username}}
            </div>
          </div>
        </div>
        <button class="btn btn-outline-secondary add_new_developer_btn" :disabled="canAddDeveloperToProject" @click="addDeveloperToProject()">Добавить разработчика</button>
      </div>
    </div>
    <div class="errors__block">
      <div v-if="errorText" class="alert alert-danger" role="alert">
        {{errorText}}
      </div>
    </div>
    <div class="project_developers_block">
      <h3>Разработчики:</h3>
      <div v-for="developer in projectInfo.developers" :key="developer" class="project_developer__block">
        <div class="developer__title" @click="filterTasks(developer)">
              <i class='fas fa-user-alt' style='font-size:20px'></i>
              {{developer}}
        </div>
      </div>
    </div>
    <div class="project_epic_tasks_block">
      <h3>Епики:</h3>
      <div v-for="epic in epic_tasks" @click="filterTasksByEpic(epic.title)" :key="epic" class="project_epic_task_block">
        <div class="epic_color_block" :style='{background: epic.color}'></div>
        {{epic.title}}
      </div>
    </div>
    <div class="actions__block">
      <div class="btns_actions">
        <button class="btn btn-outline-secondary" @click="getDashboardData()" style="margin-bottom: 15px;">Сбросить фильтры</button>
        <button class="btn btn-outline-secondary" @click="showNotifications($event)" style="margin-bottom: 15px;">Уведомления</button>
      </div>
      <div class="notifications__panel">
        <div v-for="notification in notifications" :key="notification.id" :class="getNotificationClass">
          <Notification :notification="notification" @readNotification="readNotification"/>
        </div>
      </div>
    </div>
    
    <div class="todo-container">
      <task-modal v-if="isInfoPopupVisible" :task_info="task_info" @closePopup="closePopup"></task-modal>
      <task-modal 
      v-if="isInfoPopupCreateTaskVisible" 
      :task_info="task_info" 
      :epic_tasks="epic_tasks"
      :manager_name="projectInfo.manager_name"
      :type_tasks="type_tasks" 
      :developers="projectInfo.developers" 
      @closePopup="closePopup"
      @createTask="createTask">
      </task-modal>
      <div class="status" v-for="(status, index) in Object.keys(dashboardData)" :key="status" :id=status @dragover="dragOver($event)" @drop="dragDrop($event)">
        <h1>{{status}}</h1>
        <button v-if="index == 0" @click="addNewTask()" id="add_btn">Add Task</button>
        <button v-else id="add_btn" style="opacity: 0;cursor: default;">Add Task</button>
        <div v-for="task in dashboardData[status]" :style="{'border': `1px solid ${task.epic_color}`}" :key="task" class="todo" :id=task.id @dragstart="dragStart($event, task)" @dragend="dragEnd($event)" draggable="true" data-bs-toggle="modal" data-bs-target="#exampleModal"> 
          <div class="task_info">
            <span @click="showPopup(task)">{{task.title}}</span>
            <span class="task_developer__name">{{task.developer}}</span>
          </div>
          <span v-if="task.developer == this.$store.state.username" class="close" @click="deleteTask(task.id)">&times;</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import useSideBar from '@/components/composables/useSideBar'
import axios from 'axios'
import TaskModal from './TaskModal.vue'
import Notification from './Notification.vue'

export default {
    name: 'Dashboard',
    components:{
        TaskModal,
        Notification
    },
    setup(){

      const {menu, selectSideBarLine} = useSideBar()
      return {
        selectSideBarLine,
        menu
      }
    },
    data(){
      return{
        draggableTodo: null,
        canDeleteTypeTasks: false,
        tasks: [],
        statuses: [],
        dashboardData: null,
        task_info: null,
        isInfoPopupVisible: false,
        projectInfo: null,
        newTypeTaskTitle: null,
        errorText: null,
        isInfoPopupCreateTaskVisible: false,
        epic_tasks: [],
        type_tasks: [],
        source_epic_color: null,
        developer_name: null,
        found_developer_name: null,
        found_developers: [],
        notifications: []
      }
    },
    created(){
      this.get()
      this.getProjectInfo()
      this.getDashboardData()
      this.getEpicTasks()
      this.getNotifications()
    },
    computed:{
      canAddDeveloperToProject(){
        if (this.found_developer_name !== null){
          return false
        }
        return true
      },
    },
    methods:{
      get(){
        this.$emit('selectSideBarLine', 'Dashboards')
      },
      filterTasks(developer){
        axios({
                method: "get",
                url: `http://localhost:8000/api/tasks/filter_tasks/`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                params:{
                  developer: developer,
                  project: this.$route.query.id
                },
                credentials: "include",
                })
                .then((responce) => {
                  this.dashboardData = responce.data                  
                })
                .catch((err) => {
                console.log(err);
                })
      },
      getNotifications(){
        axios({
                method: "get",
                url: `http://localhost:8000/api/notifications/`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
                })
                .then((responce) => {
                  this.notifications = responce.data                  
                })
                .catch((err) => {
                console.log(err);
                })
      },
      readNotification(notification){
        axios({
                method: "patch",
                url: `http://localhost:8000/api/notifications/${notification.id}/read/`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
                })
                .then(() => {
                  this.getNotifications()               
                })
                .catch((err) => {
                console.log(err);
                })
      },
      showNotifications(element){
        let notification_panel = element.path[1].nextElementSibling
        if (notification_panel.style.maxHeight) {
          notification_panel.style.maxHeight = null;
        } else {
          this.getNotifications()
          notification_panel.style.maxHeight = notification_panel.scrollHeight + "px";
        }
      },
      filterTasksByEpic(epic_title){
        axios({
                method: "get",
                url: `http://localhost:8000/api/tasks/filter_tasks/`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                params:{
                  epic: epic_title,
                  project: this.$route.query.id
                },
                credentials: "include",
                })
                .then((responce) => {
                  this.dashboardData = responce.data                  
                })
                .catch((err) => {
                console.log(err);
                })
      },
      findDeveloper(developer_name){
        this.found_developer_name = developer_name
      },
      addDeveloperToProject(){
        axios({
          method: "post",
          url: `http://localhost:8000/api/projects/${this.$route.query.id}/add_developer/`,
          data: {
            developers: this.found_developer_name
          },
          headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
          })
          .then(() =>{
            this.getDashboardData()
          })
          .catch((err) => {
                console.log(err);
                this.errorText = err.response.data.title[0]
          });
      },
      showCreateTypeTaskForm(element){
        let panel = element.target.nextElementSibling.nextElementSibling
        if (panel.style.maxHeight) {
          panel.style.maxHeight = null;
          panel.style.margin = '0 0 20px 0'
        } else {
          panel.style.maxHeight = panel.scrollHeight + "px";
          panel.style.margin = '20px 0 20px 0'
          
        }
      },
      showAddDeveloper(element){
        let panel = element.target.nextElementSibling.nextElementSibling
        if (panel.style.maxHeight) {
          panel.style.maxHeight = null;
          panel.style.margin = '0 0 20px 0'
        } else {
          panel.style.maxHeight = panel.scrollHeight + "px";
          panel.style.margin = '20px 0 20px 0'
          
        }
      },
      seachDevelopers(){
        if (this.developer_name){
          axios
                .get(`http://localhost:8000/api/users`, {
                headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
                params: {
                    username: this.developer_name
                },
                })
                .then((response) => {
                  response.data.forEach((element)=>{
                    if (!this.projectInfo.developers.includes(element.username)){
                      this.found_developers = response.data
                    }
                  })
                  
                })  
                .catch((err) => {
                    console.log(err);
                });
        }
        else{
          this.found_developers = []

        }
      },
      addNewTask(){
        this.isInfoPopupCreateTaskVisible = true
        this.getEpicTasks()
        this.getTypeTasks()
        this.task_info = null
      },
      createTask(data){
        data['project'] = this.$route.query.id
        axios({
          method: "post",
          url: 'http://localhost:8000/api/tasks/',
          data: data,
          headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
          })
          .then((responce) =>{
            console.log(responce.data)
            this.isInfoPopupCreateTaskVisible = false
            this.getDashboardData()
          })
          .catch((err) => {
                console.log(err);
                this.errorText = err.response.data.title[0]
          });
      },
      deleteTask(task_id){
        axios({
          method: "delete",
          url: `http://localhost:8000/api/tasks/${task_id}/`,
          headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
          })
          .then((responce) =>{
            console.log(responce.data)
            this.getDashboardData()
          })
          .catch((err) => {
                console.log(err);
                this.errorText = err.response.data.title[0]
          });

      },
      getEpicTasks(){
            axios({
                method: "get",
                url: `http://localhost:8000/api/epics/`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
                })
                .then((responce) => {
                  this.epic_tasks = responce.data                    
                })
                .catch((err) => {
                console.log(err);
                })
      },
      getTypeTasks(){
            axios({
                method: "get",
                url: `http://localhost:8000/api/types/`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
                })
                .then((responce) => {
                  this.type_tasks = responce.data                    
                })
                .catch((err) => {
                console.log(err);
                })
      },
      getProjectInfo(){
        axios({
                method: "get",
                url: `http://localhost:8000/api/projects/${this.$route.query.id}`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
                })
                .then((responce) => {
                  this.projectInfo = responce.data                    
                })
                .catch((err) => {
                console.log(err);
                });
        
      },
      createTypeTask(){
        let data = {
          title: this.newTypeTaskTitle
        }
        axios({
          method: "post",
          url: 'http://localhost:8000/api/types/',
          data: data,
          headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
          })
          .then((ressponce) =>{
            this.newTypeTaskTitle = null
            console.log(ressponce.data)
          })
          .catch((err) => {
                console.log(err);
                this.errorText = err.response.data.title[0]
          });
      },
      getDashboardData(){
        axios({
                method: "get",
                url: `http://localhost:8000/api/projects/${this.$route.query.id}/board/`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
                })
                .then((responce) => {
                  
                  this.dashboardData = responce.data                    
                })
                .catch((err) => {
                console.log(err);
                });
      },
      showPopup(task){
        this.isInfoPopupVisible = true
        this.task_info = task
      },
      closePopup(){
        this.isInfoPopupVisible =  false
        this.isInfoPopupCreateTaskVisible = false
      },
      dragStart(el, task){
        

        if (task.developer !== this.$store.state.username){
          alert("Вы не можете перетаскивать чужие задачи!")
        }
        else{
          this.draggableTodo = el.target
        }
        
      },
      dragEnd(){
        this.draggableTodo = null
        
      },
      dragOver(e){
        e.preventDefault();

      },
      dragDrop(el){
        let status_title = null
        if (el.target.className === "status"){
          status_title = el.target.id
          el.target.appendChild(this.draggableTodo)
        }
        else if(el.target.className === "todo"){
          status_title = el.target.parentElement.id
          el.target.parentElement.appendChild(this.draggableTodo)
        }
        else{
          return
        }
        let data = {
          type_task: status_title,
          implementer: this.$store.state.username
        }
        axios({
                method: "patch",
                url: `http://localhost:8000/api/tasks/${this.draggableTodo.id}/`,
                data: data,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
                })
                .catch((err) => {
                console.log(err);
                });
      }
    }
}
</script>

<style>
  .dashboard-vue{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    min-height: 100vh;
    display: flex;
    margin-top: 15px;
    /* justify-content: center; */
    flex-direction: column;
    /* align-items: center; */
    box-sizing: border-box;
  }
  .task_info{
    display: flex;
    flex-direction: column;
  }
  .task_developer__name{
    font-size: 14px;
  }
  .developer__title{
    cursor: pointer;
    border: 1px solid black;
    padding: 5px;
    border-radius: 3px;
  }
  .btns_actions{
    display: flex;
    justify-content: space-between;
  }
  .project_epic_tasks_block{
    display: flex;
    flex-direction: row;
    gap: 10px;
    margin-bottom: 10px;
  }
  .project_epic_task_block{
    display: flex;
    padding: 5px;
    border: 1px solid black;
    border-radius: 4px;
    cursor: pointer;
  }
  .project_epic_task_block:hover{
    background: rgb(226, 226, 226);
  }
  .epic_color_block{
    width: 15px;
    height: 15px;
  }
  .developer__title:hover{
    background: rgb(226, 226, 226);
  }
  .project_developers_block{
    height: 50px;
    display: flex;
    flex-direction: row;
    gap: 10px;

  }
  .type_task_title{
    margin-top: 20px;
    margin-bottom: 20px;
    /* padding: 0 18px; */
    background-color: white;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.2s ease-out;
  }
  .notifications__panel{
    /* margin-top: 20px;
    margin-bottom: 20px; */
    /* padding: 0 18px; */
    background-color: white;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.2s ease-out;
  }
  .add_new_developer_block{
    margin-top: 20px;
    margin-bottom: 20px;
    /* padding: 0 18px; */
    background-color: white;
    height: 260px;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.2s ease-out;
  }
  .add_new_developer_btn{
    margin-top: 15px;
  }
  .type_task_title_input{
    margin-bottom: 10px;
    width: 204px;
  }
  .add_type_btn{
    margin-top: 10px;
  }
  .add_developer{
    margin-top: 10px;
  }
  .block-developers{
    margin-top: 10px;
    padding: 20px;
    border: 1px solid black;
    border-radius: 5px;
    height: 150px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 30px;
  }
  .todo-container{
    width: auto;
    height: auto;
    display: flex;
    /* left: 300px;
    top: 100px; */
    /* position: absolute; */

  }
  .status{
    width: 300px;
    background-color: #f3f3f3;
    position: relative;
    padding-top: 60px;
    padding: 0.5rem 1rem;
  }
  .status:nth-child(even){
    background-color: #e9e9e96b;

  }
  .status h1{
    position: absolute;
    top: 0;
    left: 0;
    background-color: #343434;
    color: #f3f3f3;
    margin: 0;
    width: 100%;
    padding: 0.5rem 1rem;
  }

  #add_btn{
    padding: 0.5rem 1rem;
    background-color: #ccc;
    outline: none;
    border: none;
    width: 100%;
    font-size: 1.5rem;
    margin-top: 4rem;
    margin-bottom: 1rem;
    border-radius: 4px;
    cursor: pointer;
  }
  #add_btn:hover{
    background-color: #aaa;

  }
  .todo{
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    background-color: #fff;
    box-shadow: rgba(15,15,15,0.1) 0px 0px 0px 1px,
      rgba(15,15,15,0.1) 0px 2px 4px;
    border-radius: 4px;
    padding: 0.5rem 1rem;
    font-size: 1.5rem;
    margin-bottom: 10px;

  }

  .todo .close{
    position: absolute;
    right: 1rem;
    top: 0;
    font-size: 2rem;
    color: #ccc;
    cursor: pointer;
  }

  .todo .close:hover{
    color: #343444;
    /* color: #fbff00; */
  }
</style>