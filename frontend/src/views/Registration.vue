<template>
  <div class="registration__view">
    <h2 style='margin-top: 15px; margin-left: 30px;'>Регистрация</h2>
    <div class="v-login">
            <div v-if="inCorrectAuth" class="alert alert-danger" role="alert">
                Неверный логин!
            </div>
            <form @submit.prevent="register">
                <div class="mb-3">
                    <label for="exampleInputEmail1" class="form-label">Логин</label>
                    <input v-model="username" type="text" class="form-control" aria-describedby="emailHelp">
                </div>
                <div class="mb-3">
                    <label for="exampleInputEmail1" class="form-label">Имя</label>
                    <input v-model="first_name" type="text" class="form-control"  aria-describedby="emailHelp">
                </div>
                <div class="mb-3">
                    <label for="exampleInputEmail1" class="form-label">Фамилия</label>
                    <input v-model="last_name" type="text" class="form-control"  aria-describedby="emailHelp">
                </div>
                <div class="mb-3">
                    <label for="exampleInputPassword1" class="form-label">Пароль</label>
                    <input v-model="password" type="password" class="form-control" >
                </div>
                
                <button type="submit" class="btn btn-primary">Регистрация</button>
            </form>
        </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Registration',
    data(){
        return {
            username: '',
            first_name: '',
            last_name: '',
            password: '',
            inCorrectAuth: false
        }
    },
    methods:{
        register(){
            axios({
                method: "post",
                url: `http://localhost:8000/api/users/register/`,
                
                data: {
                    username: this.username,
                    first_name: this.first_name,
                    last_name: this.last_name,
                    password: this.password,
                },
                credentials: "include",
                })
                .then((responce) => {
                    console.log(responce.data)
                    this.$router.push({ path: 'login'})            
                })
                .catch((err) => {
                    console.log(err);
                })
        }
    }
}
</script>

<style>
    .registration__view{
        width: 900px;
    }
</style>