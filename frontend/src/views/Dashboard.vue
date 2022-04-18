<template>
  <div class="dashboard-vue">
    <div class="todo-container">
      <task-modal v-if="isInfoPopupVisible" :task_info="task_info" @closePopup="closePopup"></task-modal>
      <div class="status" v-for="(status, index) in Object.keys(dashboardData)" :key="status" @dragover="dragOver($event)" @dragenter="dragEnter($event)" @dragleave="dragLeave($event)" @drop="dragDrop($event)">
        <h1>{{status}}</h1>
        <button v-if="index == 0" id="add_btn">Add Task</button>
        <button v-else id="add_btn" style="opacity: 0;cursor: default;">Add Task</button>
        <div v-for="task in dashboardData[status]" :key="task" class="todo" @click="showPopup(task)" @dragstart="dragStart($event)" @dragend="dragEnd($event)" draggable="true" data-bs-toggle="modal" data-bs-target="#exampleModal"> 
          {{task.title}}
          <span class="close">&times;</span>
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
    name: 'Dashboards',
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
        tasks: [],
        statuses: [],
        dashboardData: null,
        task_info: null,
        isInfoPopupVisible: false
      }
    },
    created(){
      this.get()
      this.getDashboardData()
    },
    methods:{
      get(){
        this.$emit('selectSideBarLine', 'Dashboards')
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
      },
      dragStart(el){
        this.draggableTodo = el.target
      },
      dragEnd(){
        this.draggableTodo = null
        
      },
      dragOver(e){
        e.preventDefault();

      },
      dragEnter(el){
        el.target.style.border = "3px solid black"
      },
      dragLeave(el){
        el.target.style.border = "none"
      },
      dragDrop(el){
        if (el.target.className === "status"){
          el.target.appendChild(this.draggableTodo)
          el.target.style.border = "none" 
        }
        else if(el.target.className === "todo"){
          el.target.parentElement.appendChild(this.draggableTodo)
          el.target.style.border = "none" 
        }
        
      }
    }
}
</script>

<style>
  .dashboard-vue{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    box-sizing: border-box;
  }
  .todo-container{
    width: auto;
    height: auto;
    display: flex;

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
  }
</style>