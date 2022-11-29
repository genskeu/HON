<template>
<div id="study_overview" class="container">
  <div class="">
        <div class="row mx-auto" id="studies_ov">
            <delte-modal :title="deleteTitle" :text="deleteText" id="deleteStudy" @deleteComfirmed="deleteStudy(this.deleteIdDb)"></delte-modal>
            <!-- <loadingModal id="loadingModal" ref="loadingScreen"></loadingModal> -->
            <table class="table table-hover">
                <thead class="thead-light">
                    <tr>
                        <th>Name</th>
                        <th>Study Id</th>
                        <th>Created</th>
                        <th>Modified</th>
                        <th></th>
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
                          <button @click="editStudy(study.id)" class="btn-success btn">edit</button>
                        </td>
                        <td>
                          <button @click="showResults(study.id)" class="btn-primary btn">results</button>
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
import router from '@/router'

export default {
  name: 'StudyOverview',
  components: {
    delteModal
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
    editStudy (studyId) {
      this.$store.dispatch('currentStudy/openStudy', studyId)
        .then(() => {
          router.push(studyId + '/metainfos')
        })
    },
    showResults (studyId) {
      this.$store.dispatch('currentStudy/openStudy', studyId)
        .then(() => {
          router.push(studyId + '/results')
        })
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
  mounted () {
    this.$store.dispatch('studies/initStudies')
  }
}
</script>

<style>
</style>
