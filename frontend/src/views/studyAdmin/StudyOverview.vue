<template>
<div id="study_overview" class="">
      <div id="nav" class="navbar bg-dark p-0" style="height: 50px;">
        <div class="row mx-auto mt-4">
          <router-link to="/study-management/metaInfos" @click="createStudy">Create New Study
          </router-link>
        </div>
      </div>
  <div class="container">

        <div class="row mx-auto collapse show mt-4" id="studies_ov">
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
                                <button class="btn-success btn-sm">edit</button>
                            </router-link>
                        </td>
                        <td>
                            <form class="" action="" method="get">
                                <button class="btn-primary btn-sm">results</button>
                            </form>
                        </td>
                        <td>
                            <button class="btn-danger btn-sm" onclick="">delete
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

export default {
  name: 'StudyOverview',
  data () {
    return {
      studies: []
    }
  },
  methods: {
    createStudy () {
      this.$store.commit('addStudy')
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
