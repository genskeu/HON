<template>
    <div class="modal fade" tabindex="-1" data-bs-backdrop="static">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{this.title}}</h5>
                    <button class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>{{this.text}}</p>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button class="btn btn-danger" data-bs-dismiss="modal" @click="this.$emit('deleteComfirmed')">Delete</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  props: {
    title: undefined,
    text: undefined
  },
  data () {
    return {
    }
  }
}
</script>

<style>

</style>
