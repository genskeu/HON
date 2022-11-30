<template>
    <div ref="studyDescription" class="modal fade text-dark" tabindex="-1" data-bs-backdrop="static">
        <div class="modal-dialog modal-dialog-centered  modal-lg">
            <div  class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title"><pre>{{this.studyTitle}}</pre></h5>
                </div>
                <div class="modal-body bg-opacity-10 bg-transparent text-nowrap">
                    <pre class="text-left">{{studyDescription}}</pre>
                </div>
                <div class="modal-footer">
                    <button class="btn mx-auto btn-success" data-bs-dismiss="modal" @click="this.btnText = 'Continue Study'">{{this.btnText}}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { Modal } from 'bootstrap'

export default {
  name: 'DescriptionParticipation',
  data () {
    return {
      btnText: 'Start Study'
    }
  },
  mounted () {
    var loadingModal = new Modal(this.$refs.studyDescription, { fade: true })
    loadingModal.show()
  },
  methods: {
  },
  computed: {
    studyTitle: {
      get () {
        return this.$store.getters['currentStudy/studyTitle']
      }
    },
    studyDescription: {
      get () {
        return this.$store.getters['currentStudy/studyDescription']
      }
    }
  }
}
</script>

<style>

</style>
