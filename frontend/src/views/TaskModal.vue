<template>
    <div class="popup_wrapper">
        <div class="place-popup">
      <div v-if="task_info !== null" class="popup__header">
          <span>
              ЗАДАЧА: {{task_info.title}}
              <hr>
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
          <div class="popup_task__description">
              <h4>Описание:</h4> <p class="popup_task__description__change" @click="showChangeFormDescription()">Изменить</p>
              <textarea v-if="canShowChangeFormDescription" name="form__description" class="form-control" id="" cols="80" rows="5" :value='task_info.description'></textarea>
              <button v-if="canShowChangeFormDescription" class='btn btn-outline-primary change_description_button' style="margin-top: 15px; margin-bottom: 15px" @click="changeDescription()">Изменить</button>
              <p v-if="!canShowChangeFormDescription">{{task_info.description}}</p>
          </div>
          <div class="popup_task__type" align='left'>
              <h4>Тип задачи:</h4>  
              <div class="popup_task__type__title">
                  {{task_info.type}}
              </div>
          </div>
          <div class="popup_task__epic">
             <h4>Епик задачи:</h4>  <div class="popup_task__type__title">
                  {{task_info.epic}}
              </div>
          </div>
          <div class="popup_task__developer">
             <h4>Разработчик:</h4>  
             <div class="popup_task__developer__title">
                 {{task_info.developer}}
             </div>
          </div>
          
          
          
          
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
            canShowChangeFormDescription: false

        }
    },
    // computed:{
    //     canShowChangeFormDescription(){

    //     },
    // },
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
        },
        showChangeFormDescription(){
            this.canShowChangeFormDescription = !this.canShowChangeFormDescription

        }
    }
}
</script>

<style>
    .popup_wrapper{
        background: rgba(64, 64, 64, .4);
        display: flex;
        height: 1100px;
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
    .popup_task__description__change{
        font-size: 14px;
        color: rgb(128, 128, 255);
        cursor: pointer;
    }
    .popup__content{
        display: flex;
        flex-direction: column;
        gap: 10px;
        justify-content: center;
        padding: 70px;
        align-items: flex-start;
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
    .popup_task__type__title{
        border: 1px solid black;
        border-radius: 4px;
        padding: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .popup_task__developer__title{
        border: 1px solid black;
        border-radius: 4px;
        padding: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>