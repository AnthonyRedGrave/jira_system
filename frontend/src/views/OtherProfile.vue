<template>
  <div class="profile__view">
    <div class="profile__title" style="margin-top: 15px;">
        <h2>Профиль</h2>
        <hr>
    </div>
    <div class="profile__account">
        <div class="profile__image">
            <img class="profile__image__block" v-bind:src='`http://localhost:8000`+profile.image' alt="">
        </div>
        <div class="project__user_info">
            <div class="profile__username">
                <h2>Логин: {{profile.username}}</h2>
            </div>
            <div class="profile__first_name">
                <h2>Имя: {{profile.first_name}}</h2>
            </div>
            <div class="profile__last_name">
                <h2>Фамилия: {{profile.last_name}}</h2>
            </div>
            <div class="profile__position">
                <h2>Должность: {{profile.position}}</h2>
            </div>
        </div>
    </div>
    <div class="profile__dev_info">
        <h3 style="margin-bottom: 35px;">Проекты</h3>
        <div class="profile__projects">
            <div v-for="project in profile.projects" :key="project.id" class="project_block">
          <div class="project_title">
            Проект {{project.title}}
          </div>
          <div class="project_description">
            <span>Тип {{project.type}}</span> 
            <span>Менеджер {{project.manager_name}}</span>
          </div>
        </div>
        </div>
        <h3 style="margin-bottom: 35px; margin-top: 15px;" v-if="profile.tools.length !== 0">Инструменты</h3>
        <div class="profile__tools" v-if="profile.tools.length !== 0">
            <div v-for="tool in profile.tools" :key="tool" class="profile__tool">
                <div class="profile__tool_title">
                    <h5>{{tool.title}}</h5> 
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'OtherProfile',
    data(){
        return{
            profile: null
        }
    },
    created(){
        this.getProfile()
    },
    methods:{
        getProfile(){
            axios
                .get(`http://localhost:8000/api/users/${this.$route.query.id}/other_profile`, {
                headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
                })
                .then((response) => {
                    this.profile = response.data
                })
                .catch((err) => {
                    console.log(err);
                });
        }
    }
}
</script>

<style scoped>
    .profile__view{
        width: 1000px;
    }
    .profile__image__block{
        width: 200px;
        height: 200px;
        
    }
    .profile__image{
        border: 1px solid grey;
    }
    .profile__account{
        display: flex;
        flex-direction: row;
        gap: 20px;
        border-bottom: 1px solid black;
        padding-bottom: 15px;
    }
    .profile__dev_info{
        padding-top: 25px;
    }
    .project_block{
        height: 200px;
    }
    .project_title{
        border-bottom: 1px solid black;
        padding-bottom: 10px;
    }
    .project_description{
        padding-top: 15px;
    }
    .profile__projects{
        display: flex;
        flex-wrap: wrap;
        border-bottom: 1px solid black;
    }
    .profile__tools{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 40px;

    }
    .profile__tool{
        border: 1px solid black;
        padding: 6px;
        width: auto;
        display: inline-block;
        border-radius: 7px;
    }
</style>