<template>
<div id="study_overview" class="">
  <div id="nav" class="navbar bg-dark p-0" style="height: 50px;">
        <div class="container">
          <div class="row">
            <router-link to="#" @click.prevent="createStudy" class="btn btn-succcess">Create New Study
            </router-link>
          </div>
        </div>
  </div>
  <div class="container">
        <div class="row mx-auto mt-4" id="studies_ov">
            <delte-modal :title="deleteTitle" :text="deleteText" id="deleteStudy" @deleteComfirmed="deleteStudy(this.deleteIdDb)"></delte-modal>
            <loadingModal id="loadingModal" ref="loadingScreen"></loadingModal>
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
                    </tr>
                </tbody>
            </table>
        </div>
  </div>
</div>

</template>

<script>
import delteModal from '@/components/misc/confirmDeleteModal'
import loadingModal from '@/components/misc/loadingModal'

export default {
  name: 'StudyOverview',
  components: {
    delteModal,
    loadingModal
  },
  data () {
    return {
      deleteText: String,
      deleteTitle: String,
      deleteIdDb: Number
    }
  },
  computed: {
    studies () {
      return this.$store.state.studies.studies
    }
  },
  methods: {
    createStudy () {
      this.$store.dispatch('openStudy/createNewStudy')
    },
    setStudyDelete (study) {
      this.deleteText = 'You are about to delete study ' + study.title + '. This will also delete all results.'
      this.deleteTitle = study.title
      this.deleteIdDb = study.id
    },
    deleteStudy (studyId) {
      this.$store.dispatch('studies/deleteStudy', { studyId: studyId, loadingComp: this.$refs.loadingScreen })
    }
  },
  created () {
    this.$store.dispatch('studies/initStudies')
  }
}
</script>

<style>
</style>
