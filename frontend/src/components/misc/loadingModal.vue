<template>
    <div ref="loadingScreen" class="modal fade" tabindex="-1" data-bs-backdrop="static">
        <div class="modal-dialog modal-dialog-centered">
            <!-- loading status -->
            <div class="mx-auto">
                <div class="row mx-auto" v-if="isLoading && !errorOccured">
                    <div  class="mx-auto spinner-border text-primary" role="status" style="width: 10rem; height: 10rem;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                <div v-if="title.length > 0 & !this.errorOccured" class="row mx-auto text-white">
                    <p class="h4">{{this.title}}</p>
                </div>
            </div>
            <!-- error text -->
            <div v-if="errorOccured" class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{'Error: ' + title}}</h5>
                </div>
                <div class="modal-body bg-opacity-10 bg-transparent">
                    {{errorMsg}}
                </div>
                <div class="modal-footer">
                    <button class="btn mx-auto btn-success" data-bs-dismiss="modal" @click.prevent="this.finishLoading">Dismiss</button>
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
    errorData: Object
  },
  data () {
    return {
      errorMsg: 'An error occured. Please try again.'
    }
  },
  watch: {
    isLoading (newState) {
      if (newState === true) {
        this.loadingModal.show()
      } else if (this.errorOccured === false) {
        const loadingModal = this.loadingModal
        setTimeout(function () {
          loadingModal.hide()
        }, 500)
      }
    },
    errorOccured (newState) {
      if (newState === true) {
        if (this.errorData !== null && this.errorData.response && this.errorData.response.data && this.errorData.response.data.error_msg) {
          this.errorMsg = this.errorData.response.data.error_msg
        } else {
          this.errorMsg = 'An unkown server error occured. Please try again.'
        }
      }
    }
  },
  mounted () {
    this.loadingModal = new Modal(this.$refs.loadingScreen, { fade: true })
  },
  methods: {
    finishLoading () {
      this.$store.commit('loadingState/finishLoading')
    }
  }
}
</script>

<style>

</style>
