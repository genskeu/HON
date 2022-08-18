<template>
    <div class="modal fade" tabindex="-1" data-bs-backdrop="static">
        <div class="modal-dialog modal-dialog-centered">
            <!-- loading status -->
            <div class="mx-auto">
                <div v-if="loading" class="row mx-auto">
                    <div  class="mx-auto spinner-border text-primary" role="status" style="width: 10rem; height: 10rem;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                <div class="row mx-auto text-white">
                    <p class="h4">{{this.text}}</p>
                </div>
            </div>
            <!-- error text -->
            <div v-if="error" class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{this.title}}</h5>
                </div>
                <div class="modal-body bg-opacity-10 bg-transparent">
                    {{this.errorMsg}}
                </div>
                <div class="modal-footer">
                    <button class="btn mx-auto btn-success" data-bs-dismiss="modal">Dismiss</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  props: {
    loading: Boolean,
    text: String,
    error: Boolean,
    title: String,
    errorMsg: String
  },
  data () {
    return {
    }
  }
}
</script>

<style>

</style>
