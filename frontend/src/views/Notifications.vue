<template>
  <div class="notifications-view">
      <div class="navigation_menu">
          <span class="navigation_el" @click="getNotifications">Все уведомления</span>
          <span class="navigation_el" @click="filterNotifications('invitation')">Приглашения</span>
          <span class="navigation_el" @click="filterNotifications('change')">Изменения</span>
          <span class="navigation_el" @click="filterNotifications('message')">Сообщения</span>
          <span class="navigation_el" @click="filterNotifications('task')">Назначения</span>
      </div>
      <hr>
      

      <div v-if="projects.length" class="projects_list_box">
          <div v-for="project in projects" :key="project.id" class="project_notifications_box">
            <div class="project_box">
                <span>Проект {{project.title}}</span>
                <hr>
                <span>Менеджер проекта: {{project.manager_name}}</span>
            </div>
            <div class="notifications_list_box">
                <Notification v-for="notification in project.notifications" :key="notification.id" :notification="notification"  @readNotification="readNotification"/>
            </div>
          </div>
      </div>
      <div v-else class="notifications_list_box">
          <div class="notification_box" v-for="notification in notifications" :key="notification.id">
                <div class="project__box" >
                    <span>{{notification.project_title}}</span>
                </div>
                <Notification :notification="notification" @readNotification="readNotification"/>
            </div>
      </div>
  </div>
</template>

<script>
import Notification from './Notification.vue'
import axios from 'axios'
export default {
    name: 'Notifications',
    components:{
        Notification
    },
    data(){
        return{
            projects: [],
            notifications:[]
        }
    },
    created(){
        this.getNotifications()
    },
    methods:{
        getNotifications(){
            this.$store.dispatch("getNotifications", {
                token: this.$store.state.accessToken,
            })
            .then((response) => {
                this.projects = response.data
            })
            .catch((err) => {
                console.log(err);
            });
        },
        filterNotifications(filter){
            axios
                .get(`http://localhost:8000/api/notifications/`, {
                headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
                params: {
                    type: filter
                },
                })
                .then((response) => {
                    this.projects = []
                    this.notifications = response.data
                })
                .catch((err) => {
                    console.log(err);
                });

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
    }
}
</script>

<style>
.navigation_menu{
    display: flex;
}

.navigation_el{
    color: #0d6efd;
    margin: 5px 15px 5px 0;
    cursor: pointer;
}

.navigation_el:hover{
    color: #002e74;
}

.notifications-view{
    padding-left: 50px;
    padding-top: 15px;
}

.project_notifications_box{
    margin-bottom: 35px;
}

.project_box{
    border: 1px solid #0d6efd;
    border-radius: 5px;
    width: 700px;
    height: 150px;
    padding: 15px;
    font-size: 22px;
    box-shadow: 0 0 5px rgba(0,0,0,0.5);
    margin-bottom: 20px;
    transition: background .35s;
    display: flex;
    flex-direction: column;

}

.project__box{
    border: 1px solid #0d6efd;
    border-radius: 5px;
    width: 575px;
    height: 150px;
    padding: 15px;
    font-size: 22px;
    box-shadow: 0 0 5px rgba(0,0,0,0.5);
    margin-bottom: 20px;
    transition: background .35s;
    display: flex;
    flex-direction: column;

}

.projects_list_box{
    display: flex;
    flex-direction: column;
}

.project_block:hover{
  background: rgb(228, 228, 228);
  box-shadow: 0 0 10px rgba(0,0,0,0.5);

}
</style>