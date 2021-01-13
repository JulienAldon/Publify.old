<template>
    <dialog ref="new">
        <i v-if="message == 'done'" class="material-icons">done</i>
        <i v-else class="material-icons">error</i>
    </dialog>
</template>
<script>
export default {
    props: {
        message: String
    },
    methods: {
        show() {
            if (this.$refs.new.open) {
                this.$refs.new.close();
            }
            this.$refs.new.showModal();
        },
        hide() {
            this.$refs.new.close();
        },
    }
}
</script>
