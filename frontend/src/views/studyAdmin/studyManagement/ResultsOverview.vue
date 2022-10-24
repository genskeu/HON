<template>
    <div class="container pt-4">
        <div id="results_ov" class="">
                <table class="table table-hover">
                    <thead class="thead-light">
                        <tr>
                            <!-- col-3 for width of cloumns does not work in chrome for tables use style="width: 25%" -->
                            <th style="width: 25%">Username</th>
                            <th style="width: 25%">Created</th>
                            <th style="width: 25%">Status</th>
                            <th style="width: 25%"></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="usp in usersStudyProgress" :key="usp">
                            <td class="align-middle">{{usp.username}}</td>
                            <td class="align-middle">{{usp.updated}}</td>
                            <td class="align-middle">{{Math.round(usp.imgsets_finished/studyLength * 10000)/100 + '%'}}</td>
                            <td class="align-middle">
                                <button class="btn-danger btn-sm" @click="delResultsUser(usp.user_id)">delete
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div class="row mb-3">
                    <div class="col-4">
                        <button class="btn btn-success btn-block" @click="downloadResults()">
                            <h6 class="">download results (xlsx)</h6>
                        </button>
                    </div>
                    <!-- <div class="col-4">
                        <input type="checkbox" name="include_explanations"
                            title="Adds a row to the output that explains each column (recomended for new users).">
                        include column explanations
                        <br>
                        <input type="checkbox" name="include_raw_data"
                            title="Include raw annotation data, all filenames if stacks were used ..."> include raw data
                    </div>
                    <div class="col-4">
                        <button class="btn btn-success btn-block get_seg_btn">
                            <h6 class="">download segmentations</h6>
                        </button>
                    </div> -->
                </div>
            </div>

    </div>
</template>

<script>
import { getResults } from '@/api'

export default {
  name: 'StudyResults',
  data () {
    return {
    }
  },
  methods: {
    downloadResults () {
      const studyId = this.$route.params.id
      getResults(studyId)
    },
    delResultsUser (userId) {
      this.$store.dispatch('currentStudy/delResultsUser', userId)
    }
  },
  computed: {
    usersStudyProgress () {
      return this.$store.getters['currentStudy/usersStudyProgress']
    },
    studyLength () {
      return this.$store.getters['currentStudy/imgsets'].length
    }
  },
  created () {
  }
}
</script>

<style>
</style>
