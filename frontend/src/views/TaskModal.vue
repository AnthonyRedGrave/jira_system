<template>
    <div class="popup_wrapper">
        <div class="place-popup">
      <div v-if="task_info !== null" class="popup__header">
          <span>
              {{task_info.title}}
          </span>
          <br>
      </div>
      <div v-else class="popup__header">
          <span>
              <label class="form-label" style="width: 450px;">Создание новой задачи</label>
              <hr>
          </span>
          <br>
      </div>
      <div v-if="task_info == null" class="popup__form_content">
          <input type="text" class="form-control" v-model="new_title" placeholder="Title">
          <input type="text" class="form-control" v-model="new_description" placeholder="Description">
          <select class="form-select" v-model="new_type_task" aria-label="Default select example">
            <option selected>Type Task</option>
            <option v-for="type in type_tasks" :key="type.id" :value="type.title">{{type.title}}</option>
          </select>
          <select class="form-select" v-model="new_epic_task" aria-label="Default select example">
            <option selected>Epic Task</option>
            <option v-for="epic in epic_tasks" :key="epic.id" :value="epic.title">{{epic.title}}</option>
          </select>
          <input type="text" class="form-control" v-model="new_developer" placeholder="Developer">
          <div v-if="manager_name == this.$store.state.username" class="project_developers">
              <div class="project_developer_block" @click="addDeveloper(dev)" v-for="dev in developers" :key="dev">
                  <i class='fas fa-user-alt' style='font-size:20px'></i>
                  {{dev}}
              </div>
          </div>
          <button class='btn btn-outline-secondary create_task_button' style="margin-top: 30px;" @click="createTask()">Создать</button>

      </div>
      <div v-else class="popup__content">
          {{task_info.description}}
          {{task_info.type}}
          {{task_info.epic}}
          {{task_info.developer}}
      </div>
      <div class="popup__footer">
          <button class="btn btn-danger" @click="closePopup()">Закрыть</button>
      </div>
  </div>
    </div>
</template>

<script>
export default {
    name: 'TaskModal',
    props:{
        task_info:{
            type: Object,
            default: () => {}
        },
        epic_tasks:{
            type: Array,
            default: () => {}
        },
        type_tasks:{
            type: Array,
            default: () => {}
        },
        developers:{
            type: Array,
            default: () => {}
        },
        manager_name:{
            type: String,
            default: ()=>{}
        }
    },
    data(){
        return {
            new_title: null,
            new_description: null,
            new_type_task: null,
            new_epic_task: null,
            new_developer: null,

        }
    },
    methods:{
        closePopup(){
            this.$emit('closePopup')
        },
        createTask(){
            let data = {
                title: this.new_title,
                description: this.new_description,
                type_task: this.new_type_task,
                epic_task: this.new_epic_task,
                implementer: this.new_developer,
            }
            this.$emit('createTask', data)
        },
        addDeveloper(dev){
            this.new_developer = dev
        }
    }
}
</script>

<style>
    .popup_wrapper{
        background: rgba(64, 64, 64, .4);
        display: flex;
        justify-content: center;
        align-items: center;
        position: absolute;
        right: 0;
        left: 0;
        top: 0;
        bottom: 0;
    }
    .place-popup{
        padding: 16px;
        position: fixed;
        top: 70px;
        left: 30%;
        z-index: 5;
        margin: 0 auto;
        width: 40%;
        height: auto;
        background: #ffffff;
        box-shadow: 0 0 17px 0 #e7e7e7;
    }
    .popup__header, .popup__footer{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .popup__content{
        display: flex;
        justify-content: center;
        padding: 70px;
        align-items: center;
    }
    .popup__form_content{
        display: flex;
        flex-direction: column;
        gap: 10px;
        justify-content: center;
        padding: 70px;
        align-items: center;
    }

    .project_developers{
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 30px;
    }

    .project_developer_block{
        border: 1px solid black;
        border-radius: 15px;
        padding: 5px;
    }
    .project_developer_block:hover{
        background: rgb(201, 201, 201);
        cursor: pointer;
    }
    .create_task_button{

    }
</style>