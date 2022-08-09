<template>
    <div class="container pt-2">
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
                        <tr v-for="usp in userStudyProgress" :key="usp">
                            <td class="align-middle">{{usp.username}}</td>
                            <td class="align-middle">{{usp.updated}}</td>
                            <td class="align-middle">{{usp.imgsets_finished/studyLength * 100 + '%'}}</td>
                            <td class="align-middle">
                                <button class="btn-danger btn-sm" onclick="">delete
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div class="row mb-3">
                    <div class="col-4">
                        <button id="results_study_{{study.id}}" class="btn btn-success btn-block get_results_btn">
                            <h6 class="mt-1">download results (xlsx)</h6>
                        </button>
                    </div>
                    <div class="col-4">
                        <input type="checkbox" id="include_explanations_{{study.id}}" name="include_explanations"
                            title="Adds a row to the output that explains each column (recomended for new users).">
                        include column explanations
                        <br>
                        <input type="checkbox" id="include_raw_data_{{study.id}}" name="include_raw_data"
                            title="Include raw annotation data, all filenames if stacks were used ..."> include raw data
                    </div>
                    <div class="col-4">
                        <button id="segmentation_study_{{study.id}}" class="btn btn-success btn-block get_seg_btn">
                            <h6 class="mt-1">download segmentations</h6>
                        </button>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-4">
                        <div class="row justify-content-center">
                            <div id="loader_anim_{{study.id}}" class=""></div>
                            <div id="loader_text_{{study.id}}" class="ml-1 mt-3" style="display: none;">Please wait
                            </div>
                        </div>
                    </div>
                </div>

            </div>

    </div>
</template>

<script>
export default {
  name: 'StudyResults',
  data () {
    return {
    }
  },
  methods: {
  },
  computed: {
    userStudyProgress () {
      return this.$store.getters['openStudy/userStudyProgress']
    },
    studyLength () {
      return this.$store.getters['openStudy/imgsets'].length
    }
  },
  created () {
  }
}
</script>

<style>
</style>
