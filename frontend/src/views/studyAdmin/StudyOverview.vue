<template>
<div id="study_overview" class="">
  <div id="nav" class="navbar bg-dark p-0" style="height: 50px;">
        <div class="container">
          <div class="row">
            <router-link to="#" @click="createStudy" class="btn btn-succcess">Create New Study
            </router-link>
          </div>
        </div>
  </div>
  <div class="container">
        <div class="row mx-auto mt-4" id="studies_ov">
            <delte-modal :title="deleteTitle" :text="deleteText" id="deleteStudy" @deleteComfirmed="deleteStudy(this.deleteIdDb)"></delte-modal>
            <loadingModal id="loadingModal"></loadingModal>
            <table class="table table-hover">
                <thead class="thead-light">
                    <tr>
                        <th>Name</th>
                        <th>Study Id</th>
                        <th>Created</th>
                        <th>Modified</th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="study in studies" :key="study.id">
                        <td class="align-middle">{{study.title}}</td>
                        <td class="align-middle">{{study.id}}</td>
                        <td class="align-middle">{{study.created}}</td>
                        <td class="align-middle">{{study.updated}}</td>
                        <td>
                            <router-link :to="{ name: 'StudyMetainfos', params: { id: study.id }}">
                                <button class="btn-success btn">edit</button>
                            </router-link>
                        </td>
                        <td>
                            <router-link :to="{ name: 'StudyResults', params: { id: study.id }}">
                                <button class="btn-primary btn">results</button>
                            </router-link>
                        </td>
                        <td>
                            <button class="btn-danger btn" data-bs-toggle="modal" data-bs-target="#deleteStudy" @click="setStudyDelete(study)">delete
                            </button>
                        </td>
                        <td>
                        <button class="btn-danger btn" @click="showLoadingModal">load
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
  </div>
</div>

</template>

<script>
import axios from 'axios'
import delteModal from '@/components/misc/confirmDeleteModal'
import loadingModal from '@/components/misc/loadingModal'
import { Modal } from 'bootstrap'

export default {
  name: 'StudyOverview',
  components: {
    delteModal,
    loadingModal
  },
  data () {
    return {
      studies: [],
      deleteText: String,
      deleteTitle: String,
      deleteIdDb: Number
    }
  },
  methods: {
    createStudy () {
      this.$store.dispatch('openStudy/createStudy')
    },
    setStudyDelete (study) {
      this.deleteText = 'You are about to delete study ' + study.title + '. This will also delete all results.'
      this.deleteTitle = study.title
      this.deleteIdDb = study.id
    },
    deleteStudy (studyId) {
      axios
        .delete('http://localhost:5000/study/' + studyId)
        .then(response => {
          const index = this.studies.findIndex(study => study.id === studyId)
          this.studies.splice(index, 1)
        })
        .catch(error => console.log(error))
        .then()
    },
    showLoadingModal () {
      var myModal = new Modal(document.getElementById('loadingModal'))
      myModal.toggle()
    }
  },
  computed: {
  },
  created () {
    axios
      .get('http://localhost:5000/studies')
      .then((response) => {
        const overview = response.data
        overview.studies.forEach((study) => {
          this.studies.push(study)
        })
      })
  }
}
</script>

<style>
</style>
