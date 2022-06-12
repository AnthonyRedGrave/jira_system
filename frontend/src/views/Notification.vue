<template>
  <div :class="notificationClass" style="display:flex; justify-content:space-between; align-items:center;" role="alert">
      <div class="notification_body" style="display:flex; flex-direction: column">
          <span>От пользователя: {{notification.username_from}}</span>
          <span>{{notification.type_notification}}</span>
          <div v-if="notification.message" class="notificication_message_block">
              <hr>
              <span class="notificication_message_text">{{notification.message}}</span>
              <span class="notification_route_chat" @click="toChat(notification.username_to, notification.username_from)">Перейти в чат с пользователем</span>
          </div>
          <div v-if="notification.task" class="notification_task">
              <span class="notification_task_text">Задача {{notification.task.title}}</span>
              <span class="notification_task_type">{{notification.task.type}}</span>
              <span class="notification_task_epic">{{notification.task.epic}}</span>
              <span v-if="notification.message" class="notificication_message_text">{{notification.message}}</span>
              <span class="notification_route_task">Перейти на доску проекта</span>
          </div>
      </div>
      <button type="button" @click="readNotification(notification)" class="btn-close" aria-label="Close"></button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Notification',
    props:{
        notification:{
            type: Object,
            default: ()=>{}
        }
    },
    computed:{
        notificationClass: function(){
            return{
                "alert alert-primary": this.notification.type === "task",
                "alert alert-success": this.notification.type === "invitation",
                "alert alert-warning": this.notification.type === "change",
                "alert alert-secondary": this.notification.type === "message"
            }
        }
    },
    methods:{
        readNotification(notification){
            this.$emit('readNotification', notification)
        },
        toChat(username_to, username_from){
            axios({
                method: "get",
                url: `http://localhost:8000/api/chats/`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                params:{
                  member_1: username_to,
                  member_2: username_from
                },
                credentials: "include",
                })
                .then((responce) => {
                  this.dashboardData = responce.data                  
                })
                .catch((err) => {
                console.log(err);
                })
        }
    }
}
</script>

<style>
.notificication_message_block{
    display: flex;
    flex-direction: column;
}
.notificication_message_text{
    font-size: 16px;
    font-weight: bold;
}

.notification_task{
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    align-content: flex-start;
    align-items: flex-start;
    border-top: 1px solid black;
    margin-top: 10px;
    padding-top: 5px;
}

.notification_task_text{
    font-size: 20px;

}

.notification_task_type{
    border: 1px solid black;
    padding: 3px;
    color: black;
    background: rgb(236, 236, 236);
    border-radius: 5px;
    margin-bottom: 5px;
}

.notification_task_epic{
    border: 1px solid black;
    color: black;
    background: rgb(241, 255, 227);
    padding: 3px;
    border-radius: 5px;
}

.notification_route_chat, .notification_route_task{
    font-size: 14px;
    margin-top: 5px;
    cursor: pointer;
}
</style>