<template>
    <main>
        <table style="overflow-y: auto">
            <thead>
                <tr>
                    <th>Public Playlist</th>
                    <th>Contributive Playlist</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in playlist_links" :key="item.id">
                    <td>{{item.public.name}}</td>
                    <td>{{item.collaborative.name}}</td>
                    <td :id="item.id" ref="link" class="item-actions actions">
                        <button @click="() => syncBack(item.linkId)"><i @mouseover="() => clearStatus('Backward'+item.linkId)" :id="'Backward' + item.linkId" class="material-icons">arrow_back</i></button>
                        <button @click="() => syncForward(item.linkId)"><i @mouseover="() => clearStatus('Forward'+item.linkId)" :id="'Forward' + item.linkId" class="material-icons">arrow_forward</i></button>
                        <button @click="() => deleteLink(item.linkId)"><i class="danger material-icons">delete</i></button>
                    </td>
                </tr>
            </tbody>
        </table>
        <footer class="actions">
        <button id="new-button" ref="new-button" @click="() => this.$refs.new.show()"><i class="material-icons">add_circle_outline</i></button>
        </footer>
        <message ref="messageStatus" :message="addLinkStatus"></message>
        <base-modal v-on:status="setStatus" ref="new" id="new"></base-modal>
    </main>
</template>
<script>
import Message from './Message.vue';
import BaseModal from './ModalPlaylist.vue';
import { store, mutations } from "../store";
export default {
    components: {
      BaseModal,  
      Message,
    },
    data() {
        return {
            item: null,
            addLinkStatus: null,
        }
    },
    mounted() {
        this.getLinkedPlaylist();
    },
    computed: {
        playlist_links() {
            return store.user_playlist_links;
        },
    },
    methods: {
        setStatus(status) {
            this.addLinkStatus = status;
            this.$refs.messageStatus.show();
        },
        clearStatus(id) {
            if (!document.getElementById(id).classList.contains("warning")) {
                document.getElementById(id).classList.remove("success");
            }
        },
        syncBack(id) {
            mutations.syncUserPlaylist(id, 'Backward')
        },
        syncForward(id) {
            mutations.syncUserPlaylist(id, 'Forward')
        },
        deleteLink(id) {
            mutations.deleteUserPlaylistLink(id);
        },
        getLinkedPlaylist() {
            mutations.setUserPlaylistLinks();
        }
    }
}
</script>