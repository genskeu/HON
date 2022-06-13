<template>
  <div class="container">
        <div class="row mx-auto mt-4">
          <router-link to="/study-management/metaInfos" @click="createStudy">Create New Study
          </router-link>
        </div>
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
                    <tr v-for="study in get_studies" :key="study.id">
                        <td class="align-middle">{{study.title}}</td>
                        <td class="align-middle">{{study.id}}</td>
                        <td class="align-middle">{{study.created}}</td>
                        <td class="align-middle">{{study.updated}}</td>
                        <td>
                            <router-link to="/study-management/metaInfos">
                                <button class="btn-success btn-sm" @click="openStudy(study.id)">edit</button>
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
</template>

<script>
export default {
  name: 'StudyOverview',
  data () {
    return {
    }
  },
  methods: {
    createStudy () {
      this.$store.commit('addStudy')
    },
    openStudy (id) {
      this.$store.commit('openStudy', id)
    }
  },
  computed: {
    get_studies () {
      return this.$store.state.studies
    }
  }
}
</script>

<style>
</style>
