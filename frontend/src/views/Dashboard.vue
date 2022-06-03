<template>
  <div class="dashboard-vue">
    <div v-if="projectInfo.manager_name == this.$store.state.username" class="tasks_form-block">
      <h2>Панель менеджера проекта</h2>
      <div class="btn btn-outline-secondary add_type_btn" @click="showCreateTypeTaskForm($event)" style="margin-right: 15px;">Добавить тип для задач</div>
      <div class="type_task_title">
        <input class="form-control type_task_title_input" placeholder="Новый тип задач" v-model="newTypeTaskTitle" type="text">
        <button class="btn btn-outline-secondary" @click="createTypeTask()">Добавить</button>
      </div>
    </div>
    <div class="errors__block">
      <div v-if="errorText" class="alert alert-danger" role="alert">
        {{errorText}}
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
      <!-- @dragenter="dragEnter($event)" @dragleave="dragLeave($event)" -->
      <div class="status" v-for="(status, index) in Object.keys(dashboardData)" :key="status" :id=status @dragover="dragOver($event)" @drop="dragDrop($event)">
        <h1>{{status}}</h1>
        <button v-if="index == 0" @click="addNewTask()" id="add_btn">Add Task</button>
        <button v-else id="add_btn" style="opacity: 0;cursor: default;">Add Task</button>
        <div v-for="task in dashboardData[status]" :style="{'border': `1px solid ${task.epic_color}`}" :key="task" class="todo" :id=task.id @dragstart="dragStart($event, task)" @dragend="dragEnd($event)" draggable="true" data-bs-toggle="modal" data-bs-target="#exampleModal"> 
          <span @click="showPopup(task)">{{task.title}}</span>
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

export default {
    name: 'Dashboard',
    components:{
        TaskModal
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
      }
    },
    created(){
      this.get()
      this.getProjectInfo()
      this.getDashboardData()
    },
    methods:{
      get(){
        this.$emit('selectSideBarLine', 'Dashboards')
      },
      showCreateTypeTaskForm(element){
        let panel = element.target.nextElementSibling
        if (panel.style.maxHeight) {
          panel.style.maxHeight = null;
        } else {
          panel.style.maxHeight = panel.scrollHeight + "px";
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
      // dragEnter(el){
      //   console.log(el.target)
      //   // this.source_epic_color = el.target
      //   if (el.target.className === "todo" && el.target.className === "status"){
      //     el.target.style.border = "3px solid black"
      //   }
      // },
      // dragLeave(el){
      //   console.log(el.target)
      //   // el.target.style.border = "none"
      // },
      dragDrop(el){
        let status_title = null
        if (el.target.className === "status"){
          status_title = el.target.id
          el.target.appendChild(this.draggableTodo)
          // el.target.style.border = "none" 
        }
        else if(el.target.className === "todo"){
          status_title = el.target.parentElement.id
          el.target.parentElement.appendChild(this.draggableTodo)
          // el.target.style.border = "none"
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

  .type_task_title{
    margin-top: 20px;
    margin-bottom: 20px;
    /* padding: 0 18px; */
    background-color: white;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.2s ease-out;
  }
  .type_task_title_input{
    margin-bottom: 10px;
    width: 204px;
  }
  .add_type_btn{
    margin-top: 10px;
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