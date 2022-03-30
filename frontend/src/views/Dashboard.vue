<template>
  <div class="dashboard-vue">
    <div class="todo-container">
      <div class="status">
        <h1>No status</h1>
        <button id="add_btn">Add Task</button>
        <div class="todo">
          Buy a Pizza
          <span class="close">&times;</span>
        </div>
      </div>
      <div class="status">
        <h1>Not started</h1>
      </div>
      <div class="status">
        <h1>In progress</h1>
      </div>
      <div class="status">
        <h1>Completed</h1>
      </div>
    </div>
  </div>
</template>

<script>
import useSideBar from '@/components/composables/useSideBar'


export default {
    name: 'Dashboards',
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
  .dashboard-vue{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    box-sizing: border-box;
  }
  .todo-container{
    width: 1000px;
    height: 80vh;
    display: flex;

  }
  .status{
    width: 25%;
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
    margin: 4rem 0;
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