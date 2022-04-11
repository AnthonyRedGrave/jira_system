<template>
    <div class="popup_wrapper">
        <div class="place-popup">
      <div class="popup__header">
          <span>
              {{task_info.title}}
          </span>
          <br>
      </div>
      <div class="popup__content">
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
        }
    },
    methods:{
        closePopup(){
            this.$emit('closePopup')
        },
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
</style>