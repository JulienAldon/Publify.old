<template>
    <header>
        <h1><a href="https://publify.aldon.info/">Spotils</a> // <a href="/">Publify</a></h1>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <aside>
            <a  href="http://auth.publify.aldon.info/api/auth/login" v-on:click="logUser">Log in</a>
            <a  href="http://auth.publify.aldon.info/api/auth/logout" v-on:click="logoutUser">Log Out</a>
        </aside>
    </header>
</template>
<script>
import { store, mutations } from "../store";

export default {
    computed: {
    },
    mounted() {
    },
    methods: {
        logged() {
            return mutations.checkUserLogged()
        },
        logoutUser() {
            sessionStorage.setItem('status','loggedOut') 
        },
        logUser() {
            console.log('bite')
            sessionStorage.setItem('status','loggedIn') 
        }
    }
}
</script>
