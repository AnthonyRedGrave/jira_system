<template>
  <div class="profile__view">
        {{profile}}
  </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Profile',
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
                .get(`http://localhost:8000/api/users/profile/`, {
                headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
                })
                .then((response) => {
                    console.log(response.data)
                    this.profile = response.data
                })
                .catch((err) => {
                    console.log(err);
                });
        }
    }
}
</script>

<style>

</style>