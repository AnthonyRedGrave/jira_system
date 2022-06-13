<template>
    <div class="chat__block">
        <div class="chat__image">
            <img v-bind:src="secondMember.image" class="developer_image" alt="...">
        </div>
        <div class="chat__info">
            <div class="chat__title">
                Чат с пользователем: {{secondMember.username}}
            </div>
            <div class="chat__last_message">
                {{chat.last_message}}
            </div>
        </div>
        <div class="chat__action_buttons">
            <button class='btn btn-outline-primary'>Перейти</button>
            <button class="btn btn-outline-secondary">Профиль</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ChatBlock',
    props:{
        chat:{
            type: Object,
            default: ()=>{}
        }
    },
    data(){
        return{
            secondMember: null
        }
    },
    created() {
        this.getSecondMember()
    },
    methods: {
        getSecondMember(){
            if (this.$store.state.username == this.chat.member_1){
                this.secondMember = this.chat.user_2
            }
            else{
                this.secondMember = this.chat.user_1
            }
        }
    },
}
</script>

<style>
    .chat__info{
        display: flex;
        flex-direction: column;
    }
    .chat__title{
        border-bottom: 1px solid grey;
        margin-bottom: 15px
    }
    .chat__action_buttons{
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
</style>