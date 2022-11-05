<template>
<div class="container">
  <div class="mx-auto">
    <div id="table" class="row mx-auto overflow-auto show" style="max-height: 300px;">
      <table class="table table-hover">
                <thead class="thead-light">
                    <tr>
                        <th>Name</th>
                        <th>User Id</th>
                        <th>Created</th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in users" :key="user.id">
                        <td class="align-middle">{{user.username}}</td>
                        <td class="align-middle">{{user.id}}</td>
                        <td class="align-middle">{{user.created}}</td>
                        <td>
                          <button @click="editStudy(study.id)" class="btn-success btn">edit</button>
                        </td>
                        <td>
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
export default {
  computed: {
    users () {
      return this.$store.getters['users/users']
    }
  }
}
</script>

<style>

</style>
