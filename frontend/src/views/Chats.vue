<template>
  <div class="chats__view">
    <div class="chats__view_title" style='margin-top: 15px;'>
      <h2>Мессенджер</h2>
    </div>
    <hr>
      <div class="chats__action_buttons">
        <button class="btn btn-outline-primary" @click="showAddDeveloper($event)">Создать чат</button>

        <button class="btn btn-outline-primary">Удалить чат</button>
      </div>
      <div class="add_new_developer_block">
        <input class="form-control developer_name" placeholder="Имя пользователя" @input="seachDevelopers" v-model="developer_name" type="text">
        <div class="block-developers">
          <div v-for="dev in found_developers" :key="dev.id" class="devel-block">
            <div class="developer-name" @click="findDeveloper(dev.username)">
              {{dev.username}}
            </div>
          </div>
        </div>
        <button class="btn btn-outline-secondary add_new_developer_btn" :disabled="canAddDeveloperToProject" @click="createChat()">Создать чат</button>
      </div>
      <div class="chats__list">
        <chat-block :chat="chat" @toChat='toChat' v-for="chat in chats" :key="chat.id"/>
      </div>
  </div>
</template>

<script>
import axios from 'axios'
import ChatBlock from './ChatBlock.vue'
export default {
  components: { ChatBlock },
  name: 'Chats',
  data(){
    return{
      chats:[],
      newMemberChat: null,
      developer_name: null,
      found_developer_name: null,
      found_developers: [],

    }
  },
  created() {
    this.getChats()
  },
  computed:{
      canAddDeveloperToProject(){
        if (this.found_developer_name !== null){
          return false
        }
        return true
      },
    },
  methods:{
    getChats(){
      axios
                .get(`http://localhost:8000/api/chats/`, {
                headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
                })
                .then((response) => {
                    console.log(response.data)
                    this.chats = response.data
                })
                .catch((err) => {
                    console.log(err);
                });
    },
    seachDevelopers(){
        if (this.developer_name){
          axios
                .get(`http://localhost:8000/api/users`, {
                headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
                params: {
                    username: this.developer_name
                },
                })
                .then((response) => {
                  // response.data.forEach((element)=>{
                  //   this.found_developers = response.data
                  // })
                  this.found_developers = response.data
                  
                })  
                .catch((err) => {
                    console.log(err);
                });
        }
        else{
          this.found_developers = []

        }
      },
    showAddDeveloper(element){
      let panel = element.target.parentNode.nextElementSibling
      // console.log(panel)
        if (panel.style.maxHeight) {
          panel.style.maxHeight = null;
        } else {
          panel.style.maxHeight = panel.scrollHeight + "px";
          
        }
    },
    findDeveloper(developer_name){
        this.found_developer_name = developer_name
        this.developer_name = developer_name
    },
    toChat(id){
      this.$router.push({ path: 'chat', query: {'id': id }})
    },
    createChat(){
      
      let data = {
        member_1: this.$store.state.username,
        member_2: this.developer_name
      }
      axios({
          method: "post",
          url: 'http://localhost:8000/api/chats/',
          data: data,
          headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
          })
          .then(() =>{
            this.getChats()
            this.found_developer_name = null
            this.developer_name = null
          })
          .catch((err) => {
                console.log(err);
          });
    }
  }
}
</script>

<style>
  .chats__view{
    width: 650px;
  }
  .chats__action_buttons{
    display: flex;
    flex-direction: row;
    gap: 20px;
  }
  .developer-name{
    cursor: pointer;
  }
  .chat__block{
    display: flex;
    flex-direction: row;
    gap: 30px;
    justify-content: space-around;
    border: 1px solid black;
    border-radius: 10px;
    padding: 15px;
    padding-left: 0px;
  }
  .chats__list{
    display: flex;
    flex-direction: column;
    gap: 30px;
  }
</style>