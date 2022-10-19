<template>
    <div ref="loadingScreen" class="modal fade" tabindex="-1" data-bs-backdrop="static">
        <div class="modal-dialog modal-dialog-centered">
            <!-- loading status -->
            <div class="mx-auto">
                <div v-if="isLoading" class="row mx-auto">
                    <div  class="mx-auto spinner-border text-primary" role="status" style="width: 10rem; height: 10rem;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                <div v-if="title.length > 0" class="row mx-auto text-white">
                    <p class="h4">{{this.title}}</p>
                </div>
            </div>
            <!-- error text -->
            <div v-if="errorOccured" class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{title}}</h5>
                </div>
                <div class="modal-body bg-opacity-10 bg-transparent">
                    {{errorMsg}}
                </div>
                <div class="modal-footer">
                    <button class="btn mx-auto btn-success" data-bs-dismiss="modal">Dismiss</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { Modal } from 'bootstrap'

export default {
  props: {
    isLoading: Boolean,
    title: String,
    errorOccured: Boolean,
    errorMsg: String
  },
  data () {
    return {
    }
  },
  mounted () {
    this.loadingModal = new Modal(this.$refs.loadingScreen, { fade: true })
  },
  watch: {
    isLoading (newState) {
      if (newState === true) {
        this.loadingModal.show()
      } else {
        const loadingModal = this.loadingModal
        setTimeout(function () {
          loadingModal.hide()
        }, 500)
      }
    }
  }
}
</script>

<style>

</style>
